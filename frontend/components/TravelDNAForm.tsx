"use client";

import { useState } from "react";
import { saveTravelDNA } from "@/lib/api";

const PERSONAS = [
  { id: "phuot", label: "Phượt thủ", icon: "🏔" },
  { id: "nghi_duong", label: "Nghỉ dưỡng", icon: "🏖" },
  { id: "am_thuc", label: "Ẩm thực", icon: "🍜" },
  { id: "van_hoa", label: "Văn hóa", icon: "🏛" },
  { id: "gia_dinh", label: "Gia đình", icon: "👨‍👩‍👧‍👦" },
  { id: "couple", label: "Couple romantic", icon: "💑" },
];

const BUDGETS = [
  { id: "low", label: "Tiết kiệm (<500k/ngày)", icon: "💰" },
  { id: "medium", label: "Trung bình (500k-1tr/ngày)", icon: "💰💰" },
  { id: "high", label: "Thoải mái (1-2tr/ngày)", icon: "💰💰💰" },
  { id: "luxury", label: "Sang chảnh (>2tr/ngày)", icon: "💎" },
];

const ENERGY = [
  { id: "chill", label: "Chill — 1-2 hoạt động/ngày", icon: "😌" },
  { id: "moderate", label: "Vừa phải — 3-4 hoạt động/ngày", icon: "🚶" },
  { id: "compact", label: "Compact — 5+ hoạt động/ngày", icon: "🏃" },
];

const FOODS = [
  { id: "street_food", label: "Street food" },
  { id: "fine_dining", label: "Fine dining" },
  { id: "healthy", label: "Healthy" },
  { id: "vegetarian", label: "Chay" },
  { id: "seafood", label: "Hải sản" },
  { id: "local", label: "Đặc sản địa phương" },
];

const ACCOMMODATIONS = [
  { id: "hostel", label: "Hostel", icon: "🛏" },
  { id: "homestay", label: "Homestay", icon: "🏡" },
  { id: "hotel_3star", label: "Hotel 3*", icon: "🏨" },
  { id: "hotel_4star", label: "Hotel 4-5*", icon: "🌟" },
  { id: "resort", label: "Resort", icon: "🏝" },
];

const DEAL_BREAKERS = [
  { id: "fear_heights", label: "Sợ độ cao" },
  { id: "no_crowds", label: "Không thích đông người" },
  { id: "allergies", label: "Dị ứng thức ăn" },
  { id: "kids", label: "Trẻ nhỏ đi cùng" },
  { id: "elderly", label: "Người già đi cùng" },
  { id: "no_swim", label: "Không biết bơi" },
];

type Step = 1 | 2 | 3 | 4 | 5 | 6;

export default function TravelDNAForm() {
  const [step, setStep] = useState<Step>(1);
  const [email, setEmail] = useState("");
  const [persona, setPersona] = useState("");
  const [budget, setBudget] = useState("");
  const [energy, setEnergy] = useState("");
  const [foods, setFoods] = useState<string[]>([]);
  const [accommodation, setAccommodation] = useState("");
  const [dealBreakers, setDealBreakers] = useState<string[]>([]);
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  function toggleItem(arr: string[], item: string, setter: (v: string[]) => void) {
    setter(arr.includes(item) ? arr.filter((i) => i !== item) : [...arr, item]);
  }

  async function handleSubmit() {
    if (!email) return;
    setStatus("loading");
    try {
      await saveTravelDNA({
        email,
        travel_dna: {
          persona,
          budget_range: budget,
          energy_level: energy,
          food_preferences: foods,
          accommodation_style: accommodation,
          deal_breakers: dealBreakers,
        },
      });
      setStatus("success");
    } catch {
      setStatus("error");
    }
  }

  if (status === "success") {
    return (
      <div className="text-center py-12">
        <div className="text-5xl mb-4">🧬</div>
        <h2 className="text-2xl font-bold mb-2">Travel DNA đã lưu!</h2>
        <p className="text-gray-600 mb-6">AI sẽ dùng profile này để thiết kế lịch trình riêng cho bạn.</p>
        <a href="/itinerary" className="inline-block bg-sky-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-sky-700 transition">
          Tạo lịch trình ngay
        </a>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress */}
      <div className="flex gap-1 mb-8">
        {[1, 2, 3, 4, 5, 6].map((s) => (
          <div key={s} className={`h-1.5 flex-1 rounded-full ${s <= step ? "bg-sky-500" : "bg-gray-200"}`} />
        ))}
      </div>

      {step === 1 && (
        <div>
          <h2 className="text-2xl font-bold mb-2">Bạn là kiểu du lịch nào?</h2>
          <p className="text-gray-500 mb-6">Chọn persona phù hợp nhất với bạn</p>
          <div className="grid grid-cols-2 gap-3">
            {PERSONAS.map((p) => (
              <button key={p.id} onClick={() => setPersona(p.id)}
                className={`p-4 rounded-xl border-2 text-left transition ${persona === p.id ? "border-sky-500 bg-sky-50" : "border-gray-200 hover:border-gray-300"}`}>
                <span className="text-2xl">{p.icon}</span>
                <div className="font-medium mt-1">{p.label}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 2 && (
        <div>
          <h2 className="text-2xl font-bold mb-2">Ngân sách của bạn?</h2>
          <p className="text-gray-500 mb-6">Mức chi tiêu trung bình mỗi ngày</p>
          <div className="grid grid-cols-1 gap-3">
            {BUDGETS.map((b) => (
              <button key={b.id} onClick={() => setBudget(b.id)}
                className={`p-4 rounded-xl border-2 text-left transition ${budget === b.id ? "border-sky-500 bg-sky-50" : "border-gray-200 hover:border-gray-300"}`}>
                <span className="mr-2">{b.icon}</span>
                <span className="font-medium">{b.label}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 3 && (
        <div>
          <h2 className="text-2xl font-bold mb-2">Mức năng lượng?</h2>
          <p className="text-gray-500 mb-6">Lịch trình compact hay chill?</p>
          <div className="grid grid-cols-1 gap-3">
            {ENERGY.map((e) => (
              <button key={e.id} onClick={() => setEnergy(e.id)}
                className={`p-4 rounded-xl border-2 text-left transition ${energy === e.id ? "border-sky-500 bg-sky-50" : "border-gray-200 hover:border-gray-300"}`}>
                <span className="mr-2">{e.icon}</span>
                <span className="font-medium">{e.label}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 4 && (
        <div>
          <h2 className="text-2xl font-bold mb-2">Sở thích ẩm thực?</h2>
          <p className="text-gray-500 mb-6">Chọn nhiều tùy thích</p>
          <div className="grid grid-cols-2 gap-3">
            {FOODS.map((f) => (
              <button key={f.id} onClick={() => toggleItem(foods, f.id, setFoods)}
                className={`p-3 rounded-xl border-2 text-center transition ${foods.includes(f.id) ? "border-sky-500 bg-sky-50" : "border-gray-200 hover:border-gray-300"}`}>
                <span className="font-medium">{f.label}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 5 && (
        <div>
          <h2 className="text-2xl font-bold mb-2">Chỗ ở yêu thích?</h2>
          <p className="text-gray-500 mb-6">Bạn thích ở đâu khi đi du lịch?</p>
          <div className="grid grid-cols-2 gap-3">
            {ACCOMMODATIONS.map((a) => (
              <button key={a.id} onClick={() => setAccommodation(a.id)}
                className={`p-4 rounded-xl border-2 text-left transition ${accommodation === a.id ? "border-sky-500 bg-sky-50" : "border-gray-200 hover:border-gray-300"}`}>
                <span className="text-2xl">{a.icon}</span>
                <div className="font-medium mt-1">{a.label}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 6 && (
        <div>
          <h2 className="text-2xl font-bold mb-2">Deal breakers?</h2>
          <p className="text-gray-500 mb-6">Có điều gì cần tránh không? (tùy chọn)</p>
          <div className="grid grid-cols-2 gap-3 mb-6">
            {DEAL_BREAKERS.map((d) => (
              <button key={d.id} onClick={() => toggleItem(dealBreakers, d.id, setDealBreakers)}
                className={`p-3 rounded-xl border-2 text-center transition ${dealBreakers.includes(d.id) ? "border-red-400 bg-red-50" : "border-gray-200 hover:border-gray-300"}`}>
                <span className="font-medium">{d.label}</span>
              </button>
            ))}
          </div>
          <div className="mt-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Email của bạn</label>
            <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
              placeholder="email@example.com"
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-sky-500 focus:ring-2 focus:ring-sky-200 outline-none" />
          </div>
        </div>
      )}

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        <button onClick={() => setStep((s) => Math.max(1, s - 1) as Step)} disabled={step === 1}
          className="px-6 py-3 rounded-lg border border-gray-300 font-medium disabled:opacity-30 hover:bg-gray-50 transition">
          Quay lại
        </button>
        {step < 6 ? (
          <button onClick={() => setStep((s) => Math.min(6, s + 1) as Step)}
            className="px-6 py-3 rounded-lg bg-sky-600 text-white font-medium hover:bg-sky-700 transition">
            Tiếp theo
          </button>
        ) : (
          <button onClick={handleSubmit} disabled={!email || status === "loading"}
            className="px-6 py-3 rounded-lg bg-orange-500 text-white font-medium hover:bg-orange-600 disabled:opacity-50 transition">
            {status === "loading" ? "Đang lưu..." : "Lưu Travel DNA"}
          </button>
        )}
      </div>
    </div>
  );
}
