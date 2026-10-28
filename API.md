# LocalJobs API Reference

Base URL: `http://localhost:8000`

---

## 1. System Endpoints

### `GET /health`
Returns system health, Excel storage status, Ollama connectivity, and telephony status.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "LocalJobs",
  "version": "1.0.0",
  "excel_storage": {
    "status": "connected",
    "file": "data\\jobs.xlsx",
    "total_records": 19,
    "concurrency_risk": "NORMAL",
    "migration_recommended": false
  },
  "telephony": {
    "exotel_configured": false,
    "active_provider": "mock_simulator"
  },
  "ollama_llm": {
    "configured_url": "http://127.0.0.1:11434",
    "connected": false
  }
}
```

---

## 2. Jobs Endpoints

### `GET /jobs`
Returns public, verified, active, non-expired jobs.
- Query parameters:
  - `job_type` (string, optional): e.g. "Driver"
  - `locality` (string, optional): e.g. "Uppal"

### `GET /jobs/{job_id}`
Returns details for a specific job ID.

### `POST /jobs`
Submits a new job. Always created with `Verified="Pending"`.
- Headers: `X-Employer-Secret: <secret>` or `X-Admin-Secret: <secret>`
- Request Body:
```json
{
  "employer_id": "EMP-101",
  "job_type": "Driver",
  "location": "Hyderabad",
  "locality": "Uppal",
  "district": "Medchal-Malkajgiri",
  "state": "Telangana",
  "salary": 18000,
  "salary_type": "Month",
  "hours": "9 AM - 6 PM",
  "required_experience": "1 year",
  "vacancies": 2,
  "description": "Commercial car driver needed.",
  "expiry_date": "2026-12-31"
}
```

### `PUT /jobs/{job_id}/approve`
Admin approves a pending job.
- Headers: `X-Admin-Secret: <secret>`

### `PUT /jobs/{job_id}/reject`
Admin rejects a job.
- Headers: `X-Admin-Secret: <secret>`

### `PUT /jobs/{job_id}/close`
Closes a job posting.
- Headers: `X-Employer-Secret: <secret>` or `X-Admin-Secret: <secret>`

---

## 3. Categories Endpoints

### `GET /categories`
Returns active job categories with Telugu, Hindi, and English names.

---

## 4. Workers Endpoints

### `POST /workers`
Registers a worker profile.
```json
{
  "phone": "+919848012345",
  "language": "te",
  "location": "Hyderabad",
  "locality": "Uppal",
  "preferred_job_type": "Driver",
  "experience": "Fresher"
}
```

### `GET /workers/{phone}`
Retrieves a worker profile by phone number.

---

## 5. Applications Endpoints

### `POST /applications`
Submits worker interest. Prevents duplicate submissions.
```json
{
  "worker_phone": "+919848012345",
  "job_id": "JOB-1001"
}
```
**Status Codes:**
- `201 Created`: Application recorded.
- `409 Conflict`: Worker already applied for this job recently.

### `GET /applications/{phone}`
Returns all applications submitted by a phone number.

---

## 6. IVR Telephony Endpoints

### `POST /ivr/incoming`
Webhook triggered on incoming call from Exotel or Simulator.
- Accepts JSON or Form-URLencoded (`CallSid`, `From`).
- Returns XML for Exotel or JSON for Simulator.

### `POST /ivr/dtmf`
Webhook triggered on DTMF keypress or timeout.
- Parameters: `call_id` / `CallSid`, `digits` / `Digits`, `is_timeout` (optional boolean).

### `POST /ivr/callback`
Webhook for call completion / hangup.

---

## 7. Natural Language & LLM

### `POST /llm/intent`
Extracts structured intent from Telugu, Hindi, or English utterance.
```json
{
  "text": "నాకు ఉప్పల్ దగ్గర డ్రైవర్ పని కావాలి",
  "execute_tools": true
}
```
**Response:**
```json
{
  "intent": {
    "intent": "find_job",
    "job_type": "Driver",
    "location": "Uppal",
    "max_distance_km": 10
  },
  "tool_results": {
    "matched_jobs": [...],
    "count": 1
  }
}
```
