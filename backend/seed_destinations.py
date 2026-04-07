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
            {"author": "Thanh Hoa", "rating": 4, "text": "Làng lụa đẹp, có vườn hoa, tranh thêu tay. Miễn phí vào cửa. Thích hợp chụp hình. Không gian yên tĩnh.", "sentiment": 0.82, "trust": 0.84},
            {"author": "Minh Duc", "rating": 4, "text": "Điểm check-in đẹp ở Đà Lạt. Tranh thêu tay rất ấn tượng. Có cả coffee shop view đẹp.", "sentiment": 0.8, "trust": 0.82},
        ]
    },
    {
        "place_id": "dalat_valley_of_love",
        "place_name": "Thung Lũng Tình Yêu Đà Lạt",
        "reviews": [
            {"author": "Hong Nhung", "rating": 3, "text": "Hơi thương mại hoá, nhiều chỗ check-in sẵn but đẹp. Vé 100k. Thích hợp couple. Cuối tuần đông.", "sentiment": 0.55, "trust": 0.72},
            {"author": "Quoc Bao", "rating": 4, "text": "Thung lũng rộng, nhiều hoa, hồ Xuân Hương. Đi dạo mát. Giá vé 100k hợp lý. Nên đi buổi sáng sớm.", "sentiment": 0.78, "trust": 0.8},
            {"author": "Kim Chi", "rating": 3, "text": "Không ấn tượng lắm, hơi tourist trap. Nhưng view đẹp, hoa nhiều màu. Đi 1 lần cho biết.", "sentiment": 0.45, "trust": 0.75},
        ]
    },
    {
        "place_id": "dalat_langbiang",
        "place_name": "Núi LangBiang Đà Lạt",
        "reviews": [
            {"author": "Hai Long", "rating": 5, "text": "Leo núi LangBiang là trải nghiệm tuyệt vời! Đỉnh núi 2167m, view 360 độ. Có 2 option: đi jeep (150k) hoặc trekking 3h. Nên trekking!", "sentiment": 0.92, "trust": 0.9},
            {"author": "Thu Thao", "rating": 5, "text": "View đỉnh LangBiang siêu đẹp, nhìn thấy cả Đà Lạt. Trekking khoảng 3 tiếng, đường đi đẹp. Mang áo ấm vì đỉnh núi lạnh.", "sentiment": 0.9, "trust": 0.88},
            {"author": "Duc Minh", "rating": 4, "text": "Leo núi mệt nhưng xứng đáng. Không khí trong lành, view đẹp. Cần giày trekking và nước uống. Nên đi sáng sớm.", "sentiment": 0.78, "trust": 0.85},
        ]
    },
    {
        "place_id": "dalat_coffee",
        "place_name": "Coffee Đà Lạt",
        "reviews": [
            {"author": "Linh Dan", "rating": 5, "text": "Đà Lạt là thiên đường coffee! Mỗi quán mỗi phong cách. An Cafe (view đồi thông), La Viet (specialty), Trung Nguyên Legend. Giá 30-60k/ly.", "sentiment": 0.92, "trust": 0.88},
            {"author": "Phuong Uyen", "rating": 5, "text": "Ngồi cafe ngắm mưa Đà Lạt, không gì bằng! Recommend: An Cafe, Windmills coffee, The Married Beans. Atmosphere tuyệt vời.", "sentiment": 0.93, "trust": 0.87},
        ]
    },
    # PHU QUOC
    {
        "place_id": "phuquoc_sao_beach",
        "place_name": "Bãi Sao Phú Quốc",
        "reviews": [
            {"author": "Ngoc Trinh", "rating": 5, "text": "Bãi Sao đẹp nhất Phú Quốc! Cát trắng mịn, nước trong xanh. Thích hợp tắm biển, chụp hình. Giá ghế 50-100k. Đi sáng sớm tránh đông.", "sentiment": 0.93, "trust": 0.9},
            {"author": "Anh Khoa", "rating": 4, "text": "Biển đẹp thật nhưng cuối tuần đông. Có chỗ thuê sup, kayak. Ăn hải sản ngay biển. Giá hơi đắt hơn nơi khác.", "sentiment": 0.7, "trust": 0.83},
            {"author": "Thao Vy", "rating": 5, "text": "Wow biển đẹp quá! Nước trong như kính, cát trắng như tuyết. Instagram-worthy 100%. Nên đi ngày thường.", "sentiment": 0.95, "trust": 0.86},
        ]
    },
    {
        "place_id": "phuquoc_vinwonders",
        "place_name": "VinWonders Phú Quốc",
        "reviews": [
            {"author": "Tuan Anh", "rating": 5, "text": "VinWonders quy mô lớn, nhiều trò chơi. Đi cáp treo vượt biển 8km siêu đẹp. Aquarium, trò chơi nước, shows. Vé 880k nhưng chơi cả ngày.", "sentiment": 0.9, "trust": 0.88},
            {"author": "My Hanh", "rating": 4, "text": "Thích hợp gia đình và trẻ nhỏ. Nhiều zone: trượt nước, aquarium, safari. Cần ít nhất 1 ngày full. Giá hơi cao nhưng worth it.", "sentiment": 0.78, "trust": 0.85},
        ]
    },
    {
        "place_id": "phuquoc_night_market",
        "place_name": "Chợ đêm Phú Quốc",
        "reviews": [
            {"author": "Hoang Yen", "rating": 4, "text": "Chợ đêm Phú Quốc nhiều hải sản tươi sống. Nhum biển, cua hoàng đế, mực nướng. Giá 100-300k/phần. Nên mặc cả. Đi từ 5h chiều.", "sentiment": 0.8, "trust": 0.85},
            {"author": "Van Anh", "rating": 4, "text": "Ăn hải sản ở chợ đêm là must do! Tôm hùm nướng, ốc len nướng, bánh tráng nướng. Giá hợp lý hơn nhà hàng. Đông người nhưng vui.", "sentiment": 0.82, "trust": 0.84},
            {"author": "Quang Dat", "rating": 3, "text": "Chợ đêm đông và hơi nóng. Hải sản tươi nhưng giá hơi đắt cho khách du lịch. Nên hỏi giá trước khi gọi. Có hàng lưu niệm đẹp.", "sentiment": 0.55, "trust": 0.8},
        ]
    },
    # HOI AN
    {
        "place_id": "hoian_old_town",
        "place_name": "Phố cổ Hội An",
        "reviews": [
            {"author": "Bich Ngoc", "rating": 5, "text": "Hội An đẹp nhất vào buổi tối khi đèn lồng sáng. Phố cổ có charm riêng, kiến trúc Nhật-Việt-Hoa pha trộn. Vé tham quan 120k/5 điểm.", "sentiment": 0.93, "trust": 0.91},
            {"author": "Trung Hieu", "rating": 5, "text": "Đã đến Hội An 3 lần và lần nào cũng thích. Buổi tối thả đèn trên sông Hoài, ăn cao lầu, uống cà phê. Không gian lãng mạn.", "sentiment": 0.92, "trust": 0.9},
            {"author": "Phuong Anh", "rating": 4, "text": "Phố cổ đẹp nhưng đông khách du lịch. Nên đi sáng sớm hoặc tối muộn. Giá đồ ăn hơi cao hơn bình thường. An Cong cafe view đẹp.", "sentiment": 0.68, "trust": 0.85},
        ]
    },
    {
        "place_id": "hoian_an_bang_beach",
        "place_name": "Biển An Bàng Hội An",
        "reviews": [
            {"author": "Duc Huy", "rating": 5, "text": "An Bàng đẹp và ít đông hơn Cửa Đại. Cát mịn, nước trong. Nhiều beach bar chill. Ăn hải sản ngay biển. Giá ghế 30-50k.", "sentiment": 0.9, "trust": 0.88},
            {"author": "Thuy Linh", "rating": 4, "text": "Biển đẹp, thích hợp relax. Có surf cho người thích sport. Beach bar Soul Kitchen và Sound of Silence rất hay. Sunset đẹp.", "sentiment": 0.85, "trust": 0.86},
        ]
    },
    {
        "place_id": "hoian_food",
        "place_name": "Ẩm thực Hội An",
        "reviews": [
            {"author": "Khanh Vy", "rating": 5, "text": "Hội An là thiên đường ăn uống! Cao lầu, mì quảng, bánh mì Phượng, cơm gà, bánh bao bánh vạc. Mọi món đều ngon và rẻ (20-50k).", "sentiment": 0.95, "trust": 0.9},
            {"author": "Nhat Minh", "rating": 5, "text": "Bánh mì Phượng được CNN bình chọn ngon nhất! Cao lầu chỉ có ở Hội An. Cơm gà Bà Buội, mì quảng Ông Hai. Giá bình dân.", "sentiment": 0.92, "trust": 0.89},
            {"author": "Mai Phuong", "rating": 5, "text": "Ăn 5 bữa/ngày ở Hội An vẫn không đủ! White Rose, Bánh Bao Bánh Vạc là món độc nhất. Chợ đêm Hội An nhiều đồ ăn ngon.", "sentiment": 0.9, "trust": 0.87},
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
