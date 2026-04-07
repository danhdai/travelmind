"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import ReviewSummary from "@/components/ReviewSummary";
import { API_BASE } from "@/lib/config";

interface Place {
  place_id: string;
  place_name: string;
  review_count: number;
  avg_rating: number;
  avg_trust_score: number;
}

export default function ReviewsPage() {
  const [places, setPlaces] = useState<Place[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/reviews/places/all`)
      .then((r) => r.json())
      .then((d) => setPlaces(d.places || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <div className="text-4xl mb-3">🔍</div>
        <h1 className="text-3xl font-bold mb-2">Review Explorer</h1>
        <p className="text-gray-500">
          Review thật từ người đi thật — Quảng Bình
        </p>
      </div>

      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse bg-gray-100 h-24 rounded-xl" />
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          {places.map((place) => (
            <div key={place.place_id}>
              <button
                onClick={() => setSelected(selected === place.place_id ? null : place.place_id)}
                className="w-full p-5 rounded-xl border border-gray-200 hover:border-sky-300 hover:shadow-md transition text-left"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-lg">{place.place_name}</h3>
                    <div className="flex items-center gap-4 mt-1 text-sm text-gray-500">
                      <span className="text-yellow-500">★ {place.avg_rating}</span>
                      <span>{place.review_count} reviews</span>
                      <span className="flex items-center gap-1">
                        <span className={`w-2 h-2 rounded-full ${place.avg_trust_score >= 0.8 ? "bg-green-500" : place.avg_trust_score >= 0.6 ? "bg-yellow-500" : "bg-red-500"}`} />
                        Trust: {Math.round(place.avg_trust_score * 100)}%
                      </span>
                    </div>
                  </div>
                  <svg
                    className={`w-5 h-5 text-gray-400 transition ${selected === place.place_id ? "rotate-180" : ""}`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </button>

              {selected === place.place_id && (
                <div className="mt-2 ml-4 space-y-3">
                  <ReviewSummary placeId={place.place_id} />
                  <Link
                    href={`/reviews/${place.place_id}`}
                    className="inline-block text-sm text-sky-600 hover:underline"
                  >
                    Xem tất cả reviews →
                  </Link>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
