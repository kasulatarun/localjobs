# LocalJobs System Architecture

## 1. Architectural Overview

LocalJobs is built on a modular, decoupled architecture adhering to strict separation of concerns.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        INTERFACES LAYER                                │
│                                                                        │
│   [ Telephone (DTMF IVR) ]     [ Worker Web ]     [ Employer/Admin ]   │
│   (PSTN / Exotel / Mock)      (Accessible UI)    (Dashboard Portals)   │
└──────────────────┬────────────────────┬────────────────────┬───────────┘
                   │                    │                    │
                   ▼                    ▼                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         API ROUTING LAYER                              │
│                                                                        │
│   POST /ivr/incoming, /ivr/dtmf        GET /jobs, POST /applications   │
│   GET  /health, GET /categories        POST /employers, /admin/*       │
└───────────────────────────────────────┬────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       DOMAIN SERVICES LAYER                            │
│                                                                        │
│   ┌─────────────────────┐  ┌─────────────────────┐  ┌───────────────┐  │
│   │   IVR State Machine │  │  Matching Service   │  │ Job Service   │  │
│   └──────────┬──────────┘  └──────────┬──────────┘  └───────┬───────┘  │
│              │                        │                     │          │
│   ┌──────────┴──────────┐  ┌──────────┴──────────┐  ┌───────┴───────┐  │
│   │ Application Service │  │ Localization Manager│  │ LLM Parser    │  │
│   └─────────────────────┘  └─────────────────────┘  └───────────────┘  │
└───────────────────────────────────────┬────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     REPOSITORY & STORAGE ABSTRACTION                   │
│                                                                        │
│   IJobRepository, IEmployerRepository, IWorkerRepository, ...          │
│                                │                                       │
│                                ▼                                       │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │  UnifiedExcelRepository                                        │   │
│   │  - Threading RLock & Atomic Writes (.tmp.xlsx -> .xlsx)        │   │
│   │  - Automatic Pre-Write Backups (.backup.xlsx)                  │   │
│   │  - Concurrency & Row Threshold Monitoring                      │   │
│   └────────────────────────────────┬───────────────────────────────┘   │
└────────────────────────────────────┼───────────────────────────────────┘
                                     │
                                     ▼
                      [ data/jobs.xlsx (Workbook) ]
```

---

## 2. Telephony Subsystem

The telephony subsystem sits behind the `TelephonyProvider` interface:

- `handle_incoming_call(call_id, caller_phone)`: Initiates IVR session.
- `handle_dtmf(call_id, digits, is_timeout)`: Advances the deterministic finite state machine.
- `format_provider_response(ivr_result)`: Emits XML for Exotel or JSON for Mock.
- `send_sms(to_phone, message)`: Sends candidate confirmation SMS.

### Provider Implementations:
1. `MockTelephonyProvider`: In-memory state tracking used by automated tests and `/simulator`.
2. `ExotelTelephonyProvider`: Formats `<Response><Say/><GetDigits/></Response>` payloads for Exotel Passthru applets.
3. Future: Twilio, Tata Telephony, or Asterisk.

---

## 3. Localization Architecture

Prompts and messages are strictly isolated from source code in `locales/{lang}/messages.json`:
- `locales/te/messages.json`: Telugu
- `locales/hi/messages.json`: Hindi
- `locales/en/messages.json`: English

`LocalizationManager` caches loaded JSON files and provides fallback interpolation.

---

## 4. Excel Concurrency & Persistence Protection

Excel is not an ACID SQL database. To ensure safe MVP usage:
1. **Reentrant Lock (`threading.RLock`)**: Serializes all read/write operations within the process.
2. **Atomic Write Protocol**:
   - Write new workbook to `data/jobs.tmp.xlsx`
   - Copy existing file to `data/jobs.backup.xlsx`
   - Atomically replace `jobs.tmp.xlsx` onto `jobs.xlsx` using filesystem atomic rename (`os.replace`)
3. **Threshold Monitoring**:
   - When total records exceed 500, admin dashboard flags a warning and recommends PostgreSQL migration.

---

## 5. Dual-Backend Storage Architecture (Excel & PostgreSQL)

Repository interfaces (`IJobRepository`, `IEmployerRepository`, `IWorkerRepository`, `IApplicationRepository`, `ICategoryRepository`) abstract all storage operations.

The application implements a dual-backend architecture selected via environment variables:

```text
                  ┌──────────────────────────────┐
                  │       RepositoryProxy        │
                  │   (backend/app/repositories) │
                  └──────────────┬───────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │                                           │
           ▼                                           ▼
┌──────────────────────────────┐            ┌──────────────────────────────┐
│    UnifiedExcelRepository    │            │  UnifiedPostgresRepository   │
│   (DATA_BACKEND=excel)       │            │  (DATA_BACKEND=postgres)     │
│                              │            │                              │
│ - Zero setup local dev       │            │ - Production persistence     │
│ - Threading RLock & atomic   │            │ - Supabase / Neon / Render   │
│ - data/jobs.xlsx storage     │            │ - Foreign keys & ACID rules  │
│ - Import/Export hub          │            │ - Unique constraints         │
└──────────────────────────────┘            └──────────────────────────────┘
```

1. **Local Development Mode**:
   ```bash
   APP_ENV=development
   DATA_BACKEND=excel
   ```
   Uses `data/jobs.xlsx` with atomic backup file replacement. Zero database setup or server required.

2. **Production Cloud Mode**:
   ```bash
   APP_ENV=production
   DATA_BACKEND=postgres
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres
   ```
   Uses PostgreSQL (Supabase or Neon free tiers) to eliminate Render's ephemeral filesystem data loss. All candidate applications, employer postings, and worker registrations persist reliably across restarts.

3. **Data Migration & Seeding CLI**:
   ```bash
   python -m backend.app.repositories.import_excel_to_postgres --excel data/jobs.xlsx
   ```
   Imports seed data from Excel into PostgreSQL idempotently.
