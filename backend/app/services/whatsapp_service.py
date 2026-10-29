import threading
from typing import Dict, Any, List, Optional
from datetime import datetime

from backend.app.services.matching_service import matching_service
from backend.app.services.application_service import application_service
from backend.app.security.validation import normalize_phone
from backend.app.models.jobs import Job

class WhatsAppSession:
    def __init__(self, phone: str):
        self.phone = phone
        self.state = "START"  # START, CATEGORY_SELECTION, LOCALITY_SELECTION, JOB_VIEW, APPLIED
        self.language = "te"  # default te
        self.selected_category: Optional[str] = None
        self.selected_locality: Optional[str] = None
        self.current_jobs: List[Job] = []
        self.updated_at = datetime.now()

class WhatsAppService:
    def __init__(self, match_svc=None, app_svc=None):
        self._match_svc = match_svc or matching_service
        self._app_svc = app_svc or application_service
        self._sessions: Dict[str, WhatsAppSession] = {}
        self._lock = threading.RLock()

        self.categories_map = {
            "1": "Driver",
            "2": "Construction",
            "3": "Electrician",
            "4": "Cleaner",
            "5": "Shop / Helper",
            "6": "Other"
        }

        self.localities_map = {
            "1": "Uppal",
            "2": "Secunderabad",
            "3": "Dilsukhnagar",
            "4": "Kukatpally",
            "5": "all"
        }

    def get_or_create_session(self, phone: str) -> WhatsAppSession:
        norm = normalize_phone(phone)
        with self._lock:
            if norm not in self._sessions:
                self._sessions[norm] = WhatsAppSession(norm)
            return self._sessions[norm]

    def reset_session(self, phone: str):
        norm = normalize_phone(phone)
        with self._lock:
            self._sessions[norm] = WhatsAppSession(norm)

    def process_message(self, from_phone: str, raw_text: str) -> str:
        text = (raw_text or "").strip()
        norm_phone = normalize_phone(from_phone)
        session = self.get_or_create_session(norm_phone)
        session.updated_at = datetime.now()

        # Global reset commands
        if text.lower() in ("hi", "hello", "start", "menu", "help", "హాయ్", "నమస్తే", "restart", "0"):
            session.state = "START"
            return self._render_welcome_menu(session)

        # State 1: Language Selection
        if session.state == "START":
            if text == "1" or text.lower() in ("telugu", "te"):
                session.language = "te"
                session.state = "CATEGORY_SELECTION"
                return self._render_category_menu(session)
            elif text == "2" or text.lower() in ("hindi", "hi"):
                session.language = "hi"
                session.state = "CATEGORY_SELECTION"
                return self._render_category_menu(session)
            elif text == "3" or text.lower() in ("english", "en"):
                session.language = "en"
                session.state = "CATEGORY_SELECTION"
                return self._render_category_menu(session)
            else:
                return (
                    "⚠️ దయచేసి సరైన నంబర్ ఎంచుకోండి / कृपया सही नंबर चुनें / Please reply with 1, 2, or 3:\n\n"
                    + self._render_welcome_menu(session)
                )

        # State 2: Category Selection
        if session.state == "CATEGORY_SELECTION":
            category = self.categories_map.get(text)
            if category:
                session.selected_category = category
                session.state = "LOCALITY_SELECTION"
                return self._render_locality_menu(session)
            else:
                return self._render_invalid_category(session)

        # State 3: Locality Selection
        if session.state == "LOCALITY_SELECTION":
            locality = self.localities_map.get(text)
            if locality:
                session.selected_locality = None if locality == "all" else locality
                session.state = "JOB_VIEW"
                return self._search_and_render_jobs(session)
            else:
                return self._render_invalid_locality(session)

        # State 4: Job View & Apply
        if session.state == "JOB_VIEW":
            if text == "1" and session.current_jobs:
                target_job = session.current_jobs[0]
                app, is_dup = self._app_svc.apply_for_job(
                    worker_phone=session.phone,
                    job_id=target_job.job_id,
                    language=session.language
                )
                session.state = "APPLIED"
                return self._render_apply_success(session, target_job, is_dup)
            elif text == "9":
                session.state = "CATEGORY_SELECTION"
                return self._render_category_menu(session)
            else:
                return self._render_jobs_prompt(session)

        # State 5: Already applied or completed
        if session.state == "APPLIED":
            session.state = "CATEGORY_SELECTION"
            return (
                self._render_applied_next(session)
                + "\n\n"
                + self._render_category_menu(session)
            )

        # Fallback
        session.state = "START"
        return self._render_welcome_menu(session)

    # --- Render Helpers ---

    def _render_welcome_menu(self, session: WhatsAppSession) -> str:
        return (
            "🙏 *Welcome to LocalJobs!*\n"
            "భారత్ లోకల్ ఉద్యోగ సేవా కేంద్రం\n\n"
            "దయచేసి మీ భాషను ఎంచుకోండి / भाषा चुनें / Choose Language:\n"
            "1️⃣ తెలుగు (Telugu)\n"
            "2️⃣ हिंदी (Hindi)\n"
            "3️⃣ English\n\n"
            "_Reply with 1, 2, or 3_"
        )

    def _render_category_menu(self, session: WhatsAppSession) -> str:
        lang = session.language
        if lang == "te":
            return (
                "💼 *ఏ పని కావాలి? నంబర్ రిప్లై ఇవ్వండి:*\n\n"
                "1️⃣ 🚗 డ్రైవర్ (Driver)\n"
                "2️⃣ 🏗️ భవన నిర్మాణం (Construction)\n"
                "3️⃣ ⚡ ఎలక్ట్రీషియన్ (Electrician)\n"
                "4️⃣ 🧹 క్లీనర్ (Cleaner)\n"
                "5️⃣ 🛒 షాప్ సహాయకుడు (Shop/Helper)\n"
                "6️⃣ 🔧 ఇతర పనులు (Other)\n\n"
                "_(నంబర్ 1 నుండి 6 వరకు రిప్లై ఇవ్వండి)_"
            )
        elif lang == "hi":
            return (
                "💼 *आपको किस प्रकार का काम चाहिए? नंबर रिप्लाई करें:*\n\n"
                "1️⃣ 🚗 ड्राइवर (Driver)\n"
                "2️⃣ 🏗️ निर्माण कार्य (Construction)\n"
                "3️⃣ ⚡ इलेक्ट्रीशियन (Electrician)\n"
                "4️⃣ 🧹 सफाई कर्मचारी (Cleaner)\n"
                "5️⃣ 🛒 दुकान सहायक (Shop/Helper)\n"
                "6️⃣ 🔧 अन्य काम (Other)\n\n"
                "_(1 से 6 तक नंबर रिप्लाई करें)_"
            )
        else:
            return (
                "💼 *What job are you looking for? Reply with number:*\n\n"
                "1️⃣ 🚗 Driver\n"
                "2️⃣ 🏗️ Construction\n"
                "3️⃣ ⚡ Electrician\n"
                "4️⃣ 🧹 Cleaner\n"
                "5️⃣ 🛒 Shop / Helper\n"
                "6️⃣ 🔧 Other Jobs\n\n"
                "_(Reply 1 to 6)_"
            )

    def _render_invalid_category(self, session: WhatsAppSession) -> str:
        lang = session.language
        if lang == "te":
            return "⚠️ దయచేసి సరైన నంబర్ (1 నుండి 6) రిప్లై ఇవ్వండి.\n\n" + self._render_category_menu(session)
        elif lang == "hi":
            return "⚠️ कृपया सही नंबर (1 से 6) रिप्लाई करें।\n\n" + self._render_category_menu(session)
        else:
            return "⚠️ Please reply with a valid number (1 to 6).\n\n" + self._render_category_menu(session)

    def _render_locality_menu(self, session: WhatsAppSession) -> str:
        lang = session.language
        cat = session.selected_category
        if lang == "te":
            return (
                f"📍 *{cat} పని కోసం ప్రాంతాన్ని ఎంచుకోండి:*\n\n"
                "1️⃣ Uppal (ఉప్పల్)\n"
                "2️⃣ Secunderabad (సికింద్రాబాద్)\n"
                "3️⃣ Dilsukhnagar (దిల్‌సుఖ్‌నగర్)\n"
                "4️⃣ Kukatpally (కూకట్‌పల్లి)\n"
                "5️⃣ అన్ని ప్రాంతాలు (Any Locality)\n\n"
                "_(నంబర్ 1 నుండి 5 వరకు రిప్లై ఇవ్వండి)_"
            )
        elif lang == "hi":
            return (
                f"📍 *{cat} काम के लिए इलाका चुनें:*\n\n"
                "1️⃣ Uppal (उप्पल)\n"
                "2️⃣ Secunderabad (सिकंदराबाद)\n"
                "3️⃣ Dilsukhnagar (दिलसुखनगर)\n"
                "4️⃣ Kukatpally (कुकाटपल्ली)\n"
                "5️⃣ कोई भी इलाका (All Areas)\n\n"
                "_(1 से 5 तक नंबर रिप्लाई करें)_"
            )
        else:
            return (
                f"📍 *Select locality for {cat}:*\n\n"
                "1️⃣ Uppal\n"
                "2️⃣ Secunderabad\n"
                "3️⃣ Dilsukhnagar\n"
                "4️⃣ Kukatpally\n"
                "5️⃣ Any Locality\n\n"
                "_(Reply 1 to 5)_"
            )

    def _render_invalid_locality(self, session: WhatsAppSession) -> str:
        return "⚠️ Please select a valid locality (1 to 5).\n\n" + self._render_locality_menu(session)

    def _search_and_render_jobs(self, session: WhatsAppSession) -> str:
        jobs = self._match_svc.match_jobs(
            category=session.selected_category,
            locality=session.selected_locality,
            limit=1
        )
        session.current_jobs = jobs
        lang = session.language

        if not jobs:
            if lang == "te":
                return (
                    f"😔 క్షమించండి, ప్రస్తుతం {session.selected_category} పనికి సరిపోయే ఖాళీలు లేవు.\n\n"
                    "🔄 వేరే పని ఎంచుకోవడానికి *9* అని రిప్లై ఇవ్వండి.\n"
                    "🏠 మెనూకి వెళ్ళడానికి *0* అని రిప్లై ఇవ్వండి."
                )
            elif lang == "hi":
                return (
                    f"😔 क्षमा करें, अभी {session.selected_category} के लिए कोई पद उपलब्ध नहीं है।\n\n"
                    "🔄 दूसरा काम चुनने के लिए *9* रिप्लाई करें।\n"
                    "🏠 मुख्य मेनू के लिए *0* रिप्लाई करें।"
                )
            else:
                return (
                    f"😔 Sorry, no active verified vacancies found for {session.selected_category} right now.\n\n"
                    "🔄 Reply *9* to choose another category.\n"
                    "🏠 Reply *0* to return to main menu."
                )

        job = jobs[0]
        return self._format_job_card(session, job)

    def _format_job_card(self, session: WhatsAppSession, job: Job) -> str:
        lang = session.language
        if lang == "te":
            return (
                f"🎯 *మీకు సరిపోయే ఉద్యోగం లభించింది!*\n\n"
                f"📌 *పని:* {job.job_type}\n"
                f"📍 *ప్రాంతం:* {job.locality}, {job.location}\n"
                f"💰 *జీతం:* ₹{job.salary:,} / {job.salary_type}\n"
                f"⏰ *వేళలు:* {job.hours}\n"
                f"📝 *వివరాలు:* {job.description}\n\n"
                "👉 ఈ ఉద్యోగానికి దరఖాస్తు చేసుకోవడానికి *1* అని రిప్లై ఇవ్వండి.\n"
                "🔄 వేరే వర్గం ఎంచుకోవడానికి *9* అని రిప్లై ఇవ్వండి."
            )
        elif lang == "hi":
            return (
                f"🎯 *आपके लिए नौकरी मिली है!*\n\n"
                f"📌 *काम:* {job.job_type}\n"
                f"📍 *स्थान:* {job.locality}, {job.location}\n"
                f"💰 *वेतन:* ₹{job.salary:,} / {job.salary_type}\n"
                f"⏰ *समय:* {job.hours}\n"
                f"📝 *विवरण:* {job.description}\n\n"
                "👉 इस नौकरी के लिए आवेदन करने हेतु *1* रिप्लाई करें।\n"
                "🔄 दूसरा काम चुनने के लिए *9* रिप्लाई करें."
            )
        else:
            return (
                f"🎯 *Verified Job Found!*\n\n"
                f"📌 *Role:* {job.job_type}\n"
                f"📍 *Location:* {job.locality}, {job.location}\n"
                f"💰 *Salary:* ₹{job.salary:,} / {job.salary_type}\n"
                f"⏰ *Hours:* {job.hours}\n"
                f"📝 *Details:* {job.description}\n\n"
                "👉 Reply *1* to apply for this job.\n"
                "🔄 Reply *9* to choose another category."
            )

    def _render_jobs_prompt(self, session: WhatsAppSession) -> str:
        if session.current_jobs:
            return self._format_job_card(session, session.current_jobs[0])
        return self._search_and_render_jobs(session)

    def _render_apply_success(self, session: WhatsAppSession, job: Job, is_dup: bool) -> str:
        lang = session.language
        if is_dup:
            if lang == "te":
                return (
                    "ℹ️ *మీరు ఇప్పటికే ఈ ఉద్యోగానికి దరఖాస్తు చేసుకున్నారు.*\n\n"
                    f"ఉద్యోగ ఐడీ: {job.job_id} ({job.job_type} - {job.locality})\n"
                    f"మీ మొబైల్: {session.phone}\n"
                    "యాజమాన్యం త్వరలోనే మిమ్మల్ని సంప్రదిస్తుంది.\n\n"
                    "మరో ఉద్యోగం చూడటానికి *9* రిప్లై ఇవ్వండి."
                )
            elif lang == "hi":
                return (
                    "ℹ️ *आप इस नौकरी के लिए पहले ही आवेदन कर चुके हैं।*\n\n"
                    f"जॉब आईडी: {job.job_id} ({job.job_type} - {job.locality})\n"
                    f"आपका फोन: {session.phone}\n"
                    "नियोक्ता जल्द ही आपसे संपर्क करेगा।\n\n"
                    "अन्य नौकरी देखने के लिए *9* रिप्लाई करें।"
                )
            else:
                return (
                    "ℹ️ *You have already applied for this job.*\n\n"
                    f"Job ID: {job.job_id} ({job.job_type} - {job.locality})\n"
                    f"Your Phone: {session.phone}\n"
                    "The employer will contact you soon.\n\n"
                    "Reply *9* to view other jobs."
                )

        if lang == "te":
            return (
                "🎉 *అభినందనలు! మీ దరఖాస్తు విజయవంతంగా స్వీకరించబడింది.*\n\n"
                f"📌 ఉద్యోగం: {job.job_type} ({job.locality})\n"
                f"💰 జీతం: ₹{job.salary:,} / {job.salary_type}\n"
                f"📞 మీ రిజిస్టర్డ్ ఫోన్: {session.phone}\n\n"
                "సరిచూసిన కంపెనీ యాజమాన్యం త్వరలోనే మీ నంబర్‌కు కాల్ చేస్తుంది.\n\n"
                "ధన్యవాదాలు! మరో ఉద్యోగం చూడటానికి *9* అని రిప్లై ఇవ్వండి."
            )
        elif lang == "hi":
            return (
                "🎉 *बधाई हो! आपका आवेदन सफलतापूर्वक दर्ज कर लिया गया है।*\n\n"
                f"📌 नौकरी: {job.job_type} ({job.locality})\n"
                f"💰 वेतन: ₹{job.salary:,} / {job.salary_type}\n"
                f"📞 आपका रजिस्टर्ड फोन: {session.phone}\n\n"
                "सत्यापित नियोक्ता जल्द ही आपको कॉल करेगा।\n\n"
                "धन्यवाद! दूसरी नौकरी देखने के लिए *9* रिप्लाई करें।"
            )
        else:
            return (
                "🎉 *Congratulations! Your application has been submitted.*\n\n"
                f"📌 Job: {job.job_type} ({job.locality})\n"
                f"💰 Salary: ₹{job.salary:,} / {job.salary_type}\n"
                f"📞 Registered Phone: {session.phone}\n\n"
                "The verified employer will contact you directly.\n\n"
                "Thank you! Reply *9* to browse more jobs."
            )

    def _render_applied_next(self, session: WhatsAppSession) -> str:
        lang = session.language
        if lang == "te":
            return "కొత్త ఉద్యోగాన్ని ఎంచుకోవడానికి క్రింది జాబితా నుండి నంబర్ పంపండి:"
        elif lang == "hi":
            return "नई नौकरी चुनने के लिए नीचे दी गई सूची से नंबर भेजें:"
        else:
            return "To choose another job, reply with a category number below:"

whatsapp_service = WhatsAppService()
