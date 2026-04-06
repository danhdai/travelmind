"use client";

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface Place {
  name: string;
  lat: number;
  lng: number;
  day: number;
  description?: string;
}

// Coordinate data for known places
const PLACE_COORDS: Record<string, [number, number]> = {
  // Quang Binh
  "dong phong nha": [17.5919, 106.2833],
  "phong nha": [17.5919, 106.2833],
  "dong thien duong": [17.5433, 106.2200],
  "paradise cave": [17.5433, 106.2200],
  "thien duong": [17.5433, 106.2200],
  "dark cave": [17.5600, 106.2700],
  "hang toi": [17.5600, 106.2700],
  "suoi mooc": [17.5500, 106.2300],
  "mooc spring": [17.5500, 106.2300],
  "nhat le": [17.4676, 106.6220],
  "dong hoi": [17.4676, 106.6166],
  "son doong": [17.5453, 106.1486],
  // Da Lat
  "langbiang": [12.0500, 108.4333],
  "nui langbiang": [12.0500, 108.4333],
  "thung lung tinh yeu": [11.9600, 108.4400],
  "vuon hoa da lat": [11.9400, 108.4350],
  "cho da lat": [11.9420, 108.4420],
  "dinh bao dai": [11.9350, 108.4380],
  "duong ham dat set": [11.9460, 108.4300],
  // Phu Quoc
  "bai sao": [10.0500, 104.0300],
  "vinwonders": [10.0167, 104.0500],
  "vinwonders phu quoc": [10.0167, 104.0500],
  "sunset sanato": [10.2100, 103.9600],
  "cho dem": [10.2150, 103.9650],
  "cho dem dinh cau": [10.2150, 103.9650],
  "nha tu phu quoc": [10.3700, 103.9670],
  "an thoi": [9.9600, 104.0300],
  // Hoi An
  "pho co hoi an": [15.8801, 108.3380],
  "hoi an": [15.8801, 108.3380],
  "an bang": [15.8900, 108.3600],
  "bien an bang": [15.8900, 108.3600],
  "tra que": [15.8950, 108.3400],
  "lang rau tra que": [15.8950, 108.3400],
  "cooking class": [15.8801, 108.3380],
  "pho may do": [15.8801, 108.3380],
  "song hoai": [15.8790, 108.3370],
};

const DAY_COLORS = ["#0ea5e9", "#f97316", "#8b5cf6", "#10b981", "#ef4444"];

function getCoords(placeName: string): [number, number] | null {
  const normalized = placeName.toLowerCase().trim();
  for (const [key, coords] of Object.entries(PLACE_COORDS)) {
    if (normalized.includes(key) || key.includes(normalized)) {
      return coords;
    }
  }
  return null;
}

interface ItineraryMapProps {
  places: Array<{
    name: string;
    day: number;
    time?: string;
    activity?: string;
    description?: string;
  }>;
  destination: string;
}

export default function ItineraryMap({ places, destination }: ItineraryMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current || mapInstanceRef.current) return;

    const resolvedPlaces: Place[] = [];
    for (const p of places) {
      const coords = getCoords(p.name) || getCoords(destination);
      if (coords) {
        resolvedPlaces.push({
          name: p.activity || p.name,
          lat: coords[0] + (Math.random() - 0.5) * 0.005, // Slight jitter for overlapping
          lng: coords[1] + (Math.random() - 0.5) * 0.005,
          day: p.day,
          description: p.description,
        });
      }
    }

    if (resolvedPlaces.length === 0) return;

    const map = L.map(mapRef.current).setView(
      [resolvedPlaces[0].lat, resolvedPlaces[0].lng],
      12
    );
    mapInstanceRef.current = map;

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    // Add markers grouped by day
    const bounds: [number, number][] = [];
    const dayGroups: Record<number, [number, number][]> = {};

    resolvedPlaces.forEach((place) => {
      const color = DAY_COLORS[(place.day - 1) % DAY_COLORS.length];
      const marker = L.circleMarker([place.lat, place.lng], {
        radius: 10,
        fillColor: color,
        color: "#fff",
        weight: 2,
        fillOpacity: 0.9,
      }).addTo(map);

      marker.bindPopup(
        `<div style="min-width:150px">
          <strong style="color:${color}">Ngày ${place.day}</strong><br/>
          <b>${place.name}</b>
          ${place.description ? `<br/><small>${place.description}</small>` : ""}
        </div>`
      );

      bounds.push([place.lat, place.lng]);
      if (!dayGroups[place.day]) dayGroups[place.day] = [];
      dayGroups[place.day].push([place.lat, place.lng]);
    });

    // Draw route lines per day
    Object.entries(dayGroups).forEach(([day, coords]) => {
      if (coords.length > 1) {
        const color = DAY_COLORS[(Number(day) - 1) % DAY_COLORS.length];
        L.polyline(coords as L.LatLngExpression[], {
          color,
          weight: 3,
          opacity: 0.6,
          dashArray: "8, 8",
        }).addTo(map);
      }
    });

    if (bounds.length > 0) {
      map.fitBounds(bounds as L.LatLngBoundsExpression, { padding: [30, 30] });
    }

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, [places, destination]);

  return (
    <div className="rounded-2xl overflow-hidden border border-gray-200">
      <div ref={mapRef} className="h-[350px] w-full" />
      <div className="flex gap-3 p-3 bg-gray-50 text-xs">
        {Array.from(new Set(places.map((p) => p.day))).map((day) => (
          <div key={day} className="flex items-center gap-1">
            <span
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: DAY_COLORS[(day - 1) % DAY_COLORS.length] }}
            />
            <span className="text-gray-600">Ngày {day}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
