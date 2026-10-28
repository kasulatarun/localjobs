from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"
    EXPIRED = "Expired"

class VerificationStatus(str, Enum):
    VERIFIED = "Verified"
    PENDING = "Pending"
    REJECTED = "Rejected"

class SalaryType(str, Enum):
    MONTH = "Month"
    DAY = "Day"
    WEEK = "Week"
    HOUR = "Hour"

class SupportedLanguage(str, Enum):
    TELUGU = "te"
    HINDI = "hi"
    ENGLISH = "en"
