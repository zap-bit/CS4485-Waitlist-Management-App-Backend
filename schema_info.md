**ORGANIZATIONS**
id | name | created_at
- **Description:** Represents organizations that manage events and attendees.

**STAFF_USERS**
id | organization_id | name | email | role | username | password | created_at
- **Description:** Represents staff members who manage venues and events for organizations. Includes login credentials (username and password).

**VENUES**
id | staff_user_id | name | address | timezone | created_at
- **Description:** Represents physical locations where events are hosted.

**EVENTS**
id | venue_id | name | description | default_duration_minutes | created_at
- **Description:** Represents events that are hosted at venues and consist of multiple tables.

**TABLES**
id | event_id | name | capacity | created_at
- **Description:** Represents tables available for seating during specific events.

**EVENT_SESSIONS**
id | event_id | room_id | start_time | end_time | capacity_override | status | created_at
- **Description:** Represents individual sessions of an event, scheduled in specific rooms.

**ATTENDEES**
id | organization_id | first_name | last_name | phone_number | email | party_id | is_party_leader | created_at
- **Description:** Represents individuals who attend events, optionally grouped into parties.

**WAITLIST_ENTRIES**
id | event_session_id | attendee_id | position | status | joined_at | promoted_at | responded_at | expires_at
- **Description:** Represents attendees waiting for a spot in an event session.

**ADMISSIONS**
id | event_session_id | attendee_id | check_in_time | check_out_time | source
- **Description:** Represents records of attendees checking in and out of event sessions.

**NOTIFICATIONS**
id | attendee_id | event_session_id | type | channel | status | sent_at | created_at
- **Description:** Represents notifications sent to attendees about event updates.

**SESSION_PREDICTIONS**
id | event_session_id | predicted_wait_time_minutes | predicted_no_show_rate | predicted_fill_rate | model_version | generated_at
- **Description:** Represents predictions for session metrics like wait time and attendance rates.

**PARTIES**
id | name | created_at
- **Description:** Represents groups of attendees, such as families or teams.

**TABLE_ASSIGNMENTS**
id | table_id | attendee_id | party_id | created_at
- **Description:** Represents assignments of attendees or parties to specific tables.


RELATIONS

1. ORGANIZATIONS ↔ STAFF_USERS (1:N)
   - **Relation:** Each organization can have multiple staff users, but each staff user belongs to one organization.
   - **Operations:**
     - Fetch all staff users for a specific organization.
     - Assign a staff user to an organization.
     - Delete an organization and cascade delete its staff users.

2. ORGANIZATIONS ↔ ATTENDEES (1:N)
   - **Relation:** Each organization can have multiple attendees, but each attendee belongs to one organization.
   - **Operations:**
     - Fetch all attendees for a specific organization.
     - Assign an attendee to an organization.
     - Delete an organization and cascade delete its attendees.

3. STAFF_USERS ↔ VENUES (1:N)
   - **Relation:** Each staff user can manage multiple venues, but each venue is managed by one staff user.
   - **Operations:**
     - Fetch all venues managed by a specific staff user.
     - Assign a venue to a staff user.
     - Delete a staff user and cascade delete their venues.

4. VENUES ↔ EVENTS (1:N)
   - **Relation:** Each venue can host multiple events, but each event is hosted at one venue.
   - **Operations:**
     - Fetch all events for a specific venue.
     - Assign an event to a venue.
     - Delete a venue and cascade delete its events.

5. EVENTS ↔ EVENT_SESSIONS (1:N)
   - **Relation:** Each event can have multiple sessions, but each session belongs to one event.
   - **Operations:**
     - Fetch all sessions for a specific event.
     - Assign a session to an event.
     - Delete an event and cascade delete its sessions.

6. EVENT_SESSIONS ↔ WAITLIST_ENTRIES (1:N)
   - **Relation:** Each event session can have multiple waitlist entries, but each waitlist entry belongs to one session.
   - **Operations:**
     - Fetch all waitlist entries for a specific session.
     - Add an attendee to the waitlist for a session.
     - Delete a session and cascade delete its waitlist entries.

7. EVENT_SESSIONS ↔ ADMISSIONS (1:N)
   - **Relation:** Each event session can have multiple admissions, but each admission belongs to one session.
   - **Operations:**
     - Fetch all admissions for a specific session.
     - Check in or check out an attendee for a session.
     - Delete a session and cascade delete its admissions.

8. EVENT_SESSIONS ↔ NOTIFICATIONS (1:N)
    - **Relation:** Each event session can have multiple notifications, but each notification belongs to one session.
    - **Operations:**
      - Fetch all notifications for a specific session.
      - Send a notification for a session.
      - Delete a session and cascade delete its notifications.

9. EVENT_SESSIONS ↔ TABLES (1:N)
    - **Relation:** Each event session can have multiple tables, but each table belongs to one session.
    - **Operations:**
      - Fetch all tables for a specific session.
      - Assign a table to a session.
      - Delete a session and cascade delete its tables.

10. TABLES ↔ TABLE_ASSIGNMENTS (1:N)
    - **Relation:** Each table can have multiple assignments, but each assignment belongs to one table.
    - **Operations:**
      - Fetch all assignments for a specific table.
      - Assign an attendee or party to a table.
      - Delete a table and cascade delete its assignments.

11. ATTENDEES ↔ WAITLIST_ENTRIES (1:N)
    - **Relation:** Each attendee can have multiple waitlist entries, but each waitlist entry belongs to one attendee.
    - **Operations:**
      - Fetch all waitlist entries for a specific attendee.
      - Add an attendee to a waitlist.
      - Delete an attendee and cascade delete their waitlist entries.

12. ATTENDEES ↔ ADMISSIONS (1:N)
    - **Relation:** Each attendee can have multiple admissions, but each admission belongs to one attendee.
    - **Operations:**
      - Fetch all admissions for a specific attendee.
      - Check in or check out an attendee.
      - Delete an attendee and cascade delete their admissions.

13. ATTENDEES ↔ NOTIFICATIONS (1:N)
    - **Relation:** Each attendee can have multiple notifications, but each notification belongs to one attendee.
    - **Operations:**
      - Fetch all notifications for a specific attendee.
      - Send a notification to an attendee.
      - Delete an attendee and cascade delete their notifications.

14. ATTENDEES ↔ PARTIES (N:1)
    - **Relation:** Each attendee can belong to one party, but a party can have multiple attendees.
    - **Operations:**
      - Fetch all attendees in a specific party.
      - Assign an attendee to a party.
      - Delete a party and set `party_id` to NULL for its attendees.

15. PARTIES ↔ TABLE_ASSIGNMENTS (1:N)
    - **Relation:** Each party can have multiple table assignments, but each assignment belongs to one party.
    - **Operations:**
      - Fetch all table assignments for a specific party.
      - Assign a party to a table.
      - Delete a party and cascade delete its table assignments.

16. EVENT_SESSIONS ↔ SESSION_PREDICTIONS (1:1)
    - **Relation:** Each event session can have one prediction, and each prediction belongs to one session.
    - **Operations:**
      - Fetch the prediction for a specific session.
      - Generate or update a prediction for a session.
      - Delete a session and cascade delete its prediction.