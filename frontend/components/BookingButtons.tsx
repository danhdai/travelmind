"use client";

interface BookingButtonsProps {
  type: "hotel" | "tour" | "restaurant" | "transport";
  placeName: string;
  destination: string;
}

const BOOKING_LINKS = {
  hotel: [
    { name: "Agoda", color: "bg-red-500 hover:bg-red-600", baseUrl: "https://www.agoda.com/search?city=" },
    { name: "Booking.com", color: "bg-blue-600 hover:bg-blue-700", baseUrl: "https://www.booking.com/searchresults.html?ss=" },
  ],
  tour: [
    { name: "Klook", color: "bg-orange-500 hover:bg-orange-600", baseUrl: "https://www.klook.com/search?query=" },
    { name: "GetYourGuide", color: "bg-blue-500 hover:bg-blue-600", baseUrl: "https://www.getyourguide.com/s/?q=" },
  ],
  restaurant: [
    { name: "PasGo", color: "bg-green-600 hover:bg-green-700", baseUrl: "https://pasgo.vn/tim-kiem?q=" },
  ],
  transport: [
    { name: "Traveloka", color: "bg-sky-500 hover:bg-sky-600", baseUrl: "https://www.traveloka.com/vi-vn/search?query=" },
    { name: "Grab", color: "bg-green-500 hover:bg-green-600", baseUrl: "https://www.grab.com/" },
  ],
};

export default function BookingButtons({ type, placeName, destination }: BookingButtonsProps) {
  const links = BOOKING_LINKS[type] || [];
  const query = encodeURIComponent(`${placeName} ${destination}`);

  return (
    <div className="flex gap-1.5 mt-2">
      {links.map((link) => (
        <a
          key={link.name}
          href={`${link.baseUrl}${query}`}
          target="_blank"
          rel="noopener noreferrer"
          className={`text-[10px] text-white px-2 py-1 rounded-md ${link.color} transition`}
        >
          {link.name} →
        </a>
      ))}
    </div>
  );
}
