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
        "place_name": "Động Phong Nha",
        "reviews": [
            {"author": "Minh Tuan", "rating": 5, "text": "Động Phong Nha đẹp tuyệt vời! Đi thuyền vào động, thạch nhũ lung linh dưới ánh đèn. Nên đi sáng sớm để tránh đông. Vé 150k/người rất xứng đáng.", "sentiment": 0.9, "trust": 0.88},
            {"author": "Thu Hang", "rating": 5, "text": "Lần đầu tiên thấy động đẹp đến vậy. Nước trong xanh, thạch nhũ hàng triệu năm. Tour thuyền khoảng 1 tiếng, hướng dẫn viên nhiệt tình. Highly recommend!", "sentiment": 0.92, "trust": 0.9},
            {"author": "Duc Anh", "rating": 4, "text": "Động đẹp nhưng hơi đông vào cuối tuần. Nên đi ngày thường. Giá vé hợp lý. Lưu ý mang áo mưa vì trong động hơi ẩm.", "sentiment": 0.7, "trust": 0.85},
            {"author": "Phuong Linh", "rating": 5, "text": "Một trong những động đẹp nhất Việt Nam. Đi thuyền dọc sông Son vào động, cảm giác như lạc vào thế giới khác. View dọc đường đi cũng rất đẹp.", "sentiment": 0.95, "trust": 0.92},
            {"author": "Thanh Long", "rating": 4, "text": "Phong Nha xứng đáng là di sản thế giới. Động rộng, đẹp, hướng dẫn viên chuyên nghiệp. Chỉ tiếc là không được tự do khám phá mà phải theo tour.", "sentiment": 0.72, "trust": 0.82},
            {"author": "Ngoc Mai FB", "rating": 5, "text": "Vừa đi Phong Nha về. Nơi này đẹp hơn nhiều so với hình trên mạng. Thạch nhũ rực rỡ, nước trong vắt. 10/10 sẽ quay lại!", "sentiment": 0.95, "trust": 0.88},
        ]
    },
    # Paradise Cave
    {
        "place_id": "paradise_cave",
        "place_name": "Động Thiên Đường (Paradise Cave)",
        "reviews": [
            {"author": "Hoang Nam", "rating": 5, "text": "Động Thiên Đường đúng như tên gọi - thiên đường! Thạch nhũ hùng vĩ, dài 31km. Có 2 option: đi 1km (150k) hoặc 7km adventure (trekking). Nên chọn 7km!", "sentiment": 0.93, "trust": 0.91},
            {"author": "Lan Anh", "rating": 5, "text": "Wow! Động đẹp ngất ngây. Cầu thang đi bộ rất tốt, có đèn chiếu sáng đẹp. Leo 500 bậc thang hơi mệt nhưng xứng đáng. Mang theo nước uống.", "sentiment": 0.88, "trust": 0.87},
            {"author": "Quang Huy", "rating": 4, "text": "Động đẹp thật nhưng phải leo nhiều bậc thang. Người già và trẻ nhỏ cần cân nhắc. Giá vé 250k cho 1km, 450k cho 7km trekking.", "sentiment": 0.68, "trust": 0.85},
            {"author": "My Linh", "rating": 5, "text": "Đã đi nhiều động nhưng Thiên Đường đẹp nhất! Thạch nhũ hình dáng độc đáo, mỗi góc là một bức tranh. Nên đi buổi sáng để ít người.", "sentiment": 0.95, "trust": 0.9},
            {"author": "Tuan Kiet", "rating": 5, "text": "Trải nghiệm 7km trekking trong động là điều không thể quên. Cần thể lực tốt nhưng bối cảnh trong động xứng đáng mỗi giọt mồ hôi.", "sentiment": 0.9, "trust": 0.88},
        ]
    },
    # Dark Cave
    {
        "place_id": "dark_cave",
        "place_name": "Hang Tối (Dark Cave)",
        "reviews": [
            {"author": "Viet Hung", "rating": 5, "text": "Hang Tối là trải nghiệm tuyệt vời nhất ở Quảng Bình! Zipline qua sông, bơi vào hang, tắm bùn. Giá 450k nhưng worth every đồng!", "sentiment": 0.95, "trust": 0.92},
            {"author": "Thuy Tien", "rating": 5, "text": "Quá đỉnh! Zipline dài 400m qua sông Chày, rồi bơi 200m vào hang tối tắm bùn. Cảm giác mạo hiểm nhưng an toàn. Must do khi đến Quảng Bình!", "sentiment": 0.93, "trust": 0.9},
            {"author": "Duy Manh", "rating": 4, "text": "Trải nghiệm rất hay nhưng cần biết bơi. Có áo phao nhưng vẫn cần tự tin dưới nước. Bùn trong hang rất mịn, tốt cho da.", "sentiment": 0.78, "trust": 0.85},
            {"author": "Ha My", "rating": 5, "text": "Đi nhóm 6 người, ai cũng thích. Zipline -> bơi -> leo núi -> tắm bùn -> kayak. Combo hoàn hảo! Mang theo đồ thay vì sau khi chơi sẽ ướt hết.", "sentiment": 0.92, "trust": 0.89},
            {"author": "Quoc Dat", "rating": 5, "text": "Hang Tối chính là highlight của chuyến đi Quảng Bình. Không đi là thiếu sót. Book trước 1-2 ngày để có slot, nhất là mùa hè.", "sentiment": 0.9, "trust": 0.87},
        ]
    },
    # Suoi Mooc
    {
        "place_id": "suoi_mooc",
        "place_name": "Suối Moọc (Mooc Spring)",
        "reviews": [
            {"author": "Cam Tu", "rating": 5, "text": "Suối Moọc đẹp như tranh vẽ. Nước trong xanh màu ngọc bích, mát lạnh. Có kayak, zipline, bồn tắm tự nhiên. Giá vé 80k rất rẻ.", "sentiment": 0.93, "trust": 0.9},
            {"author": "Bao Long", "rating": 4, "text": "Suối đẹp nhưng cuối tuần đông quá. Nên đi ngày thường. Có chỗ thuê phao, kayak. Nước lạnh nhẹ, mang theo khăn tắm.", "sentiment": 0.72, "trust": 0.83},
            {"author": "Khanh Linh", "rating": 5, "text": "Một trong những suối đẹp nhất mình từng đi. Nước tự nhiên trong vắt, màu xanh ngọc. Đường đi bộ dọc suối cũng rất đẹp, nhiều chỗ check-in.", "sentiment": 0.92, "trust": 0.88},
            {"author": "Trung Kien", "rating": 4, "text": "Suối Moọc thích hợp để relax sau khi đi động. Nước mát lạnh, không khí trong lành. Đồ ăn ở quầy bán giá hợp lý. Nên dành cả buổi chiều ở đây.", "sentiment": 0.8, "trust": 0.85},
        ]
    },
    # Nhat Le Beach
    {
        "place_id": "nhat_le_beach",
        "place_name": "Bãi biển Nhật Lệ",
        "reviews": [
            {"author": "Phu Thinh", "rating": 4, "text": "Biển Nhật Lệ sạch, cát mịn, sóng không quá lớn. Thích hợp tắm biển buổi sáng sớm. Bình minh ở đây rất đẹp. Hải sản tươi sống giá rẻ.", "sentiment": 0.82, "trust": 0.86},
            {"author": "Ngoc Anh", "rating": 5, "text": "Biển đẹp, ít người hơn Nha Trang hay Đà Nẵng nhiều. Ăn hải sản ở các quán ven biển giá chỉ bằng 1/3 thành phố lớn. Tôm, mực, cá tươi rói!", "sentiment": 0.9, "trust": 0.88},
            {"author": "Minh Khoa", "rating": 4, "text": "Nhật Lệ là biển chính của Đồng Hới. Buổi tối có phố đi bộ, ăn vặt nhiều. Cát sạch, nước trong. Chỉ tiếc là có ít hoạt động giải trí.", "sentiment": 0.72, "trust": 0.82},
            {"author": "Thu Ha", "rating": 4, "text": "Biển đẹp nhất vào sáng sớm và chiều muộn. Giữa trưa nắng gắt nên tránh. Giá khách sạn quanh biển từ 300-600k/đêm, rẻ hơn resort nhiều.", "sentiment": 0.75, "trust": 0.84},
        ]
    },
    # Son Doong
    {
        "place_id": "son_doong",
        "place_name": "Hang Sơn Đoòng",
        "reviews": [
            {"author": "Anh Tu", "rating": 5, "text": "Trải nghiệm đời người! Sơn Đoòng là hang động lớn nhất thế giới, và nó hùng vĩ hơn bất kỳ hình ảnh nào. Tour 4 ngày 3 đêm, giá 70 triệu nhưng xứng đáng.", "sentiment": 0.95, "trust": 0.93},
            {"author": "Hai Yen", "rating": 5, "text": "Đã tiết kiệm 2 năm để đi Sơn Đoòng và không hề thất vọng. Rừng trong hang, sông ngầm, thạch nhũ khổng lồ. Đội ngũ Oxalis chuyên nghiệp, an toàn.", "sentiment": 0.93, "trust": 0.91},
            {"author": "Quang Minh", "rating": 5, "text": "Once in a lifetime! Hang rộng đến mức máy bay có thể bay vào được. Cần thể lực tốt vì phải trekking rừng nhiều ngày. Book trước 6-12 tháng.", "sentiment": 0.92, "trust": 0.9},
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
