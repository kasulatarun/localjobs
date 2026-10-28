import pytest
from backend.app.models.jobs import JobCreate
from backend.app.services.job_service import job_service
from backend.app.services.matching_service import matching_service
from backend.app.services.application_service import application_service
from backend.app.repositories.excel_repository import excel_repo
from backend.app.security.validation import normalize_phone

def test_job_search_excludes_unverified_jobs():
    # JOB-1007 is Pending in demo data
    public_jobs = job_service.get_public_jobs()
    job_ids = [j.job_id for j in public_jobs]
    assert "JOB-1007" not in job_ids

def test_job_search_excludes_closed_jobs():
    # JOB-1008 is Closed in demo data
    public_jobs = job_service.get_public_jobs()
    job_ids = [j.job_id for j in public_jobs]
    assert "JOB-1008" not in job_ids

def test_job_search_excludes_expired_jobs():
    # JOB-1009 has expiry 2026-09-01 in demo data (expired)
    public_jobs = job_service.get_public_jobs()
    job_ids = [j.job_id for j in public_jobs]
    assert "JOB-1009" not in job_ids

def test_new_job_starts_pending_verification():
    new_job = job_service.post_job(JobCreate(
        employer_id="EMP-101",
        job_type="Plumber",
        locality="Uppal",
        salary=17000,
        description="Plumbing contractor needed."
    ))
    assert new_job.verified == "Pending"
    assert new_job.status == "Active"

    # Should not appear in public search yet
    matches = matching_service.match_jobs(category="Plumber")
    assert not any(j.job_id == new_job.job_id for j in matches)

    # Admin approves
    approved = job_service.approve_job(new_job.job_id)
    assert approved.verified == "Verified"

    # Now appears in public search!
    matches_after = matching_service.match_jobs(category="Plumber")
    assert any(j.job_id == new_job.job_id for j in matches_after)

def test_create_job_invalid_employer_rejected(client):
    payload = {
        "employer_id": "EMP-99999", # Non-existent employer
        "job_type": "Driver",
        "locality": "Uppal",
        "salary": 18000
    }
    res = client.post("/jobs", json=payload, headers={"X-Employer-Secret": "localjobs_employer_secure_secret_token_67890"})
    assert res.status_code == 400
    assert "does not exist" in res.json()["detail"]

def test_duplicate_application_prevention():
    phone = "+919848099999"
    job_id = "JOB-1001"

    app1, is_dup1 = application_service.apply_for_job(phone, job_id)
    assert is_dup1 is False
    assert app1.job_id == job_id

    app2, is_dup2 = application_service.apply_for_job(phone, job_id)
    assert is_dup2 is True
    assert app2.job_id == job_id

def test_phone_number_normalization():
    assert normalize_phone("9848012345") == "+919848012345"
    assert normalize_phone("09848012345") == "+919848012345"
    assert normalize_phone("+91 98480-12345") == "+919848012345"
    assert normalize_phone("919848012345") == "+919848012345"
    
    with pytest.raises(ValueError):
        normalize_phone("12345") # too short

def test_api_endpoints(client):
    # Health
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

    # Categories
    res = client.get("/categories")
    assert res.status_code == 200
    assert len(res.json()) >= 5

    # Public Jobs
    res = client.get("/jobs?locality=Uppal")
    assert res.status_code == 200
    jobs = res.json()
    assert any(j["JobID"] == "JOB-1001" for j in jobs)
