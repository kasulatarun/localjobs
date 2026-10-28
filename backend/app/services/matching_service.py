from typing import List, Optional
from backend.app.models.jobs import Job
from backend.app.services.job_service import job_service

class MatchingService:
    def __init__(self, service=job_service):
        self.job_service = service

    def match_jobs(
        self,
        category: Optional[str] = None,
        locality: Optional[str] = None,
        limit: int = 3,
        offset: int = 0
    ) -> List[Job]:
        """
        Deterministic matching engine:
        1. Filters out unverified, closed, and expired jobs.
        2. Filters by category if specified.
        3. Filters by locality if specified (exact or substring).
        4. Returns at most `limit` items (default 3 per voice page).
        """
        clean_category = category.strip() if category else None
        clean_locality = locality.strip() if locality else None
        if clean_locality and clean_locality.lower() in ["all", "any", "nearby", ""]:
            clean_locality = None

        all_matches = self.job_service.get_public_jobs(job_type=clean_category, locality=clean_locality)
        
        # Sort by creation date descending
        all_matches.sort(key=lambda x: x.created_at, reverse=True)
        return all_matches[offset: offset + limit]

    def count_matches(self, category: Optional[str] = None, locality: Optional[str] = None) -> int:
        clean_category = category.strip() if category else None
        clean_locality = locality.strip() if locality else None
        if clean_locality and clean_locality.lower() in ["all", "any", "nearby", ""]:
            clean_locality = None
        matches = self.job_service.get_public_jobs(job_type=clean_category, locality=clean_locality)
        return len(matches)

matching_service = MatchingService()
