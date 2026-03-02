# Updated Schema Information

## Relationships and Operations

### Account Table
- **Relationships:**
  - `Account` ↔ `Event` (1:N): A business account can create multiple events.
  - `Account` ↔ `EventTable` (1:N): A user account can be the leader of multiple tables.
  - `Account` ↔ `Party` (1:N): A user account can lead multiple parties.
  - `Account` ↔ `Notifications` (1:N): A user account can receive multiple notifications.

- **Operations:**
  - Create a new account (user or business).
  - Update account details (e.g., email, password).
  - Delete an account and cascade delete related events, parties, and notifications.

### Event Table
- **Relationships:**
  - `Event` ↔ `Account` (N:1): Each event is created by a business account.
  - `Event` ↔ `EventTable` (1:N): An event can have multiple tables.
  - `Event` ↔ `Party` (1:N): An event can have multiple parties.
  - `Event` ↔ `Notifications` (1:N): An event can generate multiple notifications.
  - `Event` ↔ `Predictions` (1:1): Each event can have one prediction.

- **Operations:**
  - Create a new event.
  - Update event details (e.g., name, type, location).
  - Delete an event and cascade delete related tables, parties, notifications, and predictions.

### EventTable Table
- **Relationships:**
  - `EventTable` ↔ `Event` (N:1): Each table belongs to an event.
  - `EventTable` ↔ `Party` (N:1): A table can be assigned to a party.
  - `EventTable` ↔ `Account` (N:1): A table can have a party leader.

- **Operations:**
  - Create a new table for an event.
  - Assign a party or party leader to a table.
  - Delete a table.

### Party Table
- **Relationships:**
  - `Party` ↔ `Account` (N:1): Each party has a leader.
  - `Party` ↔ `Event` (N:1): Each party belongs to an event.
  - `Party` ↔ `EventTable` (1:N): A party can be assigned to multiple tables.

- **Operations:**
  - Create a new party.
  - Update party details (e.g., size, special requests).
  - Delete a party and cascade delete related table assignments.

### Notifications Table
- **Relationships:**
  - `Notifications` ↔ `Account` (N:1): Each notification is sent to a user account.
  - `Notifications` ↔ `Event` (N:1): Each notification is related to an event.

- **Operations:**
  - Create a new notification.
  - Update notification status (e.g., sent, failed).
  - Delete a notification.

### Predictions Table
- **Relationships:**
  - `Predictions` ↔ `Event` (1:1): Each prediction is associated with one event.

- **Operations:**
  - Create or update a prediction for an event.
  - Delete a prediction.

---

This document outlines the relationships and possible operations for each table in the schema. Let me know if you need further details or adjustments!