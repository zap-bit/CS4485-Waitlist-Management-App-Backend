from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer demo-token"}


def test_event_waitlist_flow():
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
