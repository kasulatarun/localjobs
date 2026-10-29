from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
import threading

from backend.app.localization.loader import localization
from backend.app.services.matching_service import matching_service
from backend.app.services.application_service import application_service
from backend.app.models.jobs import Job
from backend.app.security.validation import normalize_phone, mask_phone

MAX_RETRIES = 3

class IVRState(str, Enum):
    WELCOME = "WELCOME"
    LANGUAGE_SELECTION = "LANGUAGE_SELECTION"
    CATEGORY_SELECTION = "CATEGORY_SELECTION"
    LOCATION_SELECTION = "LOCATION_SELECTION"
    JOB_RESULTS = "JOB_RESULTS"
    NO_JOBS = "NO_JOBS"
    APPLICATION_CREATED = "APPLICATION_CREATED"
    END = "END"

class CallSession:
    def __init__(self, call_id: str, caller_phone: str):
        self.call_id = call_id
        self.caller_phone = caller_phone
        self.state: IVRState = IVRState.WELCOME
        self.language: str = "en"  # Default English for multi-lingual greeting until chosen
        self.selected_category: Optional[str] = None
        self.selected_locality: Optional[str] = None
        self.matched_jobs: List[Job] = []
        self.current_job_index: int = 0
        self.retry_count: int = 0
        self.timeout_count: int = 0
        self.last_prompt: str = ""
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()

class IVRService:
    def __init__(self, match_svc=None, app_svc=None):
        self._custom_match_svc = match_svc
        self._custom_app_svc = app_svc
        self._sessions: Dict[str, CallSession] = {}
        self._lock = threading.RLock()

    @property
    def match_svc(self):
        return self._custom_match_svc or matching_service

    @property
    def app_svc(self):
        return self._custom_app_svc or application_service

    def get_or_create_session(self, call_id: str, caller_phone: str) -> CallSession:
        with self._lock:
            if call_id not in self._sessions:
                try:
                    norm_phone = normalize_phone(caller_phone)
                except ValueError:
                    norm_phone = caller_phone
                self._sessions[call_id] = CallSession(call_id, norm_phone)
            session = self._sessions[call_id]
            session.updated_at = datetime.now()
            return session

    def get_session(self, call_id: str) -> Optional[CallSession]:
        with self._lock:
            return self._sessions.get(call_id)

    def end_session(self, call_id: str):
        with self._lock:
            if call_id in self._sessions:
                del self._sessions[call_id]

    def process_incoming_call(self, call_id: str, caller_phone: str) -> Dict[str, Any]:
        """Entry point for incoming call: starts at WELCOME and prompts language selection."""
        session = self.get_or_create_session(call_id, caller_phone)
        session.state = IVRState.LANGUAGE_SELECTION
        session.retry_count = 0
        session.timeout_count = 0

        # Initial prompt plays multi-lingual welcome and asks for language
        # 1 -> Telugu, 2 -> Hindi, 3 -> English
        prompt = localization.get_text("en", "choose_language")
        session.last_prompt = prompt

        return {
            "call_id": call_id,
            "state": session.state.value,
            "prompt": prompt,
            "expects_dtmf": True,
            "max_digits": 1,
            "terminate": False
        }

    def process_dtmf_input(self, call_id: str, dtmf_digit: Optional[str], is_timeout: bool = False) -> Dict[str, Any]:
        session = self.get_session(call_id)
        if not session:
            # Recreate session if expired
            session = self.get_or_create_session(call_id, "+919848012345")
            return self.process_incoming_call(call_id, session.caller_phone)

        digit = dtmf_digit.strip() if dtmf_digit else None

        # Timeout handling
        if is_timeout or not digit:
            session.timeout_count += 1
            if session.timeout_count > MAX_RETRIES:
                session.state = IVRState.END
                farewell = localization.get_text(session.language, "goodbye")
                self.end_session(call_id)
                return {
                    "call_id": call_id,
                    "state": IVRState.END.value,
                    "prompt": farewell,
                    "expects_dtmf": False,
                    "terminate": True
                }
            timeout_msg = localization.get_text(session.language, "timeout")
            return {
                "call_id": call_id,
                "state": session.state.value,
                "prompt": f"{timeout_msg} {session.last_prompt}",
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }

        # Reset timeout count on valid input
        session.timeout_count = 0

        # State dispatch
        if session.state == IVRState.LANGUAGE_SELECTION:
            return self._handle_language_selection(session, digit)
        elif session.state == IVRState.CATEGORY_SELECTION:
            return self._handle_category_selection(session, digit)
        elif session.state == IVRState.LOCATION_SELECTION:
            return self._handle_location_selection(session, digit)
        elif session.state == IVRState.JOB_RESULTS:
            return self._handle_job_results_navigation(session, digit)
        elif session.state == IVRState.NO_JOBS:
            return self._handle_no_jobs_navigation(session, digit)
        elif session.state == IVRState.APPLICATION_CREATED:
            return self._handle_post_application_navigation(session, digit)
        else:
            # Fallback
            return self.process_incoming_call(call_id, session.caller_phone)

    def _handle_language_selection(self, session: CallSession, digit: str) -> Dict[str, Any]:
        # 1 -> Telugu, 2 -> Hindi, 3 -> English
        lang_map = {"1": "te", "2": "hi", "3": "en"}
        if digit in lang_map:
            session.language = lang_map[digit]
            session.state = IVRState.CATEGORY_SELECTION
            session.retry_count = 0

            prompt = localization.get_text(session.language, "choose_category")
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "language": session.language,
                "prompt": prompt,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }
        
        return self._handle_invalid_input(session)

    def _handle_category_selection(self, session: CallSession, digit: str) -> Dict[str, Any]:
        # Main menu back
        if digit == "9":
            session.state = IVRState.LANGUAGE_SELECTION
            prompt = localization.get_text("en", "choose_language")
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "prompt": prompt,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }

        cat_dict = localization.get_dict(session.language, "categories")
        if digit in cat_dict:
            session.selected_category = cat_dict[digit]
            session.state = IVRState.LOCATION_SELECTION
            session.retry_count = 0

            prompt = localization.get_text(session.language, "choose_location")
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "category": session.selected_category,
                "prompt": prompt,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }

        return self._handle_invalid_input(session)

    def _handle_location_selection(self, session: CallSession, digit: str) -> Dict[str, Any]:
        if digit == "9":
            session.state = IVRState.CATEGORY_SELECTION
            prompt = localization.get_text(session.language, "choose_category")
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "prompt": prompt,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }

        loc_dict = localization.get_dict(session.language, "locations")
        if digit in loc_dict:
            session.selected_locality = loc_dict[digit]
            session.retry_count = 0
            
            # Execute deterministic search
            matches = self.match_svc.match_jobs(
                category=session.selected_category,
                locality=session.selected_locality,
                limit=3,
                offset=0
            )
            session.matched_jobs = matches
            session.current_job_index = 0

            if not matches:
                session.state = IVRState.NO_JOBS
                prompt = localization.get_text(session.language, "no_jobs")
                session.last_prompt = prompt
                return {
                    "call_id": session.call_id,
                    "state": session.state.value,
                    "prompt": prompt,
                    "expects_dtmf": True,
                    "max_digits": 1,
                    "terminate": False
                }

            session.state = IVRState.JOB_RESULTS
            prompt = self._format_job_prompt(session)
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "prompt": prompt,
                "job": session.matched_jobs[0].model_dump(by_alias=True),
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }

        return self._handle_invalid_input(session)

    def _handle_job_results_navigation(self, session: CallSession, digit: str) -> Dict[str, Any]:
        if not session.matched_jobs or session.current_job_index >= len(session.matched_jobs):
            session.state = IVRState.CATEGORY_SELECTION
            prompt = localization.get_text(session.language, "choose_category")
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "prompt": prompt,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }

        current_job = session.matched_jobs[session.current_job_index]

        # 1 -> Worker interested
        if digit == "1":
            app, is_duplicate = self.app_svc.apply_for_job(
                worker_phone=session.caller_phone,
                job_id=current_job.job_id,
                language=session.language
            )
            session.state = IVRState.APPLICATION_CREATED
            session.retry_count = 0

            msg_key = "application_duplicate" if is_duplicate else "application_success"
            prompt = localization.get_text(session.language, msg_key)
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "prompt": prompt,
                "application_id": app.application_id if app else None,
                "is_duplicate": is_duplicate,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }

        # 2 -> Next job
        elif digit == "2":
            session.current_job_index += 1
            if session.current_job_index < len(session.matched_jobs):
                prompt = self._format_job_prompt(session)
                session.last_prompt = prompt
                return {
                    "call_id": session.call_id,
                    "state": session.state.value,
                    "prompt": prompt,
                    "job": session.matched_jobs[session.current_job_index].model_dump(by_alias=True),
                    "expects_dtmf": True,
                    "max_digits": 1,
                    "terminate": False
                }
            else:
                # Reached end of available jobs
                prompt = localization.get_text(session.language, "no_more_jobs")
                session.last_prompt = prompt
                return {
                    "call_id": session.call_id,
                    "state": session.state.value,
                    "prompt": prompt,
                    "expects_dtmf": True,
                    "max_digits": 1,
                    "terminate": False
                }

        # 9 -> Main menu
        elif digit == "9":
            session.state = IVRState.CATEGORY_SELECTION
            session.retry_count = 0
            prompt = localization.get_text(session.language, "choose_category")
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "prompt": prompt,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }

        return self._handle_invalid_input(session)

    def _handle_no_jobs_navigation(self, session: CallSession, digit: str) -> Dict[str, Any]:
        # In no jobs screen, 9 returns to category selection
        if digit == "9":
            session.state = IVRState.CATEGORY_SELECTION
            session.retry_count = 0
            prompt = localization.get_text(session.language, "choose_category")
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "prompt": prompt,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }
        return self._handle_invalid_input(session)

    def _handle_post_application_navigation(self, session: CallSession, digit: str) -> Dict[str, Any]:
        # After application: 2 = next job, 9 = main menu
        if digit == "2":
            session.current_job_index += 1
            if session.current_job_index < len(session.matched_jobs):
                session.state = IVRState.JOB_RESULTS
                session.retry_count = 0
                prompt = self._format_job_prompt(session)
                session.last_prompt = prompt
                return {
                    "call_id": session.call_id,
                    "state": session.state.value,
                    "prompt": prompt,
                    "job": session.matched_jobs[session.current_job_index].model_dump(by_alias=True),
                    "expects_dtmf": True,
                    "max_digits": 1,
                    "terminate": False
                }
            else:
                prompt = localization.get_text(session.language, "no_more_jobs")
                session.last_prompt = prompt
                return {
                    "call_id": session.call_id,
                    "state": session.state.value,
                    "prompt": prompt,
                    "expects_dtmf": True,
                    "max_digits": 1,
                    "terminate": False
                }
        elif digit == "9":
            session.state = IVRState.CATEGORY_SELECTION
            session.retry_count = 0
            prompt = localization.get_text(session.language, "choose_category")
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "prompt": prompt,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }
        return self._handle_invalid_input(session)

    def _format_job_prompt(self, session: CallSession) -> str:
        job = session.matched_jobs[session.current_job_index]
        return localization.format_text(
            session.language,
            "job_template",
            index=session.current_job_index + 1,
            job_type=job.job_type,
            locality=job.locality,
            salary=job.salary,
            salary_type=job.salary_type.lower()
        )

    def _handle_invalid_input(self, session: CallSession) -> Dict[str, Any]:
        session.retry_count += 1
        if session.retry_count > MAX_RETRIES:
            # Exceeded retries -> return to category selection or welcome
            session.retry_count = 0
            session.state = IVRState.CATEGORY_SELECTION
            max_msg = localization.get_text(session.language, "max_retries")
            prompt = f"{max_msg} {localization.get_text(session.language, 'choose_category')}"
            session.last_prompt = prompt
            return {
                "call_id": session.call_id,
                "state": session.state.value,
                "prompt": prompt,
                "expects_dtmf": True,
                "max_digits": 1,
                "terminate": False
            }

        invalid_msg = localization.get_text(session.language, "invalid_choice")
        return {
            "call_id": session.call_id,
            "state": session.state.value,
            "prompt": f"{invalid_msg} {session.last_prompt}",
            "expects_dtmf": True,
            "max_digits": 1,
            "terminate": False
        }

ivr_service = IVRService()
