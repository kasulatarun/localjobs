from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class WorkerBase(BaseModel):
    phone: str = Field(..., alias="Phone")
    language: str = Field("te", alias="Language")
    location: str = Field("Hyderabad", alias="Location")
    locality: str = Field("Uppal", alias="Locality")
    preferred_job_type: str = Field("Driver", alias="PreferredJobType")
    experience: str = Field("Fresher", alias="Experience")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"), alias="CreatedAt")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

class WorkerCreate(BaseModel):
    phone: str
    language: str = "te"
    location: str = "Hyderabad"
    locality: str = "Uppal"
    preferred_job_type: str = "Driver"
    experience: str = "Fresher"

class Worker(WorkerBase):
    worker_id: str = Field(..., alias="WorkerID")
