# Waitlist Management API Backend Boilerplate

This repository now contains a FastAPI backend boilerplate based on the provided Waitlist Management API contract.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API base URL in development: `http://localhost:8000/v1`

## Implemented boilerplate endpoints

- `POST /v1/auth/login`
- `POST /v1/events`
- `GET /v1/events/{event_id}`
- `POST /v1/events/{event_id}/waitlist`
- `GET /v1/events/{event_id}/waitlist`
- `GET /v1/events/{event_id}/waitlist/{entry_id}`
- `GET /v1/events/{event_id}/staff/dashboard`
- `POST /v1/events/{event_id}/staff/promote`
- `POST /v1/events/{event_id}/staff/seat`
- `POST /v1/sync`

Swagger UI: `http://localhost:8000/docs`

## Demo auth values

- Bearer token: `demo-token`
- API key: `demo-api-key`
