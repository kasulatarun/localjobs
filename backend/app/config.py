import os
from enum import Enum
from typing import List
from pydantic import BaseModel

class TelephonyMode(str, Enum):
    MOCK = "MOCK"
    TRIAL = "TRIAL"
    PRODUCTION = "PRODUCTION"

class AppConfig:
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        origin.strip() 
        for origin in os.getenv(
            "ALLOWED_ORIGINS", 
            "http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,http://localhost:5173,https://*.pages.dev,https://*.onrender.com,*"
        ).split(",")
        if origin.strip()
    ]
    
    # Telephony
    EXOTEL_ACCOUNT_SID: str = os.getenv("EXOTEL_ACCOUNT_SID", "")
    EXOTEL_API_KEY: str = os.getenv("EXOTEL_API_KEY", "")
    EXOTEL_API_TOKEN: str = os.getenv("EXOTEL_API_TOKEN", "")
    EXOTEL_EXOPHONE: str = os.getenv("EXOTEL_EXOPHONE", "")

    # Security Secrets
    ADMIN_SECRET: str = os.getenv("ADMIN_SECRET", "localjobs_admin_secure_secret_token_12345")
    EMPLOYER_SECRET: str = os.getenv("EMPLOYER_SECRET", "localjobs_employer_secure_secret_token_67890")

    @classmethod
    def get_telephony_mode(cls) -> TelephonyMode:
        if not (cls.EXOTEL_ACCOUNT_SID and cls.EXOTEL_API_KEY and cls.EXOTEL_API_TOKEN and cls.EXOTEL_EXOPHONE):
            return TelephonyMode.MOCK
        if cls.EXOTEL_EXOPHONE.startswith("1800") or cls.EXOTEL_EXOPHONE.startswith("+1800"):
            return TelephonyMode.PRODUCTION
        return TelephonyMode.TRIAL

    @classmethod
    def get_telephony_display(cls) -> dict:
        mode = cls.get_telephony_mode()
        if mode == TelephonyMode.PRODUCTION:
            return {
                "mode": "PRODUCTION",
                "badge": "OFFICIAL TOLL-FREE",
                "phone_display": cls.EXOTEL_EXOPHONE,
                "description": "Live production 1800 toll-free helpline operated via Exotel carrier network.",
                "is_mock": False
            }
        elif mode == TelephonyMode.TRIAL:
            return {
                "mode": "TRIAL",
                "badge": "TELEPHONY TRIAL",
                "phone_display": cls.EXOTEL_EXOPHONE,
                "description": "Exotel developer sandbox trial number connected. Limited test calls permitted.",
                "is_mock": False
            }
        else:
            return {
                "mode": "MOCK",
                "badge": "SIMULATED 1800 (₹0 DEMO MODE)",
                "phone_display": "1800-DEMO-SIM (Mock IVR)",
                "description": "Zero-budget public demo mode. No carrier toll-free number is purchased yet. Use our interactive web/CLI dialer to test real DTMF voice IVR.",
                "is_mock": True
            }

config = AppConfig()
