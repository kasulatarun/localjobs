import pytest
from backend.app.services.ivr_service import ivr_service, IVRState
from backend.app.repositories.excel_repository import excel_repo

def test_ivr_telugu_complete_journey():
    call_id = "test-call-te-001"
    phone = "+919848011111"

    # 1. Incoming Call -> Welcome & Language prompt
    resp = ivr_service.process_incoming_call(call_id, phone)
    assert resp["state"] == IVRState.LANGUAGE_SELECTION.value
    assert "తెలుగు" in resp["prompt"] or "Telugu" in resp["prompt"]

    # 2. Select Telugu (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.CATEGORY_SELECTION.value
    assert resp["language"] == "te"
    assert "డ్రైవర్" in resp["prompt"]

    # 3. Select Category: Driver (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.LOCATION_SELECTION.value
    assert "ఉప్పల్" in resp["prompt"]

    # 4. Select Location: Uppal (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.JOB_RESULTS.value
    assert "ఉద్యోగం" in resp["prompt"]
    assert "18000" in resp["prompt"]
    assert "JOB-1001" == resp["job"]["JobID"]

    # 5. Worker presses '1' (Interested)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.APPLICATION_CREATED.value
    assert "ధన్యవాదాలు" in resp["prompt"]
    assert resp["is_duplicate"] is False

    # Verify application persisted in Excel
    apps = excel_repo.get_applications_by_phone(phone)
    assert len(apps) == 1
    assert apps[0].job_id == "JOB-1001"

def test_ivr_hindi_complete_journey():
    call_id = "test-call-hi-001"
    phone = "+919848022222"

    # 1. Incoming Call
    ivr_service.process_incoming_call(call_id, phone)

    # 2. Select Hindi (2)
    resp = ivr_service.process_dtmf_input(call_id, "2")
    assert resp["state"] == IVRState.CATEGORY_SELECTION.value
    assert resp["language"] == "hi"
    assert "ड्राइवर" in resp["prompt"]

    # 3. Select Driver (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.LOCATION_SELECTION.value
    assert "उप्पल" in resp["prompt"]

    # 4. Select Uppal (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.JOB_RESULTS.value
    assert "नौकरी" in resp["prompt"]

    # 5. Apply (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.APPLICATION_CREATED.value
    assert "धन्यवाद" in resp["prompt"]

def test_ivr_english_complete_journey():
    call_id = "test-call-en-001"
    phone = "+919848033333"

    # 1. Incoming Call
    ivr_service.process_incoming_call(call_id, phone)

    # 2. Select English (3)
    resp = ivr_service.process_dtmf_input(call_id, "3")
    assert resp["state"] == IVRState.CATEGORY_SELECTION.value
    assert resp["language"] == "en"
    assert "Driver" in resp["prompt"]

    # 3. Select Driver (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.LOCATION_SELECTION.value

    # 4. Select Uppal (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.JOB_RESULTS.value
    assert "Job 1:" in resp["prompt"]

    # 5. Apply (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.APPLICATION_CREATED.value
    assert "Thank you" in resp["prompt"]

def test_ivr_invalid_language_and_retry():
    call_id = "test-call-err-001"
    phone = "+919848044444"

    ivr_service.process_incoming_call(call_id, phone)
    
    # Press invalid key '7'
    resp = ivr_service.process_dtmf_input(call_id, "7")
    assert resp["state"] == IVRState.LANGUAGE_SELECTION.value
    assert "Invalid choice" in resp["prompt"]

def test_ivr_timeout_handling():
    call_id = "test-call-timeout-001"
    phone = "+919848055555"

    ivr_service.process_incoming_call(call_id, phone)

    # Simulate timeout
    resp = ivr_service.process_dtmf_input(call_id, "", is_timeout=True)
    assert resp["state"] == IVRState.LANGUAGE_SELECTION.value
    assert "did not receive any input" in resp["prompt"]

def test_ivr_max_retries_termination():
    call_id = "test-call-maxretry-001"
    phone = "+919848066666"

    ivr_service.process_incoming_call(call_id, phone)

    # Exceed timeout 4 times (> MAX_RETRIES)
    for _ in range(4):
        resp = ivr_service.process_dtmf_input(call_id, "", is_timeout=True)
    
    assert resp["state"] == IVRState.END.value
    assert resp["terminate"] is True

def test_ivr_no_jobs_scenario():
    call_id = "test-call-nojobs-001"
    phone = "+919848077777"

    ivr_service.process_incoming_call(call_id, phone)
    # English (3)
    ivr_service.process_dtmf_input(call_id, "3")
    # Category 4: Cleaner (has job in Kukatpally, none in Uppal)
    ivr_service.process_dtmf_input(call_id, "4")
    # Select Uppal (1)
    resp = ivr_service.process_dtmf_input(call_id, "1")
    assert resp["state"] == IVRState.NO_JOBS.value
    assert "No verified jobs found" in resp["prompt"]

    # Press 9 to return to category menu
    resp = ivr_service.process_dtmf_input(call_id, "9")
    assert resp["state"] == IVRState.CATEGORY_SELECTION.value

def test_ivr_duplicate_application_prevention():
    call_id = "test-call-dup-001"
    phone = "+919848088888"

    # 1st Application
    ivr_service.process_incoming_call(call_id, phone)
    ivr_service.process_dtmf_input(call_id, "3") # English
    ivr_service.process_dtmf_input(call_id, "1") # Driver
    ivr_service.process_dtmf_input(call_id, "1") # Uppal
    resp = ivr_service.process_dtmf_input(call_id, "1") # Apply
    assert resp["is_duplicate"] is False
    assert "Thank you" in resp["prompt"]

    # Call again from same number
    call_id_2 = "test-call-dup-002"
    ivr_service.process_incoming_call(call_id_2, phone)
    ivr_service.process_dtmf_input(call_id_2, "3")
    ivr_service.process_dtmf_input(call_id_2, "1")
    ivr_service.process_dtmf_input(call_id_2, "1")
    resp2 = ivr_service.process_dtmf_input(call_id_2, "1")
    assert resp2["is_duplicate"] is True
    assert "already applied" in resp2["prompt"]
