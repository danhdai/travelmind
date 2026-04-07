import TravelDNAForm from "@/components/TravelDNAForm";

export default function ProfilePage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <div className="text-4xl mb-3">🧬</div>
        <h1 className="text-3xl font-bold mb-2">Travel DNA Profile</h1>
        <p className="text-gray-500">
          Giúp AI hiểu bạn — để thiết kế lịch trình hoàn hảo
        </p>
      </div>
      <TravelDNAForm />
    </div>
  );
}
