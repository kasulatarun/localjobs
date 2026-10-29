from backend.app.config import config
from backend.app.repositories.excel_repository import (
    IJobRepository,
    IEmployerRepository,
    IWorkerRepository,
    IApplicationRepository,
    ICategoryRepository,
    UnifiedExcelRepository,
    excel_repo,
)
from backend.app.repositories.postgres_repository import (
    UnifiedPostgresRepository,
    postgres_repo,
    init_db_postgres,
)

def get_repository():
    """
    Returns the active unified repository instance based on environment configuration:
    - DATA_BACKEND=postgres -> UnifiedPostgresRepository
    - DATA_BACKEND=excel (or default) -> UnifiedExcelRepository
    """
    if config.is_postgres:
        return postgres_repo
    return excel_repo

class RepositoryProxy:
    """
    Dynamic transparent proxy that routes all repository calls to the currently active backend.
    Enables zero-friction switching without modifying calling code.
    """
    def __getattr__(self, name: str):
        target = get_repository()
        return getattr(target, name)

repo = RepositoryProxy()

__all__ = [
    "IJobRepository",
    "IEmployerRepository",
    "IWorkerRepository",
    "IApplicationRepository",
    "ICategoryRepository",
    "UnifiedExcelRepository",
    "UnifiedPostgresRepository",
    "excel_repo",
    "postgres_repo",
    "get_repository",
    "repo",
    "init_db_postgres"
]
