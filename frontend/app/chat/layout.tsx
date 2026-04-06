import { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Concierge - TravelMind",
  description: "Trợ lý du lịch AI 24/7. Hỏi đáp về điểm đến, ẩm thực, chỗ ở, di chuyển, chi phí.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
