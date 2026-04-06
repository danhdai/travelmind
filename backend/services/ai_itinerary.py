from __future__ import annotations

from typing import Dict, Optional

import json
import os
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


async def generate_itinerary(
    destination: str,
    num_days: int,
    budget: Optional[float] = None,
    travel_dna: Optional[Dict] = None,
) -> Dict:
    if not ANTHROPIC_API_KEY:
        return _mock_itinerary(destination, num_days, budget)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    travel_dna_text = ""
    if travel_dna:
        travel_dna_text = f"""
Travel DNA cua khach:
- Persona: {travel_dna.get('persona', 'N/A')}
- Budget: {travel_dna.get('budget_range', 'N/A')}
- Energy level: {travel_dna.get('energy_level', 'N/A')}
- Food: {', '.join(travel_dna.get('food_preferences', []))}
- Accommodation: {travel_dna.get('accommodation_style', 'N/A')}
- Deal breakers: {', '.join(travel_dna.get('deal_breakers', []))}
"""

    budget_text = f"\nNgan sach tong: {budget:,.0f} VND" if budget else ""

    prompt = f"""Ban la AI Travel Designer chuyen nghiep. Hay tao lich trinh du lich chi tiet.

Diem den: {destination}
So ngay: {num_days}{budget_text}
{travel_dna_text}

Hay tra ve JSON voi format:
{{
  "destination": "{destination}",
  "num_days": {num_days},
  "summary": "Tom tat ngan ve chuyen di",
  "days": [
    {{
      "day": 1,
      "title": "Tieu de ngay",
      "activities": [
        {{
          "time": "08:00",
          "activity": "Ten hoat dong",
          "place": "Dia diem",
          "description": "Mo ta chi tiet",
          "cost_estimate": 100000,
          "tips": "Meo hay"
        }}
      ],
      "meals": [
        {{
          "type": "breakfast/lunch/dinner",
          "restaurant": "Ten nha hang",
          "cuisine": "Loai mon",
          "cost_estimate": 50000
        }}
      ],
      "accommodation": {{
        "name": "Ten cho o",
        "type": "hotel/homestay/resort",
        "cost_estimate": 500000
      }},
      "day_cost": 800000
    }}
  ],
  "total_cost": 2400000,
  "budget_breakdown": {{
    "accommodation": 1500000,
    "food": 600000,
    "activities": 200000,
    "transport": 100000
  }},
  "tips": ["Meo chung cho chuyen di"]
}}

Chi tra ve JSON, khong them text nao khac."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        text = message.content[0].text
        # Try to extract JSON from the response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text.strip())
    except (json.JSONDecodeError, IndexError):
        return _mock_itinerary(destination, num_days, budget)


def _mock_itinerary(destination: str, num_days: int, budget: Optional[float]) -> Dict:
    """Fallback mock data khi chua co API key."""
    daily_budget = int((budget or 3000000) / num_days)

    activities_db = _get_activities_for_destination(destination)
    days = []
    for i in range(num_days):
        activities = activities_db["activities"][i % len(activities_db["activities"])]
        days.append({
            "day": i + 1,
            "title": f"Ngay {i + 1} - {activities[0]['place']}",
            "activities": activities,
            "meals": activities_db["meals"][i % len(activities_db["meals"])],
            "accommodation": activities_db["accommodation"],
            "day_cost": daily_budget,
        })

    total = daily_budget * num_days
    return {
        "destination": destination,
        "num_days": num_days,
        "summary": activities_db["summary"].format(num_days=num_days, destination=destination),
        "days": days,
        "total_cost": total,
        "budget_breakdown": {
            "accommodation": int(total * 0.35),
            "food": int(total * 0.3),
            "activities": int(total * 0.25),
            "transport": int(total * 0.1),
        },
        "tips": activities_db["tips"],
    }


def _get_activities_for_destination(destination: str) -> Dict:
    dest = destination.lower().replace(" ", "")
    if dest in ("dalat", "đàlạt"):
        return _dalat_data()
    elif dest in ("phuquoc", "phúquốc"):
        return _phuquoc_data()
    elif dest in ("hoian", "hộian"):
        return _hoian_data()
    return _quangbinh_data()


def _quangbinh_data() -> Dict:
    quang_binh_activities = [
        [
            {"time": "08:00", "activity": "Tham quan Dong Phong Nha", "place": "Dong Phong Nha", "description": "Di thuyen vao dong, ngam thach nhu tuyet dep", "cost_estimate": 150000, "tips": "Nen di sang som de tranh dong"},
            {"time": "14:00", "activity": "Suoi Mooc Eco Trail", "place": "Suoi Mooc", "description": "Tam suoi, cheo kayak, di zipline qua suoi", "cost_estimate": 80000, "tips": "Mang do boi va giay chong nuoc"},
        ],
        [
            {"time": "08:00", "activity": "Dong Thien Duong (Paradise Cave)", "place": "Dong Thien Duong", "description": "Dong kho dai 31km, thach nhu hung vi nhat Chau A", "cost_estimate": 250000, "tips": "Co 2 option: 1km (ngan) va 7km (du adventure)"},
            {"time": "14:00", "activity": "Song Chay - Hang Toi", "place": "Dark Cave", "description": "Zipline, boi, leo nui, tam bun trong hang toi", "cost_estimate": 450000, "tips": "Trai nghiem khong the bo qua!"},
        ],
        [
            {"time": "08:00", "activity": "Bai bien Nhat Le", "place": "Bai bien Nhat Le", "description": "Tam bien, an sang hai san tuoi song", "cost_estimate": 0, "tips": "Binh minh o Nhat Le rat dep"},
            {"time": "14:00", "activity": "Tham quan thanh pho Dong Hoi", "place": "Dong Hoi", "description": "Nha tho Tam Toa, Quang Binh Quan, cho Dong Hoi", "cost_estimate": 50000, "tips": "Mua banh loc, banh nam lam qua"},
        ],
    ]

    return {
        "summary": "Lich trinh {num_days} ngay kham pha {destination} - tu Dong Phong Nha den Suoi Mooc, Dark Cave va bien Nhat Le",
        "activities": quang_binh_activities,
        "meals": [
            [
                {"type": "breakfast", "restaurant": "Quan an dia phuong", "cuisine": "Banh loc, banh nam", "cost_estimate": 40000},
                {"type": "lunch", "restaurant": "Nha hang gan dong", "cuisine": "Hai san", "cost_estimate": 150000},
                {"type": "dinner", "restaurant": "Quan nhau Dong Hoi", "cuisine": "Dac san Quang Binh", "cost_estimate": 200000},
            ],
        ],
        "accommodation": {"name": "Homestay Phong Nha", "type": "homestay", "cost_estimate": 400000},
        "tips": [
            "Thoi diem dep nhat di Quang Binh: thang 4-8",
            "Nen thue xe may de di lai linh hoat",
            "Mang theo ao mua vi thoi tiet hay thay doi",
            "Dat tour Dark Cave truoc 1-2 ngay",
        ],
    }


def _dalat_data() -> Dict:
    return {
        "summary": "Lich trinh {num_days} ngay {destination} - thanh pho suong mu, coffee, hoa va nui",
        "activities": [
            [
                {"time": "08:00", "activity": "Leo nui LangBiang", "place": "Nui LangBiang", "description": "Trekking len dinh 2167m, view 360 do toan Da Lat", "cost_estimate": 150000, "tips": "Mang ao am, giay trekking. Di sang som"},
                {"time": "14:00", "activity": "Thung Lung Tinh Yeu", "place": "Thung Lung Tinh Yeu", "description": "Vuon hoa, ho, diem check-in dep", "cost_estimate": 100000, "tips": "Thich hop couple, chup hinh"},
            ],
            [
                {"time": "08:00", "activity": "Vuon hoa thanh pho", "place": "Vuon Hoa Da Lat", "description": "Hang tram loai hoa, nhat la hoa lavender, hydrangea", "cost_estimate": 50000, "tips": "Di sang som de tranh dong, hoa dep nhat"},
                {"time": "14:00", "activity": "Dinh Bao Dai & Coffee", "place": "Dinh Bao Dai", "description": "Tham quan dinh thu, sau do thuong thuc cafe Da Lat", "cost_estimate": 60000, "tips": "An Cafe view doi thong rat dep"},
            ],
            [
                {"time": "08:00", "activity": "Cho Da Lat", "place": "Cho Da Lat", "description": "Mua dac san: mut, tra atiso, rau cu. An sang banh can, sua dau nanh", "cost_estimate": 100000, "tips": "Cho dem tu 6h toi, do an nhieu va re"},
                {"time": "14:00", "activity": "Duong ham Dat Set", "place": "Duong ham Dat Set", "description": "Tac pham nghe thuat tu dat set doc dao, ky luc Viet Nam", "cost_estimate": 50000, "tips": "Noi doc nhat vo nhi o Viet Nam"},
            ],
        ],
        "meals": [
            [
                {"type": "breakfast", "restaurant": "Banh can Co Duyen", "cuisine": "Banh can Da Lat", "cost_estimate": 30000},
                {"type": "lunch", "restaurant": "Lau bo Da Lat", "cuisine": "Lau bo", "cost_estimate": 100000},
                {"type": "dinner", "restaurant": "Cho dem Da Lat", "cuisine": "Banh trang nuong, sua dau nanh", "cost_estimate": 60000},
            ],
        ],
        "accommodation": {"name": "Homestay view doi thong", "type": "homestay", "cost_estimate": 350000},
        "tips": [
            "Thoi tiet Da Lat mat me quanh nam (15-25 do)",
            "Buoi toi lanh, mang ao khoac",
            "Thue xe may 100-120k/ngay",
            "Coffee Da Lat la must-try: An Cafe, La Viet",
        ],
    }


def _phuquoc_data() -> Dict:
    return {
        "summary": "Lich trinh {num_days} ngay {destination} - dao ngoc voi bien xanh, hai san tuoi va hoang hon dep",
        "activities": [
            [
                {"time": "08:00", "activity": "Bai Sao", "place": "Bai Sao", "description": "Bien dep nhat Phu Quoc, cat trang nuoc trong", "cost_estimate": 50000, "tips": "Di sang som tranh dong, mang kem chong nang"},
                {"time": "14:00", "activity": "Snorkeling An Thoi", "place": "Quan dao An Thoi", "description": "Lan ngam san ho, ca nhiet doi. Tour nua ngay", "cost_estimate": 350000, "tips": "Book tour truoc, mang theo thuoc chong say"},
            ],
            [
                {"time": "08:00", "activity": "VinWonders", "place": "VinWonders Phu Quoc", "description": "Cong vien giai tri lon nhat Phu Quoc. Cap treo vuot bien 8km", "cost_estimate": 880000, "tips": "Di ca ngay, nhieu zone choi"},
                {"time": "18:00", "activity": "Sunset Sanato Beach", "place": "Sunset Sanato", "description": "Ngam hoang hon dep nhat dao, co bar va nhac song", "cost_estimate": 100000, "tips": "Den tu 5h chieu de co cho tot"},
            ],
            [
                {"time": "08:00", "activity": "Nha tu Phu Quoc", "place": "Nha tu Phu Quoc", "description": "Di tich lich su, bao tang chien tranh", "cost_estimate": 0, "tips": "Mien phi vao cua"},
                {"time": "14:00", "activity": "Cho dem Phu Quoc", "place": "Cho dem Dinh Cau", "description": "Hai san tuoi song: nhum, cua, tom hum nuong", "cost_estimate": 300000, "tips": "Hoi gia truoc khi an, nen mac ca"},
            ],
        ],
        "meals": [
            [
                {"type": "breakfast", "restaurant": "Bun quay Phu Quoc", "cuisine": "Bun quay", "cost_estimate": 35000},
                {"type": "lunch", "restaurant": "Quan hai san ven bien", "cuisine": "Hai san tuoi", "cost_estimate": 200000},
                {"type": "dinner", "restaurant": "Cho dem Dinh Cau", "cuisine": "Nhum bien, muc nuong", "cost_estimate": 250000},
            ],
        ],
        "accommodation": {"name": "Resort ven bien", "type": "resort", "cost_estimate": 800000},
        "tips": [
            "Mua dep nhat: thang 11-4 (mua kho)",
            "Thue xe may 150-200k/ngay",
            "Nuoc mam Phu Quoc mua lam qua",
            "Hoang hon o bai Dai va Ong Lang dep nhat",
        ],
    }


def _hoian_data() -> Dict:
    return {
        "summary": "Lich trinh {num_days} ngay {destination} - pho co, den long, am thuc va bien An Bang",
        "activities": [
            [
                {"time": "08:00", "activity": "Pho co Hoi An", "place": "Pho co Hoi An", "description": "Chua Cau, Nha co, Hoi quan. Kien truc Nhat-Viet-Hoa", "cost_estimate": 120000, "tips": "Ve 120k/5 diem. Di sang som tranh nong"},
                {"time": "14:00", "activity": "Lop hoc nau an", "place": "Cooking class", "description": "Hoc nau mi quang, cao lau, banh xeo voi dau bep dia phuong", "cost_estimate": 500000, "tips": "Book truoc, co nhieu lop sang va chieu"},
            ],
            [
                {"time": "08:00", "activity": "Bien An Bang", "place": "Bien An Bang", "description": "Tam bien, luot song, chill beach bar", "cost_estimate": 50000, "tips": "Beach bar Soul Kitchen rat hay"},
                {"time": "16:00", "activity": "Pho co buoi toi", "place": "Song Hoai", "description": "Tha den hoa dang tren song, ngam pho co ve dem", "cost_estimate": 30000, "tips": "Den hoa dang 10-20k/cai. Dep nhat tu 7h toi"},
            ],
            [
                {"time": "08:00", "activity": "Lang rau Tra Que", "place": "Lang rau Tra Que", "description": "Trai nghiem lam nong dan, trong rau, lam banh", "cost_estimate": 150000, "tips": "Tour nua ngay, bao an trua"},
                {"time": "14:00", "activity": "May do tai Hoi An", "place": "Pho may do", "description": "Hoi An noi tieng may do nhanh va re. Ao dai, vest, dam", "cost_estimate": 500000, "tips": "Chon tiem uy tin, hoi gia truoc. Giao trong 24h"},
            ],
        ],
        "meals": [
            [
                {"type": "breakfast", "restaurant": "Banh mi Phuong", "cuisine": "Banh mi (CNN voted best)", "cost_estimate": 25000},
                {"type": "lunch", "restaurant": "Quan cao lau", "cuisine": "Cao lau Hoi An", "cost_estimate": 40000},
                {"type": "dinner", "restaurant": "Com ga Ba Buoi", "cuisine": "Com ga Hoi An", "cost_estimate": 50000},
            ],
            [
                {"type": "breakfast", "restaurant": "Mi Quang Ong Hai", "cuisine": "Mi Quang", "cost_estimate": 30000},
                {"type": "lunch", "restaurant": "Beach bar An Bang", "cuisine": "Hai san nuong", "cost_estimate": 150000},
                {"type": "dinner", "restaurant": "Cho dem Hoi An", "cuisine": "White Rose, banh bao banh vac", "cost_estimate": 80000},
            ],
        ],
        "accommodation": {"name": "Homestay pho co", "type": "homestay", "cost_estimate": 350000},
        "tips": [
            "Thoi diem dep nhat: thang 2-5 (it mua, mat)",
            "Thue xe dap de di quanh pho co (20-30k/ngay)",
            "Pho co cam xe may tu 8h-23h",
            "An 5 bua/ngay o Hoi An - moi mon deu ngon va re!",
        ],
    }
