# Waitlist Management API Backend Boilerplate

This repository contains a FastAPI backend boilerplate based on the Waitlist Management API contract.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Primary API base URL: `http://localhost:8000/v1`

Compatibility (unversioned) base URL: `http://localhost:8000`

## Frontend connection notes

If your frontend is running at `http://localhost:3000` (or Vite defaults on `5173`), CORS is already enabled.

To customize allowed origins:

```bash
export CORS_ALLOW_ORIGINS="http://localhost:3000,http://localhost:5173"
```

## Frontend boilerplate compatibility

To reduce first-run 404s from polling demos, the backend seeds deterministic demo data at startup:

- Event `550e8400-e29b-41d4-a716-446655440000`
- Waitlist entry `880e8400-e29b-41d4-a716-446655440003` under that event
- Legacy numeric event `223` for starter form testing

This lets frontends that begin by polling reference IDs receive valid responses immediately.

## Implemented boilerplate endpoints

- `POST /v1/auth/login` (also available as `POST /auth/login`)
- `POST /v1/events` (also available as `POST /events`)
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
