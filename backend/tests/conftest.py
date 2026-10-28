import os
import shutil
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.repositories.excel_repository import excel_repo
from backend.app.repositories.init_db import create_initial_workbook
from backend.app.services.ivr_service import ivr_service

@pytest.fixture(scope="session", autouse=True)
def setup_test_excel():
    temp_dir = tempfile.mkdtemp()
    temp_excel = Path(temp_dir) / "test_jobs.xlsx"
    create_initial_workbook(temp_excel)

    original_path = excel_repo.file_path
    excel_repo.set_file_path(temp_excel)

    yield temp_excel

    excel_repo.set_file_path(original_path)
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_ivr():
    with ivr_service._lock:
        ivr_service._sessions.clear()
    yield
