# Exotel Onboarding & 1800 Toll-Free Setup Guide

This document describes the exact process for connecting LocalJobs to a live telephony carrier (Exotel) and provisioning an Indian 1800 Toll-Free Number.

---

## 1. Provider Registration & KYC

1. Visit [https://my.exotel.com](https://my.exotel.com) and create an enterprise account.
2. Complete Telecom Regulatory Authority of India (TRAI) KYC:
   - Certificate of Incorporation (or GST registration)
   - Authorized Signatory ID (Aadhaar / Passport)
   - Letter of authorization for Toll-Free number usage
3. Request an **1800 Toll-Free ExoPhone** from the Exotel dashboard under `Numbers -> Buy Numbers -> 1800 Toll-Free`.

---

## 2. Exotel Applet Flow Configuration

In the Exotel Applet Designer (`Applets -> Create Applet`):

1. **Add Passthru Applet (Greeting & First Question)**:
   - **URL**: `https://api.localjobs.in/ivr/incoming`
   - **HTTP Method**: `POST`
   - **Time to wait for response**: `5 seconds`
   - When the user calls, Exotel sends `CallSid` and `From` to LocalJobs.
   - LocalJobs responds with the initial greeting and prompts for language.

2. **Add Gather / GetDigits Applet (DTMF Menu Loop)**:
   - **URL**: `https://api.localjobs.in/ivr/dtmf`
   - **HTTP Method**: `POST`
   - **Number of Digits**: `1`
   - **Timeout**: `6 seconds`
   - **Finish on Key**: None (single keypress immediately submits)

3. **Add Status Callback Applet**:
   - **Callback URL**: `https://api.localjobs.in/ivr/callback`
   - **Trigger**: When call is completed / disconnected.

---

## 3. Configuring LocalJobs Environment

Once your ExoPhone and API tokens are issued:

Edit your `.env` file:
```env
EXOTEL_ACCOUNT_SID=your_account_sid_here
EXOTEL_API_KEY=your_api_key_here
EXOTEL_API_TOKEN=your_api_token_here
EXOTEL_EXOPHONE=1800XXXXXXX
```

Restart your server. The `/health` endpoint will confirm:
```json
{
  "telephony": {
    "exotel_configured": true,
    "active_provider": "exotel"
  }
}
```

---

## 4. Local Testing with Webhooks via Tunnel

To test incoming Exotel calls on your local development machine before public deployment:

1. Start your local server on port 8000:
   ```bash
   python -m uvicorn backend.app.main:app --port 8000
   ```
2. In a separate terminal, expose port 8000 using Cloudflare Tunnel or ngrok:
   ```bash
   ngrok http 8000
   ```
3. Copy your forwarding URL (e.g. `https://xyz.ngrok-free.app`).
4. In the Exotel Passthru Applet, enter:
   - `https://xyz.ngrok-free.app/ivr/incoming`
   - `https://xyz.ngrok-free.app/ivr/dtmf`
5. Dial your Exotel trial number from your mobile phone. You will immediately hear the LocalJobs greeting and can press 1-2-3 on your phone's keypad!
