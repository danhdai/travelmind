from __future__ import annotations

from typing import Dict, List, Optional
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.group import TripGroup
from services.auth import require_auth, get_current_user

router = APIRouter(prefix="/api/group", tags=["group"])

VOTABLE_PLACES: Dict[str, List[Dict]] = {
    "Quang Binh": [
        {"id": "phong_nha_cave", "name": "Động Phong Nha", "icon": "🏔"},
        {"id": "paradise_cave", "name": "Động Thiên Đường", "icon": "✨"},
        {"id": "dark_cave", "name": "Hang Tối (Dark Cave)", "icon": "🦇"},
        {"id": "suoi_mooc", "name": "Suối Moọc", "icon": "💧"},
        {"id": "nhat_le_beach", "name": "Biển Nhật Lệ", "icon": "🏖"},
        {"id": "son_doong", "name": "Hang Sơn Đoòng", "icon": "🌍"},
    ],
    "Da Lat": [
        {"id": "dalat_langbiang", "name": "Núi LangBiang", "icon": "⛰"},
        {"id": "dalat_valley_of_love", "name": "Thung Lũng Tình Yêu", "icon": "💕"},
        {"id": "dalat_coffee", "name": "Coffee Đà Lạt", "icon": "☕"},
        {"id": "dalat_xq_village", "name": "Làng Lụa XQ", "icon": "🎨"},
    ],
    "Phu Quoc": [
        {"id": "phuquoc_sao_beach", "name": "Bãi Sao", "icon": "🏖"},
        {"id": "phuquoc_vinwonders", "name": "VinWonders", "icon": "🎢"},
        {"id": "phuquoc_night_market", "name": "Chợ đêm", "icon": "🦞"},
    ],
    "Hoi An": [
        {"id": "hoian_old_town", "name": "Phố cổ Hội An", "icon": "🏮"},
        {"id": "hoian_an_bang_beach", "name": "Biển An Bàng", "icon": "🏄"},
        {"id": "hoian_food", "name": "Ẩm thực Hội An", "icon": "🍜"},
    ],
}


class CreateGroupRequest(BaseModel):
    name: str
    destination: str
    num_days: int = 3


class JoinGroupRequest(BaseModel):
    name: Optional[str] = None


class VoteRequest(BaseModel):
    place_id: str


@router.post("/create")
def create_group(req: CreateGroupRequest, email: str = Depends(require_auth), db: Session = Depends(get_db)):
    group = TripGroup(
        name=req.name,
        destination=req.destination,
        num_days=req.num_days,
        owner_email=email,
        members=[{"email": email, "name": email.split("@")[0], "joined_at": str(datetime.now(timezone.utc))}],
        votes={},
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return {
        "id": group.id,
        "code": group.code,
        "name": group.name,
        "invite_link": f"/group/{group.code}",
        "message": f"Group '{group.name}' da tao! Chia se link de moi ban be.",
    }


@router.get("/{code}")
def get_group(code: str, db: Session = Depends(get_db)):
    group = db.query(TripGroup).filter(TripGroup.code == code).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    places = VOTABLE_PLACES.get(group.destination, [])
    votes = group.votes or {}

    place_votes = []
    for p in places:
        voters = votes.get(p["id"], [])
        place_votes.append({
            **p,
            "votes": len(voters),
            "voters": voters,
        })

    place_votes.sort(key=lambda x: x["votes"], reverse=True)

    return {
        "id": group.id,
        "code": group.code,
        "name": group.name,
        "destination": group.destination,
        "num_days": group.num_days,
        "owner": group.owner_email,
        "members": group.members or [],
        "member_count": len(group.members or []),
        "places": place_votes,
        "status": group.status,
    }


@router.post("/{code}/join")
def join_group(code: str, req: JoinGroupRequest, db: Session = Depends(get_db), email: Optional[str] = Depends(get_current_user)):
    group = db.query(TripGroup).filter(TripGroup.code == code).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    from sqlalchemy.orm.attributes import flag_modified

    members = list(group.members or [])
    member_email = email or f"guest_{len(members)+1}"
    member_name = req.name or member_email.split("@")[0]

    if not any(m.get("email") == member_email for m in members):
        members.append({"email": member_email, "name": member_name, "joined_at": str(datetime.now(timezone.utc))})
        group.members = members
        flag_modified(group, "members")
        db.commit()

    return {"message": f"{member_name} da tham gia!", "members": members}


@router.post("/{code}/vote")
def vote_place(code: str, req: VoteRequest, db: Session = Depends(get_db), email: Optional[str] = Depends(get_current_user)):
    group = db.query(TripGroup).filter(TripGroup.code == code).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    from sqlalchemy.orm.attributes import flag_modified

    voter = email or "anonymous"
    votes = dict(group.votes or {})

    if req.place_id not in votes:
        votes[req.place_id] = []

    voters_list = list(votes[req.place_id])
    if voter in voters_list:
        voters_list.remove(voter)  # Toggle off
    else:
        voters_list.append(voter)  # Toggle on

    votes[req.place_id] = voters_list
    group.votes = votes
    flag_modified(group, "votes")
    db.commit()

    return {"message": "Vote updated!", "votes": votes}
