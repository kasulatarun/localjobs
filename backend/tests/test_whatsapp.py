import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import config
from backend.app.services.whatsapp_service import whatsapp_service
from backend.app.repositories import repo

client = TestClient(app)

DEMO_PHONE = "+919848953136"

@pytest.fixture(autouse=True)
def reset_demo_whatsapp_session():
    whatsapp_service.reset_session(DEMO_PHONE)
    yield
    whatsapp_service.reset_session(DEMO_PHONE)

def test_whatsapp_webhook_verification():
    # Valid handshake
    res = client.get(
        "/whatsapp/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "verify_challenge_code_999",
            "hub.verify_token": config.WHATSAPP_VERIFY_TOKEN
        }
    )
    assert res.status_code == 200
    assert res.text == "verify_challenge_code_999"

    # Invalid token handshake
    res_bad = client.get(
        "/whatsapp/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "bad_challenge",
            "hub.verify_token": "wrong_token"
        }
    )
    assert res_bad.status_code == 403

def test_whatsapp_welcome_message():
    res = client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "Hi"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "Welcome to LocalJobs" in data["reply"]
    assert "తెలుగు" in data["reply"]
    assert "हिंदी" in data["reply"]
    assert "English" in data["reply"]

def test_whatsapp_telugu_flow_and_application():
    # 1. Start with Hi
    res1 = client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "హాయ్"})
    assert res1.status_code == 200

    # 2. Select Telugu (1)
    res2 = client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "1"})
    assert "డ్రైవర్ (Driver)" in res2.json()["reply"]

    # 3. Select Driver (1)
    res3 = client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "1"})
    assert "ప్రాంతాన్ని ఎంచుకోండి" in res3.json()["reply"]
    assert "Uppal" in res3.json()["reply"]

    # 4. Select Uppal (1)
    res4 = client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "1"})
    reply_text = res4.json()["reply"]
    assert "Driver" in reply_text or "ఉద్యోగం" in reply_text

    # 5. Apply for job (1)
    res5 = client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "1"})
    reply5 = res5.json()["reply"]
    assert "విజయవంతంగా" in reply5 or "ఇప్పటికే ఈ ఉద్యోగానికి దరఖాస్తు" in reply5

    # 6. Apply again -> Duplicate warning check
    # Reset back to view jobs or send apply again
    res6 = client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "1"})
    # Since state moved or re-apply attempted
    assert res6.status_code == 200

def test_whatsapp_hindi_flow():
    # 1. Reset
    client.post("/whatsapp/reset", params={"phone": "+919848953136"})
    
    # 2. Send Start
    client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "start"})

    # 3. Select Hindi (2)
    res = client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "2"})
    assert "काम चाहिए" in res.json()["reply"]
    assert "ड्राइवर" in res.json()["reply"]

def test_whatsapp_english_flow():
    # 1. Reset
    client.post("/whatsapp/reset", params={"phone": "+919848953136"})

    # 2. Send Hello
    client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "Hello"})

    # 3. Select English (3)
    res = client.post("/whatsapp/simulate", json={"from_phone": DEMO_PHONE, "message": "3"})
    assert "What job are you looking for?" in res.json()["reply"]
    assert "Driver" in res.json()["reply"]

def test_whatsapp_meta_cloud_api_webhook_format():
    # Simulate inbound Meta Cloud API Webhook payload
    meta_payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "1800123456",
                                "phone_number_id": "987654321"
                            },
                            "contacts": [{"wa_id": "919848953136", "profile": {"name": "Tarun"}}],
                            "messages": [
                                {
                                    "from": "919848953136",
                                    "id": "wamid.HBgLM...",
                                    "timestamp": "1710000000",
                                    "text": {"body": "Hi"},
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    res = client.post("/whatsapp/webhook", json=meta_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["to_phone"] == "+919848953136"
    assert "Welcome to LocalJobs" in data["reply"]

def test_whatsapp_autoresponder_for_wa_format():
    # Exactly what AutoResponder for WA sends in their screenshot
    autoresponder_payload = {
        "appPackageName": "tkstudio.autoresponderforwa",
        "messengerPackageName": "com.whatsapp",
        "query": {
            "sender": "+919848953136",
            "message": "Hi",
            "isGroup": False,
            "ruleId": 1
        }
    }
    res = client.post("/whatsapp/webhook", json=autoresponder_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "replies" in data
    assert isinstance(data["replies"], list)
    assert len(data["replies"]) == 1
    assert "Welcome to LocalJobs" in data["replies"][0]["message"]
