"use client";

import { useState } from "react";

const faqs = [
  {
    q: "TravelMind là gì?",
    a: "TravelMind là AI Travel Designer — ứng dụng giúp bạn research review thật từ người đi thật, tạo lịch trình du lịch cá nhân hóa theo đúng phong cách của bạn. AI hiểu bạn thông qua Travel DNA Profile và thiết kế chuyến đi hoàn hảo.",
  },
  {
    q: "Review trên TravelMind có thật không?",
    a: "Có! Chúng tôi tổng hợp review từ nhiều nguồn (Google Maps, Facebook Groups, TikTok) và sử dụng AI NLP để phân tích sentiment, detect fake review, và tính Trust Score cho mỗi đánh giá. Chỉ review có Trust Score cao mới được hiển thị nổi bật.",
  },
  {
    q: "Trust Score là gì?",
    a: "Trust Score (0-100%) đánh giá độ tin cậy của mỗi review dựa trên 5 yếu tố: Content Depth (chi tiết nội dung), Sentiment Coherence (rating khớp với text), Authenticity (không phải fake), Photo Evidence (có ảnh thật), và Consistency (nhất quán với reviews khác).",
  },
  {
    q: "Tạo lịch trình mất bao lâu?",
    a: "Chỉ ~30 giây! Bạn chọn điểm đến, số ngày, ngân sách → AI tạo lịch trình day-by-day chi tiết với hoạt động, ăn uống, chỗ ở, budget breakdown, và review thật cho mỗi địa điểm.",
  },
  {
    q: "Travel DNA Profile là gì?",
    a: "Travel DNA là hồ sơ du lịch cá nhân của bạn. AI hỏi 6 câu về: phong cách (phượt/nghỉ dưỡng/ẩm thực...), ngân sách, mức năng lượng, sở thích ẩm thực, chỗ ở, và deal breakers. AI dùng profile này để thiết kế lịch trình riêng cho bạn.",
  },
  {
    q: "TravelMind có miễn phí không?",
    a: "Có! Gói Free cho phép xem 5 địa điểm/tháng, Travel DNA basic, và lịch trình outline. Gói Explorer (199k/lịch trình) có lịch trình chi tiết + review không giới hạn. Premium (599k) thêm AI Concierge 24/7 và group planning.",
  },
  {
    q: "AI Concierge hoạt động như thế nào?",
    a: "AI Concierge là trợ lý du lịch 24/7 — bạn có thể chat hỏi bất cứ điều gì về điểm đến: ăn gì, ở đâu, đi chuyển, thời tiết, chi phí, gợi ý hoạt động. Concierge có kiến thức từ database review thật.",
  },
  {
    q: "Group Planning là gì?",
    a: "Tính năng cho nhóm bạn cùng lên kế hoạch. Tạo group → share link mời → mọi người vote địa điểm muốn đi → AI tạo lịch trình dựa trên kết quả vote. Hỗ trợ đến 10 người/group.",
  },
  {
    q: "Hiện hỗ trợ những điểm đến nào?",
    a: "MVP hiện hỗ trợ 4 điểm đến: Quảng Bình, Đà Lạt, Phú Quốc, Hội An. Chúng tôi đang mở rộng thêm nhiều điểm đến mới trên toàn Việt Nam và Đông Nam Á.",
  },
  {
    q: "Dữ liệu cá nhân có được bảo mật không?",
    a: "Có. Chúng tôi sử dụng JWT authentication, mật khẩu được mã hóa bcrypt. Dữ liệu Travel DNA chỉ dùng để cá nhân hóa lịch trình và không chia sẻ với bên thứ ba.",
  },
];

export default function FAQPage() {
  const [openIdx, setOpenIdx] = useState<number | null>(null);

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <div className="text-4xl mb-3">❓</div>
        <h1 className="text-3xl font-bold mb-2">Câu hỏi thường gặp</h1>
        <p className="text-gray-500">Mọi thứ bạn cần biết về TravelMind</p>
      </div>

      <div className="space-y-2">
        {faqs.map((faq, i) => (
          <div key={i} className="border border-gray-100 rounded-xl overflow-hidden">
            <button
              onClick={() => setOpenIdx(openIdx === i ? null : i)}
              className="w-full flex items-center justify-between p-5 text-left hover:bg-gray-50 transition"
            >
              <span className="font-medium text-sm pr-4">{faq.q}</span>
              <svg
                className={`w-5 h-5 text-gray-400 flex-shrink-0 transition ${openIdx === i ? "rotate-180" : ""}`}
                fill="none" viewBox="0 0 24 24" stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            {openIdx === i && (
              <div className="px-5 pb-5 text-sm text-gray-600 leading-relaxed">
                {faq.a}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-12 text-center bg-sky-50 rounded-2xl p-8">
        <h3 className="font-semibold mb-2">Còn câu hỏi khác?</h3>
        <p className="text-sm text-gray-600 mb-4">Hỏi AI Concierge hoặc liên hệ team</p>
        <div className="flex gap-3 justify-center">
          <a href="/chat" className="px-4 py-2 bg-sky-600 text-white text-sm rounded-lg hover:bg-sky-700 transition">
            Hỏi AI Concierge
          </a>
          <a href="mailto:hello@travelmind.vn" className="px-4 py-2 border border-gray-200 text-sm rounded-lg hover:bg-gray-50 transition">
            Email support
          </a>
        </div>
      </div>
    </div>
  );
}
