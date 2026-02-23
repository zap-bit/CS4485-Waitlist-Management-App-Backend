from __future__ import annotations

from math import ceil

from app.errors import ApiError
from app.models import (
    DashboardResponse,
    EntryStatus,
    EntryType,
    Event,
    EventCreate,
    EventType,
    PromoteRequest,
    SeatRequest,
    Table,
    WaitlistCreate,
    WaitlistEntry,
)
from app.store import store


def create_event(payload: EventCreate) -> Event:
    event = Event(**payload.model_dump())

    if event.eventType == EventType.INDOOR_TABLES:
        total_tables = payload.totalTables or 0
        tables: list[Table] = []
        for i in range(total_tables):
            tables.append(Table(id=i + 1, name=f"Table {i+1}", capacity=4, row=i // 4, col=i % 4))
        event.tables = tables

    store.events[event.id] = event
    store.waitlists[event.id] = []
    return event


def get_event(event_id: str) -> Event:
    event = store.events.get(event_id)
    if not event:
        raise ApiError(404, "RESOURCE_NOT_FOUND", "Event not found", {"eventId": event_id})
    return event


def add_waitlist_entry(event_id: str, payload: WaitlistCreate) -> WaitlistEntry:
    get_event(event_id)
    entries = store.waitlists[event_id]

    if any(e.name.lower() == payload.name.lower() and e.status in {EntryStatus.QUEUED, EntryStatus.NOTIFIED} for e in entries):
        raise ApiError(409, "ALREADY_EXISTS", "Guest already on waitlist")

    position = sum(1 for e in entries if e.status == EntryStatus.QUEUED) + 1
    estimated_wait = max(5, position * 8)
    entry = WaitlistEntry(
        eventId=event_id,
        name=payload.name,
        partySize=payload.partySize,
        type=payload.type,
        position=position,
        estimatedWait=estimated_wait,
    )
    entries.append(entry)
    return entry


def get_waitlist_entry(event_id: str, entry_id: str) -> WaitlistEntry:
    get_event(event_id)
    for entry in store.waitlists[event_id]:
        if entry.id == entry_id:
            return entry
    raise ApiError(404, "RESOURCE_NOT_FOUND", "Entry not found", {"eventId": event_id, "entryId": entry_id})


def list_waitlist(event_id: str, page: int, page_size: int, type_filter: EntryType | None, status: EntryStatus | None) -> dict:
    get_event(event_id)
    entries = store.waitlists[event_id]
    filtered = [e for e in entries if (type_filter is None or e.type == type_filter) and (status is None or e.status == status)]
    start = (page - 1) * page_size
    data = filtered[start : start + page_size]
    return {"data": data, "page": page, "pageSize": page_size, "total": len(filtered), "totalPages": ceil(len(filtered) / page_size) if filtered else 0}


def get_dashboard(event_id: str) -> DashboardResponse:
    event = get_event(event_id)
    entries = store.waitlists[event_id]
    seated = [e for e in entries if e.status == EntryStatus.SEATED]
    occupancy = sum(e.partySize for e in seated)
    available_tables = None
    if event.eventType == EventType.INDOOR_TABLES:
        available_tables = sum(1 for t in event.tables if not t.occupied)

    return DashboardResponse(
        eventId=event_id,
        occupancy=occupancy,
        maxCapacity=event.maxCapacity,
        queuedReservations=sum(1 for e in entries if e.status == EntryStatus.QUEUED and e.type == EntryType.reservation),
        queuedWaitlist=sum(1 for e in entries if e.status == EntryStatus.QUEUED and e.type == EntryType.waitlist),
        availableTables=available_tables,
        recentActivity=[{"entryId": e.id, "name": e.name, "status": e.status} for e in entries[-5:]],
    )


def _best_table(event: Event, party_size: int, preferred_table_id: int | None = None) -> Table | None:
    tables = [t for t in event.tables if not t.occupied and t.capacity >= party_size]
    if preferred_table_id is not None:
        for table in tables:
            if table.id == preferred_table_id:
                return table
    return sorted(tables, key=lambda t: t.capacity)[0] if tables else None


def promote(event_id: str, payload: PromoteRequest) -> dict:
    event = get_event(event_id)
    entries = store.waitlists[event_id]
    queue = [e for e in entries if e.status == EntryStatus.QUEUED]
    if payload.type:
        queue = [e for e in queue if e.type == payload.type]

    promoted: list[WaitlistEntry] = []
    for entry in queue[: payload.count]:
        if event.eventType == EventType.INDOOR_TABLES:
            table = _best_table(event, entry.partySize)
            if not table:
                raise ApiError(409, "NO_CAPACITY", "No table available for current queue")
            table.occupied = True
            entry.assignedTableId = table.id
        entry.status = EntryStatus.NOTIFIED
        promoted.append(entry)

    return {"promoted": promoted, "count": len(promoted)}


def seat(event_id: str, payload: SeatRequest) -> WaitlistEntry:
    event = get_event(event_id)
    entry = get_waitlist_entry(event_id, payload.entryId)

    if entry.status not in {EntryStatus.NOTIFIED, EntryStatus.QUEUED}:
        raise ApiError(409, "INVALID_INPUT", "Only queued/notified guests can be seated")

    if event.eventType == EventType.INDOOR_TABLES:
        table = _best_table(event, entry.partySize, payload.tableId)
        if not table:
            raise ApiError(409, "TABLE_OCCUPIED", "Requested table unavailable")
        table.occupied = True
        entry.assignedTableId = table.id

    entry.status = EntryStatus.SEATED
    return entry
