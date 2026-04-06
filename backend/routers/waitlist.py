from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.waitlist import Waitlist

router = APIRouter(prefix="/api/waitlist", tags=["waitlist"])


class WaitlistRequest(BaseModel):
    email: str
    name: Optional[str] = None


class WaitlistResponse(BaseModel):
    id: int
    email: str
    message: str


def _validate_email(email: str) -> bool:
    import re
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)) and len(email) <= 255


@router.post("/", response_model=WaitlistResponse)
def join_waitlist(req: WaitlistRequest, db: Session = Depends(get_db)):
    if not req.email or not _validate_email(req.email):
        raise HTTPException(status_code=400, detail="Email khong hop le")

    existing = db.query(Waitlist).filter(Waitlist.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email da dang ky waitlist")

    entry = Waitlist(email=req.email, name=req.name)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return WaitlistResponse(id=entry.id, email=entry.email, message="Dang ky thanh cong!")
