from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .common import VerificationStatus

class EmployerBase(BaseModel):
    company_name: str = Field(..., alias="CompanyName")
    contact_name: str = Field(..., alias="ContactName")
    phone: str = Field(..., alias="Phone")
    location: str = Field(..., alias="Location")
    verified: str = Field(default=VerificationStatus.PENDING.value, alias="Verified")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"), alias="CreatedAt")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

class EmployerCreate(BaseModel):
    company_name: str
    contact_name: str
    phone: str
    location: str

class EmployerUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    verified: Optional[str] = None

class Employer(EmployerBase):
    employer_id: str = Field(..., alias="EmployerID")
