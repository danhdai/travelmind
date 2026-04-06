import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-[60vh] flex items-center justify-center px-4">
      <div className="text-center">
        <div className="text-6xl mb-4">🧭</div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">404</h1>
        <p className="text-lg text-gray-500 mb-6">
          Trang này không tồn tại — có lẽ bạn đã lạc đường!
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Link
            href="/"
            className="px-6 py-3 bg-sky-600 text-white font-medium rounded-xl hover:bg-sky-700 transition"
          >
            Về trang chủ
          </Link>
          <Link
            href="/itinerary"
            className="px-6 py-3 border border-gray-200 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition"
          >
            Tạo lịch trình
          </Link>
          <Link
            href="/chat"
            className="px-6 py-3 border border-gray-200 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition"
          >
            Hỏi AI Concierge
          </Link>
        </div>
      </div>
    </div>
  );
}
