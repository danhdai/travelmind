const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }
  return res.json();
}

export async function joinWaitlist(email: string, name?: string) {
  return fetchAPI("/api/waitlist/", {
    method: "POST",
    body: JSON.stringify({ email, name }),
  });
}

export async function saveTravelDNA(data: {
  email: string;
  name?: string;
  travel_dna: Record<string, unknown>;
}) {
  return fetchAPI("/api/profile/travel-dna", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function generateItinerary(data: {
  destination: string;
  num_days: number;
  budget?: number;
  travel_dna?: Record<string, unknown>;
  email?: string;
}) {
  return fetchAPI<{ id: number; itinerary_data: Record<string, unknown> }>(
    "/api/itinerary/generate",
    { method: "POST", body: JSON.stringify(data) }
  );
}

export async function getItinerary(id: number) {
  return fetchAPI<{ id: number; itinerary_data: Record<string, unknown> }>(
    `/api/itinerary/${id}`
  );
}

export async function getPricing() {
  return fetchAPI<{ tiers: Array<Record<string, unknown>> }>(
    "/api/payment/pricing"
  );
}

export async function getReviews(placeId: string) {
  return fetchAPI(`/api/reviews/${placeId}`);
}
