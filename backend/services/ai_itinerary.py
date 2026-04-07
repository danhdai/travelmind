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
Travel DNA của khách:
- Persona: {travel_dna.get('persona', 'N/A')}
- Budget: {travel_dna.get('budget_range', 'N/A')}
- Energy level: {travel_dna.get('energy_level', 'N/A')}
- Food: {', '.join(travel_dna.get('food_preferences', []))}
- Accommodation: {travel_dna.get('accommodation_style', 'N/A')}
- Deal breakers: {', '.join(travel_dna.get('deal_breakers', []))}
"""

    budget_text = f"\nNgân sách tổng: {budget:,.0f} VND" if budget else ""

    prompt = f"""Bạn là AI Travel Designer chuyên nghiệp. Hãy tạo lịch trình du lịch chi tiết.

Điểm đến: {destination}
Số ngày: {num_days}{budget_text}
{travel_dna_text}

Hãy trả về JSON với format:
{{
  "destination": "{destination}",
  "num_days": {num_days},
  "summary": "Tóm tắt ngắn về chuyến đi",
  "days": [
    {{
      "day": 1,
      "title": "Tiêu đề ngày",
      "activities": [
        {{
          "time": "08:00",
          "activity": "Tên hoạt động",
          "place": "Địa điểm",
          "description": "Mô tả chi tiết",
          "cost_estimate": 100000,
          "tips": "Mẹo hay"
        }}
      ],
      "meals": [
        {{
          "type": "breakfast/lunch/dinner",
          "restaurant": "Tên nhà hàng",
          "cuisine": "Loại món",
          "cost_estimate": 50000
        }}
      ],
      "accommodation": {{
        "name": "Tên chỗ ở",
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
  "tips": ["Mẹo chung cho chuyến đi"]
}}

Chỉ trả về JSON, không thêm text nào khác."""

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
    """Fallback mock data khi chưa có API key."""
    daily_budget = int((budget or 3000000) / num_days)

    activities_db = _get_activities_for_destination(destination)
    days = []
    for i in range(num_days):
        activities = activities_db["activities"][i % len(activities_db["activities"])]
        days.append({
            "day": i + 1,
            "title": f"Ngày {i + 1} - {activities[0]['place']}",
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
            {"time": "08:00", "activity": "Tham quan Động Phong Nha", "place": "Động Phong Nha", "description": "Đi thuyền vào động, ngắm thạch nhũ tuyệt đẹp", "cost_estimate": 150000, "tips": "Nên đi sáng sớm để tránh đông"},
            {"time": "14:00", "activity": "Suối Moọc Eco Trail", "place": "Suối Moọc", "description": "Tắm suối, chèo kayak, đi zipline qua suối", "cost_estimate": 80000, "tips": "Mang đồ bơi và giày chống nước"},
        ],
        [
            {"time": "08:00", "activity": "Động Thiên Đường (Paradise Cave)", "place": "Động Thiên Đường", "description": "Động khô dài 31km, thạch nhũ hùng vĩ nhất Châu Á", "cost_estimate": 250000, "tips": "Có 2 option: 1km (ngắn) và 7km (dư adventure)"},
            {"time": "14:00", "activity": "Sông Chày - Hang Tối", "place": "Dark Cave", "description": "Zipline, bơi, leo núi, tắm bùn trong hang tối", "cost_estimate": 450000, "tips": "Trải nghiệm không thể bỏ qua!"},
        ],
        [
            {"time": "08:00", "activity": "Bãi biển Nhật Lệ", "place": "Bãi biển Nhật Lệ", "description": "Tắm biển, ăn sáng hải sản tươi sống", "cost_estimate": 0, "tips": "Bình minh ở Nhật Lệ rất đẹp"},
            {"time": "14:00", "activity": "Tham quan thành phố Đồng Hới", "place": "Đồng Hới", "description": "Nhà thờ Tam Toà, Quảng Bình Quan, chợ Đồng Hới", "cost_estimate": 50000, "tips": "Mua bánh lọc, bánh nậm làm quà"},
        ],
    ]

    return {
        "summary": "Lịch trình {num_days} ngày khám phá {destination} - từ Động Phong Nha đến Suối Moọc, Dark Cave và biển Nhật Lệ",
        "activities": quang_binh_activities,
        "meals": [
            [
                {"type": "breakfast", "restaurant": "Quán ăn địa phương", "cuisine": "Bánh lọc, bánh nậm", "cost_estimate": 40000},
                {"type": "lunch", "restaurant": "Nhà hàng gần động", "cuisine": "Hải sản", "cost_estimate": 150000},
                {"type": "dinner", "restaurant": "Quán nhậu Đồng Hới", "cuisine": "Đặc sản Quảng Bình", "cost_estimate": 200000},
            ],
        ],
        "accommodation": {"name": "Homestay Phong Nha", "type": "homestay", "cost_estimate": 400000},
        "tips": [
            "Thời điểm đẹp nhất đi Quảng Bình: tháng 4-8",
            "Nên thuê xe máy để đi lại linh hoạt",
            "Mang theo áo mưa vì thời tiết hay thay đổi",
            "Đặt tour Dark Cave trước 1-2 ngày",
        ],
    }


def _dalat_data() -> Dict:
    return {
        "summary": "Lịch trình {num_days} ngày {destination} - thành phố sương mù, coffee, hoa và núi",
        "activities": [
            [
                {"time": "08:00", "activity": "Leo núi LangBiang", "place": "Núi LangBiang", "description": "Trekking lên đỉnh 2167m, view 360 độ toàn Đà Lạt", "cost_estimate": 150000, "tips": "Mang áo ấm, giày trekking. Đi sáng sớm"},
                {"time": "14:00", "activity": "Thung Lũng Tình Yêu", "place": "Thung Lũng Tình Yêu", "description": "Vườn hoa, hồ, điểm check-in đẹp", "cost_estimate": 100000, "tips": "Thích hợp couple, chụp hình"},
            ],
            [
                {"time": "08:00", "activity": "Vườn hoa thành phố", "place": "Vườn Hoa Đà Lạt", "description": "Hàng trăm loại hoa, nhất là hoa lavender, hydrangea", "cost_estimate": 50000, "tips": "Đi sáng sớm để tránh đông, hoa đẹp nhất"},
                {"time": "14:00", "activity": "Dinh Bảo Đại & Coffee", "place": "Dinh Bảo Đại", "description": "Tham quan dinh thự, sau đó thưởng thức cafe Đà Lạt", "cost_estimate": 60000, "tips": "An Cafe view đồi thông rất đẹp"},
            ],
            [
                {"time": "08:00", "activity": "Chợ Đà Lạt", "place": "Chợ Đà Lạt", "description": "Mua đặc sản: mứt, trà atiso, rau củ. Ăn sáng bánh căn, sữa đậu nành", "cost_estimate": 100000, "tips": "Chợ đêm từ 6h tối, đồ ăn nhiều và rẻ"},
                {"time": "14:00", "activity": "Đường hầm Đất Sét", "place": "Đường hầm Đất Sét", "description": "Tác phẩm nghệ thuật từ đất sét độc đáo, kỷ lục Việt Nam", "cost_estimate": 50000, "tips": "Nơi độc nhất vô nhị ở Việt Nam"},
            ],
        ],
        "meals": [
            [
                {"type": "breakfast", "restaurant": "Bánh căn Cô Duyên", "cuisine": "Bánh căn Đà Lạt", "cost_estimate": 30000},
                {"type": "lunch", "restaurant": "Lẩu bò Đà Lạt", "cuisine": "Lẩu bò", "cost_estimate": 100000},
                {"type": "dinner", "restaurant": "Chợ đêm Đà Lạt", "cuisine": "Bánh tráng nướng, sữa đậu nành", "cost_estimate": 60000},
            ],
        ],
        "accommodation": {"name": "Homestay view đồi thông", "type": "homestay", "cost_estimate": 350000},
        "tips": [
            "Thời tiết Đà Lạt mát mẻ quanh năm (15-25 độ)",
            "Buổi tối lạnh, mang áo khoác",
            "Thuê xe máy 100-120k/ngày",
            "Coffee Đà Lạt là must-try: An Cafe, La Viet",
        ],
    }


def _phuquoc_data() -> Dict:
    return {
        "summary": "Lịch trình {num_days} ngày {destination} - đảo ngọc với biển xanh, hải sản tươi và hoàng hôn đẹp",
        "activities": [
            [
                {"time": "08:00", "activity": "Bãi Sao", "place": "Bãi Sao", "description": "Biển đẹp nhất Phú Quốc, cát trắng nước trong", "cost_estimate": 50000, "tips": "Đi sáng sớm tránh đông, mang kem chống nắng"},
                {"time": "14:00", "activity": "Snorkeling An Thới", "place": "Quần đảo An Thới", "description": "Lặn ngắm san hô, cá nhiệt đới. Tour nửa ngày", "cost_estimate": 350000, "tips": "Book tour trước, mang theo thuốc chống say"},
            ],
            [
                {"time": "08:00", "activity": "VinWonders", "place": "VinWonders Phú Quốc", "description": "Công viên giải trí lớn nhất Phú Quốc. Cáp treo vượt biển 8km", "cost_estimate": 880000, "tips": "Đi cả ngày, nhiều zone chơi"},
                {"time": "18:00", "activity": "Sunset Sanato Beach", "place": "Sunset Sanato", "description": "Ngắm hoàng hôn đẹp nhất đảo, có bar và nhạc sống", "cost_estimate": 100000, "tips": "Đến từ 5h chiều để có chỗ tốt"},
            ],
            [
                {"time": "08:00", "activity": "Nhà tù Phú Quốc", "place": "Nhà tù Phú Quốc", "description": "Di tích lịch sử, bảo tàng chiến tranh", "cost_estimate": 0, "tips": "Miễn phí vào cửa"},
                {"time": "14:00", "activity": "Chợ đêm Phú Quốc", "place": "Chợ đêm Dinh Cậu", "description": "Hải sản tươi sống: nhum, cua, tôm hùm nướng", "cost_estimate": 300000, "tips": "Hỏi giá trước khi ăn, nên mặc cả"},
            ],
        ],
        "meals": [
            [
                {"type": "breakfast", "restaurant": "Bún quậy Phú Quốc", "cuisine": "Bún quậy", "cost_estimate": 35000},
                {"type": "lunch", "restaurant": "Quán hải sản ven biển", "cuisine": "Hải sản tươi", "cost_estimate": 200000},
                {"type": "dinner", "restaurant": "Chợ đêm Dinh Cậu", "cuisine": "Nhum biển, mực nướng", "cost_estimate": 250000},
            ],
        ],
        "accommodation": {"name": "Resort ven biển", "type": "resort", "cost_estimate": 800000},
        "tips": [
            "Mùa đẹp nhất: tháng 11-4 (mùa khô)",
            "Thuê xe máy 150-200k/ngày",
            "Nước mắm Phú Quốc mua làm quà",
            "Hoàng hôn ở bãi Dài và Ông Lang đẹp nhất",
        ],
    }


def _hoian_data() -> Dict:
    return {
        "summary": "Lịch trình {num_days} ngày {destination} - phố cổ, đèn lồng, ẩm thực và biển An Bàng",
        "activities": [
            [
                {"time": "08:00", "activity": "Phố cổ Hội An", "place": "Phố cổ Hội An", "description": "Chùa Cầu, Nhà cổ, Hội quán. Kiến trúc Nhật-Việt-Hoa", "cost_estimate": 120000, "tips": "Vé 120k/5 điểm. Đi sáng sớm tránh nóng"},
                {"time": "14:00", "activity": "Lớp học nấu ăn", "place": "Cooking class", "description": "Học nấu mì quảng, cao lầu, bánh xèo với đầu bếp địa phương", "cost_estimate": 500000, "tips": "Book trước, có nhiều lớp sáng và chiều"},
            ],
            [
                {"time": "08:00", "activity": "Biển An Bàng", "place": "Biển An Bàng", "description": "Tắm biển, lướt sóng, chill beach bar", "cost_estimate": 50000, "tips": "Beach bar Soul Kitchen rất hay"},
                {"time": "16:00", "activity": "Phố cổ buổi tối", "place": "Sông Hoài", "description": "Thả đèn hoa đăng trên sông, ngắm phố cổ về đêm", "cost_estimate": 30000, "tips": "Đèn hoa đăng 10-20k/cái. Đẹp nhất từ 7h tối"},
            ],
            [
                {"time": "08:00", "activity": "Làng rau Trà Quế", "place": "Làng rau Trà Quế", "description": "Trải nghiệm làm nông dân, trồng rau, làm bánh", "cost_estimate": 150000, "tips": "Tour nửa ngày, bao ăn trưa"},
                {"time": "14:00", "activity": "May đo tại Hội An", "place": "Phố may đo", "description": "Hội An nổi tiếng may đo nhanh và rẻ. Áo dài, vest, đầm", "cost_estimate": 500000, "tips": "Chọn tiệm uy tín, hỏi giá trước. Giao trong 24h"},
            ],
        ],
        "meals": [
            [
                {"type": "breakfast", "restaurant": "Bánh mì Phượng", "cuisine": "Bánh mì (CNN voted best)", "cost_estimate": 25000},
                {"type": "lunch", "restaurant": "Quán cao lầu", "cuisine": "Cao lầu Hội An", "cost_estimate": 40000},
                {"type": "dinner", "restaurant": "Cơm gà Bà Buội", "cuisine": "Cơm gà Hội An", "cost_estimate": 50000},
            ],
            [
                {"type": "breakfast", "restaurant": "Mì Quảng Ông Hai", "cuisine": "Mì Quảng", "cost_estimate": 30000},
                {"type": "lunch", "restaurant": "Beach bar An Bàng", "cuisine": "Hải sản nướng", "cost_estimate": 150000},
                {"type": "dinner", "restaurant": "Chợ đêm Hội An", "cuisine": "White Rose, bánh bao bánh vạc", "cost_estimate": 80000},
            ],
        ],
        "accommodation": {"name": "Homestay phố cổ", "type": "homestay", "cost_estimate": 350000},
        "tips": [
            "Thời điểm đẹp nhất: tháng 2-5 (ít mưa, mát)",
            "Thuê xe đạp để đi quanh phố cổ (20-30k/ngày)",
            "Phố cổ cấm xe máy từ 8h-23h",
            "Ăn 5 bữa/ngày ở Hội An - mọi món đều ngon và rẻ!",
        ],
    }
