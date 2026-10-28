import os
from typing import Dict, Any, Optional
import httpx
from xml.sax.saxutils import escape

from backend.app.telephony.base import TelephonyProvider
from backend.app.services.ivr_service import ivr_service
from backend.app.security.validation import normalize_phone

class ExotelProvider(TelephonyProvider):
    def __init__(self):
        self.account_sid = os.getenv("EXOTEL_ACCOUNT_SID", "")
        self.api_key = os.getenv("EXOTEL_API_KEY", "")
        self.api_token = os.getenv("EXOTEL_API_TOKEN", "")
        self.exophone = os.getenv("EXOTEL_EXOPHONE", "")

    def is_configured(self) -> bool:
        return bool(self.account_sid and self.api_key and self.api_token and self.exophone)

    def parse_incoming_webhook(self, request_data: Dict[str, Any]) -> Dict[str, str]:
        call_id = str(request_data.get("CallSid") or request_data.get("call_id") or "")
        from_number = str(request_data.get("From") or request_data.get("caller_phone") or "")
        digits = request_data.get("Digits") or request_data.get("digits")

        try:
            phone = normalize_phone(from_number)
        except ValueError:
            phone = from_number

        return {
            "call_id": call_id,
            "caller_phone": phone,
            "digits": str(digits) if digits is not None else None
        }

    def handle_incoming_call(self, call_id: str, caller_phone: str) -> Dict[str, Any]:
        return ivr_service.process_incoming_call(call_id, caller_phone)

    def handle_dtmf(self, call_id: str, digits: Optional[str], is_timeout: bool = False) -> Dict[str, Any]:
        return ivr_service.process_dtmf_input(call_id, digits, is_timeout=is_timeout)

    def format_provider_response(self, ivr_result: Dict[str, Any]) -> str:
        """
        Generates standard Exotel-compatible XML response.
        Exotel parses <Response> <Play> <Gather> tags.
        """
        prompt = escape(ivr_result.get("prompt", ""))
        terminate = ivr_result.get("terminate", False)
        expects_dtmf = ivr_result.get("expects_dtmf", True)
        max_digits = ivr_result.get("max_digits", 1)

        if terminate:
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{prompt}</Say>
    <Hangup/>
</Response>"""

        if expects_dtmf:
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <GetDigits action="/ivr/dtmf" method="POST" numDigits="{max_digits}" timeout="6">
        <Say>{prompt}</Say>
    </GetDigits>
</Response>"""

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{prompt}</Say>
</Response>"""

    async def send_sms(self, to_phone: str, message: str) -> bool:
        if not self.is_configured():
            return False

        url = f"https://api.exotel.com/v1/Accounts/{self.account_sid}/Sms/send.json"
        auth = (self.api_key, self.api_token)
        payload = {
            "From": self.exophone,
            "To": to_phone,
            "Body": message
        }
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.post(url, data=payload, auth=auth)
                return res.status_code == 200
        except Exception:
            return False

exotel_provider = ExotelProvider()
