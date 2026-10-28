from typing import Optional, Dict, Any
from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel

from backend.app.services.ivr_service import ivr_service
from backend.app.telephony.mock import mock_telephony
from backend.app.telephony.exotel import exotel_provider
from backend.app.security.validation import mask_phone

router = APIRouter(prefix="/ivr", tags=["IVR"])

class IVRIncomingRequest(BaseModel):
    call_id: Optional[str] = None
    caller_phone: Optional[str] = None
    CallSid: Optional[str] = None
    From: Optional[str] = None

class IVRDTMFRequest(BaseModel):
    call_id: Optional[str] = None
    CallSid: Optional[str] = None
    digits: Optional[str] = None
    Digits: Optional[str] = None
    is_timeout: Optional[bool] = False

async def _extract_payload(request: Request) -> Dict[str, Any]:
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            return await request.json()
        except Exception:
            return {}
    elif "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        return dict(form)
    else:
        # Check query params or fallback
        if request.query_params:
            return dict(request.query_params)
        try:
            return await request.json()
        except Exception:
            return {}

@router.post("/incoming")
async def handle_incoming_call(request: Request):
    """
    Receives incoming call from Exotel or Local Simulator.
    Initializes IVR session, returns greeting & language prompt.
    """
    payload = await _extract_payload(request)
    call_id = payload.get("CallSid") or payload.get("call_id") or "call-sim-001"
    caller_phone = payload.get("From") or payload.get("caller_phone") or "+919848012345"

    result = ivr_service.process_incoming_call(call_id, caller_phone)

    # If Exotel called us (CallSid present or User-Agent contains Exotel)
    if "CallSid" in payload:
        xml_resp = exotel_provider.format_provider_response(result)
        return Response(content=xml_resp, media_type="application/xml")

    return result

@router.post("/dtmf")
async def handle_dtmf_input(request: Request):
    """
    Processes DTMF key presses or timeouts.
    Executes state transition in deterministic IVR state machine.
    """
    payload = await _extract_payload(request)
    call_id = payload.get("CallSid") or payload.get("call_id") or "call-sim-001"
    digits = payload.get("Digits") or payload.get("digits")
    is_timeout = str(payload.get("is_timeout", "false")).lower() in ["true", "1"]

    result = ivr_service.process_dtmf_input(call_id, digits, is_timeout=is_timeout)

    if "CallSid" in payload:
        xml_resp = exotel_provider.format_provider_response(result)
        return Response(content=xml_resp, media_type="application/xml")

    return result

@router.post("/callback")
async def handle_call_callback(request: Request):
    """Call termination or status callback from telephony carrier."""
    payload = await _extract_payload(request)
    call_id = payload.get("CallSid") or payload.get("call_id")
    if call_id:
        ivr_service.end_session(call_id)
    return {"status": "recorded", "call_id": call_id}

@router.get("/session/{call_id}")
def get_session_info(call_id: str):
    """Debug and simulator inspection endpoint."""
    session = ivr_service.get_session(call_id)
    if not session:
        return {"active": False, "call_id": call_id}
    return {
        "active": True,
        "call_id": session.call_id,
        "masked_phone": mask_phone(session.caller_phone),
        "state": session.state.value,
        "language": session.language,
        "selected_category": session.selected_category,
        "selected_locality": session.selected_locality,
        "current_job_index": session.current_job_index,
        "matched_jobs_count": len(session.matched_jobs),
        "retry_count": session.retry_count,
        "timeout_count": session.timeout_count,
        "last_prompt": session.last_prompt
    }
