from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer demo-token"}


def test_event_waitlist_flow_v1():
    create_event_response = client.post(
        "/v1/events",
        headers=auth_headers(),
        json={
            "name": "Fine Dining Restaurant",
            "eventType": "INDOOR_TABLES",
            "maxCapacity": 100,
            "totalTables": 12,
            "startTime": "2026-03-20T17:00:00Z",
            "endTime": "2026-03-20T23:00:00Z",
        },
    )
    assert create_event_response.status_code == 200
    event_id = create_event_response.json()["id"]

    waitlist_response = client.post(
        f"/v1/events/{event_id}/waitlist",
        json={
            "name": "Sarah Johnson",
            "partySize": 4,
            "type": "waitlist",
            "specialRequests": "Table 5",
        },
    )
    assert waitlist_response.status_code == 200
    entry_id = waitlist_response.json()["id"]

    dashboard_response = client.get(f"/v1/events/{event_id}/staff/dashboard", headers=auth_headers())
    assert dashboard_response.status_code == 200
    assert dashboard_response.json()["queuedWaitlist"] == 1

    promote_response = client.post(
        f"/v1/events/{event_id}/staff/promote",
        headers=auth_headers(),
        json={"count": 1, "type": "waitlist"},
    )
    assert promote_response.status_code == 200
    assert promote_response.json()["count"] == 1

    seat_response = client.post(
        f"/v1/events/{event_id}/staff/seat",
        headers=auth_headers(),
        json={"entryId": entry_id, "tableId": 2},
    )
    assert seat_response.status_code == 200
    assert seat_response.json()["status"] == "SEATED"


def test_unversioned_aliases_and_cors_preflight():
    login_response = client.post("/auth/login", json={"email": "a@b.com", "password": "pw"})
    assert login_response.status_code == 200
    assert login_response.json()["token"] == "demo-token"

    preflight_response = client.options(
        "/v1/events",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert preflight_response.status_code == 200
    assert preflight_response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_seeded_demo_records_exist_for_frontend_boilerplates():
    seeded_entry = client.get(
        "/v1/events/550e8400-e29b-41d4-a716-446655440000/waitlist/880e8400-e29b-41d4-a716-446655440003"
    )
    assert seeded_entry.status_code == 200
    assert seeded_entry.json()["name"] == "Sarah Johnson"

    add_to_legacy_event = client.post(
        "/v1/events/223/waitlist",
        json={"name": "Frontend Smoke Test", "partySize": 2, "type": "waitlist"},
    )
    assert add_to_legacy_event.status_code == 200
    assert add_to_legacy_event.json()["eventId"] == "223"
