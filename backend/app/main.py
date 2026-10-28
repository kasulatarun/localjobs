import os
from pathlib import Path
from typing import Dict, Any
from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx

from backend.app.api import jobs, categories, workers, applications, employers, ivr, llm
from backend.app.repositories.excel_repository import excel_repo
from backend.app.services.job_service import job_service
from backend.app.telephony.exotel import exotel_provider
from backend.app.security.validation import verify_admin

APP_DIR = Path(__file__).parent
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

app = FastAPI(
    title="LocalJobs API",
    description="Voice-first local employment platform connecting workers via DTMF IVR and web dashboards",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Mount API Routers
app.include_router(jobs.router)
app.include_router(categories.router)
app.include_router(workers.router)
app.include_router(applications.router)
app.include_router(employers.router)
app.include_router(ivr.router)
app.include_router(llm.router)

# --- Health Check ---

@app.get("/health", tags=["System"])
async def health_check():
    """System health check verifying Excel repository, Ollama LLM connectivity, and Telephony."""
    storage_stats = excel_repo.get_storage_stats()
    
    # Check Ollama
    ollama_url = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    ollama_ok = False
    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            resp = await client.get(f"{ollama_url}/api/version")
            ollama_ok = (resp.status_code == 200)
    except Exception:
        ollama_ok = False

    return {
        "status": "healthy",
        "service": "LocalJobs",
        "version": "1.0.0",
        "excel_storage": {
            "status": "connected",
            "file": str(excel_repo.file_path),
            **storage_stats
        },
        "telephony": {
            "exotel_configured": exotel_provider.is_configured(),
            "active_provider": "exotel" if exotel_provider.is_configured() else "mock_simulator"
        },
        "ollama_llm": {
            "configured_url": ollama_url,
            "connected": ollama_ok
        }
    }

# --- Web UI Routes ---

def _render_html(filename: str) -> HTMLResponse:
    file_path = TEMPLATES_DIR / filename
    if not file_path.exists():
        return HTMLResponse(f"<h3>Template {filename} not found</h3>", status_code=404)
    with open(file_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/", response_class=HTMLResponse, tags=["Web"])
@app.get("/worker", response_class=HTMLResponse, tags=["Web"])
def worker_portal():
    """Worker-facing high-accessibility web portal."""
    return _render_html("index.html")

@app.get("/employer", response_class=HTMLResponse, tags=["Web"])
def employer_portal():
    """Employer posting and hiring dashboard."""
    return _render_html("employer.html")

@app.get("/admin", response_class=HTMLResponse, tags=["Web"])
def admin_portal():
    """Administrator verification and command console."""
    return _render_html("admin.html")

@app.get("/simulator", response_class=HTMLResponse, tags=["Web"])
def ivr_simulator():
    """Interactive DTMF telephone keypad & voice simulator."""
    return _render_html("simulator.html")

# --- Admin API Routes ---

@app.get("/admin/stats", tags=["Admin"])
def get_admin_stats(_: bool = Depends(verify_admin)):
    """Aggregates overview stats for admin dashboard."""
    all_jobs = job_service.get_all_jobs_admin()
    pending = len([j for j in all_jobs if j.verified == "Pending"])
    verified_active = len([j for j in all_jobs if j.verified == "Verified" and j.status == "Active"])
    all_apps = excel_repo.get_all_applications()
    storage_stats = excel_repo.get_storage_stats()

    return {
        "total_jobs": len(all_jobs),
        "pending_jobs": pending,
        "verified_active_jobs": verified_active,
        "total_applications": len(all_apps),
        "total_employers": len(excel_repo.get_all_employers()),
        "total_workers": len(excel_repo.get_all_workers()),
        "migration_recommended": storage_stats.get("migration_recommended", False),
        "concurrency_risk": storage_stats.get("concurrency_risk", "NORMAL")
    }

@app.get("/admin/jobs", tags=["Admin"])
def get_all_jobs_for_admin(_: bool = Depends(verify_admin)):
    """Admin endpoint to view all jobs (including Pending, Closed, Expired)."""
    return [j.model_dump(by_alias=True) for j in job_service.get_all_jobs_admin()]

@app.get("/admin/workers", tags=["Admin"])
def get_all_workers_for_admin(_: bool = Depends(verify_admin)):
    """Admin endpoint to view all registered workers."""
    return [w.model_dump(by_alias=True) for w in excel_repo.get_all_workers()]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
