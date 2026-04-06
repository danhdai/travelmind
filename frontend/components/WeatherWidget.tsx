"use client";

import { useEffect, useState } from "react";

interface WeatherData {
  temperature: number;
  description: string;
  icon: string;
  humidity: number;
  windSpeed: number;
  forecast: Array<{ date: string; tempMax: number; tempMin: number; icon: string }>;
}

const DEST_COORDS: Record<string, { lat: number; lng: number }> = {
  "Quang Binh": { lat: 17.47, lng: 106.62 },
  "Da Lat": { lat: 11.94, lng: 108.44 },
  "Phu Quoc": { lat: 10.22, lng: 103.97 },
  "Hoi An": { lat: 15.88, lng: 108.34 },
};

const WMO_CODES: Record<number, { desc: string; icon: string }> = {
  0: { desc: "Trời quang", icon: "☀" },
  1: { desc: "Ít mây", icon: "🌤" },
  2: { desc: "Có mây", icon: "⛅" },
  3: { desc: "Nhiều mây", icon: "☁" },
  45: { desc: "Sương mù", icon: "🌫" },
  48: { desc: "Sương muối", icon: "🌫" },
  51: { desc: "Mưa phùn nhẹ", icon: "🌦" },
  53: { desc: "Mưa phùn", icon: "🌦" },
  55: { desc: "Mưa phùn dày", icon: "🌧" },
  61: { desc: "Mưa nhẹ", icon: "🌦" },
  63: { desc: "Mưa vừa", icon: "🌧" },
  65: { desc: "Mưa to", icon: "🌧" },
  80: { desc: "Mưa rào nhẹ", icon: "🌦" },
  81: { desc: "Mưa rào", icon: "🌧" },
  82: { desc: "Mưa rào to", icon: "⛈" },
  95: { desc: "Giông", icon: "⛈" },
  96: { desc: "Giông + mưa đá", icon: "⛈" },
};

function getWeatherInfo(code: number) {
  return WMO_CODES[code] || { desc: "Không rõ", icon: "🌡" };
}

export default function WeatherWidget({ destination }: { destination: string }) {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const coords = DEST_COORDS[destination];
    if (!coords) { setLoading(false); return; }

    fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${coords.lat}&longitude=${coords.lng}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Asia/Ho_Chi_Minh&forecast_days=5`
    )
      .then((r) => r.json())
      .then((data) => {
        const current = data.current;
        const info = getWeatherInfo(current.weather_code);
        const forecast = data.daily.time.map((date: string, i: number) => ({
          date,
          tempMax: data.daily.temperature_2m_max[i],
          tempMin: data.daily.temperature_2m_min[i],
          icon: getWeatherInfo(data.daily.weather_code[i]).icon,
        }));
        setWeather({
          temperature: current.temperature_2m,
          description: info.desc,
          icon: info.icon,
          humidity: current.relative_humidity_2m,
          windSpeed: current.wind_speed_10m,
          forecast,
        });
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [destination]);

  if (loading) return <div className="animate-pulse bg-gray-100 h-24 rounded-xl" />;
  if (!weather) return null;

  return (
    <div className="bg-gradient-to-r from-sky-500 to-blue-600 rounded-xl p-4 text-white">
      <div className="flex items-center justify-between mb-3">
        <div>
          <div className="text-xs opacity-80">Thời tiết {destination}</div>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-3xl">{weather.icon}</span>
            <span className="text-2xl font-bold">{weather.temperature}°C</span>
          </div>
          <div className="text-xs opacity-80 mt-0.5">{weather.description}</div>
        </div>
        <div className="text-right text-xs opacity-80 space-y-1">
          <div>Độ ẩm: {weather.humidity}%</div>
          <div>Gió: {weather.windSpeed} km/h</div>
        </div>
      </div>
      <div className="flex gap-2 border-t border-white/20 pt-2">
        {weather.forecast.map((day) => (
          <div key={day.date} className="flex-1 text-center">
            <div className="text-[10px] opacity-70">
              {new Date(day.date).toLocaleDateString("vi", { weekday: "short" })}
            </div>
            <div className="text-sm my-0.5">{day.icon}</div>
            <div className="text-[10px]">
              {Math.round(day.tempMax)}° / {Math.round(day.tempMin)}°
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
