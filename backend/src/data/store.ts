import { nanoid } from 'nanoid';
import type { AccessSession, BusinessModel, EventModel, RefreshSession, UserModel, WaitlistEntry } from '../types/contracts.js';
import { hashPassword } from '../lib/security.js';
import { calculateHeuristicWait } from '../lib/models.js'; 

const makeTables = (totalTables = 12) => {
  const cols = 4;
  return Array.from({ length: totalTables }).map((_, index) => ({
    id: index + 1,
    row: Math.floor(index / cols),
    col: index % cols,
    name: `Table ${index + 1}`,
    capacity: [2, 2, 4, 4, 2, 4, 6, 6, 4, 4, 6, 8][index] ?? 4,
    occupied: false,
  }));
};

const now = new Date();
const demoBusinessId = 'biz-demo';

const demoBusiness: BusinessModel = {
  id: demoBusinessId,
  name: 'Figma Demo Restaurant',
  ownerId: 'staff-demo',
};

const demoStaffUser: UserModel = {
  id: 'staff-demo',
  email: 'admin@demo.com',
  name: 'Demo Manager',
  role: 'staff',
  businessId: demoBusiness.id,
};

const demoAttendeeUser: UserModel = {
  id: 'user-demo',
  email: 'guest@demo.com',
  name: 'Demo Guest',
  role: 'user',
};

const demoEvent: EventModel = {
  id: 'demo-event',
  businessId: demoBusinessId,
  name: 'Figma Demo Restaurant',
  type: 'table-based',
  status: 'active',
  createdAt: now.toISOString(),
  numberOfTables: 12,
  averageTableSize: 4,
  reservationDuration: 90,
  noShowPolicy: 'Hold table for 15 minutes',
  currentFilledTables: 1,
  tables: makeTables(12),
  avgServiceTime: 5,           
  historicalNoShowRate: 0.15,   
  startTime: now.toISOString(),
  waitlist: [
    {
      id: nanoid(),
      eventId: 'demo-event',
      name: 'Sarah Johnson',
      partySize: 4,
      type: 'waitlist',
      status: 'QUEUED',
      position: 1,
      estimatedWait: 20,
      joinedAt: new Date(now.getTime() - 15 * 60 * 1000).toISOString(),
      createdByUserId: demoAttendeeUser.id,
      interactionCount: 0,      
      lastActiveTime: now.toISOString(), 
      isHighRisk: false,        
    },
  ],
};

demoEvent.tables[0].occupied = true;
demoEvent.tables[0].guestName = 'Michael Chen';
demoEvent.tables[0].partySize = 2;
demoEvent.tables[0].seatedAt = new Date(now.getTime() - 12 * 60 * 1000).toISOString();

export const db = {
  events: new Map<string, EventModel>([[demoEvent.id, demoEvent]]),
  users: new Map<string, UserModel>([
    [demoStaffUser.id, demoStaffUser],
    [demoAttendeeUser.id, demoAttendeeUser],
  ]),
  usersByEmail: new Map<string, string>([
    [demoStaffUser.email.toLowerCase(), demoStaffUser.id],
    [demoAttendeeUser.email.toLowerCase(), demoAttendeeUser.id],
  ]),
  passwordHashes: new Map<string, string>(),
  businesses: new Map<string, BusinessModel>([[demoBusiness.id, demoBusiness]]),
  accessTokens: new Map<string, AccessSession>(),
  refreshTokens: new Map<string, RefreshSession>(),
};

export async function seedStore() {
  if (!db.passwordHashes.size) {
    db.passwordHashes.set(demoStaffUser.id, await hashPassword('password123'));
    db.passwordHashes.set(demoAttendeeUser.id, await hashPassword('password123'));
  }
}

export function recalcQueuePositions(eventId: string) {
  const event = db.events.get(eventId);
  if (!event) {
    console.log(`[RECALC] Error: Event ${eventId} not found`);
    return;
  }

  const totalPredictedWait = calculateHeuristicWait(event);
  const queuedEntries = event.waitlist.filter(e => e.status === 'QUEUED');
  const totalInQueue = queuedEntries.length || 1;

  event.waitlist = event.waitlist.map((entry) => {
    if (entry.status !== 'QUEUED') return entry;

    const relativePos = queuedEntries.findIndex(e => e.id === entry.id) + 1;
    const calculatedWait = Math.ceil((totalPredictedWait / totalInQueue) * relativePos);
    
    return {
      ...entry,
      position: relativePos,
      estimatedWait: Math.max(5, calculatedWait), 
    };
  });
}

setInterval(() => {
  db.events.forEach((event, eventId) => {
    if (event.status === 'active') {
      recalcQueuePositions(eventId);
    }
  });
}, 60000);

export function addWaitlistEntry(
  eventId: string,
  payload: Pick<WaitlistEntry, 'name' | 'partySize' | 'type' | 'specialRequests' | 'createdByUserId'>,
) {
  const event = db.events.get(eventId);
  if (!event) return null;

  const entry: WaitlistEntry = {
    id: nanoid(),
    eventId,
    name: payload.name,
    partySize: payload.partySize,
    type: payload.type,
    status: 'QUEUED',
    position: event.waitlist.length + 1,
    estimatedWait: 5, 
    specialRequests: payload.specialRequests,
    joinedAt: new Date().toISOString(),
    createdByUserId: payload.createdByUserId,
    interactionCount: 0,
    lastActiveTime: new Date().toISOString(),
    isHighRisk: false,
  };

  event.waitlist.push(entry);

  if (event.type === 'capacity-based') {
    event.currentCount += payload.partySize;
  }

  recalcQueuePositions(eventId);
  const updatedEntry = event.waitlist.find(e => e.id === entry.id);
  
  return updatedEntry || entry;
}
