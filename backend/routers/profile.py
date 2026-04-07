from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import User
from services.auth import get_current_user

router = APIRouter(prefix="/api/profile", tags=["profile"])


class TravelDNA(BaseModel):
    persona: str  # phượt thủ, nghỉ dưỡng, ẩm thực, văn hóa, gia đình, couple
    budget_range: str  # low, medium, high, luxury
    budget_per_day: Optional[int] = None  # VND
    energy_level: str  # chill, moderate, compact
    activities_per_day: Optional[int] = None
    food_preferences: List[str] = []  # street_food, fine_dining, healthy, vegetarian
    accommodation_style: str  # homestay, hotel_3star, hotel_4star, resort, hostel
    deal_breakers: List[str] = []  # fear_heights, no_crowds, allergies, kids
    past_trips: List[str] = []
    notes: Optional[str] = None


class ProfileRequest(BaseModel):
    email: str
    name: Optional[str] = None
    travel_dna: TravelDNA


class ProfileResponse(BaseModel):
    email: str
    name: Optional[str]
    travel_dna: Dict
    message: str


@router.post("/travel-dna", response_model=ProfileResponse)
def save_travel_dna(req: ProfileRequest, db: Session = Depends(get_db), auth_email: Optional[str] = Depends(get_current_user)):
    # If authenticated, only allow modifying own profile
    if auth_email and auth_email != req.email:
        raise HTTPException(status_code=403, detail="Khong co quyen chinh sua profile nguoi khac")
    user = db.query(User).filter(User.email == req.email).first()
    if user:
        user.travel_dna = req.travel_dna.model_dump()
        if req.name:
            user.name = req.name
    else:
        user = User(email=req.email, name=req.name, travel_dna=req.travel_dna.model_dump())
        db.add(user)

    db.commit()
    db.refresh(user)
    return ProfileResponse(
        email=user.email,
        name=user.name,
        travel_dna=user.travel_dna,
        message="Travel DNA đã lưu!"
    )


@router.get("/travel-dna/{email}", response_model=ProfileResponse)
def get_travel_dna(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ProfileResponse(
        email=user.email,
        name=user.name,
        travel_dna=user.travel_dna or {},
        message="OK"
    )
