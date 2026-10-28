from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from backend.app.models.employers import Employer, EmployerCreate, EmployerUpdate
from backend.app.repositories.excel_repository import excel_repo
from backend.app.security.validation import normalize_phone, verify_admin

router = APIRouter(prefix="/employers", tags=["Employers"])

@router.post("", response_model=Employer, status_code=status.HTTP_201_CREATED)
def register_employer(emp_in: EmployerCreate):
    """Registers an employer. Always starts as 'Pending' verification."""
    try:
        norm_phone = normalize_phone(emp_in.phone)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    emp_in.phone = norm_phone
    return excel_repo.create_employer(emp_in)

@router.get("", response_model=List[Employer])
def get_employers(_: bool = Depends(verify_admin)):
    """Admin endpoint to list all employers."""
    return excel_repo.get_all_employers()

@router.get("/{employer_id}", response_model=Employer)
def get_employer(employer_id: str):
    emp = excel_repo.get_employer_by_id(employer_id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer not found")
    return emp

@router.put("/{employer_id}/verify", response_model=Employer)
def verify_employer_account(employer_id: str, _: bool = Depends(verify_admin)):
    """Admin approves an employer after review/KYC."""
    emp = excel_repo.update_employer(employer_id, EmployerUpdate(verified="Verified"))
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer not found")
    return emp
