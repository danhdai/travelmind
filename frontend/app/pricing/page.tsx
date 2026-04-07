const tiers = [
  {
    id: "free",
    name: "Free",
    price: "0",
    period: "",
    popular: false,
    features: [
      "Xem review (5 địa điểm/tháng)",
      "Travel DNA basic",
      "Lịch trình outline",
    ],
    cta: "Bắt đầu miễn phí",
    href: "/itinerary",
  },
  {
    id: "explorer",
    name: "Explorer",
    price: "199k",
    period: "/lịch trình",
    popular: false,
    features: [
      "Lịch trình day-by-day chi tiết",
      "Review không giới hạn",
      "Budget breakdown",
      "Interactive map",
      "1 lần chỉnh sửa AI",
    ],
    cta: "Chọn Explorer",
    href: "/itinerary",
  },
  {
    id: "premium",
    name: "Premium",
    price: "599k",
    period: "/lịch trình",
    popular: true,
    features: [
      "Tất cả Explorer features",
      "AI Concierge 24/7",
      "Group planning (10 người)",
      "Plan B cho mọi activity",
      "Unlimited chỉnh sửa",
      "Priority booking",
    ],
    cta: "Chọn Premium",
    href: "/itinerary",
  },
  {
    id: "vip",
    name: "VIP",
    price: "1.5-3tr",
    period: "",
    popular: false,
    features: [
      "Tất cả Premium features",
      "Human expert review",
      "Concierge call",
      "Emergency support",
      "Group lớn, honeymoon, gia đình",
    ],
    cta: "Liên hệ",
    href: "/itinerary",
  },
];

export default function PricingPage() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold mb-2">Bảng giá TravelMind</h1>
        <p className="text-gray-500">
          Chọn gói phù hợp — từ miễn phí đến VIP
        </p>
      </div>

      <div className="grid md:grid-cols-4 gap-6">
        {tiers.map((tier) => (
          <div
            key={tier.id}
            className={`rounded-2xl border-2 p-6 flex flex-col ${
              tier.popular
                ? "border-sky-500 shadow-lg shadow-sky-100 relative"
                : "border-gray-200"
            }`}
          >
            {tier.popular && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-sky-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                Phổ biến
              </div>
            )}
            <h3 className="text-xl font-bold">{tier.name}</h3>
            <div className="mt-3 mb-4">
              <span className="text-3xl font-bold">{tier.price}</span>
              <span className="text-gray-500 text-sm"> VND{tier.period}</span>
            </div>
            <ul className="space-y-2 flex-1 mb-6">
              {tier.features.map((f) => (
                <li key={f} className="flex items-start gap-2 text-sm text-gray-600">
                  <span className="text-green-500 mt-0.5">✓</span>
                  {f}
                </li>
              ))}
            </ul>
            <a
              href={tier.href}
              className={`block text-center py-3 rounded-xl font-medium transition ${
                tier.popular
                  ? "bg-sky-600 text-white hover:bg-sky-700"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {tier.cta}
            </a>
          </div>
        ))}
      </div>

      <div className="mt-12 text-center text-gray-400 text-sm">
        + Revenue từ booking commission: 5-15% mỗi booking qua app
      </div>
    </div>
  );
}
