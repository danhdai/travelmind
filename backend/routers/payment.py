from __future__ import annotations

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/payment", tags=["payment"])


class PaymentRequest(BaseModel):
    email: str
    tier: str  # explorer, premium, vip
    itinerary_id: Optional[int] = None


class PaymentResponse(BaseModel):
    checkout_url: str
    message: str


PRICING = {
    "explorer": {"name": "Explorer", "price": 199000, "currency": "VND"},
    "premium": {"name": "Premium", "price": 599000, "currency": "VND"},
    "vip": {"name": "VIP", "price": 3000000, "currency": "VND"},
}


@router.post("/create-session", response_model=PaymentResponse)
async def create_payment_session(req: PaymentRequest):
    tier_info = PRICING.get(req.tier)
    if not tier_info:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid tier")

    # TODO: Integrate Stripe/VNPay when API keys are configured
    return PaymentResponse(
        checkout_url=f"/payment/mock?tier={req.tier}&email={req.email}",
        message=f"Thanh toan {tier_info['name']}: {tier_info['price']:,} VND (mock - chưa kết nối payment gateway)"
    )


@router.get("/pricing")
def get_pricing():
    return {
        "tiers": [
            {
                "id": "free",
                "name": "Free",
                "price": 0,
                "features": [
                    "Xem review (5 dia diem/thang)",
                    "Travel DNA basic",
                    "Lich trinh outline",
                ]
            },
            {
                "id": "explorer",
                "name": "Explorer",
                "price": 199000,
                "price_label": "199k VND/lich trinh",
                "features": [
                    "Lich trinh day-by-day chi tiet",
                    "Review khong gioi han",
                    "Budget breakdown",
                    "Interactive map",
                    "1 lan chinh sua AI",
                ]
            },
            {
                "id": "premium",
                "name": "Premium",
                "price": 599000,
                "price_label": "599k VND/lich trinh",
                "popular": True,
                "features": [
                    "Tat ca Explorer features",
                    "AI Concierge 24/7",
                    "Group planning (10 nguoi)",
                    "Plan B cho moi activity",
                    "Unlimited chinh sua",
                    "Priority booking",
                ]
            },
            {
                "id": "vip",
                "name": "VIP",
                "price": 3000000,
                "price_label": "1.5tr-3tr VND",
                "features": [
                    "Tat ca Premium features",
                    "Human expert review",
                    "Concierge call",
                    "Emergency support",
                    "Group lon, honeymoon, gia dinh",
                ]
            },
        ]
    }
