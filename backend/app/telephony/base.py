from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class TelephonyProvider(ABC):
    @abstractmethod
    def parse_incoming_webhook(self, request_data: Dict[str, Any]) -> Dict[str, str]:
        """Extracts call_id, caller_phone, and any DTMF digits from webhook payload."""
        pass

    @abstractmethod
    def handle_incoming_call(self, call_id: str, caller_phone: str) -> Dict[str, Any]:
        """Initializes IVR session for incoming call."""
        pass

    @abstractmethod
    def handle_dtmf(self, call_id: str, digits: Optional[str], is_timeout: bool = False) -> Dict[str, Any]:
        """Processes DTMF input for an active call."""
        pass

    @abstractmethod
    def format_provider_response(self, ivr_result: Dict[str, Any]) -> Any:
        """Transforms generic IVR output into provider-specific response (e.g., Exotel XML/JSON)."""
        pass

    @abstractmethod
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Sends an SMS notification if supported by the provider."""
        pass
