"""Seed more destinations: Da Lat, Phu Quoc, Hoi An."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import engine, Base, SessionLocal
from models.review import Review

Base.metadata.create_all(bind=engine)

DESTINATIONS = [
    # DA LAT
    {
        "place_id": "dalat_xq_village",
        "place_name": "Làng lụa XQ Đà Lạt",
        "reviews": [
            {"author": "Thanh Hoa", "rating": 4, "text": "Lang lua dep, co vuon hoa, tranh theu tay. Mien phi vao cua. Thich hop chup hinh. Khong gian yen tinh.", "sentiment": 0.82, "trust": 0.84},
            {"author": "Minh Duc", "rating": 4, "text": "Diem check-in dep o Da Lat. Tranh theu tay rat an tuong. Co ca coffee shop view dep.", "sentiment": 0.8, "trust": 0.82},
        ]
    },
    {
        "place_id": "dalat_valley_of_love",
        "place_name": "Thung Lũng Tình Yêu Đà Lạt",
        "reviews": [
            {"author": "Hong Nhung", "rating": 3, "text": "Hoi thuong mai hoa, nhieu cho check-in san but dep. Ve 100k. Thich hop couple. Cuoi tuan dong.", "sentiment": 0.55, "trust": 0.72},
            {"author": "Quoc Bao", "rating": 4, "text": "Thung lung rong, nhieu hoa, ho xuan huong. Di dao mat. Gia ve 100k hop ly. Nen di buoi sang som.", "sentiment": 0.78, "trust": 0.8},
            {"author": "Kim Chi", "rating": 3, "text": "Khong an tuong lam, hoi tourist trap. Nhung view dep, hoa nhieu mau. Di 1 lan cho biet.", "sentiment": 0.45, "trust": 0.75},
        ]
    },
    {
        "place_id": "dalat_langbiang",
        "place_name": "Núi LangBiang Đà Lạt",
        "reviews": [
            {"author": "Hai Long", "rating": 5, "text": "Leo nui LangBiang la trai nghiem tuyet voi! Dinh nui 2167m, view 360 do. Co 2 option: di jeep (150k) hoac trekking 3h. Nen trekking!", "sentiment": 0.92, "trust": 0.9},
            {"author": "Thu Thao", "rating": 5, "text": "View dinh LangBiang sieu dep, nhin thay ca Da Lat. Trekking khoang 3 tieng, duong di dep. Mang ao am vi dinh nui lanh.", "sentiment": 0.9, "trust": 0.88},
            {"author": "Duc Minh", "rating": 4, "text": "Leo nui met nhung xung dang. Khong khi trong lanh, view dep. Can giay trekking va nuoc uong. Nen di sang som.", "sentiment": 0.78, "trust": 0.85},
        ]
    },
    {
        "place_id": "dalat_coffee",
        "place_name": "Coffee Đà Lạt",
        "reviews": [
            {"author": "Linh Dan", "rating": 5, "text": "Da Lat la thien duong coffee! Moi quan moi phong cach. An Cafe (view doi thong), La Viet (specialty), Trung Nguyen Legend. Gia 30-60k/ly.", "sentiment": 0.92, "trust": 0.88},
            {"author": "Phuong Uyen", "rating": 5, "text": "Ngoi cafe ngam mua Da Lat, khong gi bang! Recommend: An Cafe, Windmills coffee, The Married Beans. Atmosphere tuyet voi.", "sentiment": 0.93, "trust": 0.87},
        ]
    },
    # PHU QUOC
    {
        "place_id": "phuquoc_sao_beach",
        "place_name": "Bãi Sao Phú Quốc",
        "reviews": [
            {"author": "Ngoc Trinh", "rating": 5, "text": "Bai Sao dep nhat Phu Quoc! Cat trang min, nuoc trong xanh. Thich hop tam bien, chup hinh. Gia ghe 50-100k. Di sang som tranh dong.", "sentiment": 0.93, "trust": 0.9},
            {"author": "Anh Khoa", "rating": 4, "text": "Bien dep that nhung cuoi tuan dong. Co cho thue sup, kayak. An hai san ngay bien. Gia hoi dat hon noi khac.", "sentiment": 0.7, "trust": 0.83},
            {"author": "Thao Vy", "rating": 5, "text": "Wow bien dep qua! Nuoc trong nhu kinh, cat trang nhu tuyet. Instagram-worthy 100%. Nen di ngay thuong.", "sentiment": 0.95, "trust": 0.86},
        ]
    },
    {
        "place_id": "phuquoc_vinwonders",
        "place_name": "VinWonders Phú Quốc",
        "reviews": [
            {"author": "Tuan Anh", "rating": 5, "text": "VinWonders quy mo lon, nhieu tro choi. Di cap treo vuot bien 8km sieu dep. Aquarium, tro choi nuoc, shows. Ve 880k nhung choi ca ngay.", "sentiment": 0.9, "trust": 0.88},
            {"author": "My Hanh", "rating": 4, "text": "Thich hop gia dinh va tre nho. Nhieu zone: truot nuoc, aquarium, safari. Can it nhat 1 ngay full. Gia hoi cao nhung worth it.", "sentiment": 0.78, "trust": 0.85},
        ]
    },
    {
        "place_id": "phuquoc_night_market",
        "place_name": "Chợ đêm Phú Quốc",
        "reviews": [
            {"author": "Hoang Yen", "rating": 4, "text": "Cho dem Phu Quoc nhieu hai san tuoi song. Nhum bien, cua hoang de, muc nuong. Gia 100-300k/phan. Nen mac ca. Di tu 5h chieu.", "sentiment": 0.8, "trust": 0.85},
            {"author": "Van Anh", "rating": 4, "text": "An hai san o cho dem la must do! Tom hum nuong, oc len nuong, banh trang nuong. Gia hop ly hon nha hang. Dong nguoi nhung vui.", "sentiment": 0.82, "trust": 0.84},
            {"author": "Quang Dat", "rating": 3, "text": "Cho dem dong va hoi nong. Hai san tuoi nhung gia hoi dat cho khach du lich. Nen hoi gia truoc khi goi. Co hang luu niem dep.", "sentiment": 0.55, "trust": 0.8},
        ]
    },
    # HOI AN
    {
        "place_id": "hoian_old_town",
        "place_name": "Phố cổ Hội An",
        "reviews": [
            {"author": "Bich Ngoc", "rating": 5, "text": "Hoi An dep nhat vao buoi toi khi den long sang. Pho co co charm rieng, kien truc Nhat-Viet-Hoa pha tron. Ve tham quan 120k/5 diem.", "sentiment": 0.93, "trust": 0.91},
            {"author": "Trung Hieu", "rating": 5, "text": "Da den Hoi An 3 lan va lan nao cung thich. Buoi toi tha den tren song Hoai, an cao lau, uong ca phe. Khong gian lang man.", "sentiment": 0.92, "trust": 0.9},
            {"author": "Phuong Anh", "rating": 4, "text": "Pho co dep nhung dong khach du lich. Nen di sang som hoac toi muon. Gia do an hoi cao hon binh thuong. An Cong cafe view dep.", "sentiment": 0.68, "trust": 0.85},
        ]
    },
    {
        "place_id": "hoian_an_bang_beach",
        "place_name": "Biển An Bàng Hội An",
        "reviews": [
            {"author": "Duc Huy", "rating": 5, "text": "An Bang dep va it dong hon Cua Dai. Cat min, nuoc trong. Nhieu beach bar chill. An hai san ngay bien. Gia ghe 30-50k.", "sentiment": 0.9, "trust": 0.88},
            {"author": "Thuy Linh", "rating": 4, "text": "Bien dep, thich hop relax. Co surf cho nguoi thich sport. Beach bar Soul Kitchen va Sound of Silence rat hay. Sunset dep.", "sentiment": 0.85, "trust": 0.86},
        ]
    },
    {
        "place_id": "hoian_food",
        "place_name": "Ẩm thực Hội An",
        "reviews": [
            {"author": "Khanh Vy", "rating": 5, "text": "Hoi An la thien duong an uong! Cao lau, mi quang, banh mi Phuong, com ga, banh bao banh vac. Moi mon deu ngon va re (20-50k).", "sentiment": 0.95, "trust": 0.9},
            {"author": "Nhat Minh", "rating": 5, "text": "Banh mi Phuong duoc CNN binh chon ngon nhat! Cao lau chi co o Hoi An. Com ga Ba Buoi, mi quang Ong Hai. Gia binh dan.", "sentiment": 0.92, "trust": 0.89},
            {"author": "Mai Phuong", "rating": 5, "text": "An 5 bua/ngay o Hoi An van khong du! White Rose, Banh Bao Banh Vac la mon doc nhat. Cho dem Hoi An nhieu do an ngon.", "sentiment": 0.9, "trust": 0.87},
        ]
    },
]


def seed():
    db = SessionLocal()
    count = 0

    for place in DESTINATIONS:
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
    print(f"Seeded {count} reviews for {len(DESTINATIONS)} places (Da Lat, Phu Quoc, Hoi An)")


if __name__ == "__main__":
    seed()
