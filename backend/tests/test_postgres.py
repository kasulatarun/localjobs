import os
from pathlib import Path
import pytest
from datetime import date, datetime
from sqlalchemy import create_engine

from backend.app.config import config
from backend.app.models.jobs import JobCreate, JobUpdate
from backend.app.models.employers import EmployerCreate, EmployerUpdate
from backend.app.models.workers import WorkerCreate
from backend.app.models.applications import ApplicationCreate
from backend.app.repositories.postgres_repository import (
    UnifiedPostgresRepository,
    init_db_postgres,
    set_engine,
    get_engine,
    Base
)
from backend.app.repositories.import_excel_to_postgres import import_excel_to_postgres
from backend.app.services.job_service import JobService
from sqlalchemy.pool import StaticPool
from backend.app.services.application_service import ApplicationService
from backend.app.services.matching_service import MatchingService
from backend.app.services.ivr_service import IVRService, IVRState

@pytest.fixture(scope="module")
def pg_engine():
    """
    Creates an isolated in-memory SQLite database using StaticPool for SQL repository testing.
    Validates complete SQL schema and relational constraints.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    init_db_postgres(engine)
    return engine

@pytest.fixture
def pg_repo(pg_engine):
    """Clean database and import standard seed data for each test."""
    Base.metadata.drop_all(bind=pg_engine)
    Base.metadata.create_all(bind=pg_engine)
    import_excel_to_postgres(excel_path=Path("data/jobs.xlsx"), engine=pg_engine)
    return UnifiedPostgresRepository(engine=pg_engine)


def test_postgres_schema_and_seed_import(pg_repo):
    """Verifies that seed data is imported into PostgreSQL correctly."""
    stats = pg_repo.get_storage_stats()
    assert stats["backend"] == "postgresql"
    assert stats["Jobs"] >= 9
    assert stats["Employers"] >= 6
    assert stats["Workers"] >= 3
    assert stats["Applications"] >= 1
    assert stats["Categories"] >= 18
    assert stats["concurrency_risk"] == "LOW (PostgreSQL ACID active)"


def test_postgres_job_filters(pg_repo):
    """Verifies unverified, closed, and expired jobs are excluded from public search in PostgreSQL."""
    js = JobService(repo=pg_repo)
    public_jobs = js.get_public_jobs()
    job_ids = [j.job_id for j in public_jobs]

    # JOB-1007 is Pending
    assert "JOB-1007" not in job_ids
    # JOB-1008 is Closed
    assert "JOB-1008" not in job_ids
    # JOB-1009 is Expired
    assert "JOB-1009" not in job_ids
    # JOB-1001 is Active & Verified
    assert "JOB-1001" in job_ids


def test_postgres_job_creation_and_admin_workflow(pg_repo):
    """Verifies job creation starts as Pending and requires admin approval."""
    js = JobService(repo=pg_repo)
    ms = MatchingService(service=js)

    new_job = js.post_job(JobCreate(
        employer_id="EMP-101",
        job_type="Painter",
        locality="Uppal",
        salary=16000,
        description="Interior wall painting."
    ))

    assert new_job.verified == "Pending"
    assert new_job.status == "Active"

    # Not visible to workers yet
    matches = ms.match_jobs(category="Painter")
    assert not any(j.job_id == new_job.job_id for j in matches)

    # Admin approves
    approved = js.approve_job(new_job.job_id)
    assert approved.verified == "Verified"

    # Now visible to workers
    matches_after = ms.match_jobs(category="Painter")
    assert any(j.job_id == new_job.job_id for j in matches_after)

    # Admin closes
    closed = js.close_job(new_job.job_id)
    assert closed.status == "Closed"
    matches_closed = ms.match_jobs(category="Painter")
    assert not any(j.job_id == new_job.job_id for j in matches_closed)


def test_postgres_employer_registration_and_verification(pg_repo):
    """Verifies employer registration and admin verification in PostgreSQL."""
    emp = pg_repo.create_employer(EmployerCreate(
        company_name="Hyderabad Metro Works",
        contact_name="G. Narayana",
        phone="+919876543299",
        location="Secunderabad"
    ))
    assert emp.employer_id.startswith("EMP-")
    assert emp.verified == "Pending"

    # Admin verifies employer
    verified_emp = pg_repo.update_employer(emp.employer_id, EmployerUpdate(verified="Verified"))
    assert verified_emp.verified == "Verified"


def test_postgres_worker_idempotency(pg_repo):
    """Verifies worker creation is idempotent by phone number."""
    phone = "+919848077777"
    w1 = pg_repo.create_worker(WorkerCreate(
        phone=phone,
        language="te",
        location="Hyderabad",
        locality="Uppal",
        preferred_job_type="Driver"
    ))
    assert w1.worker_id.startswith("WRK-")

    # Second call with same phone returns existing record
    w2 = pg_repo.create_worker(WorkerCreate(
        phone=phone,
        language="hi",
        location="Hyderabad",
        locality="Uppal",
        preferred_job_type="Driver"
    ))
    assert w2.worker_id == w1.worker_id


def test_postgres_duplicate_application_prevention(pg_repo):
    """Verifies PostgreSQL prevents duplicate applications for the same job and phone."""
    app_service = ApplicationService(repo=pg_repo)
    phone = "+919848088888"
    job_id = "JOB-1001"

    app1, is_dup1 = app_service.apply_for_job(phone, job_id)
    assert is_dup1 is False
    assert app1.job_id == job_id
    assert app1.application_id.startswith("APP-")

    # Second application must be flagged as duplicate
    app2, is_dup2 = app_service.apply_for_job(phone, job_id)
    assert is_dup2 is True
    assert app2.job_id == job_id

    # Direct repository call must raise ValueError
    with pytest.raises(ValueError, match="Duplicate application"):
        pg_repo.create_application(ApplicationCreate(
            worker_phone=phone,
            job_id=job_id
        ))


def test_postgres_full_ivr_journey(pg_repo):
    """Full IVR journey against PostgreSQL repository: Telugu -> Driver -> Uppal -> Apply."""
    js = JobService(repo=pg_repo)
    ms = MatchingService(service=js)
    asvc = ApplicationService(repo=pg_repo)
    ivr = IVRService(match_svc=ms, app_svc=asvc)

    call_id = "PG-TEST-CALL-01"
    worker_phone = "+919848055667"

    # Step 1: Call incoming
    r1 = ivr.process_incoming_call(call_id, worker_phone)
    assert r1["state"] == IVRState.LANGUAGE_SELECTION.value

    # Step 2: Language = Telugu (1)
    r2 = ivr.process_dtmf_input(call_id, "1")
    assert r2["state"] == IVRState.CATEGORY_SELECTION.value
    assert r2["language"] == "te"

    # Step 3: Category = Driver (1)
    r3 = ivr.process_dtmf_input(call_id, "1")
    assert r3["state"] == IVRState.LOCATION_SELECTION.value

    # Step 4: Location = Uppal (1)
    r4 = ivr.process_dtmf_input(call_id, "1")
    assert r4["state"] == IVRState.JOB_RESULTS.value
    assert r4["job"]["JobID"] == "JOB-1001"

    # Step 5: Interested (1)
    r5 = ivr.process_dtmf_input(call_id, "1")
    assert r5["state"] == IVRState.APPLICATION_CREATED.value
    assert r5["application_id"] is not None

    # Step 6: Verify application was persisted in PostgreSQL
    apps = pg_repo.get_applications_by_phone(worker_phone)
    assert len(apps) == 1
    assert apps[0].job_id == "JOB-1001"
    assert apps[0].status == "Interested"


def test_postgres_api_health_and_readiness(pg_repo, pg_engine, monkeypatch):
    """Verifies that FastAPI /health and /ready endpoints correctly report PostgreSQL status."""
    from fastapi.testclient import TestClient
    from backend.app.main import app
    from backend.app.repositories.postgres_repository import set_engine

    set_engine(pg_engine)
    monkeypatch.setattr(config, "DATA_BACKEND", "postgres")
    try:
        with TestClient(app) as client:
            health_res = client.get("/health")
            assert health_res.status_code == 200
            data = health_res.json()
            assert data["status"] == "healthy"
            assert data["storage"]["backend"] == "postgres"
            assert data["storage"]["concurrency_risk"] == "LOW (PostgreSQL ACID active)"
            assert data["storage"]["total_records"] >= 30

            ready_res = client.get("/ready")
            assert ready_res.status_code == 200
            assert ready_res.json()["ready"] is True
    finally:
        set_engine(None)


def test_postgres_categories_and_search(pg_repo):
    """Verifies category queries and fuzzy/substring job search in PostgreSQL."""
    cats = pg_repo.get_all_categories(active_only=True)
    assert len(cats) >= 18
    driver_cat = next((c for c in cats if c.name == "Driver"), None)
    assert driver_cat is not None
    assert driver_cat.telugu_name == "డ్రైవర్"
    assert driver_cat.hindi_name == "ड्राइवर"

    # Search case-insensitive
    driver_jobs = pg_repo.search(job_type="driver", locality="uppal")
    assert any(j.job_id == "JOB-1001" for j in driver_jobs)


def test_postgres_admin_stats_and_endpoints(pg_repo, pg_engine, monkeypatch):
    """Verifies that admin stats and endpoints aggregate accurately with PostgreSQL backend."""
    from fastapi.testclient import TestClient
    from backend.app.main import app
    from backend.app.repositories.postgres_repository import set_engine

    set_engine(pg_engine)
    monkeypatch.setattr(config, "DATA_BACKEND", "postgres")
    try:
        with TestClient(app) as client:
            res = client.get("/admin/stats", headers={"X-Admin-Secret": config.ADMIN_SECRET})
            assert res.status_code == 200
            stats = res.json()
            assert stats["total_jobs"] >= 9
            assert stats["total_employers"] >= 6
            assert stats["concurrency_risk"] == "LOW (PostgreSQL ACID active)"
            assert stats["migration_recommended"] is False

            # Check admin jobs endpoint
            jobs_res = client.get("/admin/jobs", headers={"X-Admin-Secret": config.ADMIN_SECRET})
            assert jobs_res.status_code == 200
            all_jobs = jobs_res.json()
            # Admin sees all jobs including Pending (JOB-1007) and Closed (JOB-1008)
            job_ids = [j["JobID"] for j in all_jobs]
            assert "JOB-1007" in job_ids
            assert "JOB-1008" in job_ids
    finally:
        set_engine(None)


def test_postgres_connection_check(pg_repo):
    """Verifies check_connection returns True on active engine."""
    ok, err = pg_repo.check_connection()
    assert ok is True
    assert err is None
