"""
Data Migration & Seed Utility: Excel -> PostgreSQL
Imports data/jobs.xlsx into PostgreSQL database (Supabase, Neon, or local PostgreSQL).
Idempotent: updates or preserves existing records without duplication errors.
"""

import sys
import argparse
from pathlib import Path
from datetime import date

# Ensure project root is on sys.path for direct script execution
_project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import openpyxl

from backend.app.config import config
from backend.app.repositories.postgres_repository import (
    get_engine,
    session_scope,
    init_db_postgres,
    EmployerModel,
    JobModel,
    WorkerModel,
    ApplicationModel,
    CategoryModel
)

def import_excel_to_postgres(excel_path: Path = Path("data/jobs.xlsx"), db_url: str = None, engine = None) -> dict:
    excel_path = Path(excel_path)
    if not excel_path.exists():
        raise FileNotFoundError(f"Source Excel file not found at: {excel_path.resolve()}")

    target_engine = engine or get_engine(db_url)
    init_db_postgres(target_engine)

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    summary = {
        "employers": 0,
        "jobs": 0,
        "workers": 0,
        "applications": 0,
        "categories": 0
    }

    with session_scope(target_engine) as session:
        # 1. Employers
        if "Employers" in wb.sheetnames:
            ws = wb["Employers"]
            headers = [c.value for c in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                eid = str(row_dict.get("EmployerID") or "").strip()
                if not eid:
                    continue

                existing = session.query(EmployerModel).filter_by(employer_id=eid).first()
                if not existing:
                    emp = EmployerModel(
                        employer_id=eid,
                        company_name=str(row_dict.get("CompanyName") or ""),
                        contact_name=str(row_dict.get("ContactName") or ""),
                        phone=str(row_dict.get("Phone") or ""),
                        location=str(row_dict.get("Location") or ""),
                        verified=str(row_dict.get("Verified") or "Pending"),
                        created_at=str(row_dict.get("CreatedAt") or "")[:10]
                    )
                    session.add(emp)
                    summary["employers"] += 1

        # 2. Jobs
        if "Jobs" in wb.sheetnames:
            ws = wb["Jobs"]
            headers = [c.value for c in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                jid = str(row_dict.get("JobID") or "").strip()
                if not jid:
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

                existing = session.query(JobModel).filter_by(job_id=jid).first()
                if not existing:
                    job = JobModel(
                        job_id=jid,
                        employer_id=str(row_dict.get("EmployerID") or ""),
                        job_type=str(row_dict.get("JobType") or ""),
                        location=str(row_dict.get("Location") or "Hyderabad"),
                        locality=str(row_dict.get("Locality") or ""),
                        district=str(row_dict.get("District") or "Medchal-Malkajgiri"),
                        state=str(row_dict.get("State") or "Telangana"),
                        salary=salary_int,
                        salary_type=str(row_dict.get("SalaryType") or "Month"),
                        hours=str(row_dict.get("Hours") or "8 hours"),
                        required_experience=str(row_dict.get("RequiredExperience") or "Fresher"),
                        vacancies=vacancies_int,
                        description=str(row_dict.get("Description") or ""),
                        status=str(row_dict.get("Status") or "Active"),
                        verified=str(row_dict.get("Verified") or "Pending"),
                        created_at=str(row_dict.get("CreatedAt") or "")[:10],
                        expiry_date=str(row_dict.get("ExpiryDate") or "2026-12-31")[:10]
                    )
                    session.add(job)
                    summary["jobs"] += 1

        # 3. Workers
        if "Workers" in wb.sheetnames:
            ws = wb["Workers"]
            headers = [c.value for c in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                wid = str(row_dict.get("WorkerID") or "").strip()
                phone = str(row_dict.get("Phone") or "").strip()
                if not wid or not phone:
                    continue

                existing = session.query(WorkerModel).filter_by(worker_id=wid).first()
                if not existing:
                    worker = WorkerModel(
                        worker_id=wid,
                        phone=phone,
                        language=str(row_dict.get("Language") or "te"),
                        location=str(row_dict.get("Location") or "Hyderabad"),
                        locality=str(row_dict.get("Locality") or "Uppal"),
                        preferred_job_type=str(row_dict.get("PreferredJobType") or "Driver"),
                        experience=str(row_dict.get("Experience") or "Fresher"),
                        created_at=str(row_dict.get("CreatedAt") or "")[:10]
                    )
                    session.add(worker)
                    summary["workers"] += 1

        # 4. Applications
        if "Applications" in wb.sheetnames:
            ws = wb["Applications"]
            headers = [c.value for c in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                aid = str(row_dict.get("ApplicationID") or "").strip()
                if not aid:
                    continue

                existing = session.query(ApplicationModel).filter_by(application_id=aid).first()
                if not existing:
                    app = ApplicationModel(
                        application_id=aid,
                        worker_id=str(row_dict.get("WorkerID") or "") or None,
                        worker_phone=str(row_dict.get("WorkerPhone") or ""),
                        job_id=str(row_dict.get("JobID") or ""),
                        applied_at=str(row_dict.get("AppliedAt") or ""),
                        status=str(row_dict.get("Status") or "Interested")
                    )
                    session.add(app)
                    summary["applications"] += 1

        # 5. Categories
        if "Categories" in wb.sheetnames:
            ws = wb["Categories"]
            headers = [c.value for c in ws[1]]
            col_map = {name: idx for idx, name in enumerate(headers) if name}
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                row_dict = {name: row[idx] for name, idx in col_map.items() if idx < len(row)}
                cid = str(row_dict.get("CategoryID") or "").strip()
                if not cid:
                    continue

                existing = session.query(CategoryModel).filter_by(category_id=cid).first()
                if not existing:
                    active_val = row_dict.get("Active")
                    is_active = True if active_val in (True, 1, "True", "1") else False
                    cat = CategoryModel(
                        category_id=cid,
                        name=str(row_dict.get("Name") or ""),
                        telugu_name=str(row_dict.get("TeluguName") or ""),
                        hindi_name=str(row_dict.get("HindiName") or ""),
                        english_name=str(row_dict.get("EnglishName") or ""),
                        active=is_active
                    )
                    session.add(cat)
                    summary["categories"] += 1

    wb.close()
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate LocalJobs Excel data to PostgreSQL")
    parser.add_argument("--excel", default="data/jobs.xlsx", help="Path to source Excel file")
    parser.add_argument("--db-url", default=None, help="PostgreSQL connection string (defaults to DATABASE_URL env var)")
    args = parser.parse_args()

    source = Path(args.excel)
    print(f"[*] Starting migration from {source}...")
    try:
        res = import_excel_to_postgres(excel_path=source, db_url=args.db_url)
        print("[+] Migration completed successfully!")
        print(f"    - Employers imported:    {res['employers']}")
        print(f"    - Jobs imported:         {res['jobs']}")
        print(f"    - Workers imported:      {res['workers']}")
        print(f"    - Applications imported: {res['applications']}")
        print(f"    - Categories imported:   {res['categories']}")
    except Exception as e:
        print(f"[-] Migration failed: {e}", file=sys.stderr)
        sys.exit(1)
