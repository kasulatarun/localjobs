from typing import List
from fastapi import APIRouter
from backend.app.models.categories import Category
from backend.app.repositories.excel_repository import excel_repo

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=List[Category])
def get_categories():
    """Returns active job categories with multilingual names."""
    return excel_repo.get_all_categories(active_only=True)
