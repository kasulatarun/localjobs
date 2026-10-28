from typing import Dict, Any, Optional
from backend.app.telephony.base import TelephonyProvider
from backend.app.services.ivr_service import ivr_service
from backend.app.security.validation import normalize_phone

class MockTelephonyProvider(TelephonyProvider):
    """
    Mock Telephony Provider for local testing, browser dialer, and automated tests.
    Enables 100% of IVR functionality without carrier contracts or call fees.
    """
    def __init__(self):
        self.sms_log = []

    def parse_incoming_webhook(self, request_data: Dict[str, Any]) -> Dict[str, str]:
        call_id = str(request_data.get("call_id") or request_data.get("CallSid") or "mock-call-1")
        raw_phone = str(request_data.get("caller_phone") or request_data.get("From") or "+919848012345")
        try:
            phone = normalize_phone(raw_phone)
        except ValueError:
            phone = "+919848012345"
            
        digits = request_data.get("digits") or request_data.get("Digits")
        return {
            "call_id": call_id,
            "caller_phone": phone,
            "digits": str(digits) if digits is not None else None
        }

    def handle_incoming_call(self, call_id: str, caller_phone: str) -> Dict[str, Any]:
        return ivr_service.process_incoming_call(call_id, caller_phone)

    def handle_dtmf(self, call_id: str, digits: Optional[str], is_timeout: bool = False) -> Dict[str, Any]:
        return ivr_service.process_dtmf_input(call_id, digits, is_timeout=is_timeout)

    def format_provider_response(self, ivr_result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "success",
            "provider": "mock",
            "data": ivr_result
        }

    async def send_sms(self, to_phone: str, message: str) -> bool:
        self.sms_log.append({"to": to_phone, "message": message})
        return True

mock_telephony = MockTelephonyProvider()
