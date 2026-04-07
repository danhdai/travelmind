"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { getItinerary } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import ReviewSummary from "@/components/ReviewSummary";
import BookingButtons from "@/components/BookingButtons";
import dynamic from "next/dynamic";
import { API_BASE } from "@/lib/config";

const ItineraryMap = dynamic(() => import("@/components/ItineraryMap"), { ssr: false });

interface Activity {
  time: string;
  activity: string;
  place: string;
  description: string;
  cost_estimate: number;
  tips?: string;
}

interface Meal {
  type: string;
  restaurant: string;
  cuisine: string;
  cost_estimate: number;
}

interface Day {
  day: number;
  title: string;
  activities: Activity[];
  meals: Meal[];
  accommodation: { name: string; type: string; cost_estimate: number };
  day_cost: number;
}

interface ItineraryData {
  destination: string;
  num_days: number;
  summary: string;
  days: Day[];
  total_cost: number;
  budget_breakdown: Record<string, number>;
  tips: string[];
}

export default function ItineraryDetailPage() {
  const params = useParams();
  const { user } = useAuth();
  const [data, setData] = useState<ItineraryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saved, setSaved] = useState(false);

  const itineraryId = Number(params.id);

  useEffect(() => {
    if (!itineraryId) return;
    getItinerary(itineraryId)
      .then((res) => setData(res.itinerary_data as unknown as ItineraryData))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [itineraryId]);

  const toggleSave = useCallback(async () => {
    if (!user) { alert("Đăng nhập để lưu lịch trình"); return; }
    const method = saved ? "DELETE" : "POST";
    await fetch(`${API_BASE}/api/auth/save-itinerary/${itineraryId}`, {
      method,
      headers: { Authorization: `Bearer ${user.token}` },
    });
    setSaved(!saved);
  }, [user, saved, itineraryId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <svg className="animate-spin h-8 w-8 text-sky-600" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-32">
        <p className="text-gray-500">Khong tim thay lich trinh</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header + Share */}
      <div className="mb-8">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold mb-2">
              Lịch trình {data.destination} — {data.num_days} ngày
            </h1>
            <p className="text-gray-600">{data.summary}</p>
          </div>
          <div className="flex gap-2 flex-shrink-0">
            <button
              onClick={toggleSave}
              className={`px-3 py-2 text-xs border rounded-lg transition flex items-center gap-1 ${
                saved ? "border-yellow-400 bg-yellow-50 text-yellow-700" : "border-gray-200 hover:bg-gray-50"
              }`}
            >
              {saved ? "★ Đã lưu" : "☆ Lưu"}
            </button>
            <button
              onClick={() => {
                navigator.clipboard.writeText(window.location.href);
                alert("Đã copy link!");
              }}
              className="px-3 py-2 text-xs border border-gray-200 rounded-lg hover:bg-gray-50 transition flex items-center gap-1"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
              </svg>
              Chia sẻ
            </button>
            <button
              onClick={() => window.print()}
              className="px-3 py-2 text-xs border border-gray-200 rounded-lg hover:bg-gray-50 transition flex items-center gap-1"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              In/PDF
            </button>
          </div>
        </div>
      </div>

      {/* Budget Breakdown */}
      <div className="bg-sky-50 rounded-2xl p-6 mb-8">
        <h2 className="font-semibold mb-3">Tong chi phi: {data.total_cost?.toLocaleString()} VND</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {data.budget_breakdown && Object.entries(data.budget_breakdown).map(([key, val]) => (
            <div key={key} className="text-center">
              <div className="text-sm text-gray-500 capitalize">{key}</div>
              <div className="font-semibold">{val.toLocaleString()} VND</div>
            </div>
          ))}
        </div>
      </div>

      {/* Map */}
      <div className="mb-8">
        <h2 className="font-semibold mb-3">Bản đồ lịch trình</h2>
        <ItineraryMap
          destination={data.destination}
          places={
            data.days?.flatMap((day) =>
              day.activities?.map((act) => ({
                name: act.place,
                day: day.day,
                time: act.time,
                activity: act.activity,
                description: act.description,
              })) || []
            ) || []
          }
        />
      </div>

      {/* Day by day */}
      <div className="space-y-8">
        {data.days?.map((day) => (
          <div key={day.day} className="border border-gray-100 rounded-2xl overflow-hidden">
            <div className="bg-sky-600 text-white px-6 py-4">
              <h3 className="text-xl font-bold">{day.title}</h3>
              <p className="text-sky-100 text-sm">Chi phi ngay: ~{day.day_cost?.toLocaleString()} VND</p>
            </div>

            <div className="p-6 space-y-4">
              {/* Activities */}
              <div>
                <h4 className="font-semibold text-gray-700 mb-3">Hoat dong</h4>
                <div className="space-y-3">
                  {day.activities?.map((act, i) => (
                    <div key={i} className="flex gap-4 p-3 bg-gray-50 rounded-xl">
                      <div className="text-sky-600 font-mono font-bold text-sm whitespace-nowrap pt-0.5">
                        {act.time}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium">{act.activity}</div>
                        <div className="text-sm text-gray-500">{act.place}</div>
                        <div className="text-sm text-gray-600 mt-1">{act.description}</div>
                        {act.tips && (
                          <div className="text-xs text-orange-600 mt-1">Tip: {act.tips}</div>
                        )}
                        <div className="text-xs text-gray-400 mt-1">
                          ~{act.cost_estimate?.toLocaleString()} VND
                        </div>
                        <BookingButtons type="tour" placeName={act.place} destination={data.destination} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Meals */}
              <div>
                <h4 className="font-semibold text-gray-700 mb-3">An uong</h4>
                <div className="grid grid-cols-3 gap-3">
                  {day.meals?.map((meal, i) => (
                    <div key={i} className="p-3 bg-orange-50 rounded-xl text-center">
                      <div className="text-xs text-orange-600 font-medium uppercase">{meal.type}</div>
                      <div className="text-sm font-medium mt-1">{meal.restaurant}</div>
                      <div className="text-xs text-gray-500">{meal.cuisine}</div>
                      <div className="text-xs text-gray-400 mt-1">~{meal.cost_estimate?.toLocaleString()} VND</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Accommodation */}
              {day.accommodation && (
                <div className="p-3 bg-purple-50 rounded-xl">
                  <div>
                    <span className="text-xs text-purple-600 font-medium">Chỗ ở: </span>
                    <span className="text-sm font-medium">{day.accommodation.name}</span>
                    <span className="text-xs text-gray-500 ml-2">
                      ({day.accommodation.type}) ~{day.accommodation.cost_estimate?.toLocaleString()} VND
                    </span>
                  </div>
                  <BookingButtons type="hotel" placeName={day.accommodation.name} destination={data.destination} />
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Reviews for key places */}
      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4">Reviews dia diem</h3>
        <div className="space-y-3">
          <ReviewSummary placeId="phong_nha_cave" />
          <ReviewSummary placeId="paradise_cave" />
          <ReviewSummary placeId="dark_cave" />
          <ReviewSummary placeId="suoi_mooc" />
          <ReviewSummary placeId="nhat_le_beach" />
        </div>
      </div>

      {/* Tips */}
      {data.tips && data.tips.length > 0 && (
        <div className="mt-8 bg-yellow-50 rounded-2xl p-6">
          <h3 className="font-semibold mb-3">Meo hay</h3>
          <ul className="space-y-1">
            {data.tips.map((tip, i) => (
              <li key={i} className="text-sm text-gray-700">• {tip}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
