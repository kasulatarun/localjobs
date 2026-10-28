from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from .common import JobStatus, VerificationStatus, SalaryType

class JobBase(BaseModel):
    employer_id: str = Field(..., alias="EmployerID")
    job_type: str = Field(..., alias="JobType")
    location: str = Field("Hyderabad", alias="Location")
    locality: str = Field(..., alias="Locality")
    district: str = Field("Medchal-Malkajgiri", alias="District")
    state: str = Field("Telangana", alias="State")
    salary: int = Field(..., ge=0, alias="Salary")
    salary_type: str = Field(default=SalaryType.MONTH.value, alias="SalaryType")
    hours: str = Field("8 hours", alias="Hours")
    required_experience: str = Field("Fresher", alias="RequiredExperience")
    vacancies: int = Field(1, ge=1, alias="Vacancies")
    description: str = Field("", alias="Description")
    status: str = Field(default=JobStatus.ACTIVE.value, alias="Status")
    verified: str = Field(default=VerificationStatus.PENDING.value, alias="Verified")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"), alias="CreatedAt")
    expiry_date: str = Field(default="2026-12-31", alias="ExpiryDate")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

class JobCreate(BaseModel):
    employer_id: str
    job_type: str
    location: str = "Hyderabad"
    locality: str
    district: str = "Medchal-Malkajgiri"
    state: str = "Telangana"
    salary: int
    salary_type: str = "Month"
    hours: str = "9 AM - 6 PM"
    required_experience: str = "Fresher"
    vacancies: int = 1
    description: str = ""
    expiry_date: str = "2026-12-31"

class JobUpdate(BaseModel):
    job_type: Optional[str] = None
    location: Optional[str] = None
    locality: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    salary: Optional[int] = None
    salary_type: Optional[str] = None
    hours: Optional[str] = None
    required_experience: Optional[str] = None
    vacancies: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None
    verified: Optional[str] = None
    expiry_date: Optional[str] = None

class Job(JobBase):
    job_id: str = Field(..., alias="JobID")
