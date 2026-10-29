from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status
from backend.app.models.jobs import Job, JobCreate, JobUpdate
from backend.app.services.job_service import job_service
from backend.app.repositories import repo
from backend.app.security.validation import verify_admin, verify_employer

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("", response_model=List[Job])
def get_jobs(
    job_type: Optional[str] = Query(None, description="Filter by job type"),
    locality: Optional[str] = Query(None, description="Filter by locality")
):
    """Returns verified, active, non-expired jobs for workers."""
    return job_service.get_public_jobs(job_type=job_type, locality=locality)

@router.get("/{job_id}", response_model=Job)
def get_job_details(job_id: str):
    job = job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.post("", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job(job_in: JobCreate, _: bool = Depends(verify_employer)):
    """
    Submits a new job. 
    Starts as 'Pending' verification. Requires Admin review before publishing.
    """
    # Verify employer exists
    emp = repo.get_employer_by_id(job_in.employer_id)
    if not emp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employer with ID '{job_in.employer_id}' does not exist. Please register company first."
        )

    return job_service.post_job(job_in)

@router.put("/{job_id}/approve", response_model=Job)
def approve_job(job_id: str, _: bool = Depends(verify_admin)):
    """Admin approves pending job for public display."""
    job = job_service.approve_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.put("/{job_id}/reject", response_model=Job)
def reject_job(job_id: str, _: bool = Depends(verify_admin)):
    """Admin rejects job."""
    job = job_service.reject_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.put("/{job_id}/close", response_model=Job)
def close_job(job_id: str, _: bool = Depends(verify_employer)):
    """Closes a job posting."""
    job = job_service.close_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job
