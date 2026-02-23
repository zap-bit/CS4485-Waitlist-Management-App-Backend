from __future__ import annotations

from fastapi import Depends, FastAPI, Query

from app.auth import DEMO_BEARER, require_auth
from app.errors import ApiError, api_error_handler
from app.models import (
    AuthLoginRequest,
    AuthLoginResponse,
    EntryStatus,
    EntryType,
    EventCreate,
    PromoteRequest,
    SeatRequest,
    SyncRequest,
    WaitlistCreate,
)
from app.services import (
    add_waitlist_entry,
    create_event,
    get_dashboard,
    get_event,
    get_waitlist_entry,
    list_waitlist,
    promote,
    seat,
)

app = FastAPI(title="Waitlist Management API", version="1.0.0")
app.add_exception_handler(ApiError, api_error_handler)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/auth/login", response_model=AuthLoginResponse)
def login(payload: AuthLoginRequest) -> AuthLoginResponse:
    _ = payload
    return AuthLoginResponse(token=DEMO_BEARER)


@app.post("/v1/events", dependencies=[Depends(require_auth)])
def create_event_endpoint(payload: EventCreate):
    return create_event(payload)


@app.get("/v1/events/{event_id}", dependencies=[Depends(require_auth)])
def get_event_endpoint(event_id: str):
    return get_event(event_id)


@app.post("/v1/events/{event_id}/waitlist")
def join_waitlist_endpoint(event_id: str, payload: WaitlistCreate):
    return add_waitlist_entry(event_id, payload)


@app.get("/v1/events/{event_id}/waitlist", dependencies=[Depends(require_auth)])
def list_waitlist_endpoint(
    event_id: str,
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=20, ge=1, le=100),
    type: EntryType | None = Query(default=None),
    status: EntryStatus | None = Query(default=None),
):
    return list_waitlist(event_id, page, pageSize, type, status)


@app.get("/v1/events/{event_id}/waitlist/{entry_id}")
def get_entry_endpoint(event_id: str, entry_id: str):
    return get_waitlist_entry(event_id, entry_id)


@app.get("/v1/events/{event_id}/staff/dashboard", dependencies=[Depends(require_auth)])
def dashboard_endpoint(event_id: str):
    return get_dashboard(event_id)


@app.post("/v1/events/{event_id}/staff/promote", dependencies=[Depends(require_auth)])
def promote_endpoint(event_id: str, payload: PromoteRequest):
    return promote(event_id, payload)


@app.post("/v1/events/{event_id}/staff/seat", dependencies=[Depends(require_auth)])
def seat_endpoint(event_id: str, payload: SeatRequest):
    return seat(event_id, payload)


@app.post("/v1/sync", dependencies=[Depends(require_auth)])
def sync_endpoint(payload: SyncRequest):
    conflicts: list[dict] = []
    for op in payload.operations:
        if op.conflictResolution is None:
            conflicts.append({"resource": op.resource, "resourceId": op.resourceId, "resolution": "SERVER_WINS"})
    return {
        "deviceId": payload.deviceId,
        "syncTimestamp": payload.syncTimestamp,
        "processed": len(payload.operations),
        "conflicts": conflicts,
    }
