/**
 * SmartTrip AI API Client
 * Typed interfaces and fetch functions for all 10 assignment endpoints.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function fetchSystemStatus() {
  const res = await fetch(`${API_BASE}/api/status`);
  if (!res.ok) throw new Error("Status fetch failed");
  return res.json();
}

export async function fetchPeasDocs() {
  const res = await fetch(`${API_BASE}/api/peas`);
  if (!res.ok) throw new Error("PEAS fetch failed");
  return res.json();
}

export async function evaluateRules(facts: {
  origin: string;
  destination: string;
  budget: number;
  traveler_type: string;
  interests: string[];
  passengers?: number;
}) {
  const res = await fetch(`${API_BASE}/api/rules/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(facts),
  });
  if (!res.ok) throw new Error("Rule evaluation failed");
  return res.json();
}

export async function fetchConcurrencyStatus() {
  const res = await fetch(`${API_BASE}/api/concurrency/status`);
  if (!res.ok) throw new Error("Concurrency status failed");
  return res.json();
}

export async function triggerConcurrencyBatch(count: number = 5) {
  const res = await fetch(`${API_BASE}/api/concurrency/trigger?count=${count}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Concurrency trigger failed");
  return res.json();
}

export async function runSocketExchange(payload?: {
  origin: string;
  destination: string;
  budget: number;
}) {
  const res = await fetch(`${API_BASE}/api/socket/run-exchange`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload || {}),
  });
  if (!res.ok) throw new Error("Socket exchange failed");
  return res.json();
}

export async function runNegotiation(payload: {
  budget: number;
  max_rounds?: number;
  force_overage?: boolean;
}) {
  const res = await fetch(`${API_BASE}/api/negotiation/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      budget: payload.budget,
      max_rounds: payload.max_rounds ?? 3,
      force_overage: payload.force_overage ?? true,
    }),
  });
  if (!res.ok) throw new Error("Negotiation execution failed");
  return res.json();
}

export async function optimizeUtility(payload: { budget: number; destination: string }) {
  const res = await fetch(`${API_BASE}/api/utility/optimize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Utility optimization failed");
  return res.json();
}

export async function runBdiReplanning(payload: { budget: number; shock_type: string }) {
  const res = await fetch(`${API_BASE}/api/bdi/replan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("BDI replanning failed");
  return res.json();
}

export async function fetchKnowledgeDestination(city: string) {
  const res = await fetch(`${API_BASE}/api/knowledge/destination/${encodeURIComponent(city)}`);
  if (!res.ok) throw new Error("Destination knowledge fetch failed");
  return res.json();
}

export async function fetchWeather(city: string) {
  const res = await fetch(`${API_BASE}/api/weather/${encodeURIComponent(city)}`);
  if (!res.ok) throw new Error("Weather fetch failed");
  return res.json();
}

export async function runSecurityAudit() {
  const res = await fetch(`${API_BASE}/api/security/audit`);
  if (!res.ok) throw new Error("Security audit failed");
  return res.json();
}

export async function verifySignedMessage(message: {
  sender_id: string;
  recipient_id: string;
  timestamp: number;
  nonce: string;
  payload: Record<string, unknown>;
  signature: string;
}) {
  const res = await fetch(`${API_BASE}/api/security/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(message),
  });
  if (!res.ok) throw new Error("Message verification failed");
  return res.json();
}

export async function runCapstoneDemo(payload?: {
  origin?: string;
  destination?: string;
  budget?: number;
  traveler_type?: string;
  interests?: string[];
}) {
  const res = await fetch(`${API_BASE}/api/demo/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload || {}),
  });
  if (!res.ok) throw new Error("Capstone execution failed");
  return res.json();
}

export async function fetchDemoHistory() {
  const res = await fetch(`${API_BASE}/api/demo/history`);
  if (!res.ok) throw new Error("Demo history fetch failed");
  return res.json();
}
