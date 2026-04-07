"use client";

import { useEffect, useState } from "react";
import { API_BASE } from "@/lib/config";

interface ReviewSummaryData {
  place_id: string;
  place_name: string;
  summary: string;
  highlights: string[];
  concerns: string[];
  best_time: string | null;
  avg_sentiment: number;
  avg_rating: number;
  top_activities: string[];
  price_range: { min: number; max: number } | null;
  total_reviews: number;
}

export default function ReviewSummary({ placeId }: { placeId: string }) {
  const [data, setData] = useState<ReviewSummaryData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/reviews/${placeId}/summary`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [placeId]);

  if (loading) return <div className="animate-pulse bg-gray-100 h-32 rounded-xl" />;
  if (!data || data.total_reviews === 0) return null;

  const sentimentColor =
    data.avg_sentiment >= 0.65
      ? "text-green-600 bg-green-50"
      : data.avg_sentiment >= 0.4
        ? "text-yellow-600 bg-yellow-50"
        : "text-red-600 bg-red-50";

  return (
    <div className="border border-gray-100 rounded-xl p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="font-semibold text-sm">{data.place_name}</h4>
        <div className="flex items-center gap-2">
          <span className="text-yellow-500 text-sm">★ {data.avg_rating}</span>
          <span className="text-xs text-gray-400">({data.total_reviews} reviews)</span>
        </div>
      </div>

      <p className="text-sm text-gray-600">{data.summary}</p>

      <div className="flex flex-wrap gap-2">
        {data.highlights.map((h) => (
          <span key={h} className="text-xs px-2 py-1 bg-green-50 text-green-700 rounded-full">
            {h}
          </span>
        ))}
        {data.concerns.map((c) => (
          <span key={c} className="text-xs px-2 py-1 bg-red-50 text-red-600 rounded-full">
            {c}
          </span>
        ))}
      </div>

      {data.top_activities.length > 0 && (
        <div className="text-xs text-gray-500">
          Hoạt động: {data.top_activities.join(", ")}
        </div>
      )}

      <div className="flex items-center gap-3 text-xs">
        <span className={`px-2 py-0.5 rounded-full ${sentimentColor}`}>
          Sentiment: {Math.round(data.avg_sentiment * 100)}%
        </span>
        {data.price_range && (
          <span className="text-gray-500">
            Giá: {data.price_range.min.toLocaleString()}-{data.price_range.max.toLocaleString()} VND
          </span>
        )}
        {data.best_time && (
          <span className="text-gray-500">Thời điểm: {data.best_time}</span>
        )}
      </div>
    </div>
  );
}
