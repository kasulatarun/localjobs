from typing import Dict, Any, Optional
from fastapi import APIRouter, Request, Response, Query, HTTPException
from pydantic import BaseModel

from backend.app.services.whatsapp_service import whatsapp_service
from backend.app.config import config

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])

class SimulateMessageRequest(BaseModel):
    from_phone: str = "+919848953136"
    message: str = "Hi"

class SimulateMessageResponse(BaseModel):
    status: str
    from_phone: str
    reply: str
    helpline: str

@router.get("/webhook")
async def verify_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token")
):
    """
    Standard Meta WhatsApp Cloud API Webhook Verification handshake.
    """
    expected_token = getattr(config, "WHATSAPP_VERIFY_TOKEN", "localjobs_whatsapp_verify_token")
    if hub_mode == "subscribe" and hub_verify_token == expected_token:
        return Response(content=hub_challenge or "", media_type="text/plain")
    return Response(content="Verification token mismatch", status_code=403)

@router.post("/webhook")
async def handle_whatsapp_webhook(request: Request):
    """
    Parses inbound WhatsApp webhooks from Meta Cloud API or Twilio,
    processes the conversation in the user's preferred language, and returns the response.
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    from_phone = "+919848953136"
    incoming_text = ""

    # 1. Check Meta WhatsApp Cloud API structure
    entry = body.get("entry", [])
    if entry and isinstance(entry, list):
        changes = entry[0].get("changes", [])
        if changes:
            value = changes[0].get("value", {})
            messages = value.get("messages", [])
            if messages:
                msg = messages[0]
                from_phone = msg.get("from", from_phone)
                if not from_phone.startswith("+"):
                    from_phone = "+" + from_phone
                if msg.get("type") == "text":
                    incoming_text = msg.get("text", {}).get("body", "")
                elif msg.get("type") == "interactive":
                    interactive = msg.get("interactive", {})
                    incoming_text = (
                        interactive.get("button_reply", {}).get("id")
                        or interactive.get("list_reply", {}).get("id")
                        or ""
                    )

    # 2. Check Twilio WhatsApp structure
    elif "From" in body and "Body" in body:
        from_phone = body.get("From", "").replace("whatsapp:", "")
        incoming_text = body.get("Body", "")

    # 3. Direct/Simulated JSON payload: {"from_phone": "+91...", "message": "1"}
    elif "from_phone" in body or "message" in body:
        from_phone = body.get("from_phone", from_phone)
        incoming_text = body.get("message", "")

    if not incoming_text:
        return {"status": "ignored", "reason": "No text message found"}

    reply_text = whatsapp_service.process_message(from_phone, incoming_text)

    return {
        "status": "success",
        "to_phone": from_phone,
        "reply": reply_text
    }

@router.post("/simulate", response_model=SimulateMessageResponse)
def simulate_whatsapp_interaction(req: SimulateMessageRequest):
    """
    Direct simulation endpoint for testing automated multi-lingual WhatsApp responses.
    """
    reply = whatsapp_service.process_message(req.from_phone, req.message)
    return SimulateMessageResponse(
        status="success",
        from_phone=req.from_phone,
        reply=reply,
        helpline=getattr(config, "DEMO_PHONE", "+919848953136")
    )

@router.post("/reset")
def reset_whatsapp_session(phone: str = "+919848953136"):
    """Resets the WhatsApp conversation state for testing."""
    whatsapp_service.reset_session(phone)
    return {"status": "reset", "phone": phone}
