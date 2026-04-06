from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import User
from models.itinerary import Itinerary
from services.auth import hash_password, verify_password, create_token, require_auth

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    referral_code: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    token: str
    email: str
    name: Optional[str]


class UserProfile(BaseModel):
    email: str
    name: Optional[str]
    travel_dna: Optional[Dict]
    saved_itineraries: Optional[List]
    referral_code: Optional[str]
    referral_count: Optional[int]


def _validate_email(email: str) -> bool:
    import re
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)) and len(email) <= 255


@router.post("/register", response_model=AuthResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if not req.email or not _validate_email(req.email):
        raise HTTPException(status_code=400, detail="Email khong hop le")
    if not req.password or len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Mat khau phai co it nhat 6 ky tu")
    if len(req.password) > 128:
        raise HTTPException(status_code=400, detail="Mat khau qua dai")
    if req.name and len(req.name) > 100:
        raise HTTPException(status_code=400, detail="Ten qua dai")

    existing = db.query(User).filter(User.email == req.email).first()
    if existing and existing.password_hash:
        raise HTTPException(status_code=400, detail="Email da dang ky")

    import hashlib
    ref_code = hashlib.md5(req.email.encode()).hexdigest()[:8]

    if existing:
        existing.password_hash = hash_password(req.password)
        if req.name:
            existing.name = req.name
        if not existing.referral_code:
            existing.referral_code = ref_code
        db.commit()
        user = existing
    else:
        user = User(
            email=req.email,
            password_hash=hash_password(req.password),
            name=req.name,
            referral_code=ref_code,
            referred_by=req.referral_code,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Credit referrer
    if req.referral_code:
        referrer = db.query(User).filter(User.referral_code == req.referral_code).first()
        if referrer:
            referrer.referral_count = (referrer.referral_count or 0) + 1
            db.commit()

    token = create_token(user.email)
    return AuthResponse(token=token, email=user.email, name=user.name)


@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Email hoac mat khau sai")
    if not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email hoac mat khau sai")

    token = create_token(user.email)
    return AuthResponse(token=token, email=user.email, name=user.name)


@router.get("/me", response_model=UserProfile)
def get_me(email: str = Depends(require_auth), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(
        email=user.email,
        name=user.name,
        travel_dna=user.travel_dna,
        saved_itineraries=user.saved_itineraries or [],
        referral_code=user.referral_code,
        referral_count=user.referral_count or 0,
    )


@router.post("/save-itinerary/{itinerary_id}")
def save_itinerary(itinerary_id: int, email: str = Depends(require_auth), db: Session = Depends(get_db)):
    from sqlalchemy.orm.attributes import flag_modified
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    saved = list(user.saved_itineraries or [])
    if itinerary_id not in saved:
        saved.append(itinerary_id)
        user.saved_itineraries = saved
        flag_modified(user, "saved_itineraries")
        db.commit()

    return {"message": "Da luu!", "saved": saved}


@router.delete("/save-itinerary/{itinerary_id}")
def unsave_itinerary(itinerary_id: int, email: str = Depends(require_auth), db: Session = Depends(get_db)):
    from sqlalchemy.orm.attributes import flag_modified
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    saved = list(user.saved_itineraries or [])
    if itinerary_id in saved:
        saved.remove(itinerary_id)
        user.saved_itineraries = saved
        flag_modified(user, "saved_itineraries")
        db.commit()

    return {"message": "Da xoa!", "saved": saved}


@router.get("/my-itineraries")
def my_itineraries(email: str = Depends(require_auth), db: Session = Depends(get_db)):
    """Get all itineraries created by or saved by user."""
    created = (
        db.query(Itinerary)
        .filter(Itinerary.user_email == email)
        .order_by(Itinerary.created_at.desc())
        .all()
    )
    user = db.query(User).filter(User.email == email).first()
    saved_ids = user.saved_itineraries or [] if user else []
    saved = db.query(Itinerary).filter(Itinerary.id.in_(saved_ids)).all() if saved_ids else []

    def to_dict(it: Itinerary) -> Dict:
        data = it.itinerary_data or {}
        return {
            "id": it.id,
            "destination": it.destination,
            "num_days": it.num_days,
            "budget": it.budget,
            "summary": data.get("summary", ""),
            "total_cost": data.get("total_cost"),
            "created_at": str(it.created_at),
        }

    return {
        "created": [to_dict(i) for i in created],
        "saved": [to_dict(i) for i in saved],
    }
