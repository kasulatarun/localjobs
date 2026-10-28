from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ApplicationBase(BaseModel):
    worker_id: Optional[str] = Field(None, alias="WorkerID")
    worker_phone: str = Field(..., alias="WorkerPhone")
    job_id: str = Field(..., alias="JobID")
    applied_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), alias="AppliedAt")
    status: str = Field("Interested", alias="Status")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

class ApplicationCreate(BaseModel):
    worker_phone: str
    job_id: str
    worker_id: Optional[str] = None
    status: str = "Interested"

class Application(ApplicationBase):
    application_id: str = Field(..., alias="ApplicationID")
