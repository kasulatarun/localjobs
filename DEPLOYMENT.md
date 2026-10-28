# LocalJobs Deployment & Rollout Strategy

## 1. Staged Rollout Strategy

LocalJobs must not be deployed blindly to nationwide production. Follow this strict phased rollout:

```text
PHASE 1: LOCAL DEVELOPMENT & SIMULATOR
   ↓  (Interactive browser dialer & automated unit tests)
PHASE 2: TELEPHONY TEST NUMBER (PILOT)
   ↓  (Single Exotel virtual number mapped to dev server webhook via ngrok/tailscale)
PHASE 3: LIMITED GEOGRAPHIC PILOT (UPPAL / EAST HYDERABAD)
   ↓  (5-10 verified employers, ~50 local workers, physical posters at tea stalls/bus stands)
PHASE 4: REGIONAL EXPANSION
   ↓  (Hyderabad & Secunderabad districts, migration to PostgreSQL)
PHASE 5: MULTI-STATE NATIONWIDE PRODUCTION
```

---

## 2. Server Deployment Guide (Ubuntu / Debian / Docker)

### Step 1: System Packages
```bash
sudo apt update && sudo apt install -y python3-pip python3-venv git nginx
```

### Step 2: Clone & Virtualenv
```bash
git clone <repo_url> /opt/localjobs
cd /opt/localjobs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Production Environment (`/opt/localjobs/.env`)
```env
APP_ENV=production
HOST=127.0.0.1
PORT=8000

OLLAMA_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3

EXOTEL_ACCOUNT_SID=your_exotel_sid
EXOTEL_API_KEY=your_exotel_key
EXOTEL_API_TOKEN=your_exotel_token
EXOTEL_EXOPHONE=0804710XXXX

ADMIN_SECRET=generate_strong_64_character_hex_secret
EMPLOYER_SECRET=generate_strong_64_character_hex_secret
```

### Step 4: Systemd Service (`/etc/systemd/system/localjobs.service`)
```ini
[Unit]
Description=LocalJobs Voice & Web Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/localjobs
EnvironmentFile=/opt/localjobs/.env
ExecStart=/opt/localjobs/venv/bin/uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --workers 2

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now localjobs
```

### Step 5: Nginx Reverse Proxy with HTTPS
```nginx
server {
    server_name api.localjobs.in;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Install SSL certificate using Certbot:
```bash
sudo certbot --nginx -d api.localjobs.in
```
