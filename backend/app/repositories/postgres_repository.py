import os
from contextlib import contextmanager
from datetime import date, datetime
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Text,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    text
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

from backend.app.config import config, normalize_postgres_url
from backend.app.models.jobs import Job, JobCreate, JobUpdate
from backend.app.models.employers import Employer, EmployerCreate, EmployerUpdate
from backend.app.models.workers import Worker, WorkerCreate
from backend.app.models.applications import Application, ApplicationCreate
from backend.app.models.categories import Category
from backend.app.repositories.excel_repository import (
    IJobRepository,
    IEmployerRepository,
    IWorkerRepository,
    IApplicationRepository,
    ICategoryRepository
)

Base = declarative_base()


# --- SQLAlchemy Models ---

class EmployerModel(Base):
    __tablename__ = "employers"

    employer_id = Column(String(50), primary_key=True)
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    location = Column(String(255), nullable=False)
    verified = Column(String(50), nullable=False, default="Pending")
    created_at = Column(String(50), nullable=False)

    jobs = relationship("JobModel", back_populates="employer", cascade="all, delete-orphan")


class JobModel(Base):
    __tablename__ = "jobs"

    job_id = Column(String(50), primary_key=True)
    employer_id = Column(String(50), ForeignKey("employers.employer_id", ondelete="CASCADE"), nullable=False)
    job_type = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False, default="Hyderabad")
    locality = Column(String(255), nullable=False)
    district = Column(String(255), nullable=False, default="Medchal-Malkajgiri")
    state = Column(String(255), nullable=False, default="Telangana")
    salary = Column(Integer, nullable=False, default=0)
    salary_type = Column(String(50), nullable=False, default="Month")
    hours = Column(String(100), nullable=False, default="8 hours")
    required_experience = Column(String(100), nullable=False, default="Fresher")
    vacancies = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=False, default="")
    status = Column(String(50), nullable=False, default="Active")
    verified = Column(String(50), nullable=False, default="Pending")
    created_at = Column(String(50), nullable=False)
    expiry_date = Column(String(50), nullable=False, default="2026-12-31")

    employer = relationship("EmployerModel", back_populates="jobs")
    applications = relationship("ApplicationModel", back_populates="job", cascade="all, delete-orphan")


class WorkerModel(Base):
    __tablename__ = "workers"

    worker_id = Column(String(50), primary_key=True)
    phone = Column(String(50), unique=True, nullable=False)
    language = Column(String(10), nullable=False, default="te")
    location = Column(String(255), nullable=False, default="Hyderabad")
    locality = Column(String(255), nullable=False, default="Uppal")
    preferred_job_type = Column(String(100), nullable=False, default="Driver")
    experience = Column(String(100), nullable=False, default="Fresher")
    created_at = Column(String(50), nullable=False)

    applications = relationship("ApplicationModel", back_populates="worker")


class ApplicationModel(Base):
    __tablename__ = "applications"

    application_id = Column(String(50), primary_key=True)
    worker_id = Column(String(50), ForeignKey("workers.worker_id", ondelete="SET NULL"), nullable=True)
    worker_phone = Column(String(50), nullable=False)
    job_id = Column(String(50), ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False)
    applied_at = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="Interested")

    __table_args__ = (
        UniqueConstraint("worker_phone", "job_id", name="uq_worker_job_application"),
    )

    worker = relationship("WorkerModel", back_populates="applications")
    job = relationship("JobModel", back_populates="applications")


class CategoryModel(Base):
    __tablename__ = "categories"

    category_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    telugu_name = Column(String(100), nullable=False)
    hindi_name = Column(String(100), nullable=False)
    english_name = Column(String(100), nullable=False)
    active = Column(Boolean, nullable=False, default=True)


# --- Database Engine & Session Management ---

_global_engine = None

def get_engine(db_url: Optional[str] = None):
    global _global_engine
    if db_url:
        normalized = normalize_postgres_url(db_url)
        if normalized.startswith("sqlite"):
            return create_engine(normalized, connect_args={"check_same_thread": False})
        return create_engine(normalized, pool_pre_ping=True)

    if _global_engine is None:
        url = config.normalized_database_url
        if not url:
            # Fallback for local testing/development when no PostgreSQL server is running
            data_dir = Path("data")
            data_dir.mkdir(parents=True, exist_ok=True)
            url = "sqlite:///data/localjobs_postgres_fallback.db"

        if url.startswith("sqlite"):
            _global_engine = create_engine(url, connect_args={"check_same_thread": False})
        else:
            _global_engine = create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=10)

    return _global_engine

def set_engine(engine):
    global _global_engine
    _global_engine = engine

@contextmanager
def session_scope(engine=None):
    eng = engine or get_engine()
    session_factory = sessionmaker(bind=eng)
    session: Session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db_postgres(engine=None):
    """
    Idempotent table initialization.
    Creates tables if they do not exist without modifying or dropping existing data.
    """
    eng = engine or get_engine()
    Base.metadata.create_all(bind=eng)


# --- Mapping Helpers ---

def _job_to_pydantic(row: JobModel) -> Job:
    return Job(
        job_id=row.job_id,
        employer_id=row.employer_id,
        job_type=row.job_type,
        location=row.location,
        locality=row.locality,
        district=row.district,
        state=row.state,
        salary=int(row.salary),
        salary_type=row.salary_type,
        hours=row.hours,
        required_experience=row.required_experience,
        vacancies=int(row.vacancies),
        description=row.description or "",
        status=row.status,
        verified=row.verified,
        created_at=row.created_at,
        expiry_date=row.expiry_date
    )

def _employer_to_pydantic(row: EmployerModel) -> Employer:
    return Employer(
        employer_id=row.employer_id,
        company_name=row.company_name,
        contact_name=row.contact_name,
        phone=row.phone,
        location=row.location,
        verified=row.verified,
        created_at=row.created_at
    )

def _worker_to_pydantic(row: WorkerModel) -> Worker:
    return Worker(
        worker_id=row.worker_id,
        phone=row.phone,
        language=row.language,
        location=row.location,
        locality=row.locality,
        preferred_job_type=row.preferred_job_type,
        experience=row.experience,
        created_at=row.created_at
    )

def _application_to_pydantic(row: ApplicationModel) -> Application:
    return Application(
        application_id=row.application_id,
        worker_id=row.worker_id,
        worker_phone=row.worker_phone,
        job_id=row.job_id,
        applied_at=row.applied_at,
        status=row.status
    )

def _category_to_pydantic(row: CategoryModel) -> Category:
    return Category(
        category_id=row.category_id,
        name=row.name,
        telugu_name=row.telugu_name,
        hindi_name=row.hindi_name,
        english_name=row.english_name,
        active=bool(row.active)
    )


# --- Concrete PostgreSQL Repositories ---

class PostgresJobRepository(IJobRepository):
    def __init__(self, engine=None):
        self._engine = engine

    def _get_engine(self):
        return self._engine or get_engine()

    def get_all(self, verified_only: bool = True, active_only: bool = True) -> List[Job]:
        today_str = date.today().isoformat()
        with session_scope(self._get_engine()) as session:
            query = session.query(JobModel)
            if active_only:
                query = query.filter(JobModel.status == "Active", JobModel.expiry_date >= today_str)
            if verified_only:
                query = query.filter(JobModel.verified == "Verified")
            rows = query.all()
            return [_job_to_pydantic(r) for r in rows]

    def get_by_id(self, job_id: str) -> Optional[Job]:
        clean_id = job_id.strip().upper()
        with session_scope(self._get_engine()) as session:
            # Fetch all to do case-insensitive match safely across SQL dialects
            rows = session.query(JobModel).all()
            for r in rows:
                if r.job_id.upper() == clean_id:
                    return _job_to_pydantic(r)
            return None

    def create(self, job: JobCreate) -> Job:
        with session_scope(self._get_engine()) as session:
            rows = session.query(JobModel.job_id).all()
            max_id = 1000
            for (jid,) in rows:
                if jid and jid.startswith("JOB-"):
                    try:
                        num = int(jid.split("-")[1])
                        if num > max_id:
                            max_id = num
                    except (IndexError, ValueError):
                        pass
            new_id = f"JOB-{max_id + 1}"
            today_str = datetime.now().strftime("%Y-%m-%d")

            new_job_model = JobModel(
                job_id=new_id,
                employer_id=job.employer_id,
                job_type=job.job_type,
                location=job.location,
                locality=job.locality,
                district=job.district,
                state=job.state,
                salary=job.salary,
                salary_type=job.salary_type,
                hours=job.hours,
                required_experience=job.required_experience,
                vacancies=job.vacancies,
                description=job.description,
                status="Active",
                verified="Pending",
                created_at=today_str,
                expiry_date=job.expiry_date
            )
            session.add(new_job_model)
            session.flush()
            return _job_to_pydantic(new_job_model)

    def update(self, job_id: str, updates: JobUpdate) -> Optional[Job]:
        clean_id = job_id.strip().upper()
        with session_scope(self._get_engine()) as session:
            target_model = None
            for r in session.query(JobModel).all():
                if r.job_id.upper() == clean_id:
                    target_model = r
                    break
            if not target_model:
                return None

            update_data = updates.model_dump(exclude_unset=True)
            for field, val in update_data.items():
                if hasattr(target_model, field) and val is not None:
                    setattr(target_model, field, val)

            session.flush()
            return _job_to_pydantic(target_model)

    def search(self, job_type: Optional[str] = None, locality: Optional[str] = None) -> List[Job]:
        jobs = self.get_all(verified_only=True, active_only=True)
        results = []
        for j in jobs:
            if job_type:
                if job_type.lower() not in j.job_type.lower() and j.job_type.lower() not in job_type.lower():
                    continue
            if locality and locality.lower() not in ["all", "any", ""]:
                if locality.lower() not in j.locality.lower() and j.locality.lower() not in locality.lower():
                    continue
            results.append(j)
        return results


class PostgresEmployerRepository(IEmployerRepository):
    def __init__(self, engine=None):
        self._engine = engine

    def _get_engine(self):
        return self._engine or get_engine()

    def get_all(self) -> List[Employer]:
        with session_scope(self._get_engine()) as session:
            rows = session.query(EmployerModel).all()
            return [_employer_to_pydantic(r) for r in rows]

    def get_by_id(self, employer_id: str) -> Optional[Employer]:
        clean_id = employer_id.strip().upper()
        with session_scope(self._get_engine()) as session:
            for r in session.query(EmployerModel).all():
                if r.employer_id.upper() == clean_id:
                    return _employer_to_pydantic(r)
            return None

    def create(self, emp: EmployerCreate) -> Employer:
        with session_scope(self._get_engine()) as session:
            rows = session.query(EmployerModel.employer_id).all()
            max_id = 100
            for (eid,) in rows:
                if eid and eid.startswith("EMP-"):
                    try:
                        num = int(eid.split("-")[1])
                        if num > max_id:
                            max_id = num
                    except (IndexError, ValueError):
                        pass
            new_id = f"EMP-{max_id + 1}"
            today_str = datetime.now().strftime("%Y-%m-%d")

            new_emp_model = EmployerModel(
                employer_id=new_id,
                company_name=emp.company_name,
                contact_name=emp.contact_name,
                phone=emp.phone,
                location=emp.location,
                verified="Pending",
                created_at=today_str
            )
            session.add(new_emp_model)
            session.flush()
            return _employer_to_pydantic(new_emp_model)

    def update(self, employer_id: str, updates: EmployerUpdate) -> Optional[Employer]:
        clean_id = employer_id.strip().upper()
        with session_scope(self._get_engine()) as session:
            target = None
            for r in session.query(EmployerModel).all():
                if r.employer_id.upper() == clean_id:
                    target = r
                    break
            if not target:
                return None

            update_data = updates.model_dump(exclude_unset=True)
            for field, val in update_data.items():
                if hasattr(target, field) and val is not None:
                    setattr(target, field, val)

            session.flush()
            return _employer_to_pydantic(target)


class PostgresWorkerRepository(IWorkerRepository):
    def __init__(self, engine=None):
        self._engine = engine

    def _get_engine(self):
        return self._engine or get_engine()

    def get_all(self) -> List[Worker]:
        with session_scope(self._get_engine()) as session:
            rows = session.query(WorkerModel).all()
            return [_worker_to_pydantic(r) for r in rows]

    def get_by_phone(self, phone: str) -> Optional[Worker]:
        normalized = phone.strip()
        with session_scope(self._get_engine()) as session:
            row = session.query(WorkerModel).filter(WorkerModel.phone == normalized).first()
            return _worker_to_pydantic(row) if row else None

    def create(self, worker: WorkerCreate) -> Worker:
        existing = self.get_by_phone(worker.phone)
        if existing:
            return existing

        with session_scope(self._get_engine()) as session:
            rows = session.query(WorkerModel.worker_id).all()
            max_id = 500
            for (wid,) in rows:
                if wid and wid.startswith("WRK-"):
                    try:
                        num = int(wid.split("-")[1])
                        if num > max_id:
                            max_id = num
                    except (IndexError, ValueError):
                        pass
            new_id = f"WRK-{max_id + 1}"
            today_str = datetime.now().strftime("%Y-%m-%d")

            new_worker = WorkerModel(
                worker_id=new_id,
                phone=worker.phone,
                language=worker.language,
                location=worker.location,
                locality=worker.locality,
                preferred_job_type=worker.preferred_job_type,
                experience=worker.experience,
                created_at=today_str
            )
            session.add(new_worker)
            session.flush()
            return _worker_to_pydantic(new_worker)


class PostgresApplicationRepository(IApplicationRepository):
    def __init__(self, engine=None):
        self._engine = engine

    def _get_engine(self):
        return self._engine or get_engine()

    def get_all(self) -> List[Application]:
        with session_scope(self._get_engine()) as session:
            rows = session.query(ApplicationModel).all()
            return [_application_to_pydantic(r) for r in rows]

    def get_by_id(self, app_id: str) -> Optional[Application]:
        clean_id = app_id.strip().upper()
        with session_scope(self._get_engine()) as session:
            for r in session.query(ApplicationModel).all():
                if r.application_id.upper() == clean_id:
                    return _application_to_pydantic(r)
            return None

    def get_by_phone(self, phone: str) -> List[Application]:
        normalized = phone.strip()
        with session_scope(self._get_engine()) as session:
            rows = session.query(ApplicationModel).filter(ApplicationModel.worker_phone == normalized).all()
            return [_application_to_pydantic(r) for r in rows]

    def exists_recent(self, worker_phone: str, job_id: str) -> bool:
        normalized_phone = worker_phone.strip()
        clean_job_id = job_id.strip().upper()
        with session_scope(self._get_engine()) as session:
            rows = session.query(ApplicationModel).filter(ApplicationModel.worker_phone == normalized_phone).all()
            for r in rows:
                if r.job_id.upper() == clean_job_id:
                    return True
            return False

    def create(self, app: ApplicationCreate) -> Application:
        if self.exists_recent(app.worker_phone, app.job_id):
            raise ValueError("Duplicate application: you have already applied for this job.")

        with session_scope(self._get_engine()) as session:
            rows = session.query(ApplicationModel.application_id).all()
            max_id = 10000
            for (aid,) in rows:
                if aid and aid.startswith("APP-"):
                    try:
                        num = int(aid.split("-")[1])
                        if num > max_id:
                            max_id = num
                    except (IndexError, ValueError):
                        pass
            new_id = f"APP-{max_id + 1}"
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_app = ApplicationModel(
                application_id=new_id,
                worker_id=app.worker_id,
                worker_phone=app.worker_phone,
                job_id=app.job_id,
                applied_at=now_str,
                status=app.status or "Interested"
            )
            session.add(new_app)
            session.flush()
            return _application_to_pydantic(new_app)


class PostgresCategoryRepository(ICategoryRepository):
    def __init__(self, engine=None):
        self._engine = engine

    def _get_engine(self):
        return self._engine or get_engine()

    def get_all(self, active_only: bool = True) -> List[Category]:
        with session_scope(self._get_engine()) as session:
            query = session.query(CategoryModel)
            if active_only:
                query = query.filter(CategoryModel.active == True)
            rows = query.all()
            return [_category_to_pydantic(r) for r in rows]


class UnifiedPostgresRepository:
    """
    Unified PostgreSQL Repository Facade implementing the exact same interface
    as UnifiedExcelRepository.
    """
    def __init__(self, engine=None):
        self.jobs = PostgresJobRepository(engine)
        self.employers = PostgresEmployerRepository(engine)
        self.workers = PostgresWorkerRepository(engine)
        self.applications = PostgresApplicationRepository(engine)
        self.categories = PostgresCategoryRepository(engine)
        self._custom_engine = engine

    def _get_engine(self):
        return self._custom_engine or get_engine()

    def check_connection(self) -> Tuple[bool, Optional[str]]:
        try:
            eng = self._get_engine()
            with session_scope(eng) as session:
                session.execute(text("SELECT 1"))
            return True, None
        except Exception as e:
            return False, str(e)

    def get_storage_stats(self) -> Dict[str, Any]:
        eng = self._get_engine()
        init_db_postgres(eng)
        with session_scope(eng) as session:
            num_jobs = session.query(JobModel).count()
            num_emp = session.query(EmployerModel).count()
            num_wrk = session.query(WorkerModel).count()
            num_app = session.query(ApplicationModel).count()
            num_cat = session.query(CategoryModel).count()
            total = num_jobs + num_emp + num_wrk + num_app + num_cat

            return {
                "backend": "postgresql",
                "Jobs": num_jobs,
                "Employers": num_emp,
                "Workers": num_wrk,
                "Applications": num_app,
                "Categories": num_cat,
                "total_records": total,
                "concurrency_risk": "LOW (PostgreSQL ACID active)",
                "migration_recommended": False
            }

    # Jobs Facade
    def get_all(self, verified_only: bool = True, active_only: bool = True) -> List[Job]:
        return self.jobs.get_all(verified_only=verified_only, active_only=active_only)

    def get_by_id(self, job_id: str) -> Optional[Job]:
        return self.jobs.get_by_id(job_id)

    def create(self, job: JobCreate) -> Job:
        return self.jobs.create(job)

    def update(self, job_id: str, updates: JobUpdate) -> Optional[Job]:
        return self.jobs.update(job_id, updates)

    def search(self, job_type: Optional[str] = None, locality: Optional[str] = None) -> List[Job]:
        return self.jobs.search(job_type=job_type, locality=locality)

    # Employers Facade
    def get_all_employers(self) -> List[Employer]:
        return self.employers.get_all()

    def get_employer_by_id(self, employer_id: str) -> Optional[Employer]:
        return self.employers.get_by_id(employer_id)

    def create_employer(self, emp: EmployerCreate) -> Employer:
        return self.employers.create(emp)

    def update_employer(self, employer_id: str, updates: EmployerUpdate) -> Optional[Employer]:
        return self.employers.update(employer_id, updates)

    # Workers Facade
    def get_all_workers(self) -> List[Worker]:
        return self.workers.get_all()

    def get_worker_by_phone(self, phone: str) -> Optional[Worker]:
        return self.workers.get_by_phone(phone)

    def create_worker(self, worker: WorkerCreate) -> Worker:
        return self.workers.create(worker)

    # Applications Facade
    def get_all_applications(self) -> List[Application]:
        return self.applications.get_all()

    def get_application_by_id(self, app_id: str) -> Optional[Application]:
        return self.applications.get_by_id(app_id)

    def get_applications_by_phone(self, phone: str) -> List[Application]:
        return self.applications.get_by_phone(phone)

    def exists_recent(self, worker_phone: str, job_id: str) -> bool:
        return self.applications.exists_recent(worker_phone, job_id)

    def create_application(self, app: ApplicationCreate) -> Application:
        return self.applications.create(app)

    # Categories Facade
    def get_all_categories(self, active_only: bool = True) -> List[Category]:
        return self.categories.get_all(active_only=active_only)


postgres_repo = UnifiedPostgresRepository()
