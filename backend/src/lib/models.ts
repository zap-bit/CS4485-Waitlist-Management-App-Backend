import { WaitlistEntry, EventModel } from '../types/contracts.js';

export function getRealTimeNoShowRate(event: EventModel): number {
  const finished = event.waitlist.filter(e => 
    e.status === 'SEATED' || e.status === 'NO_SHOW'
  );
  
  if (finished.length < 5) {
    return event.historicalNoShowRate || 0.15; 
  }

  const noShows = finished.filter(e => e.status === 'NO_SHOW').length;
  return noShows / finished.length;
}

export function getUserWeight(entry: WaitlistEntry): number {
  const now = new Date().getTime();
  const lastActive = new Date(entry.lastActiveTime).getTime();
  const minutesStale = (now - lastActive) / 60000;
  const gracePeriod = Math.max(20, Math.min(90, (entry.estimatedWait || 30) * 0.5));
  let weight = 1.0;
  
  if (minutesStale <= gracePeriod) {
    weight = 1.0;
  } else if (minutesStale >= (gracePeriod + 20)) {
    weight = 0.1;
  } else {
    weight = 1.0 - (0.9 * (minutesStale - gracePeriod) / 20);
  }

  if (entry.interactionCount > 5) {
    weight = Math.min(1.0, weight + 0.1);
  }

  return parseFloat(weight.toFixed(2));
}

export function calculateHeuristicWait(event: EventModel): number {
  const queue = event.waitlist.filter(e => e.status === 'QUEUED');
  
  if (queue.length === 0) return 0;

  const weightedCount = queue.reduce((sum, e) => sum + getUserWeight(e), 0);
  const noShowRate = Math.min(0.8, getRealTimeNoShowRate(event));
  const adjustedCount = weightedCount * (1 - noShowRate);
  const serviceTime = event.avgServiceTime || 10;
  const rawWait = Math.ceil(adjustedCount * serviceTime);
  
  return Math.max(serviceTime, rawWait); 
}

export function updateUserActivity(entry: WaitlistEntry): void {
  entry.interactionCount += 1;
  entry.lastActiveTime = new Date().toISOString();
  entry.isHighRisk = false; 
}

export function refreshServiceTime(event: EventModel): void {
  const seatedEntries = event.waitlist.filter(e => e.status === 'SEATED');
  
  if (seatedEntries.length === 0) return;

  const startTime = new Date(event.startTime).getTime();
  const now = new Date().getTime();
  const elapsedMinutes = (now - startTime) / 60000;

  if (elapsedMinutes < 1) return;

  const newAvg = elapsedMinutes / seatedEntries.length;

  event.avgServiceTime = Math.max(2, Math.min(60, Math.round(newAvg * 10) / 10));
}

export function markNoShow(entry: WaitlistEntry): void {
  const validTransitions = new Set(['QUEUED', 'NOTIFIED']);
  
  if (!validTransitions.has(entry.status)) {
    throw new Error(`Invalid Status: Cannot mark ${entry.status} as NO_SHOW`);
  }

  entry.status = 'NO_SHOW';
}