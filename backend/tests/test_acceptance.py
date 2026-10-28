import pytest
from backend.app.services.ivr_service import ivr_service, IVRState
from backend.app.repositories.excel_repository import excel_repo
from backend.app.services.job_service import job_service
from backend.app.services.llm_service import llm_service, ControlledTools

def test_full_acceptance_journey_telugu():
    call_id = "ACC-CALL-TE-01"
    worker_phone = "+919848011223"

    # Step 1: Call comes in
    r1 = ivr_service.process_incoming_call(call_id, worker_phone)
    assert r1["state"] == IVRState.LANGUAGE_SELECTION.value

    # Step 2: Language = Telugu (1)
    r2 = ivr_service.process_dtmf_input(call_id, "1")
    assert r2["state"] == IVRState.CATEGORY_SELECTION.value
    assert r2["language"] == "te"

    # Step 3: Category = Driver (1)
    r3 = ivr_service.process_dtmf_input(call_id, "1")
    assert r3["state"] == IVRState.LOCATION_SELECTION.value

    # Step 4: Location = Uppal (1)
    r4 = ivr_service.process_dtmf_input(call_id, "1")
    assert r4["state"] == IVRState.JOB_RESULTS.value
    # Step 5: Real Excel job returned
    assert r4["job"]["JobID"] == "JOB-1001"
    assert r4["job"]["Salary"] == 18000
    # Step 6: Job details played/displayed
    assert "18000" in r4["prompt"]
    assert "ఉప్పల్" in r4["prompt"] or "Uppal" in r4["prompt"]

    # Step 7: Worker selects Interested (1)
    r5 = ivr_service.process_dtmf_input(call_id, "1")
    assert r5["state"] == IVRState.APPLICATION_CREATED.value
    # Step 8: Application created
    assert r5["application_id"] is not None

    # Step 9: Application appears in Excel
    apps = excel_repo.get_applications_by_phone(worker_phone)
    assert len(apps) == 1
    assert apps[0].job_id == "JOB-1001"
    assert apps[0].status == "Interested"

    # Step 10: Employer / Admin can see application
    all_apps = excel_repo.get_all_applications()
    assert any(a.application_id == r5["application_id"] for a in all_apps)

def test_full_acceptance_journey_hindi():
    call_id = "ACC-CALL-HI-01"
    worker_phone = "+919848022334"

    # 1. Incoming Call
    ivr_service.process_incoming_call(call_id, worker_phone)
    # 2. Language = Hindi (2)
    ivr_service.process_dtmf_input(call_id, "2")
    # 3. Category = Driver (1)
    ivr_service.process_dtmf_input(call_id, "1")
    # 4. Location = Uppal (1)
    r4 = ivr_service.process_dtmf_input(call_id, "1")
    assert r4["job"]["JobID"] == "JOB-1001"
    assert "उप्पल" in r4["prompt"] or "Uppal" in r4["prompt"]
    # 5. Worker selects Interested (1)
    r5 = ivr_service.process_dtmf_input(call_id, "1")
    assert r5["state"] == IVRState.APPLICATION_CREATED.value

    # Persisted in Excel
    apps = excel_repo.get_applications_by_phone(worker_phone)
    assert len(apps) == 1
    assert apps[0].job_id == "JOB-1001"

def test_full_acceptance_journey_english():
    call_id = "ACC-CALL-EN-01"
    worker_phone = "+919848033445"

    ivr_service.process_incoming_call(call_id, worker_phone)
    ivr_service.process_dtmf_input(call_id, "3") # English
    ivr_service.process_dtmf_input(call_id, "1") # Driver
    r4 = ivr_service.process_dtmf_input(call_id, "1") # Uppal
    assert r4["job"]["JobID"] == "JOB-1001"
    assert "Driver required in Uppal" in r4["prompt"]

    r5 = ivr_service.process_dtmf_input(call_id, "1") # Interested
    assert r5["state"] == IVRState.APPLICATION_CREATED.value

    apps = excel_repo.get_applications_by_phone(worker_phone)
    assert len(apps) == 1
    assert apps[0].job_id == "JOB-1001"

def test_acceptance_unverified_employer_exclusion():
    """Verify that jobs from unverified employers (EMP-106) never show to workers."""
    # JOB-1007 is from EMP-106 (Pending verification)
    public_jobs = job_service.get_public_jobs()
    for job in public_jobs:
        assert job.verified == "Verified"
        assert job.employer_id != "EMP-106"
