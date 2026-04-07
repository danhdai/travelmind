"use client";

import { useEffect, useState } from "react";
import { API_BASE } from "@/lib/config";

interface Stats {
  overview: {
    waitlist: number;
    users: number;
    itineraries: number;
    reviews: number;
    places: number;
  };
  recent_waitlist: Array<{ email: string; name: string; date: string }>;
  top_destinations: Array<{ destination: string; count: number }>;
  review_stats: Array<{ place: string; reviews: number; avg_rating: number; avg_trust: number }>;
}

export default function AdminPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/admin/stats`)
      .then((r) => r.json())
      .then(setStats)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <div className="animate-spin h-8 w-8 border-4 border-sky-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!stats) return <div className="text-center py-32 text-gray-500">Không thể tải dữ liệu</div>;

  const cards = [
    { label: "Waitlist", value: stats.overview.waitlist, color: "bg-sky-500", icon: "📧" },
    { label: "Users", value: stats.overview.users, color: "bg-green-500", icon: "👤" },
    { label: "Lịch trình", value: stats.overview.itineraries, color: "bg-orange-500", icon: "🗺" },
    { label: "Reviews", value: stats.overview.reviews, color: "bg-purple-500", icon: "⭐" },
    { label: "Địa điểm", value: stats.overview.places, color: "bg-pink-500", icon: "📍" },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
        <p className="text-sm text-gray-500">TravelMind — Tổng quan hệ thống</p>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
        {cards.map((card) => (
          <div key={card.label} className="bg-white rounded-xl border border-gray-100 p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">{card.icon}</span>
              <span className={`w-2 h-2 rounded-full ${card.color}`} />
            </div>
            <div className="text-2xl font-bold">{card.value}</div>
            <div className="text-xs text-gray-500">{card.label}</div>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Recent waitlist */}
        <div className="bg-white rounded-xl border border-gray-100 p-5">
          <h2 className="font-semibold mb-4">Waitlist gần đây</h2>
          {stats.recent_waitlist.length === 0 ? (
            <p className="text-sm text-gray-400">Chưa có đăng ký</p>
          ) : (
            <div className="space-y-3">
              {stats.recent_waitlist.map((w, i) => (
                <div key={i} className="flex items-center justify-between text-sm">
                  <div>
                    <span className="font-medium">{w.email}</span>
                    {w.name && <span className="text-gray-400 ml-2">({w.name})</span>}
                  </div>
                  <span className="text-xs text-gray-400">
                    {w.date ? new Date(w.date).toLocaleDateString("vi") : ""}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Top destinations */}
        <div className="bg-white rounded-xl border border-gray-100 p-5">
          <h2 className="font-semibold mb-4">Top điểm đến</h2>
          {stats.top_destinations.length === 0 ? (
            <p className="text-sm text-gray-400">Chưa có lịch trình</p>
          ) : (
            <div className="space-y-3">
              {stats.top_destinations.map((d, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 bg-sky-100 text-sky-600 rounded-full flex items-center justify-center text-xs font-bold">
                      {i + 1}
                    </span>
                    <span className="font-medium text-sm">{d.destination}</span>
                  </div>
                  <span className="text-sm text-gray-500">{d.count} lịch trình</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Review stats */}
        <div className="bg-white rounded-xl border border-gray-100 p-5 md:col-span-2">
          <h2 className="font-semibold mb-4">Review theo địa điểm</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="pb-2 font-medium">Địa điểm</th>
                  <th className="pb-2 font-medium text-center">Reviews</th>
                  <th className="pb-2 font-medium text-center">Rating TB</th>
                  <th className="pb-2 font-medium text-center">Trust Score</th>
                </tr>
              </thead>
              <tbody>
                {stats.review_stats.map((r, i) => (
                  <tr key={i} className="border-b border-gray-50">
                    <td className="py-2.5 font-medium">{r.place}</td>
                    <td className="py-2.5 text-center">{r.reviews}</td>
                    <td className="py-2.5 text-center">
                      <span className="text-yellow-500">★</span> {r.avg_rating}
                    </td>
                    <td className="py-2.5 text-center">
                      <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${
                        r.avg_trust >= 0.8 ? "bg-green-100 text-green-700" :
                        r.avg_trust >= 0.6 ? "bg-yellow-100 text-yellow-700" :
                        "bg-red-100 text-red-700"
                      }`}>
                        {Math.round(r.avg_trust * 100)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
