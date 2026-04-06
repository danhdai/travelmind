from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.review import Review
from services.nlp_vietnamese import generate_review_summary
import json
import os

router = APIRouter(prefix="/api/concierge", tags=["concierge"])

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Knowledge base for Quang Binh
QUANG_BINH_KB = {
    "phong_nha_cave": {
        "name": "Động Phong Nha",
        "tips": "Đi thuyền vào động ~1 tiếng. Vé 150k/người. Nên đi sáng sớm tránh đông. Mang áo mưa.",
        "best_time": "Tháng 4-8",
        "cost": "150,000 VND/vé",
    },
    "paradise_cave": {
        "name": "Động Thiên Đường",
        "tips": "2 options: 1km (250k) hoặc 7km trekking (450k). Leo 500 bậc thang. Mang nước uống.",
        "best_time": "Tháng 4-8",
        "cost": "250,000-450,000 VND/vé",
    },
    "dark_cave": {
        "name": "Hang Tối (Dark Cave)",
        "tips": "Zipline 400m + bơi + tắm bùn. Cần biết bơi. Mang đồ thay. Book trước 1-2 ngày mùa hè.",
        "best_time": "Tháng 4-8",
        "cost": "450,000 VND/combo",
    },
    "suoi_mooc": {
        "name": "Suối Moọc",
        "tips": "Nước trong xanh ngọc bích. Có kayak, zipline. Nên dành cả buổi chiều.",
        "best_time": "Tháng 4-8",
        "cost": "80,000 VND/vé",
    },
    "nhat_le_beach": {
        "name": "Biển Nhật Lệ",
        "tips": "Biển sạch, cát mịn. Hải sản tươi giá rẻ. Bình minh rất đẹp. Phố đi bộ buổi tối.",
        "best_time": "Tháng 5-8",
        "cost": "Miễn phí",
    },
    "son_doong": {
        "name": "Hang Sơn Đoòng",
        "tips": "Hang động lớn nhất thế giới. Tour 4 ngày 3 đêm bởi Oxalis. Book trước 6-12 tháng.",
        "best_time": "Tháng 2-8",
        "cost": "~70,000,000 VND/tour",
    },
    "transport": {
        "tips": "Thuê xe máy 120-150k/ngày. Grab có ở Đồng Hới. Xe bus từ Huế/Hà Nội. Bay đến sân bay Đồng Hới (VDH).",
    },
    "food": {
        "tips": "Bánh lọc, bánh nậm, cháo canh, ram cuốn. Hải sản ở Nhật Lệ rẻ và tươi. Quán ăn địa phương ~30-80k/món.",
    },
    "accommodation": {
        "tips": "Phong Nha: homestay 200-400k/đêm. Đồng Hới: hotel 300-800k/đêm. Nên ở Phong Nha 2 đêm, Đồng Hới 1 đêm.",
    },
}


class ChatMessage(BaseModel):
    role: str  # user, assistant
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    context: Optional[Dict] = None  # itinerary context, travel DNA, etc.


class ChatResponse(BaseModel):
    reply: str
    suggestions: List[str] = []
    related_places: List[str] = []


def _build_context(db: Session) -> str:
    """Build knowledge context from DB reviews."""
    context_parts = []
    for place_id, info in QUANG_BINH_KB.items():
        name = info.get("name", place_id)
        tips = info.get("tips", "")
        cost = info.get("cost", "")
        context_parts.append(f"- {name}: {tips} Giá: {cost}")

    # Add review summaries
    for place_id in ["phong_nha_cave", "paradise_cave", "dark_cave", "suoi_mooc", "nhat_le_beach"]:
        reviews = db.query(Review).filter(Review.place_id == place_id).all()
        if reviews:
            review_dicts = [{"text": r.text or "", "rating": r.rating or 3} for r in reviews]
            summary = generate_review_summary(review_dicts)
            context_parts.append(f"  Review {place_id}: {summary['summary']}")

    return "\n".join(context_parts)


def _word_match(msg: str, keywords: list) -> bool:
    """Match whole words to avoid partial matches like 'an' in 'quang'."""
    import re
    words = set(re.findall(r'\b\w+\b', msg))
    for kw in keywords:
        if " " in kw:
            if kw in msg:
                return True
        elif kw in words:
            return True
    return False


def _smart_reply(message: str, history: List[ChatMessage], db: Session) -> ChatResponse:
    """Rule-based smart reply when no API key."""
    msg = message.lower()
    suggestions = []
    related = []

    # Weather / time
    if _word_match(msg, ["thoi tiet", "mua nao", "nang", "khi hau", "thoi diem", "khi nao", "thang may", "thang 5", "thang 6", "thang 7", "thang 8"]):
        return ChatResponse(
            reply="Thời điểm đẹp nhất đi Quảng Bình là tháng 4-8 (mùa khô). Tháng 9-11 hay có mưa bão. Nếu đi mùa mưa, nên chuẩn bị áo mưa và có plan B cho hoạt động indoor.\n\nNhiệt độ trung bình 25-35°C mùa hè, 18-25°C mùa đông.",
            suggestions=["Gợi ý hoạt động indoor khi mưa?", "Nên đi mấy ngày?", "Chi phí trung bình bao nhiêu?"],
            related_places=["phong_nha_cave", "dark_cave"],
        )

    # Budget
    if _word_match(msg, ["chi phi", "gia ca", "budget", "tien", "bao nhieu", "het bao nhieu"]):
        return ChatResponse(
            reply="Chi phí trung bình cho chuyến Quảng Bình 3 ngày:\n\n"
                  "- **Tiết kiệm** (~1.5-2 triệu/người): Homestay, ăn quán địa phương, đi 2-3 điểm\n"
                  "- **Trung bình** (~3-4 triệu/người): Hotel 3*, ăn hải sản, đi 4-5 điểm + Dark Cave\n"
                  "- **Thoải mái** (~5-7 triệu/người): Resort, ăn nhà hàng, full combo\n\n"
                  "Vé tham quan: Phong Nha 150k, Thiên Đường 250k, Dark Cave 450k, Suối Moọc 80k.\n"
                  "Thuê xe máy: 120-150k/ngày.",
            suggestions=["Tạo lịch trình 3 ngày budget 3 triệu?", "Chỗ nào ăn ngon giá rẻ?", "Nên ở đâu?"],
            related_places=["phong_nha_cave", "paradise_cave", "dark_cave"],
        )

    # Food
    if _word_match(msg, ["an gi", "mon an", "nha hang", "quan an", "hai san", "dac san", "banh", "com", "do an", "am thuc"]):
        return ChatResponse(
            reply="Đặc sản Quảng Bình bạn nên thử:\n\n"
                  "1. **Bánh lọc, bánh nậm** - Ăn sáng kinh điển, ~30-50k/phần\n"
                  "2. **Cháo canh** - Cháo hải sản đặc trưng QB\n"
                  "3. **Ram cuốn** - Chả ram cuốn rau sống\n"
                  "4. **Hải sản Nhật Lệ** - Tôm, mực, cá tươi rói, giá chỉ 1/3 thành phố lớn\n"
                  "5. **Ốc** - Quán ốc dọc biển Nhật Lệ\n\n"
                  "Khu ăn uống: Biển Nhật Lệ (hải sản), chợ Đồng Hới (đặc sản), Phong Nha (quán địa phương).",
            suggestions=["Nhà hàng nào rating cao?", "Ăn chay ở đâu?", "Quán coffee đẹp?"],
            related_places=["nhat_le_beach"],
        )

    # Accommodation
    if _word_match(msg, ["khach san", "hotel", "homestay", "o dau", "ngu o", "resort", "cho o", "phong nghi"]):
        return ChatResponse(
            reply="Gợi ý chỗ ở Quảng Bình:\n\n"
                  "**Khu Phong Nha** (nên ở 2 đêm):\n"
                  "- Homestay: 200-400k/đêm, gần động, view đẹp\n"
                  "- Hotel: 400-800k/đêm\n\n"
                  "**Đồng Hới** (nên ở 1 đêm):\n"
                  "- Hotel 3*: 300-600k/đêm\n"
                  "- Hotel 4*: 800k-1.5tr/đêm\n"
                  "- Resort ven biển: 1.5-3tr/đêm\n\n"
                  "Tip: Nên ở Phong Nha trước để khám phá động, sau đó về Đồng Hới tắm biển.",
            suggestions=["Homestay nào rating cao nhất?", "Resort ven biển?", "Book qua app?"],
            related_places=["phong_nha_cave", "nhat_le_beach"],
        )

    # Dark Cave specific
    if _word_match(msg, ["hang toi", "dark cave", "zipline", "tam bun"]):
        return ChatResponse(
            reply="**Hang Tối (Dark Cave)** - Highlight #1 Quảng Bình!\n\n"
                  "Combo trải nghiệm: Zipline 400m → Bơi 200m vào hang → Tắm bùn → Leo núi → Kayak\n\n"
                  "- Giá: 450,000 VND/combo\n"
                  "- Thời gian: 2-3 tiếng\n"
                  "- Cần biết bơi (có áo phao)\n"
                  "- Mang: đồ bơi, đồ thay, dép chống trượt\n"
                  "- Book trước 1-2 ngày (nhất là mùa hè)\n\n"
                  "Trust Score: 89% (5 reviews thật) ⭐ 4.8/5",
            suggestions=["Không biết bơi có đi được không?", "So sánh với Phong Nha?", "Đi kết hợp Suối Moọc?"],
            related_places=["dark_cave", "suoi_mooc"],
        )

    # Phong Nha
    if _word_match(msg, ["phong nha", "dong phong"]):
        return ChatResponse(
            reply="**Động Phong Nha** - Di sản thế giới UNESCO\n\n"
                  "- Đi thuyền vào động ~1 tiếng, ngắm thạch nhũ lung linh\n"
                  "- Vé: 150,000 VND/người\n"
                  "- Nên đi: sáng sớm 7-8h tránh đông\n"
                  "- Mang theo: áo mưa (trong động hơi ẩm)\n\n"
                  "Trust Score: 88% (6 reviews thật) ⭐ 4.7/5\n\n"
                  "Có thể kết hợp: Động Thiên Đường (cùng ngày) + Suối Moọc (chiều).",
            suggestions=["Kết hợp Thiên Đường cùng ngày?", "So sánh Phong Nha vs Thiên Đường?", "Tour trọn gói?"],
            related_places=["phong_nha_cave", "paradise_cave", "suoi_mooc"],
        )

    # Son Doong
    if _word_match(msg, ["son doong", "hang lon nhat"]):
        return ChatResponse(
            reply="**Hang Sơn Đoòng** - Hang động lớn nhất thế giới!\n\n"
                  "- Tour 4 ngày 3 đêm bởi Oxalis Adventure\n"
                  "- Giá: ~70 triệu VND/người\n"
                  "- Cần: thể lực tốt, trekking rừng nhiều ngày\n"
                  "- Book trước: 6-12 tháng (slot rất limited)\n"
                  "- Mùa tour: tháng 2-8\n\n"
                  "Trust Score: 91% (3 reviews) ⭐ 5.0/5\n"
                  "\"Trải nghiệm đời người!\" - 100% review tích cực.",
            suggestions=["Có tour rẻ hơn không?", "Cần chuẩn bị gì?", "Thay thế Son Doong?"],
            related_places=["son_doong"],
        )

    # Transport
    if _word_match(msg, ["di chuyen", "xe may", "may bay", "tau hoa", "bus", "grab", "san bay"]):
        return ChatResponse(
            reply="Di chuyển đến & trong Quảng Bình:\n\n"
                  "**Đến Quảng Bình:**\n"
                  "- Bay: Vietnam Airlines/Vietjet đến sân bay Đồng Hới (VDH)\n"
                  "- Tàu: Ga Đồng Hới (tuyến Bắc-Nam)\n"
                  "- Bus: Từ Huế (~4h), Hà Nội (~10h)\n\n"
                  "**Trong Quảng Bình:**\n"
                  "- Thuê xe máy: 120-150k/ngày (phổ biến nhất)\n"
                  "- Grab: có ở Đồng Hới\n"
                  "- Xe ôm: quanh Phong Nha\n"
                  "- Đồng Hới → Phong Nha: ~45km, 1h xe máy",
            suggestions=["Thuê xe máy ở đâu?", "Giá vé máy bay?", "Đường đi Phong Nha?"],
        )

    # General / itinerary
    if _word_match(msg, ["lich trinh", "plan", "ke hoach", "may ngay", "bao nhieu ngay", "ngay"]):
        return ChatResponse(
            reply="Gợi ý lịch trình Quảng Bình 3 ngày:\n\n"
                  "**Ngày 1:** Động Phong Nha (sáng) → Suối Moọc (chiều)\n"
                  "**Ngày 2:** Động Thiên Đường (sáng) → Dark Cave (chiều)\n"
                  "**Ngày 3:** Biển Nhật Lệ (sáng) → Thành phố Đồng Hới (chiều)\n\n"
                  "Bạn muốn tôi tạo lịch trình chi tiết không? Hãy cho tôi biết budget và sở thích!",
            suggestions=["Tạo lịch trình chi tiết!", "Thêm 1 ngày nữa?", "Lịch trình cho couple?"],
            related_places=["phong_nha_cave", "paradise_cave", "dark_cave", "suoi_mooc", "nhat_le_beach"],
        )

    # Fallback
    return ChatResponse(
        reply="Tôi là AI Concierge của TravelMind! Tôi có thể giúp bạn:\n\n"
              "- Thông tin địa điểm Quảng Bình (Phong Nha, Dark Cave, Suối Moọc...)\n"
              "- Gợi ý lịch trình theo budget & sở thích\n"
              "- Đặc sản ẩm thực, nhà hàng\n"
              "- Chỗ ở (homestay, hotel, resort)\n"
              "- Di chuyển, thời tiết, tips\n\n"
              "Bạn muốn hỏi gì?",
        suggestions=["Nên đi Quảng Bình mấy ngày?", "Chi phí trung bình bao nhiêu?", "Địa điểm nào hay nhất?", "Ăn gì ở Quảng Bình?"],
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """AI Concierge chat endpoint."""
    if ANTHROPIC_API_KEY:
        return await _ai_chat(req, db)
    return _smart_reply(req.message, req.history, db)


async def _ai_chat(req: ChatRequest, db: Session) -> ChatResponse:
    """Chat using Claude API when available."""
    import anthropic

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    kb_context = _build_context(db)

    system_prompt = f"""Bạn là AI Concierge của TravelMind - trợ lý du lịch thông minh chuyên về Quảng Bình.

Thông tin địa điểm và reviews:
{kb_context}

Quy tắc:
- Trả lời bằng tiếng Việt, thân thiện, ngắn gọn
- Luôn đưa ra thông tin cụ thể (giá, thời gian, tips)
- Khi gợi ý, đính kèm Trust Score và rating từ reviews thật
- Nếu không chắc chắn, nói rõ và gợi ý nguồn kiểm tra
- Cuối mỗi reply, gợi ý 2-3 câu hỏi tiếp theo

Trả về JSON:
{{"reply": "nội dung trả lời", "suggestions": ["gợi ý 1", "gợi ý 2"], "related_places": ["place_id"]}}"""

    messages = []
    for h in req.history[-10:]:  # Last 10 messages
        messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": req.message})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )
        text = response.content[0].text

        try:
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            data = json.loads(text.strip())
            return ChatResponse(**data)
        except (json.JSONDecodeError, KeyError):
            return ChatResponse(reply=text, suggestions=[], related_places=[])
    except Exception:
        return _smart_reply(req.message, req.history, db)
