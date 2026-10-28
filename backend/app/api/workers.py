from fastapi import APIRouter, HTTPException, status
from backend.app.models.workers import Worker, WorkerCreate
from backend.app.repositories.excel_repository import excel_repo
from backend.app.security.validation import normalize_phone

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.post("", response_model=Worker, status_code=status.HTTP_201_CREATED)
def register_worker(worker_in: WorkerCreate):
    """Registers or updates a worker profile."""
    try:
        norm_phone = normalize_phone(worker_in.phone)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    worker_in.phone = norm_phone
    return excel_repo.create_worker(worker_in)

@router.get("/{phone}", response_model=Worker)
def get_worker(phone: str):
    """Fetches a worker profile by phone number."""
    try:
        norm_phone = normalize_phone(phone)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    worker = excel_repo.get_worker_by_phone(norm_phone)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")
    return worker
