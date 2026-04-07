"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { useToast } from "@/lib/toast";
import Link from "next/link";
import { API_BASE } from "@/lib/config";

interface Place {
  id: string;
  name: string;
  icon: string;
  votes: number;
  voters: string[];
}

interface GroupData {
  id: number;
  code: string;
  name: string;
  destination: string;
  num_days: number;
  owner: string;
  members: Array<{ email: string; name: string }>;
  member_count: number;
  places: Place[];
  status: string;
}

export default function GroupPage() {
  const params = useParams();
  const code = params.code as string;
  const { user } = useAuth();
  const { toast } = useToast();
  const [data, setData] = useState<GroupData | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchGroup = useCallback(() => {
    fetch(`${API_BASE}/api/group/${code}`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [code]);

  useEffect(() => { fetchGroup(); }, [fetchGroup]);

  async function handleVote(placeId: string) {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (user) headers.Authorization = `Bearer ${user.token}`;

    await fetch(`${API_BASE}/api/group/${code}/vote`, {
      method: "POST",
      headers,
      body: JSON.stringify({ place_id: placeId }),
    });
    toast("Vote cập nhật!", "success");
    fetchGroup();
  }

  async function handleJoin() {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (user) headers.Authorization = `Bearer ${user.token}`;

    await fetch(`${API_BASE}/api/group/${code}/join`, {
      method: "POST",
      headers,
      body: JSON.stringify({ name: user?.name || user?.email?.split("@")[0] }),
    });
    toast("Đã tham gia group!", "success");
    fetchGroup();
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <div className="animate-spin h-8 w-8 border-4 border-sky-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!data) return <div className="text-center py-32 text-gray-500">Group không tồn tại</div>;

  const maxVotes = Math.max(...data.places.map((p) => p.votes), 1);
  const userEmail = user?.email || "";
  const isMember = data.members.some((m) => m.email === userEmail);

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="text-4xl mb-2">👥</div>
        <h1 className="text-2xl font-bold">{data.name}</h1>
        <p className="text-gray-500">
          {data.destination} — {data.num_days} ngày • {data.member_count} thành viên
        </p>
        <div className="flex justify-center gap-2 mt-3">
          <button
            onClick={() => { navigator.clipboard.writeText(window.location.href); toast("Đã copy link!", "success"); }}
            className="text-xs px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            📋 Copy link mời
          </button>
          {!isMember && (
            <button onClick={handleJoin} className="text-xs px-3 py-1.5 bg-sky-600 text-white rounded-lg hover:bg-sky-700">
              Tham gia
            </button>
          )}
        </div>
      </div>

      {/* Members */}
      <div className="flex flex-wrap gap-2 justify-center mb-8">
        {data.members.map((m) => (
          <div key={m.email} className="flex items-center gap-1.5 bg-gray-100 rounded-full px-3 py-1.5">
            <div className="w-5 h-5 bg-sky-200 text-sky-700 rounded-full flex items-center justify-center text-[10px] font-bold">
              {m.name[0].toUpperCase()}
            </div>
            <span className="text-xs">{m.name}</span>
          </div>
        ))}
      </div>

      {/* Vote */}
      <h2 className="font-semibold mb-4">Vote địa điểm muốn đi</h2>
      <div className="space-y-3">
        {data.places.map((place) => {
          const voted = place.voters.includes(userEmail);
          const pct = maxVotes > 0 ? (place.votes / maxVotes) * 100 : 0;
          return (
            <button
              key={place.id}
              onClick={() => handleVote(place.id)}
              className={`w-full text-left p-4 rounded-xl border-2 transition relative overflow-hidden ${
                voted ? "border-sky-500 bg-sky-50" : "border-gray-200 hover:border-gray-300"
              }`}
            >
              {/* Vote bar */}
              <div
                className="absolute inset-y-0 left-0 bg-sky-100 transition-all duration-500"
                style={{ width: `${pct}%` }}
              />
              <div className="relative flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{place.icon}</span>
                  <span className="font-medium">{place.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-sky-600">{place.votes}</span>
                  <span className="text-xs text-gray-400">votes</span>
                  {voted && <span className="text-sky-500 text-sm">✓</span>}
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Generate itinerary from votes */}
      <div className="mt-8 text-center">
        <Link
          href={`/itinerary`}
          className="inline-block bg-sky-600 text-white font-medium px-6 py-3 rounded-xl hover:bg-sky-700 transition"
        >
          Tạo lịch trình từ kết quả vote →
        </Link>
      </div>
    </div>
  );
}
