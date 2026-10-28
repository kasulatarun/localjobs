import os
import shutil
import threading
from abc import ABC, abstractmethod
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Dict, Any
import openpyxl

from backend.app.models.jobs import Job, JobCreate, JobUpdate
from backend.app.models.employers import Employer, EmployerCreate, EmployerUpdate
from backend.app.models.workers import Worker, WorkerCreate
from backend.app.models.applications import Application, ApplicationCreate
from backend.app.models.categories import Category

EXCEL_LOCK = threading.RLock()
DEFAULT_DATA_PATH = Path("data/jobs.xlsx")

# --- Base Helper ---

class ExcelBase:
    def __init__(self, file_path: Path = DEFAULT_DATA_PATH):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.file_path.exists():
            from backend.app.repositories.init_db import create_initial_workbook
            create_initial_workbook(self.file_path)

    def _load_workbook(self, read_only: bool = True) -> openpyxl.Workbook:
        self._ensure_file_exists()
        return openpyxl.load_workbook(self.file_path, data_only=True, read_only=read_only)

    def _save_workbook_atomic(self, wb: openpyxl.Workbook):
        """
        Saves workbook atomically with backup and file locking to prevent Excel corruption.
        """
        tmp_file = self.file_path.with_suffix(".tmp.xlsx")
        backup_file = self.file_path.with_suffix(".backup.xlsx")

        wb.save(tmp_file)
        wb.close()

        if self.file_path.exists():
            shutil.copy2(self.file_path, backup_file)

        os.replace(tmp_file, self.file_path)


# --- Abstract Repositories ---

class IJobRepository(ABC):
    @abstractmethod
    def get_all(self, verified_only: bool = True, active_only: bool = True) -> List[Job]:
        pass

    @abstractmethod
    def get_by_id(self, job_id: str) -> Optional[Job]:
        pass

    @abstractmethod
    def create(self, job: JobCreate) -> Job:
        pass

    @abstractmethod
    def update(self, job_id: str, updates: JobUpdate) -> Optional[Job]:
        pass

    @abstractmethod
    def search(self, job_type: Optional[str] = None, locality: Optional[str] = None) -> List[Job]:
        pass


class IEmployerRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Employer]:
        pass

    @abstractmethod
    def get_by_id(self, employer_id: str) -> Optional[Employer]:
        pass

    @abstractmethod
    def create(self, emp: EmployerCreate) -> Employer:
        pass

    @abstractmethod
    def update(self, employer_id: str, updates: EmployerUpdate) -> Optional[Employer]:
        pass


class IWorkerRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Worker]:
        pass

    @abstractmethod
    def get_by_phone(self, phone: str) -> Optional[Worker]:
        pass

    @abstractmethod
    def create(self, worker: WorkerCreate) -> Worker:
        pass


class IApplicationRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Application]:
        pass

    @abstractmethod
    def get_by_id(self, app_id: str) -> Optional[Application]:
        pass

    @abstractmethod
    def get_by_phone(self, phone: str) -> List[Application]:
        pass

    @abstractmethod
    def exists_recent(self, worker_phone: str, job_id: str) -> bool:
        pass

    @abstractmethod
    def create(self, app: ApplicationCreate) -> Application:
        pass


class ICategoryRepository(ABC):
    @abstractmethod
    def get_all(self, active_only: bool = True) -> List[Category]:
        pass


# --- Concrete Implementations ---

class ExcelJobRepository(ExcelBase, IJobRepository):
    def get_all(self, verified_only: bool = True, active_only: bool = True) -> List[Job]:
        with EXCEL_LOCK:
            wb = self._load_workbook(read_only=True)
            ws = wb["Jobs"]
            headers = [cell.value for cell in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}
            
            jobs = []
            today = date.today().isoformat()

            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                job_id = str(row_dict.get("JobID") or "").strip()
                if not job_id:
                    continue

                status = str(row_dict.get("Status") or "Active").strip()
                verified = str(row_dict.get("Verified") or "Pending").strip()
                expiry = str(row_dict.get("ExpiryDate") or "2099-12-31")[:10]

                if active_only:
                    if status.lower() != "active":
                        continue
                    if expiry < today:
                        continue
                if verified_only and verified.lower() != "verified":
                    continue

                salary_val = row_dict.get("Salary")
                try:
                    salary_int = int(float(salary_val)) if salary_val is not None else 0
                except (ValueError, TypeError):
                    salary_int = 0

                vacancies_val = row_dict.get("Vacancies")
                try:
                    vacancies_int = int(float(vacancies_val)) if vacancies_val is not None else 1
                except (ValueError, TypeError):
                    vacancies_int = 1

                jobs.append(Job(
                    job_id=job_id,
                    employer_id=str(row_dict.get("EmployerID") or ""),
                    job_type=str(row_dict.get("JobType") or ""),
                    location=str(row_dict.get("Location") or ""),
                    locality=str(row_dict.get("Locality") or ""),
                    district=str(row_dict.get("District") or ""),
                    state=str(row_dict.get("State") or ""),
                    salary=salary_int,
                    salary_type=str(row_dict.get("SalaryType") or "Month"),
                    hours=str(row_dict.get("Hours") or ""),
                    required_experience=str(row_dict.get("RequiredExperience") or ""),
                    vacancies=vacancies_int,
                    description=str(row_dict.get("Description") or ""),
                    status=status,
                    verified=verified,
                    created_at=str(row_dict.get("CreatedAt") or "")[:10],
                    expiry_date=expiry
                ))
            wb.close()
            return jobs

    def get_by_id(self, job_id: str) -> Optional[Job]:
        all_jobs = self.get_all(verified_only=False, active_only=False)
        for j in all_jobs:
            if j.job_id.upper() == job_id.upper():
                return j
        return None

    def create(self, job: JobCreate) -> Job:
        with EXCEL_LOCK:
            wb = openpyxl.load_workbook(self.file_path)
            ws = wb["Jobs"]
            max_id = 1000
            for row in ws.iter_rows(min_row=2, max_col=1, values_only=True):
                val = row[0]
                if val and str(val).startswith("JOB-"):
                    try:
                        num = int(str(val).split("-")[1])
                        if num > max_id:
                            max_id = num
                    except (IndexError, ValueError):
                        pass
            new_id = f"JOB-{max_id + 1}"
            today_str = datetime.now().strftime("%Y-%m-%d")

            new_job = Job(
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

            row_data = [
                new_job.job_id,
                new_job.employer_id,
                new_job.job_type,
                new_job.location,
                new_job.locality,
                new_job.district,
                new_job.state,
                new_job.salary,
                new_job.salary_type,
                new_job.hours,
                new_job.required_experience,
                new_job.vacancies,
                new_job.description,
                new_job.status,
                new_job.verified,
                new_job.created_at,
                new_job.expiry_date
            ]
            ws.append(row_data)
            self._save_workbook_atomic(wb)
            return new_job

    def update(self, job_id: str, updates: JobUpdate) -> Optional[Job]:
        with EXCEL_LOCK:
            wb = openpyxl.load_workbook(self.file_path)
            ws = wb["Jobs"]
            headers = [cell.value for cell in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}

            target_row_idx = None
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, max_col=1, values_only=True), start=2):
                if row[0] and str(row[0]).strip().upper() == job_id.strip().upper():
                    target_row_idx = row_idx
                    break

            if not target_row_idx:
                wb.close()
                return None

            update_dict = updates.model_dump(exclude_unset=True)
            field_to_col = {
                "job_type": "JobType",
                "location": "Location",
                "locality": "Locality",
                "district": "District",
                "state": "State",
                "salary": "Salary",
                "salary_type": "SalaryType",
                "hours": "Hours",
                "required_experience": "RequiredExperience",
                "vacancies": "Vacancies",
                "description": "Description",
                "status": "Status",
                "verified": "Verified",
                "expiry_date": "ExpiryDate"
            }

            for field, val in update_dict.items():
                col_name = field_to_col.get(field)
                if col_name and col_name in col_map:
                    ws.cell(row=target_row_idx, column=col_map[col_name] + 1, value=val)

            self._save_workbook_atomic(wb)
            return self.get_by_id(job_id)

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


class ExcelEmployerRepository(ExcelBase, IEmployerRepository):
    def get_all(self) -> List[Employer]:
        with EXCEL_LOCK:
            wb = self._load_workbook(read_only=True)
            ws = wb["Employers"]
            headers = [cell.value for cell in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}

            employers = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                emp_id = str(row_dict.get("EmployerID") or "").strip()
                if not emp_id:
                    continue
                employers.append(Employer(
                    employer_id=emp_id,
                    company_name=str(row_dict.get("CompanyName") or ""),
                    contact_name=str(row_dict.get("ContactName") or ""),
                    phone=str(row_dict.get("Phone") or ""),
                    location=str(row_dict.get("Location") or ""),
                    verified=str(row_dict.get("Verified") or "Pending"),
                    created_at=str(row_dict.get("CreatedAt") or "")[:10]
                ))
            wb.close()
            return employers

    def get_by_id(self, employer_id: str) -> Optional[Employer]:
        for e in self.get_all():
            if e.employer_id.upper() == employer_id.upper():
                return e
        return None

    def create(self, emp: EmployerCreate) -> Employer:
        with EXCEL_LOCK:
            wb = openpyxl.load_workbook(self.file_path)
            ws = wb["Employers"]
            max_id = 100
            for row in ws.iter_rows(min_row=2, max_col=1, values_only=True):
                val = row[0]
                if val and str(val).startswith("EMP-"):
                    try:
                        num = int(str(val).split("-")[1])
                        if num > max_id:
                            max_id = num
                    except (IndexError, ValueError):
                        pass
            new_id = f"EMP-{max_id + 1}"
            today_str = datetime.now().strftime("%Y-%m-%d")

            new_emp = Employer(
                employer_id=new_id,
                company_name=emp.company_name,
                contact_name=emp.contact_name,
                phone=emp.phone,
                location=emp.location,
                verified="Pending",
                created_at=today_str
            )

            row_data = [
                new_emp.employer_id,
                new_emp.company_name,
                new_emp.contact_name,
                new_emp.phone,
                new_emp.location,
                new_emp.verified,
                new_emp.created_at
            ]
            ws.append(row_data)
            self._save_workbook_atomic(wb)
            return new_emp

    def update(self, employer_id: str, updates: EmployerUpdate) -> Optional[Employer]:
        with EXCEL_LOCK:
            wb = openpyxl.load_workbook(self.file_path)
            ws = wb["Employers"]
            headers = [cell.value for cell in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}

            target_row_idx = None
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, max_col=1, values_only=True), start=2):
                if row[0] and str(row[0]).strip().upper() == employer_id.strip().upper():
                    target_row_idx = row_idx
                    break

            if not target_row_idx:
                wb.close()
                return None

            update_dict = updates.model_dump(exclude_unset=True)
            field_to_col = {
                "company_name": "CompanyName",
                "contact_name": "ContactName",
                "phone": "Phone",
                "location": "Location",
                "verified": "Verified"
            }
            for field, val in update_dict.items():
                col_name = field_to_col.get(field)
                if col_name and col_name in col_map:
                    ws.cell(row=target_row_idx, column=col_map[col_name] + 1, value=val)

            self._save_workbook_atomic(wb)
            return self.get_by_id(employer_id)


class ExcelWorkerRepository(ExcelBase, IWorkerRepository):
    def get_all(self) -> List[Worker]:
        with EXCEL_LOCK:
            wb = self._load_workbook(read_only=True)
            ws = wb["Workers"]
            headers = [cell.value for cell in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}

            workers = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                w_id = str(row_dict.get("WorkerID") or "").strip()
                if not w_id:
                    continue
                workers.append(Worker(
                    worker_id=w_id,
                    phone=str(row_dict.get("Phone") or ""),
                    language=str(row_dict.get("Language") or "te"),
                    location=str(row_dict.get("Location") or "Hyderabad"),
                    locality=str(row_dict.get("Locality") or ""),
                    preferred_job_type=str(row_dict.get("PreferredJobType") or ""),
                    experience=str(row_dict.get("Experience") or "Fresher"),
                    created_at=str(row_dict.get("CreatedAt") or "")[:10]
                ))
            wb.close()
            return workers

    def get_by_phone(self, phone: str) -> Optional[Worker]:
        normalized = phone.strip()
        for w in self.get_all():
            if w.phone == normalized:
                return w
        return None

    def create(self, worker: WorkerCreate) -> Worker:
        with EXCEL_LOCK:
            existing = self.get_by_phone(worker.phone)
            if existing:
                return existing

            wb = openpyxl.load_workbook(self.file_path)
            ws = wb["Workers"]
            max_id = 500
            for row in ws.iter_rows(min_row=2, max_col=1, values_only=True):
                val = row[0]
                if val and str(val).startswith("WRK-"):
                    try:
                        num = int(str(val).split("-")[1])
                        if num > max_id:
                            max_id = num
                    except (IndexError, ValueError):
                        pass
            new_id = f"WRK-{max_id + 1}"
            today_str = datetime.now().strftime("%Y-%m-%d")

            new_worker = Worker(
                worker_id=new_id,
                phone=worker.phone,
                language=worker.language,
                location=worker.location,
                locality=worker.locality,
                preferred_job_type=worker.preferred_job_type,
                experience=worker.experience,
                created_at=today_str
            )
            row_data = [
                new_worker.worker_id,
                new_worker.phone,
                new_worker.language,
                new_worker.location,
                new_worker.locality,
                new_worker.preferred_job_type,
                new_worker.experience,
                new_worker.created_at
            ]
            ws.append(row_data)
            self._save_workbook_atomic(wb)
            return new_worker


class ExcelApplicationRepository(ExcelBase, IApplicationRepository):
    def get_all(self) -> List[Application]:
        with EXCEL_LOCK:
            wb = self._load_workbook(read_only=True)
            ws = wb["Applications"]
            headers = [cell.value for cell in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}

            apps = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                app_id = str(row_dict.get("ApplicationID") or "").strip()
                if not app_id:
                    continue
                apps.append(Application(
                    application_id=app_id,
                    worker_id=str(row_dict.get("WorkerID") or ""),
                    worker_phone=str(row_dict.get("WorkerPhone") or ""),
                    job_id=str(row_dict.get("JobID") or ""),
                    applied_at=str(row_dict.get("AppliedAt") or ""),
                    status=str(row_dict.get("Status") or "Interested")
                ))
            wb.close()
            return apps

    def get_by_id(self, app_id: str) -> Optional[Application]:
        for a in self.get_all():
            if a.application_id.upper() == app_id.upper():
                return a
        return None

    def get_by_phone(self, phone: str) -> List[Application]:
        normalized = phone.strip()
        return [a for a in self.get_all() if a.worker_phone == normalized]

    def exists_recent(self, worker_phone: str, job_id: str) -> bool:
        for a in self.get_all():
            if a.worker_phone == worker_phone and a.job_id.upper() == job_id.upper():
                return True
        return False

    def create(self, app: ApplicationCreate) -> Application:
        with EXCEL_LOCK:
            if self.exists_recent(app.worker_phone, app.job_id):
                raise ValueError("Duplicate application: you have already applied for this job.")

            wb = openpyxl.load_workbook(self.file_path)
            ws = wb["Applications"]
            max_id = 10000
            for row in ws.iter_rows(min_row=2, max_col=1, values_only=True):
                val = row[0]
                if val and str(val).startswith("APP-"):
                    try:
                        num = int(str(val).split("-")[1])
                        if num > max_id:
                            max_id = num
                    except (IndexError, ValueError):
                        pass
            new_id = f"APP-{max_id + 1}"
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_app = Application(
                application_id=new_id,
                worker_id=app.worker_id or "",
                worker_phone=app.worker_phone,
                job_id=app.job_id,
                applied_at=now_str,
                status=app.status or "Interested"
            )
            row_data = [
                new_app.application_id,
                new_app.worker_id,
                new_app.worker_phone,
                new_app.job_id,
                new_app.applied_at,
                new_app.status
            ]
            ws.append(row_data)
            self._save_workbook_atomic(wb)
            return new_app


class ExcelCategoryRepository(ExcelBase, ICategoryRepository):
    def get_all(self, active_only: bool = True) -> List[Category]:
        with EXCEL_LOCK:
            wb = self._load_workbook(read_only=True)
            ws = wb["Categories"]
            headers = [cell.value for cell in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}

            cats = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                cat_id = str(row_dict.get("CategoryID") or "").strip()
                if not cat_id:
                    continue
                active_val = row_dict.get("Active")
                is_active = True if active_val in [True, 1, "True", "1", "TRUE"] else False
                if active_only and not is_active:
                    continue
                cats.append(Category(
                    category_id=cat_id,
                    name=str(row_dict.get("Name") or ""),
                    telugu_name=str(row_dict.get("TeluguName") or ""),
                    hindi_name=str(row_dict.get("HindiName") or ""),
                    english_name=str(row_dict.get("EnglishName") or ""),
                    active=is_active
                ))
            wb.close()
            return cats


# --- Unified Facade Repository ---

class UnifiedExcelRepository(ExcelBase):
    def __init__(self, file_path: Path = DEFAULT_DATA_PATH):
        super().__init__(file_path)
        self.jobs = ExcelJobRepository(file_path)
        self.employers = ExcelEmployerRepository(file_path)
        self.workers = ExcelWorkerRepository(file_path)
        self.applications = ExcelApplicationRepository(file_path)
        self.categories = ExcelCategoryRepository(file_path)

    def set_file_path(self, path: Path):
        self.file_path = path
        self.jobs.file_path = path
        self.employers.file_path = path
        self.workers.file_path = path
        self.applications.file_path = path
        self.categories.file_path = path

    def get_storage_stats(self) -> Dict[str, Any]:
        with EXCEL_LOCK:
            wb = self._load_workbook(read_only=True)
            stats = {}
            total_records = 0
            for name in wb.sheetnames:
                ws = wb[name]
                count = max(0, ws.max_row - 1)
                stats[name] = count
                total_records += count
            wb.close()
            
            stats["total_records"] = total_records
            stats["concurrency_risk"] = "HIGH" if total_records > 500 else "NORMAL"
            stats["migration_recommended"] = total_records > 500
            return stats

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

# Singleton facade instance
excel_repo = UnifiedExcelRepository()
