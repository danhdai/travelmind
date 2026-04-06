"""Seed database with Quang Binh sample data for demo."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import engine, Base, SessionLocal
from models.review import Review

# Create tables
Base.metadata.create_all(bind=engine)

QUANG_BINH_REVIEWS = [
    # Phong Nha Cave
    {
        "place_id": "phong_nha_cave",
        "place_name": "Dong Phong Nha",
        "reviews": [
            {"author": "Minh Tuan", "rating": 5, "text": "Dong Phong Nha dep tuyet voi! Di thuyen vao dong, thach nhu lung linh duoi anh den. Nen di sang som de tranh dong. Ve 150k/nguoi rat xung dang.", "sentiment": 0.9, "trust": 0.88},
            {"author": "Thu Hang", "rating": 5, "text": "Lan dau tien thay dong dep den vay. Nuoc trong xanh, thach nhu hang trieu nam. Tour thuyen khoang 1 tieng, huong dan vien nhiet tinh. Highly recommend!", "sentiment": 0.92, "trust": 0.9},
            {"author": "Duc Anh", "rating": 4, "text": "Dong dep nhung hoi dong vao cuoi tuan. Nen di ngay thuong. Gia ve hop ly. Luu y mang ao mua vi trong dong hoi am.", "sentiment": 0.7, "trust": 0.85},
            {"author": "Phuong Linh", "rating": 5, "text": "Mot trong nhung dong dep nhat Viet Nam. Di thuyen doc song Son vao dong, cam giac nhu lac vao the gioi khac. View doc duong di cung rat dep.", "sentiment": 0.95, "trust": 0.92},
            {"author": "Thanh Long", "rating": 4, "text": "Phong Nha xung dang la di san the gioi. Dong rong, dep, huong dan vien chuyen nghiep. Chi tiec la khong duoc tu do kham pha ma phai theo tour.", "sentiment": 0.72, "trust": 0.82},
            {"author": "Ngoc Mai FB", "rating": 5, "text": "Vua di Phong Nha ve. Noi nay dep hon nhieu so voi hinh tren mang. Thach nhu ruc ro, nuoc trong vanh. 10/10 se quay lai!", "sentiment": 0.95, "trust": 0.88},
        ]
    },
    # Paradise Cave
    {
        "place_id": "paradise_cave",
        "place_name": "Dong Thien Duong (Paradise Cave)",
        "reviews": [
            {"author": "Hoang Nam", "rating": 5, "text": "Dong Thien Duong dung nhu ten goi - thien duong! Thach nhu hung vi, dai 31km. Co 2 option: di 1km (150k) hoac 7km adventure (trekking). Nen chon 7km!", "sentiment": 0.93, "trust": 0.91},
            {"author": "Lan Anh", "rating": 5, "text": "Wow! Dong dep ngat ngay. Cau thang di bo rat tot, co den chieu sang dep. Leo 500 bac thang hoi met nhung xung dang. Mang theo nuoc uong.", "sentiment": 0.88, "trust": 0.87},
            {"author": "Quang Huy", "rating": 4, "text": "Dong dep that nhung phai leo nhieu bac thang. Nguoi gia va tre nho can can nhac. Gia ve 250k cho 1km, 450k cho 7km trekking.", "sentiment": 0.68, "trust": 0.85},
            {"author": "My Linh", "rating": 5, "text": "Da di nhieu dong nhung Thien Duong dep nhat! Thach nhu hinh dang doc dao, moi goc la mot buc tranh. Nen di buoi sang de it nguoi.", "sentiment": 0.95, "trust": 0.9},
            {"author": "Tuan Kiet", "rating": 5, "text": "Trai nghiem 7km trekking trong dong la dieu khong the quen. Can the luc tot nhung boi canh trong dong xung dang moi giot mo hoi.", "sentiment": 0.9, "trust": 0.88},
        ]
    },
    # Dark Cave
    {
        "place_id": "dark_cave",
        "place_name": "Hang Toi (Dark Cave)",
        "reviews": [
            {"author": "Viet Hung", "rating": 5, "text": "Hang Toi la trai nghiem tuyet voi nhat o Quang Binh! Zipline qua song, boi vao hang, tam bun. Gia 450k nhung worth every dong!", "sentiment": 0.95, "trust": 0.92},
            {"author": "Thuy Tien", "rating": 5, "text": "Qua dinh! Zipline dai 400m qua song Chay, roi boi 200m vao hang toi tam bun. Cam giac mao hiem nhung an toan. Must do khi den Quang Binh!", "sentiment": 0.93, "trust": 0.9},
            {"author": "Duy Manh", "rating": 4, "text": "Trai nghiem rat hay nhung can biet boi. Co ao phao nhung van can tu tin duoi nuoc. Bun trong hang rat min, tot cho da.", "sentiment": 0.78, "trust": 0.85},
            {"author": "Ha My", "rating": 5, "text": "Di nhom 6 nguoi, ai cung thich. Zipline -> boi -> leo nui -> tam bun -> kayak. Combo hoan hao! Mang theo do thay vi sau khi choi se uot het.", "sentiment": 0.92, "trust": 0.89},
            {"author": "Quoc Dat", "rating": 5, "text": "Hang Toi chinh la highlight cua chuyen di Quang Binh. Khong di la thieu sot. Book truoc 1-2 ngay de co slot, nhat la mua he.", "sentiment": 0.9, "trust": 0.87},
        ]
    },
    # Suoi Mooc
    {
        "place_id": "suoi_mooc",
        "place_name": "Suoi Mooc (Mooc Spring)",
        "reviews": [
            {"author": "Cam Tu", "rating": 5, "text": "Suoi Mooc dep nhu tranh ve. Nuoc trong xanh mau ngoc bich, mat lanh. Co kayak, zipline, bon tam tu nhien. Gia ve 80k rat re.", "sentiment": 0.93, "trust": 0.9},
            {"author": "Bao Long", "rating": 4, "text": "Suoi dep nhung cuoi tuan dong qua. Nen di ngay thuong. Co cho thue phao, kayak. Nuoc lanh nhe, mang theo khan tam.", "sentiment": 0.72, "trust": 0.83},
            {"author": "Khanh Linh", "rating": 5, "text": "Mot trong nhung suoi dep nhat minh tung di. Nuoc tu nhien trong vanh, mau xanh ngoc. Duong di bo doc suoi cung rat dep, nhieu cho check-in.", "sentiment": 0.92, "trust": 0.88},
            {"author": "Trung Kien", "rating": 4, "text": "Suoi Mooc thich hop de relax sau khi di dong. Nuoc mat lanh, khong khi trong lanh. Do an o quay ban gia hop ly. Nen danh ca buoi chieu o day.", "sentiment": 0.8, "trust": 0.85},
        ]
    },
    # Nhat Le Beach
    {
        "place_id": "nhat_le_beach",
        "place_name": "Bai bien Nhat Le",
        "reviews": [
            {"author": "Phu Thinh", "rating": 4, "text": "Bien Nhat Le sach, cat min, song khong qua lon. Thich hop tam bien buoi sang som. Binh minh o day rat dep. Hai san tuoi song gia re.", "sentiment": 0.82, "trust": 0.86},
            {"author": "Ngoc Anh", "rating": 5, "text": "Bien dep, it nguoi hon Nha Trang hay Da Nang nhieu. An hai san o cac quan ven bien gia chi bang 1/3 thanh pho lon. Tom, muc, ca tuoi roi!", "sentiment": 0.9, "trust": 0.88},
            {"author": "Minh Khoa", "rating": 4, "text": "Nhat Le la bien chinh cua Dong Hoi. Buoi toi co pho di bo, an vat nhieu. Cat sach, nuoc trong. Chi tiec la co it hoat dong giai tri.", "sentiment": 0.72, "trust": 0.82},
            {"author": "Thu Ha", "rating": 4, "text": "Bien dep nhat vao sang som va chieu muon. Giua trua nang gat nen tranh. Gia khach san quanh bien tu 300-600k/dem, re hon resort nhieu.", "sentiment": 0.75, "trust": 0.84},
        ]
    },
    # Son Doong
    {
        "place_id": "son_doong",
        "place_name": "Hang Son Doong",
        "reviews": [
            {"author": "Anh Tu", "rating": 5, "text": "Trai nghiem doi nguoi! Son Doong la hang dong lon nhat the gioi, va no hung vi hon bat ky hinh anh nao. Tour 4 ngay 3 dem, gia 70 trieu nhung xung dang.", "sentiment": 0.95, "trust": 0.93},
            {"author": "Hai Yen", "rating": 5, "text": "Da tiet kiem 2 nam de di Son Doong va khong he that vong. Rung trong hang, song ngam, thach nhu khong lo. Doi ngu Oxalis chuyen nghiep, an toan.", "sentiment": 0.93, "trust": 0.91},
            {"author": "Quang Minh", "rating": 5, "text": "Once in a lifetime! Hang rong den muc may bay co the bay vao duoc. Can the luc tot vi phai trekking rung nhieu ngay. Book truoc 6-12 thang.", "sentiment": 0.92, "trust": 0.9},
        ]
    },
]


def seed():
    db = SessionLocal()
    count = 0

    for place in QUANG_BINH_REVIEWS:
        for rev in place["reviews"]:
            existing = db.query(Review).filter(
                Review.place_id == place["place_id"],
                Review.author_name == rev["author"],
            ).first()
            if existing:
                continue

            review = Review(
                place_id=place["place_id"],
                place_name=place["place_name"],
                source="seed_data",
                author_name=rev["author"],
                rating=rev["rating"],
                text=rev["text"],
                sentiment_score=rev["sentiment"],
                trust_score=rev["trust"],
            )
            db.add(review)
            count += 1

    db.commit()
    db.close()
    print(f"Seeded {count} reviews for {len(QUANG_BINH_REVIEWS)} places")


if __name__ == "__main__":
    seed()
