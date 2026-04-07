"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { API_BASE } from "@/lib/config";

interface ItinerarySummary {
  id: number;
  destination: string;
  num_days: number;
  budget: number | null;
  summary: string;
  total_cost: number | null;
  created_at: string;
}

interface DashboardData {
  created: ItinerarySummary[];
  saved: ItinerarySummary[];
}

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"created" | "saved">("created");

  useEffect(() => {
    if (authLoading) return;
    if (!user) { router.push("/login"); return; }

    fetch(`${API_BASE}/api/auth/my-itineraries`, {
      headers: { Authorization: `Bearer ${user.token}` },
    })
      .then((r) => r.json())
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user, authLoading, router]);

  if (authLoading || !user) return null;

  const items = tab === "created" ? data?.created : data?.saved;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Profile header */}
      <div className="flex items-center gap-4 mb-8">
        <div className="w-16 h-16 bg-sky-100 text-sky-600 rounded-full flex items-center justify-center text-2xl font-bold">
          {(user.name || user.email)[0].toUpperCase()}
        </div>
        <div>
          <h1 className="text-2xl font-bold">{user.name || "Traveler"}</h1>
          <p className="text-sm text-gray-500">{user.email}</p>
        </div>
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-3 gap-3 mb-8">
        <Link href="/itinerary" className="p-4 bg-sky-50 rounded-xl text-center hover:bg-sky-100 transition">
          <div className="text-2xl mb-1">🗺</div>
          <div className="text-xs font-medium text-sky-700">Tạo lịch trình</div>
        </Link>
        <Link href="/profile" className="p-4 bg-purple-50 rounded-xl text-center hover:bg-purple-100 transition">
          <div className="text-2xl mb-1">🧬</div>
          <div className="text-xs font-medium text-purple-700">Travel DNA</div>
        </Link>
        <Link href="/chat" className="p-4 bg-orange-50 rounded-xl text-center hover:bg-orange-100 transition">
          <div className="text-2xl mb-1">💬</div>
          <div className="text-xs font-medium text-orange-700">AI Concierge</div>
        </Link>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-gray-100 rounded-lg p-1 mb-6">
        {(["created", "saved"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`flex-1 py-2 rounded-md text-sm font-medium transition ${
              tab === t ? "bg-white shadow text-gray-900" : "text-gray-500"
            }`}
          >
            {t === "created" ? `Đã tạo (${data?.created.length || 0})` : `Đã lưu (${data?.saved.length || 0})`}
          </button>
        ))}
      </div>

      {/* List */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => <div key={i} className="animate-pulse bg-gray-100 h-24 rounded-xl" />)}
        </div>
      ) : !items || items.length === 0 ? (
        <div className="text-center py-16">
          <div className="text-4xl mb-3">{tab === "created" ? "🗺" : "⭐"}</div>
          <p className="text-gray-500 mb-4">
            {tab === "created" ? "Chưa có lịch trình nào" : "Chưa lưu lịch trình nào"}
          </p>
          <Link href="/itinerary" className="text-sky-600 font-medium hover:underline">
            Tạo lịch trình đầu tiên →
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {items.map((it) => (
            <Link
              key={it.id}
              href={`/itinerary/${it.id}`}
              className="block p-5 border border-gray-100 rounded-xl hover:border-sky-200 hover:shadow-md transition"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold">
                  {it.destination} — {it.num_days} ngày
                </h3>
                {it.total_cost && (
                  <span className="text-sm text-sky-600 font-medium">
                    {it.total_cost.toLocaleString()} VND
                  </span>
                )}
              </div>
              <p className="text-sm text-gray-500 line-clamp-1">{it.summary}</p>
              <div className="text-xs text-gray-400 mt-2">
                {new Date(it.created_at).toLocaleDateString("vi")}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
