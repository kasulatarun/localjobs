from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from backend.app.models.applications import Application, ApplicationCreate
from backend.app.services.application_service import application_service
from backend.app.security.validation import normalize_phone, verify_admin

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("", response_model=Application, status_code=status.HTTP_201_CREATED)
def submit_application(app_in: ApplicationCreate):
    """Submits worker interest for a job. Prevents duplicate applications."""
    try:
        norm_phone = normalize_phone(app_in.worker_phone)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    try:
        app, is_duplicate = application_service.apply_for_job(
            worker_phone=norm_phone,
            job_id=app_in.job_id
        )
        if is_duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Duplicate application: You have already applied for this job."
            )
        return app
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{phone}", response_model=List[Application])
def get_worker_applications(phone: str):
    """Returns all applications for a specific worker phone."""
    try:
        norm_phone = normalize_phone(phone)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return application_service.get_worker_applications(norm_phone)

@router.get("", response_model=List[Application])
def get_all_applications(_: bool = Depends(verify_admin)):
    """Admin endpoint to view all system applications."""
    return application_service.get_all_applications()
