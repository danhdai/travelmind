"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import ReviewSummary from "@/components/ReviewSummary";
import SubmitReview from "@/components/SubmitReview";
import { API_BASE } from "@/lib/config";

interface ReviewDetail {
  id: number;
  author: string;
  text: string;
  rating: number;
  trust_score: number;
  trust_breakdown: Record<string, number>;
  sentiment: { score: number; label: string; positive_words: string[]; negative_words: string[] };
  fake_check: { is_suspicious: boolean; reasons: string[]; fake_probability: number };
  entities: { places: string[]; prices: Array<{ amount: number; raw: string }>; activities: Array<{ vietnamese: string; type: string }> };
}

interface AnalysisData {
  place_id: string;
  place_name: string;
  total_analyzed: number;
  analysis: ReviewDetail[];
}

export default function PlaceReviewsPage() {
  const params = useParams();
  const placeId = params.placeId as string;
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!placeId) return;
    fetch(`${API_BASE}/api/reviews/${placeId}/analyze`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [placeId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <div className="animate-spin h-8 w-8 border-4 border-sky-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!data) return <div className="text-center py-32 text-gray-500">Khong tim thay</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">{data.place_name}</h1>
      <p className="text-gray-500 mb-6">{data.total_analyzed} reviews - NLP Analysis</p>

      <div className="mb-6">
        <ReviewSummary placeId={placeId} />
      </div>

      <div className="mb-8">
        <SubmitReview
          placeId={placeId}
          placeName={data.place_name}
          onSubmitted={() => window.location.reload()}
        />
      </div>

      <h2 className="font-semibold text-lg mb-4">Chi tiet reviews</h2>
      <div className="space-y-4">
        {data.analysis.map((rev) => (
          <div
            key={rev.id}
            className={`p-5 rounded-xl border ${rev.fake_check.is_suspicious ? "border-red-200 bg-red-50/30" : "border-gray-100"}`}
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-sky-100 text-sky-600 rounded-full flex items-center justify-center text-sm font-bold">
                  {(rev.author || "?")[0]}
                </div>
                <div>
                  <span className="font-medium text-sm">{rev.author}</span>
                  <div className="flex items-center gap-2 text-xs text-gray-400">
                    <span className="text-yellow-500">{"★".repeat(Math.round(rev.rating))}</span>
                    <span>{rev.rating}/5</span>
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-gray-500">Trust Score</div>
                <div className={`text-sm font-bold ${rev.trust_score >= 0.7 ? "text-green-600" : rev.trust_score >= 0.5 ? "text-yellow-600" : "text-red-600"}`}>
                  {Math.round(rev.trust_score * 100)}%
                </div>
              </div>
            </div>

            <p className="text-sm text-gray-700 mb-3">{rev.text}</p>

            {/* Sentiment */}
            <div className="flex flex-wrap gap-1.5 mb-2">
              {rev.sentiment.positive_words.map((w) => (
                <span key={w} className="text-[10px] px-1.5 py-0.5 bg-green-50 text-green-700 rounded">+{w}</span>
              ))}
              {rev.sentiment.negative_words.map((w) => (
                <span key={w} className="text-[10px] px-1.5 py-0.5 bg-red-50 text-red-600 rounded">-{w}</span>
              ))}
            </div>

            {/* Entities */}
            {rev.entities.prices.length > 0 && (
              <div className="text-[10px] text-gray-500">
                Gia: {rev.entities.prices.map((p) => p.raw).join(", ")}
              </div>
            )}

            {/* Trust breakdown bar */}
            <div className="mt-2 flex gap-0.5 h-1.5 rounded overflow-hidden">
              {Object.entries(rev.trust_breakdown).map(([key, val]) => {
                const colors: Record<string, string> = {
                  content_depth: "bg-blue-400",
                  sentiment_coherence: "bg-green-400",
                  authenticity: "bg-purple-400",
                  photo_evidence: "bg-yellow-400",
                  consistency: "bg-pink-400",
                };
                return (
                  <div
                    key={key}
                    className={`${colors[key] || "bg-gray-300"}`}
                    style={{ width: `${val * 100}%` }}
                    title={`${key}: ${Math.round(val * 100)}%`}
                  />
                );
              })}
            </div>

            {/* Fake warning */}
            {rev.fake_check.is_suspicious && (
              <div className="mt-2 text-xs text-red-600 flex items-center gap-1">
                <span>⚠</span>
                {rev.fake_check.reasons.join(", ")}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
