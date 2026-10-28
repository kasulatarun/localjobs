# LocalJobs Security & Privacy Specification

## 1. Threat Model & Protections

| Threat | Risk Level | Mitigation Architecture |
| :--- | :--- | :--- |
| **Fake / Malicious Job Postings** | HIGH | Mandatory Admin Verification (`Verified="Pending"` on creation). Unverified jobs are never broadcast via IVR. |
| **AI Job Hallucination / Fabrication** | HIGH | Single Source of Truth Rule: LLM has zero direct write access to database and cannot fabricate jobs. All matching queries run through deterministic repository filters. |
| **Prompt Injection Attacks** | HIGH | Strict Pydantic validation on all LLM outputs; adversarial instructions attempting to force fictional jobs or salaries are discarded. |
| **Caller Phone Spoofing / PII Leaks** | MEDIUM | Masked phone logging (`mask_phone`). Only employers with legitimate vacancies can view applicant phone numbers. |
| **Timing Attacks on API Secrets** | MEDIUM | Constant-time token comparison via `secrets.compare_digest`. |
| **Excel Corruption from Concurrency**| MEDIUM | In-process Reentrant Lock (`threading.RLock`), atomic temporary writes, and automatic backup before overwrite. |
| **Credential Exposure** | HIGH | Strict `.env` isolation; `.gitignore` enforcement; no API keys committed to source. |

---

## 2. Authentication & Authorization

### Roles & Access:
1. **Public Worker**:
   - Access: View verified active jobs, register phone, submit interest, listen to IVR.
   - Credentials: None required (Voice relies on caller CLI; web uses 10-digit phone verification).
2. **Employer**:
   - Access: Post job openings, view applicant list for own postings.
   - Header: `X-Employer-Secret: <token>`
   - Constraint: Submitted jobs remain `Pending` until verified by Administrator.
3. **Administrator**:
   - Access: Review pending jobs, approve/reject postings, verify employers, inspect system audit logs and concurrency health.
   - Header: `X-Admin-Secret: <token>`

---

## 3. PII & Privacy Protection

- **Phone Normalization**: Standardizes Indian phone numbers into `+91XXXXXXXXXX` (E.164).
- **Log Masking**: System logs mask phone numbers (e.g. `+919848****45`) to prevent sensitive customer information leaks in application server logs or APM dashboards.
- **Zero Third-Party Ad Trackers**: The worker portal contains zero tracking scripts, third-party beacons, or telemetry that could compromise vulnerable workers.
