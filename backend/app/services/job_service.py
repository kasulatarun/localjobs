from typing import List, Optional
from backend.app.models.jobs import Job, JobCreate, JobUpdate
from backend.app.repositories import repo as active_repo

class JobService:
    def __init__(self, repo=None):
        self._custom_repo = repo

    @property
    def repo(self):
        return self._custom_repo if self._custom_repo is not None else active_repo

    def get_public_jobs(self, job_type: Optional[str] = None, locality: Optional[str] = None) -> List[Job]:
        """Returns only verified, active, non-expired jobs."""
        return self.repo.search(job_type=job_type, locality=locality)

    def get_job_by_id(self, job_id: str) -> Optional[Job]:
        return self.repo.get_by_id(job_id)

    def get_all_jobs_admin(self) -> List[Job]:
        """Returns all jobs regardless of status for admin review."""
        return self.repo.get_all(verified_only=False, active_only=False)

    def post_job(self, job_in: JobCreate) -> Job:
        """
        Creates a new job. 
        Always starts with Status='Active' and Verified='Pending'.
        Never immediately public until reviewed.
        """
        return self.repo.create(job_in)

    def approve_job(self, job_id: str) -> Optional[Job]:
        return self.repo.update(job_id, JobUpdate(verified="Verified"))

    def reject_job(self, job_id: str) -> Optional[Job]:
        return self.repo.update(job_id, JobUpdate(verified="Rejected", status="Closed"))

    def close_job(self, job_id: str) -> Optional[Job]:
        return self.repo.update(job_id, JobUpdate(status="Closed"))

job_service = JobService()
