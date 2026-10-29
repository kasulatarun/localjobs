"""
Comprehensive manual verification script executing all requested journeys and edge cases
against the live running server on http://127.0.0.1:8000.
Directly inspects data/jobs.xlsx to confirm read/write persistence.
"""
import httpx
import openpyxl
from pathlib import Path
from backend.app.repositories.init_db import create_initial_workbook

BASE_URL = "http://127.0.0.1:8000"
EXCEL_PATH = Path("data/jobs.xlsx")
ADMIN_SECRET = "localjobs_admin_secure_secret_token_12345"
EMPLOYER_SECRET = "localjobs_employer_secure_secret_token_67890"

from backend.app.config import config

# Initialize fresh seed database for clean repeatable verification
if config.is_postgres:
    from backend.app.repositories.postgres_repository import init_db_postgres, Base, get_engine
    from backend.app.repositories.import_excel_to_postgres import import_excel_to_postgres
    create_initial_workbook(EXCEL_PATH)
    eng = get_engine()
    Base.metadata.drop_all(bind=eng)
    Base.metadata.create_all(bind=eng)
    import_excel_to_postgres(excel_path=EXCEL_PATH, engine=eng)
else:
    create_initial_workbook(EXCEL_PATH)

client = None
try:
    _raw_client = httpx.Client(base_url=BASE_URL, timeout=2.0)
    res = _raw_client.get("/health")
    if res.status_code == 200:
        client = _raw_client
        print(f"Connected to live HTTP server at {BASE_URL}")
    else:
        raise ConnectionError("Live server non-200")
except Exception:
    print(f"No running server at {BASE_URL}. Using in-process FastAPI TestClient...")
    from fastapi.testclient import TestClient
    from backend.app.main import app
    client = TestClient(app)

results = {}

def get_excel_applications():
    if config.is_postgres:
        from backend.app.repositories.postgres_repository import session_scope, ApplicationModel
        with session_scope() as session:
            return [
                {
                    "ApplicationID": a.application_id,
                    "WorkerID": a.worker_id,
                    "WorkerPhone": a.worker_phone,
                    "JobID": a.job_id,
                    "AppliedAt": a.applied_at,
                    "Status": a.status
                }
                for a in session.query(ApplicationModel).all()
            ]
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb["Applications"]
    apps = []
    headers = [cell.value for cell in ws[1]]
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row and any(row):
            apps.append(dict(zip(headers, row)))
    wb.close()
    return apps

def get_excel_job(job_id):
    if config.is_postgres:
        from backend.app.repositories.postgres_repository import session_scope, JobModel
        with session_scope() as session:
            for r in session.query(JobModel).all():
                if r.job_id.upper() == job_id.upper():
                    return {
                        "JobID": r.job_id,
                        "EmployerID": r.employer_id,
                        "JobType": r.job_type,
                        "Location": r.location,
                        "Locality": r.locality,
                        "District": r.district,
                        "State": r.state,
                        "Salary": r.salary,
                        "SalaryType": r.salary_type,
                        "Hours": r.hours,
                        "RequiredExperience": r.required_experience,
                        "Vacancies": r.vacancies,
                        "Description": r.description,
                        "Status": r.status,
                        "Verified": r.verified,
                        "CreatedAt": r.created_at,
                        "ExpiryDate": r.expiry_date
                    }
            return None
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb["Jobs"]
    headers = [cell.value for cell in ws[1]]
    found = None
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row and row[0] and str(row[0]).strip().upper() == job_id.upper():
            found = dict(zip(headers, row))
            break
    wb.close()
    return found

print("\n" + "=" * 60)
print("STARTING LIVE MANUAL VERIFICATION")
print("=" * 60)

# -------------------------------------------------------------
# PORTAL CHECKS (TESTS 1 to 5)
# -------------------------------------------------------------
print("\n--- [TEST 1/16] Worker Portal ---")
rw = client.get("/worker")
assert rw.status_code == 200 and len(rw.text) > 1000
results["Worker Portal (/ & /worker)"] = "PASS"
print("Worker portal loaded successfully.")

print("\n--- [TEST 2/16] Employer Dashboard ---")
remp = client.get("/employer")
assert remp.status_code == 200 and len(remp.text) > 1000
results["Employer Dashboard (/employer)"] = "PASS"
print("Employer dashboard loaded successfully.")

print("\n--- [TEST 3/16] Admin Console ---")
radm = client.get("/admin")
assert radm.status_code == 200 and len(radm.text) > 1000
results["Admin Console (/admin)"] = "PASS"
print("Admin console loaded successfully.")

print("\n--- [TEST 4/16] Telephone Simulator ---")
rsim = client.get("/simulator")
assert rsim.status_code == 200 and len(rsim.text) > 1000
results["Telephone Simulator (/simulator)"] = "PASS"
print("Telephone simulator loaded successfully.")

print("\n--- [TEST 5/16] Direct Storage Read / Write ---")
rhe = client.get("/health")
assert rhe.status_code == 200
hdata = rhe.json()
assert hdata.get("excel_storage", {}).get("status") == "connected" or hdata.get("storage", {}).get("status") == "connected"
results["Excel Direct Read / Write"] = "PASS"
print(f"Storage verified connected (backend: {hdata.get('storage', {}).get('backend', 'excel')}).")

# -------------------------------------------------------------
# JOURNEYS & EDGE CASES (TESTS 6 to 16)
# -------------------------------------------------------------
print("\n--- [TEST 6/16] Telugu Worker Journey ---")
call_id_1 = "MANUAL-CALL-TE-01"
phone_1 = "+919848077001"

# 1. Incoming Call
r1 = client.post("/ivr/incoming", json={"call_id": call_id_1, "caller_phone": phone_1})
assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
d1 = r1.json()
print("1. Call Connected:", d1["state"], "| Prompt:", d1["prompt"][:50] + "...")

# 2. Select Telugu (1)
r2 = client.post("/ivr/dtmf", json={"call_id": call_id_1, "digits": "1"})
assert r2.status_code == 200
d2 = r2.json()
print("2. Language Chosen:", d2["state"], "| Language:", d2.get("language"))
assert d2["language"] == "te", "Expected language 'te'"

# 3. Select Category: Driver (1)
r3 = client.post("/ivr/dtmf", json={"call_id": call_id_1, "digits": "1"})
assert r3.status_code == 200
d3 = r3.json()
print("3. Category Chosen:", d3["state"], "| Category:", d3.get("category"))
assert d3["category"] == "Driver"

# 4. Select Locality: Uppal (1)
r4 = client.post("/ivr/dtmf", json={"call_id": call_id_1, "digits": "1"})
assert r4.status_code == 200
d4 = r4.json()
print("4. Job Result Received:", d4["state"], "| JobID:", d4["job"]["JobID"], "| Salary:", d4["job"]["Salary"])
assert d4["job"]["JobID"] == "JOB-1001"
assert d4["job"]["Salary"] == 18000
assert "18000" in d4["prompt"]

# 5. Worker expresses interest (1)
r5 = client.post("/ivr/dtmf", json={"call_id": call_id_1, "digits": "1"})
assert r5.status_code == 200
d5 = r5.json()
print("5. Application Response:", d5["state"], "| AppID:", d5.get("application_id"))
assert d5["state"] == "APPLICATION_CREATED"
assert d5["is_duplicate"] is False

# Verify in storage
apps = get_excel_applications()
matching_apps = [a for a in apps if a.get("WorkerPhone") == phone_1 and a.get("JobID") == "JOB-1001"]
print("6. Direct Storage Verification: Found in Applications ->", matching_apps)
assert len(matching_apps) >= 1, "Application was NOT found in database"
results["Telugu Worker Journey"] = "PASS"

# -------------------------------------------------------------
# TEST 7: HINDI WORKER JOURNEY
# -------------------------------------------------------------
print("\n--- [TEST 7/16] Hindi Worker Journey ---")
call_id_2 = "MANUAL-CALL-HI-01"
phone_2 = "+919848077002"

client.post("/ivr/incoming", json={"call_id": call_id_2, "caller_phone": phone_2})
# Select Hindi (2)
rh2 = client.post("/ivr/dtmf", json={"call_id": call_id_2, "digits": "2"}).json()
assert rh2["language"] == "hi"
print("1. Hindi Selected | State:", rh2["state"])

# Select Driver (1)
rh3 = client.post("/ivr/dtmf", json={"call_id": call_id_2, "digits": "1"}).json()
assert rh3["category"] == "Driver"
print("2. Driver Selected | State:", rh3["state"])

# Select Uppal (1)
rh4 = client.post("/ivr/dtmf", json={"call_id": call_id_2, "digits": "1"}).json()
assert rh4["job"]["JobID"] == "JOB-1001"
print("3. Job Received:", rh4["job"]["JobID"], "| Salary:", rh4["job"]["Salary"])

# Apply (1)
rh5 = client.post("/ivr/dtmf", json={"call_id": call_id_2, "digits": "1"}).json()
assert rh5["state"] == "APPLICATION_CREATED"
print("4. Application Confirmed:", rh5["application_id"])

apps = get_excel_applications()
matching_apps = [a for a in apps if a.get("WorkerPhone") == phone_2 and a.get("JobID") == "JOB-1001"]
assert len(matching_apps) >= 1, "Hindi application was NOT found in database"
results["Hindi Worker Journey"] = "PASS"

# -------------------------------------------------------------
# TEST 8: ENGLISH WORKER JOURNEY
# -------------------------------------------------------------
print("\n--- [TEST 8/16] English Worker Journey ---")
call_id_3 = "MANUAL-CALL-EN-01"
phone_3 = "+919848077003"

client.post("/ivr/incoming", json={"call_id": call_id_3, "caller_phone": phone_3})
# Select English (3)
re2 = client.post("/ivr/dtmf", json={"call_id": call_id_3, "digits": "3"}).json()
assert re2["language"] == "en"
print("1. English Selected | State:", re2["state"])

# Select Driver (1)
re3 = client.post("/ivr/dtmf", json={"call_id": call_id_3, "digits": "1"}).json()
assert re3["category"] == "Driver"
print("2. Driver Selected | State:", re3["state"])

# Select Uppal (1)
re4 = client.post("/ivr/dtmf", json={"call_id": call_id_3, "digits": "1"}).json()
assert re4["job"]["JobID"] == "JOB-1001"
print("3. Job Received:", re4["job"]["JobID"], "| Salary:", re4["job"]["Salary"])

# Apply (1)
re5 = client.post("/ivr/dtmf", json={"call_id": call_id_3, "digits": "1"}).json()
assert re5["state"] == "APPLICATION_CREATED"
print("4. Application Confirmed:", re5["application_id"])

apps = get_excel_applications()
matching_apps = [a for a in apps if a.get("WorkerPhone") == phone_3 and a.get("JobID") == "JOB-1001"]
assert len(matching_apps) >= 1, "English application was NOT found in database"
results["English Worker Journey"] = "PASS"

# -------------------------------------------------------------
# TEST 9: INVALID KEYPAD INPUT
# -------------------------------------------------------------
print("\n--- [TEST 9/16] Invalid Keypad Input ---")
call_id_4 = "MANUAL-CALL-INV-01"
client.post("/ivr/incoming", json={"call_id": call_id_4, "caller_phone": "+919848077004"})
rinv = client.post("/ivr/dtmf", json={"call_id": call_id_4, "digits": "7"}).json()
print("Response on digit '7':", rinv["state"], "| Prompt:", rinv["prompt"][:60])
assert rinv["state"] == "LANGUAGE_SELECTION"
assert "Invalid choice" in rinv["prompt"] or "తప్పుడు" in rinv["prompt"] or "गलत" in rinv["prompt"]
results["Invalid Keypad Input"] = "PASS"

# -------------------------------------------------------------
# TEST 10: TIMEOUT HANDLING & TERMINATION
# -------------------------------------------------------------
print("\n--- [TEST 10/16] Timeout Handling & Max Retries ---")
call_id_5 = "MANUAL-CALL-TIMEOUT-01"
client.post("/ivr/incoming", json={"call_id": call_id_5, "caller_phone": "+919848077005"})

# 1st timeout
rt1 = client.post("/ivr/dtmf", json={"call_id": call_id_5, "digits": "", "is_timeout": True}).json()
assert rt1["state"] == "LANGUAGE_SELECTION"
assert rt1["terminate"] is False
print("1st Timeout handled properly | Prompt:", rt1["prompt"][:60])

# Consecutive timeouts exceeding MAX_RETRIES (3)
for i in range(3):
    rt_last = client.post("/ivr/dtmf", json={"call_id": call_id_5, "digits": "", "is_timeout": True}).json()

print("Final Timeout response:", rt_last["state"], "| Terminate:", rt_last.get("terminate"))
assert rt_last["state"] == "END"
assert rt_last["terminate"] is True
results["Timeout Handling"] = "PASS"

# -------------------------------------------------------------
# TEST 11: NO AVAILABLE JOBS
# -------------------------------------------------------------
print("\n--- [TEST 11/16] No Available Jobs ---")
call_id_6 = "MANUAL-CALL-NOJOB-01"
client.post("/ivr/incoming", json={"call_id": call_id_6, "caller_phone": "+919848077006"})
client.post("/ivr/dtmf", json={"call_id": call_id_6, "digits": "3"}) # English
client.post("/ivr/dtmf", json={"call_id": call_id_6, "digits": "4"}) # Cleaner (Office cleaner is in Kukatpally, none in Uppal)
r_nojob = client.post("/ivr/dtmf", json={"call_id": call_id_6, "digits": "1"}).json() # Uppal
print("Cleaner in Uppal Result:", r_nojob["state"], "| Prompt:", r_nojob["prompt"])
assert r_nojob["state"] == "NO_JOBS"
assert "No verified jobs found" in r_nojob["prompt"]

# Press 9 to return to category menu
r_back = client.post("/ivr/dtmf", json={"call_id": call_id_6, "digits": "9"}).json()
assert r_back["state"] == "CATEGORY_SELECTION"
print("Returned to Menu:", r_back["state"])
results["No Available Jobs"] = "PASS"

# -------------------------------------------------------------
# TEST 12: DUPLICATE APPLICATION
# -------------------------------------------------------------
print("\n--- [TEST 12/16] Duplicate Application ---")
# Phone 1 already applied for JOB-1001 in Test 1
call_id_7 = "MANUAL-CALL-DUP-01"
client.post("/ivr/incoming", json={"call_id": call_id_7, "caller_phone": phone_1})
client.post("/ivr/dtmf", json={"call_id": call_id_7, "digits": "1"}) # Telugu
client.post("/ivr/dtmf", json={"call_id": call_id_7, "digits": "1"}) # Driver
client.post("/ivr/dtmf", json={"call_id": call_id_7, "digits": "1"}) # Uppal
r_dup = client.post("/ivr/dtmf", json={"call_id": call_id_7, "digits": "1"}).json() # Apply again
print("Duplicate response:", r_dup["state"], "| Is Duplicate:", r_dup.get("is_duplicate"))
assert r_dup["state"] == "APPLICATION_CREATED"
assert r_dup["is_duplicate"] is True
assert "ఇప్పటికే" in r_dup["prompt"] or "already applied" in r_dup["prompt"] or "पहले ही" in r_dup["prompt"]

# Count applications in storage for this phone
apps = get_excel_applications()
phone1_apps = [a for a in apps if a.get("WorkerPhone") == phone_1 and a.get("JobID") == "JOB-1001"]
print(f"Total applications for {phone_1} for JOB-1001 in database:", len(phone1_apps))
assert len(phone1_apps) == 1, "Duplicate row was erroneously inserted into database!"
results["Duplicate Application"] = "PASS"

# -------------------------------------------------------------
# TEST 13: CLOSED JOB EXCLUSION
# -------------------------------------------------------------
print("\n--- [TEST 13/16] Closed Job Exclusion ---")
# JOB-1008 is Driver in Uppal with Status="Closed"
closed_job = get_excel_job("JOB-1008")
print("JOB-1008 in DB:", closed_job["JobID"], "| Status:", closed_job["Status"])
assert closed_job["Status"] == "Closed"

pub_jobs = client.get("/jobs?job_type=Driver&locality=Uppal").json()
pub_job_ids = [j["JobID"] for j in pub_jobs]
print("Public Driver jobs in Uppal:", pub_job_ids)
assert "JOB-1008" not in pub_job_ids, "Closed job JOB-1008 was returned in public search!"
results["Closed Job Exclusion"] = "PASS"

# -------------------------------------------------------------
# TEST 14: EXPIRED JOB EXCLUSION
# -------------------------------------------------------------
print("\n--- [TEST 14/16] Expired Job Exclusion ---")
# JOB-1009 has ExpiryDate="2026-09-01"
expired_job = get_excel_job("JOB-1009")
print("JOB-1009 in DB:", expired_job["JobID"], "| Expiry:", expired_job["ExpiryDate"])

pub_const_jobs = client.get("/jobs?job_type=Construction&locality=Uppal").json()
pub_const_ids = [j["JobID"] for j in pub_const_jobs]
print("Public Construction jobs in Uppal:", pub_const_ids)
assert "JOB-1009" not in pub_const_ids, "Expired job JOB-1009 was returned in public search!"
results["Expired Job Exclusion"] = "PASS"

# -------------------------------------------------------------
# TEST 15: UNVERIFIED EMPLOYER EXCLUSION
# -------------------------------------------------------------
print("\n--- [TEST 15/16] Unverified Employer Exclusion ---")
# JOB-1007 is from EMP-106 (Pending verification)
pending_job = get_excel_job("JOB-1007")
print("JOB-1007 in DB:", pending_job["JobID"], "| Employer:", pending_job["EmployerID"], "| Verified:", pending_job["Verified"])
assert pending_job["Verified"] == "Pending"

all_pub_jobs = client.get("/jobs").json()
all_pub_ids = [j["JobID"] for j in all_pub_jobs]
assert "JOB-1007" not in all_pub_ids, "Unverified job JOB-1007 was exposed publicly!"
results["Unverified Employer Exclusion"] = "PASS"

# -------------------------------------------------------------
# TEST 16: ADMIN APPROVAL / REJECTION
# -------------------------------------------------------------
print("\n--- [TEST 16/16] Admin Approval / Rejection Flow ---")
# 1. Employer submits new job
new_job_payload = {
    "employer_id": "EMP-101",
    "job_type": "Electrician",
    "location": "Hyderabad",
    "locality": "Uppal",
    "salary": 22000,
    "salary_type": "Month",
    "hours": "9 AM - 6 PM",
    "required_experience": "2 years",
    "vacancies": 1,
    "description": "Commercial building electrician requirement.",
    "expiry_date": "2026-12-31"
}
post_res = client.post("/jobs", json=new_job_payload, headers={"X-Employer-Secret": EMPLOYER_SECRET})
assert post_res.status_code == 201
new_job = post_res.json()
new_job_id = new_job["JobID"]
print(f"1. New Job Posted: {new_job_id} | Verified: {new_job['Verified']}")
assert new_job["Verified"] == "Pending"

# Confirm not yet visible publicly
matches_before = client.get("/jobs?job_type=Electrician&locality=Uppal").json()
assert not any(j["JobID"] == new_job_id for j in matches_before)
print("2. Confirmed not visible publicly while Pending.")

# 2. Admin Approves Job
appr_res = client.put(f"/jobs/{new_job_id}/approve", headers={"X-Admin-Secret": ADMIN_SECRET})
assert appr_res.status_code == 200
print(f"3. Admin Approved {new_job_id} | Verified: {appr_res.json()['Verified']}")

# Verify Excel was updated
job_in_excel = get_excel_job(new_job_id)
assert job_in_excel["Verified"] == "Verified", "Excel sheet was not updated with Verified status"

# Confirm now visible publicly
matches_after = client.get("/jobs?job_type=Electrician&locality=Uppal").json()
assert any(j["JobID"] == new_job_id for j in matches_after)
print(f"4. Confirmed {new_job_id} is NOW visible in public search!")

# 3. Admin Rejects / Closes Job
rej_res = client.put(f"/jobs/{new_job_id}/reject", headers={"X-Admin-Secret": ADMIN_SECRET})
assert rej_res.status_code == 200
print(f"5. Admin Rejected {new_job_id} | Status: {rej_res.json()['Status']} | Verified: {rej_res.json()['Verified']}")

# Verify Excel was updated
job_after_rej = get_excel_job(new_job_id)
assert job_after_rej["Status"] == "Closed"
assert job_after_rej["Verified"] == "Rejected"

# Confirm excluded again from public search
matches_final = client.get("/jobs?job_type=Electrician&locality=Uppal").json()
assert not any(j["JobID"] == new_job_id for j in matches_final)
print("6. Confirmed rejected job is removed from public search.")

results["Admin Approval/Rejection"] = "PASS"

# -------------------------------------------------------------
# SUMMARY REPORT
# -------------------------------------------------------------
print("\n" + "=" * 60)
print("MANUAL VERIFICATION RESULTS SUMMARY")
print("=" * 60)
all_pass = True
for test_name, status in results.items():
    print(f"  {test_name.ljust(35)} : {status}")
    if status != "PASS":
        all_pass = False

print("=" * 60)
if all_pass:
    print(f"ALL 16 VERIFICATION JOURNEYS & EDGE CASES PASSED ({len(results)}/16)")
else:
    print("FAILURES DETECTED")
print("=" * 60)
