from typing import List, Optional, Tuple
from backend.app.models.applications import Application, ApplicationCreate
from backend.app.models.workers import WorkerCreate
from backend.app.repositories import repo as active_repo
from backend.app.security.validation import normalize_phone, mask_phone

class ApplicationService:
    def __init__(self, repo=None):
        self._custom_repo = repo

    @property
    def repo(self):
        return self._custom_repo if self._custom_repo is not None else active_repo

    def apply_for_job(self, worker_phone: str, job_id: str, language: str = "te") -> Tuple[Optional[Application], bool]:
        """
        Creates a job application.
        Returns: (application_obj, is_duplicate)
        """
        clean_phone = normalize_phone(worker_phone)
        job = self.repo.get_by_id(job_id)
        if not job:
            raise ValueError(f"Job with ID '{job_id}' does not exist.")

        # Check duplicate
        if self.repo.exists_recent(clean_phone, job_id):
            # Fetch existing application
            apps = [a for a in self.repo.get_applications_by_phone(clean_phone) if a.job_id.upper() == job_id.upper()]
            existing_app = apps[0] if apps else None
            return existing_app, True

        # Ensure worker record exists
        worker = self.repo.get_worker_by_phone(clean_phone)
        worker_id = None
        if not worker:
            new_worker = self.repo.create_worker(WorkerCreate(
                phone=clean_phone,
                language=language,
                preferred_job_type=job.job_type,
                locality=job.locality
            ))
            worker_id = new_worker.worker_id
        else:
            worker_id = worker.worker_id

        # Create application
        app = self.repo.create_application(ApplicationCreate(
            worker_id=worker_id,
            worker_phone=clean_phone,
            job_id=job.job_id,
            status="Interested"
        ))
        return app, False

    def get_worker_applications(self, phone: str) -> List[Application]:
        clean_phone = normalize_phone(phone)
        return self.repo.get_applications_by_phone(clean_phone)

    def get_all_applications(self) -> List[Application]:
        return self.repo.get_all_applications()

application_service = ApplicationService()
