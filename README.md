# LocalJobs — Voice-First Local Employment Platform

> Connecting local blue-collar workers with nearby employment opportunities through a voice-first telephone interface (DTMF IVR) and verified web portals.

---

## 🌟 Overview & Product Mission

In India, millions of essential workers (drivers, construction workers, electricians, cleaners, shop helpers, mechanics, cooks) face significant digital barriers:
- Limited literacy or discomfort with English
- Feature phones without internet or mobile apps
- Difficulty typing resumes and filling long multi-step web forms

**LocalJobs** solves this by providing a **direct telephone interface** where any worker can dial a number, press 1-2-3 on their dial pad in **Telugu (తెలుగు), Hindi (हिंदी), or English**, hear verified jobs near their locality, and apply with a single keypress using their Caller ID.

Simultaneously, local employers and administrators have access to verified web dashboards to publish requirements, manage KYC, and track applications.

---

## 🚀 Key Features

1. **Deterministic DTMF-First Telephony**:
   - `CALL -> Language -> Category -> Locality -> Jobs Read -> 1 for Interested`
   - Zero AI hallucination in core job matching.
   - Built-in retry handling, timeouts, and max retry limits.
2. **Multilingual Architecture**:
   - Telugu, Hindi, and English with decoupled JSON prompt catalogs (`locales/te/`, `locales/hi/`, `locales/en/`).
   - Easily extensible to additional languages (Tamil, Kannada, Marathi, Bengali) without modifying business logic.
3. **Location-First Matching**:
   - Neighborhood-level granularity (Uppal, Kukatpally, Dilsukhnagar, Secunderabad, etc.).
   - Deterministic matching filters out unverified, closed, and expired postings.
4. **Excel MVP Data Store with Atomic Writes & Backup**:
   - Uses `data/jobs.xlsx` with separate sheets (`Jobs`, `Employers`, `Workers`, `Applications`, `Categories`).
   - Thread-safe file locking, atomic temp-file replace, automated backups (`jobs.backup.xlsx`), and built-in concurrency warning for PostgreSQL migration.
5. **Local LLM Intelligence Layer (Ollama)**:
   - Understands natural speech and informal text in Telugu, Hindi, and English.
   - Converts utterances into strict Pydantic JSON schemas.
   - Sandboxed tool execution with strict prompt injection resistance.
6. **Telephony Abstraction Layer**:
   - Provider-agnostic interface supporting both **Exotel** (carrier provider) and **Mock Provider** (local simulator).
7. **Complete Local Development & Testing Suite**:
   - In-browser interactive dialer with real voice speech synthesis (`/simulator`).
   - CLI terminal dialer (`python -m backend.app.telephony.mock_cli`).
   - 24 automated unit, integration, and acceptance tests.

---

## 🛠️ Quick Start & Local Development

### 1. Requirements
- Python 3.10+ (tested on Python 3.14)
- Packages: `fastapi`, `uvicorn`, `openpyxl`, `pydantic`, `pytest`, `pytest-asyncio`, `httpx`, `python-multipart`

### 2. Setup Environment
```bash
# Clone and enter workspace
cd loophole

# Install dependencies
pip install fastapi uvicorn openpyxl pydantic pytest pytest-asyncio httpx python-multipart

# Copy environment config
copy .env.example .env
```

### 3. Initialize Excel Database
```bash
python backend/app/repositories/init_db.py
```
This generates `data/jobs.xlsx` with verified and realistic demo jobs.

### 4. Run Backend Server
```bash
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access Interfaces
- **Worker Portal**: [http://localhost:8000/](http://localhost:8000/)
- **Interactive Phone Simulator**: [http://localhost:8000/simulator](http://localhost:8000/simulator)
- **Employer Dashboard**: [http://localhost:8000/employer](http://localhost:8000/employer)
- **Admin Command Console**: [http://localhost:8000/admin](http://localhost:8000/admin)
- **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 6. Terminal Interactive IVR
You can also simulate the IVR directly from your shell:
```bash
python -m backend.app.telephony.mock_cli
```

---

## 🧪 Running Automated Tests

Run the full automated test suite:
```bash
python -m pytest backend/tests -v
```

All 24 unit, integration, and acceptance tests will run and validate:
- Full end-to-end user journeys (Telugu, Hindi, English)
- DTMF state machine transitions, retries, and timeouts
- Exclusion of unverified, closed, and expired jobs
- Duplicate application prevention
- Ollama intent extraction and adversarial injection resistance

---

## 📚 Project Documentation

- [`ARCHITECTURE.md`](ARCHITECTURE.md): System architecture, layers, and service boundaries.
- [`API.md`](API.md): Full REST API endpoint reference and payload specifications.
- [`IVR_FLOW.md`](IVR_FLOW.md): Finite state machine diagram, state transitions, and keypad matrix.
- [`EXCEL_SCHEMA.md`](EXCEL_SCHEMA.md): Complete Excel sheet column definitions, types, and constraints.
- [`SECURITY.md`](SECURITY.md): Threat model, authentication, timing-safe checks, and PII protection.
- [`TESTING.md`](TESTING.md): Test plan, scenarios, and verification steps.
- [`DEPLOYMENT.md`](DEPLOYMENT.md): Deployment stages from local mock to cloud and production.
- [`TELEPHONY_SETUP.md`](TELEPHONY_SETUP.md): Step-by-step Exotel onboarding and 1800 toll-free provisioning.
- [`LLM_INTEGRATION.md`](LLM_INTEGRATION.md): Ollama setup, structured schemas, sandboxed tools, and prompt injection defense.
