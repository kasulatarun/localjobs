import os
import re
import secrets
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "localjobs_admin_secure_secret_token_12345")
EMPLOYER_SECRET = os.getenv("EMPLOYER_SECRET", "localjobs_employer_secure_secret_token_67890")

admin_header = APIKeyHeader(name="X-Admin-Secret", auto_error=False)
employer_header = APIKeyHeader(name="X-Employer-Secret", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)

def normalize_phone(phone: str) -> str:
    """
    Standardize Indian phone numbers into +91XXXXXXXXXX format.
    Accepts 10-digit numbers, 0-prefixed numbers, or +91 prefixed numbers.
    """
    if not phone:
        raise ValueError("Phone number cannot be empty")
    cleaned = re.sub(r"[\s\-\(\)]", "", phone.strip())
    
    # +919848012345 -> 13 chars
    if cleaned.startswith("+91") and len(cleaned) == 13 and cleaned[3:].isdigit():
        return cleaned
    # 919848012345 -> 12 chars
    if cleaned.startswith("91") and len(cleaned) == 12 and cleaned.isdigit():
        return f"+{cleaned}"
    # 09848012345 -> 11 chars
    if cleaned.startswith("0") and len(cleaned) == 11 and cleaned.isdigit():
        return f"+91{cleaned[1:]}"
    # 9848012345 -> 10 chars
    if len(cleaned) == 10 and cleaned.isdigit():
        return f"+91{cleaned}"

    # If it's a toll free like 1800XXXXXX or special mock number
    if cleaned.startswith("1800") or cleaned.startswith("+1800"):
        return cleaned

    raise ValueError(f"Invalid phone number format: {phone}")

def mask_phone(phone: str) -> str:
    """Mask phone number for safe logging (no full PII in logs)."""
    if not phone or len(phone) < 7:
        return "***"
    return f"{phone[:6]}****{phone[-2:]}"

def sanitize_string(val: Optional[str], max_length: int = 500) -> str:
    """Sanitize text input by removing control characters, trimming, and enforcing length."""
    if not val:
        return ""
    # Strip HTML tags
    cleaned = re.sub(r"<[^>]*>", "", val)
    cleaned = cleaned.replace("\r", " ").strip()
    return cleaned[:max_length]

def verify_admin(
    x_admin_secret: Optional[str] = Security(admin_header),
    auth: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme)
) -> bool:
    token = x_admin_secret
    if not token and auth:
        token = auth.credentials
    if not token or not secrets.compare_digest(token, ADMIN_SECRET):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid Admin Secret"
        )
    return True

def verify_employer(
    x_employer_secret: Optional[str] = Security(employer_header),
    auth: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme)
) -> bool:
    token = x_employer_secret
    if not token and auth:
        token = auth.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Missing Employer Secret"
        )
    # Allow employer token or admin token
    valid_employer = secrets.compare_digest(token, EMPLOYER_SECRET)
    valid_admin = secrets.compare_digest(token, ADMIN_SECRET)
    if not (valid_employer or valid_admin):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid Employer Secret"
        )
    return True
