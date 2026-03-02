-- =====================================================
-- Updated Schema for Event Waitlist Management System
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

CREATE TYPE role_type AS ENUM (
    'USER',
    'BUSINESS'
);

CREATE TYPE event_type AS ENUM (
    'CAPACITY',
    'TABLE'
);

CREATE TYPE notification_status AS ENUM (
    'sent',
    'failedToSend'
);

-- =====================================================
-- CORE TABLES
-- =====================================================

CREATE TABLE Account (
    UUID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT,
    businessName TEXT,
    role role_type NOT NULL,
    CHECK (
        (role = 'USER' AND businessName IS NULL) OR
        (role = 'BUSINESS' AND name IS NULL)
    )
);

CREATE TABLE Event (
    UUID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    BusinessAccountUUID UUID NOT NULL REFERENCES Account(UUID) ON DELETE CASCADE,
    name TEXT NOT NULL,
    eventType event_type NOT NULL,
    location TEXT,
    capacity INTEGER,
    estimatedTimePerPerson INTEGER,
    numberOfTables INTEGER,
    avgTableSize INTEGER,
    reservationDuration INTEGER,
    noShowPolicy TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CHECK (
        (eventType = 'CAPACITY' AND numberOfTables IS NULL AND avgTableSize IS NULL AND reservationDuration IS NULL AND noShowPolicy IS NULL) OR
        (eventType = 'TABLE' AND location IS NULL AND capacity IS NULL AND estimatedTimePerPerson IS NULL)
    )
);

CREATE TABLE EventTable (
    UUID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    EventUUID UUID NOT NULL REFERENCES Event(UUID) ON DELETE CASCADE,
    PartyLeaderUUID UUID REFERENCES Account(UUID),
    PartyUUID UUID REFERENCES Party(UUID), -- Added connection to Party table
    capacity INTEGER NOT NULL
);

CREATE TABLE Party (
    UUID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    PartyLeaderUUID UUID NOT NULL REFERENCES Account(UUID),
    EventUUID UUID NOT NULL REFERENCES Event(UUID) ON DELETE CASCADE,
    partySize INTEGER NOT NULL,
    specialRequests TEXT
);

CREATE TABLE Notifications (
    UUID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    PartyLeaderUUID UUID NOT NULL REFERENCES Account(UUID),
    EventUUID UUID NOT NULL REFERENCES Event(UUID),
    status notification_status NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE Predictions (
    UUID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    EventUUID UUID NOT NULL REFERENCES Event(UUID) ON DELETE CASCADE,
    PredictedWaittime INTEGER,
    PredictedNoShowRate NUMERIC(5, 2),
    PredictedFillRate NUMERIC(5, 2),
    ModelVersion TEXT NOT NULL,
    GeneratedAt TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- INDEXES (Performance Optimization)
-- =====================================================

CREATE INDEX idx_events_business ON Event(BusinessAccountUUID);
CREATE INDEX idx_eventtables_event ON EventTable(EventUUID);
CREATE INDEX idx_parties_event ON Party(EventUUID);
CREATE INDEX idx_notifications_event ON Notifications(EventUUID);
CREATE INDEX idx_notifications_partyleader ON Notifications(PartyLeaderUUID);
CREATE INDEX idx_predictions_event ON Predictions(EventUUID);

-- =====================================================
-- END OF SCHEMA
-- ======================================================