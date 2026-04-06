import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Reviews Thật - TravelMind",
  description: "Tổng hợp review thật từ người đi thật. Trust Score, sentiment analysis, NLP cho mỗi địa điểm du lịch Việt Nam.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
