-- =====================================================
-- Event Waitlist Management System - Full Schema
-- =====================================================

-- Create the database (if it doesn't already exist)
CREATE DATABASE event_waitlist;

-- Connect to the database
\c event_waitlist;

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- ENUM TYPES
-- =====================================================

CREATE TYPE session_status AS ENUM (
    'scheduled',
    'live',
    'completed',
    'cancelled'
);

CREATE TYPE waitlist_status AS ENUM (
    'waiting',
    'promoted',
    'accepted',
    'expired',
    'cancelled',
    'no_show'
);

CREATE TYPE notification_status AS ENUM (
    'pending',
    'sent',
    'failed'
);

CREATE TYPE staff_role AS ENUM (
    'admin',
    'manager',
    'checkin_staff'
);

-- =====================================================
-- CORE TABLES
-- =====================================================

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Staff Users Table
CREATE TABLE staff_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role staff_role NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Updated Venues Table to reference Staff Users
CREATE TABLE venues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    staff_user_id UUID NOT NULL REFERENCES staff_users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    timezone TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Updated EVENTS table to reference VENUES directly
ALTER TABLE events
DROP COLUMN venue_id,
ADD COLUMN venue_id UUID NOT NULL REFERENCES venues(id) ON DELETE CASCADE;

-- Updated TABLES table to reference EVENTS directly
ALTER TABLE tables
DROP COLUMN event_session_id,
ADD COLUMN event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE;

CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id UUID NOT NULL REFERENCES venues(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    default_duration_minutes INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE event_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    room_id UUID NOT NULL REFERENCES rooms(id),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    capacity_override INTEGER CHECK (capacity_override > 0),
    status session_status DEFAULT 'scheduled',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CHECK (end_time > start_time)
);

CREATE TABLE attendees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT,
    email TEXT,
    party_id UUID REFERENCES parties(id) ON DELETE SET NULL,
    is_party_leader BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE waitlist_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_session_id UUID NOT NULL REFERENCES event_sessions(id) ON DELETE CASCADE,
    attendee_id UUID NOT NULL REFERENCES attendees(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    status waitlist_status DEFAULT 'waiting',
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    promoted_at TIMESTAMP WITH TIME ZONE,
    responded_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(event_session_id, attendee_id)
);

CREATE TABLE admissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_session_id UUID NOT NULL REFERENCES event_sessions(id) ON DELETE CASCADE,
    attendee_id UUID NOT NULL REFERENCES attendees(id) ON DELETE CASCADE,
    check_in_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    check_out_time TIMESTAMP WITH TIME ZONE,
    source TEXT CHECK (source IN ('qr', 'staff_manual', 'auto'))
);

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attendee_id UUID NOT NULL REFERENCES attendees(id) ON DELETE CASCADE,
    event_session_id UUID REFERENCES event_sessions(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    channel TEXT CHECK (channel IN ('sms', 'email', 'push')),
    status notification_status DEFAULT 'pending',
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE session_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_session_id UUID NOT NULL REFERENCES event_sessions(id) ON DELETE CASCADE,
    predicted_wait_time_minutes INTEGER,
    predicted_no_show_rate NUMERIC(5,2),
    predicted_fill_rate NUMERIC(5,2),
    model_version TEXT,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- Add Parties Table
-- =====================================================
CREATE TABLE parties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL, -- Optional name for the party (e.g., "Smith Family")
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- Add Tables Table
-- =====================================================
CREATE TABLE tables (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    name TEXT NOT NULL, -- Table name or number (e.g., "Table 1")
    capacity INTEGER NOT NULL CHECK (capacity > 0), -- Max number of attendees per table
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- Update Attendees Table
-- =====================================================
ALTER TABLE attendees
ADD COLUMN party_id UUID REFERENCES parties(id) ON DELETE SET NULL, -- Associate attendee with a party
ADD COLUMN is_party_leader BOOLEAN DEFAULT FALSE; -- Flag to indicate if the attendee is the party leader

-- =====================================================
-- Add Table Assignments Table
-- =====================================================
CREATE TABLE table_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_id UUID NOT NULL REFERENCES tables(id) ON DELETE CASCADE,
    attendee_id UUID REFERENCES attendees(id) ON DELETE CASCADE, -- Assign individual attendees to tables
    party_id UUID REFERENCES parties(id) ON DELETE CASCADE, -- OR assign entire parties to tables
    UNIQUE(table_id, attendee_id), -- Ensure no duplicate attendee assignments
    UNIQUE(table_id, party_id), -- Ensure no duplicate party assignments
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- INDEXES (Performance Optimization)
-- =====================================================

CREATE INDEX idx_venues_org ON venues(organization_id);
CREATE INDEX idx_rooms_venue ON rooms(venue_id);
CREATE INDEX idx_events_venue ON events(venue_id);

CREATE INDEX idx_sessions_event ON event_sessions(event_id);
CREATE INDEX idx_sessions_room ON event_sessions(room_id);
CREATE INDEX idx_sessions_time ON event_sessions(start_time);

CREATE INDEX idx_attendees_org ON attendees(organization_id);
CREATE INDEX idx_attendees_email ON attendees(email);

CREATE INDEX idx_waitlist_session ON waitlist_entries(event_session_id);
CREATE INDEX idx_waitlist_attendee ON waitlist_entries(attendee_id);
CREATE INDEX idx_waitlist_status ON waitlist_entries(status);

CREATE INDEX idx_admissions_session ON admissions(event_session_id);
CREATE INDEX idx_admissions_attendee ON admissions(attendee_id);

CREATE INDEX idx_notifications_attendee ON notifications(attendee_id);
CREATE INDEX idx_notifications_status ON notifications(status);

CREATE INDEX idx_predictions_session ON session_predictions(event_session_id);

CREATE INDEX idx_staff_org ON staff_users(organization_id);

-- =====================================================
-- END OF SCHEMA
-- ======================================================