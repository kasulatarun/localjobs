# LocalJobs Free Public Demo Deployment Guide (₹0 Budget)

> Complete operational guide for deploying the LocalJobs MVP online at zero cost without purchasing domains or carrier subscriptions.

---

## 1. Selected ₹0 Free Hosting Architecture

To achieve a 100% genuine, free public deployment with HTTPS and zero credit card requirements, LocalJobs uses a decoupled JAMstack + Container architecture:

```text
┌───────────────────────────────────────┐         ┌────────────────────────────────────────┐
│     FRONTEND: Cloudflare Pages        │         │        BACKEND: Render Web Service     │
│     (or GitHub Pages / Vercel)        │  HTTPS  │        (Free Python/FastAPI Tier)      │
│  - URL: https://localjobs.pages.dev   ├────────►│  - URL: https://localjobs.onrender.com │
│  - Zero build step / Static HTML/CSS  │  REST   │  - Auto-deploys from Git               │
│  - Cost: ₹0 (Unlimited bandwidth)     │         │  - Cost: ₹0 (Free 0.1 CPU, 512MB RAM)  │
└───────────────────────────────────────┘         └───────────────────┬────────────────────┘
                                                                      │
                                                                      ▼
                                                          [ data/jobs.xlsx (Packaged) ]
                                                          (Persistent within session;
                                                           Resets to Git state on dyno cycle)
```

---

## 2. Cost Analysis: What Costs ₹0 vs What Cannot Be Free

| Resource | Service | Monthly Cost | Notes |
| :--- | :--- | :---: | :--- |
| **Frontend Hosting** | Cloudflare Pages | **₹0.00** | Unlimited bandwidth, free `*.pages.dev` subdomain, free automated SSL certificate. |
| **Backend API Server** | Render.com (Free Web Service) | **₹0.00** | Free 512MB RAM instance, automatic Git deploys, free `*.onrender.com` HTTPS endpoint. Spins down after 15 min inactivity; wakes in ~30s. |
| **Domain Name** | Subdomain (`*.pages.dev`, `*.onrender.com`) | **₹0.00** | No custom domain purchase required. |
| **SSL / HTTPS** | Cloudflare & Let's Encrypt | **₹0.00** | Automatically provisioned and auto-renewed. |
| **CI/CD Automation** | GitHub Actions | **₹0.00** | 2,000 free build minutes/month on public/private repositories. |
| **Interactive Voice Simulator** | Browser SpeechSynthesis + Backend DTMF | **₹0.00** | Works in all modern browsers with Telugu, Hindi, English TTS. |
| **Telecom Toll-Free Number (1800)** | Commercial Telecom Carrier | **Paid** *(Cannot be free)* | TRAI regulations in India require enterprise KYC and commercial billing (~₹1,500/month rental + per-minute inbound call charges). |

---

## 3. Accounts Needed (All ₹0)

1. **GitHub Account** ([github.com](https://github.com)): To host your repository and run automated CI/CD.
2. **Cloudflare Account** ([dash.cloudflare.com](https://dash.cloudflare.com)): To deploy the frontend static pages on Cloudflare Pages.
3. **Render Account** ([render.com](https://render.com)): To host the FastAPI backend container. (Login with GitHub).

---

## 4. Step-by-Step Deployment Instructions

### STEP A: Push Your Code to GitHub
1. Create a new repository on GitHub: `https://github.com/<your-username>/localjobs`.
2. Push your local repository:
   ```bash
   git remote add origin https://github.com/<your-username>/localjobs.git
   git branch -M main
   git push -u origin main
   ```
3. GitHub Actions will automatically run the 24 automated tests and 16 manual verification checks to validate the build.

---

### STEP B: Deploy Backend to Render (₹0)
1. Go to [dashboard.render.com](https://dashboard.render.com) and click **New +** -> **Web Service**.
2. Connect your GitHub repository `localjobs`.
3. Configure the service settings:
   - **Name**: `localjobs-backend`
   - **Region**: Singapore (fastest for India) or Oregon
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python backend/app/repositories/init_db.py`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
4. Add Environment Variables under **Advanced**:
   - `APP_ENV`: `production`
   - `ALLOWED_ORIGINS`: `*`
   - `ADMIN_SECRET`: `<generate-a-secret-string>`
   - `EMPLOYER_SECRET`: `<generate-a-secret-string>`
5. Click **Create Web Service**.
6. Wait 2 minutes. Once deployed, Render will provide your public URL:
   `https://localjobs-backend.onrender.com`
7. Verify by visiting `https://localjobs-backend.onrender.com/health` in your browser.

---

### STEP C: Deploy Frontend to Cloudflare Pages (₹0)
1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) and select **Workers & Pages** -> **Create application** -> **Pages** -> **Connect to Git**.
2. Select your `localjobs` repository.
3. Configure Build Settings:
   - **Project Name**: `localjobs`
   - **Production Branch**: `main`
   - **Framework Preset**: `None`
   - **Build Output Directory**: `frontend`
4. Add Environment Variable:
   - `VITE_API_BASE_URL`: `https://localjobs-backend.onrender.com` (Your Render backend URL)
5. Click **Save and Deploy**.
6. Cloudflare will deploy your site in under 30 seconds at:
   `https://localjobs.pages.dev`

---

## 5. Connecting & Testing the Public System

1. Visit your Cloudflare Pages URL (`https://localjobs.pages.dev`).
2. Click **⚙️ API Backend** in the top navigation bar to confirm or switch your Backend URL:
   - Set to `https://localjobs-backend.onrender.com`.
3. **Test the Worker Journey**:
   - Filter by **Driver** -> Locality **Uppal** -> Confirm Job `JOB-1001` (₹18,000/mo) renders.
   - Click **Interested / Apply** -> Enter phone number `9848012345` -> Submit.
4. **Test the Voice IVR Simulator**:
   - Click **📞 Phone Simulator** in the navbar.
   - Click **DIAL IVR**.
   - Press **1** (Telugu) -> **1** (Driver) -> **1** (Uppal) -> Hear the voice synthesis reading the job -> Press **1** (Interested).
5. **Test the Admin Console**:
   - Open `/admin` -> Enter your `ADMIN_SECRET`.
   - Verify the candidate application is visible in real-time.

---

## 6. Persistent Cloud Storage: Free Managed PostgreSQL Setup (Supabase / Neon)

On free hosting providers like Render Free, the local filesystem is **ephemeral** (restarting the dyno wipes runtime changes to local files). 

LocalJobs solves this with an active repository architecture:
* **Local Development**: `DATA_BACKEND=excel` uses `data/jobs.xlsx` (zero setup, no database daemon required).
* **Public Production Deployment**: `DATA_BACKEND=postgres` uses a free managed PostgreSQL database with ACID transactions and persistent storage.

---

### Step-by-Step: Setting Up ₹0 Free PostgreSQL

#### Option A: Supabase (Recommended)
1. Go to [supabase.com](https://supabase.com) and create a free account (no credit card needed).
2. Click **New Project** -> Name it `localjobs-db` -> Set a database password -> Choose **Singapore** or **Mumbai** (South Asia).
3. Under **Project Settings** -> **Database** -> **Connection string**, copy the **URI** connection string:
   ```text
   postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```
4. (Optional) Run `backend/app/repositories/postgres_schema.sql` directly in Supabase's **SQL Editor** if you wish to inspect tables manually. (The FastAPI backend also auto-creates all tables on startup via `init_db_postgres()`).

#### Option B: Neon Serverless PostgreSQL
1. Go to [neon.tech](https://neon.tech) and create a free account.
2. Create project `localjobs` -> Select region **Asia Pacific (Singapore)**.
3. Copy the pooled connection string:
   ```text
   postgresql://[user]:[password]@[endpoint].neon.tech/neondb?sslmode=require
   ```

---

### Importing Seed Data to PostgreSQL

Run the idempotent import script locally or against your remote cloud database:
```bash
# Import into remote Supabase/Neon database:
python -m backend.app.repositories.import_excel_to_postgres --excel data/jobs.xlsx --db-url "postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres"
```

---

### Render Environment Configuration for Production

In your Render service dashboard under **Environment Variables**, configure:
```text
APP_ENV=production
DATA_BACKEND=postgres
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres
ADMIN_SECRET=<your-chosen-admin-token>
EMPLOYER_SECRET=<your-chosen-employer-token>
ALLOWED_ORIGINS=*
```

Once configured, candidate applications, employer registrations, and job postings remain persistent across all dyno restarts and sleeps.
