import os
from enum import Enum
from typing import List
from pydantic import BaseModel

class TelephonyMode(str, Enum):
    MOCK = "MOCK"
    TRIAL = "TRIAL"
    PRODUCTION = "PRODUCTION"

def normalize_postgres_url(raw_url: str) -> str:
    """Normalizes PostgreSQL connection URLs to the available Python driver (psycopg 3 or psycopg2)."""
    url = (raw_url or "").strip()
    if not url:
        return ""
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    
    if url.startswith("postgresql://"):
        try:
            import psycopg
            return url
        except ImportError:
            try:
                import psycopg2
                return url.replace("postgresql://", "postgresql+psycopg2://", 1)
            except ImportError:
                return url
    return url

class AppConfig:
    def __init__(self):
        self._app_env = None
        self._data_backend = None
        self._database_url = None

    @property
    def APP_ENV(self) -> str:
        if self._app_env is not None:
            return self._app_env
        return os.getenv("APP_ENV", "development")

    @APP_ENV.setter
    def APP_ENV(self, value: str):
        self._app_env = value

    @property
    def DATA_BACKEND(self) -> str:
        if self._data_backend is not None:
            return self._data_backend
        env_backend = os.getenv("DATA_BACKEND")
        if env_backend:
            return env_backend.lower()
        return "postgres" if self.APP_ENV == "production" else "excel"

    @DATA_BACKEND.setter
    def DATA_BACKEND(self, value: str):
        self._data_backend = value

    @property
    def DATABASE_URL(self) -> str:
        if self._database_url is not None:
            return self._database_url
        return os.getenv("DATABASE_URL", "")

    @DATABASE_URL.setter
    def DATABASE_URL(self, value: str):
        self._database_url = value

    @property
    def DEBUG(self) -> bool:
        return os.getenv("DEBUG", "false").lower() in ("true", "1")

    @property
    def HOST(self) -> str:
        return os.getenv("HOST", "0.0.0.0")

    @property
    def PORT(self) -> int:
        return int(os.getenv("PORT", "8000"))

    @property
    def is_postgres(self) -> bool:
        return self.DATA_BACKEND.lower() in ("postgres", "postgresql")

    @property
    def normalized_database_url(self) -> str:
        return normalize_postgres_url(self.DATABASE_URL)
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        origin.strip() 
        for origin in os.getenv(
            "ALLOWED_ORIGINS", 
            "http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,http://localhost:5173,https://*.pages.dev,https://*.onrender.com,*"
        ).split(",")
        if origin.strip()
    ]
    
    # Telephony & WhatsApp
    DEMO_PHONE: str = os.getenv("DEMO_PHONE", "+919848953136")
    WHATSAPP_PHONE: str = os.getenv("WHATSAPP_PHONE", "+919848953136")
    WHATSAPP_VERIFY_TOKEN: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "localjobs_whatsapp_verify_token")
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
                "badge": "DEMO HELPLINE & WHATSAPP",
                "phone_display": "+91 98489 53136",
                "raw_phone": cls.DEMO_PHONE,
                "description": "Interactive demo helpline & automated WhatsApp assistant for +919848953136.",
                "is_mock": True
            }

config = AppConfig()
