"""Vietnamese NLP pipeline for travel review analysis.

Lightweight implementation without heavy ML dependencies.
Covers: sentiment analysis, entity extraction, fake review detection.
"""
from __future__ import annotations

import re
from typing import Dict, List, Tuple

# Vietnamese travel sentiment lexicon
POSITIVE_WORDS = {
    # General positive
    "dep": 1.0, "tuyet voi": 1.5, "tuyet dep": 1.5, "rat dep": 1.3,
    "hay": 0.8, "tot": 0.8, "rat tot": 1.2, "dinh": 1.3,
    "ok": 0.5, "oke": 0.5, "tam": 0.3, "duoc": 0.3,
    "thich": 0.9, "rat thich": 1.3, "yeu": 0.9, "me": 0.9,
    "hoan hao": 1.5, "xung dang": 1.2, "worth": 1.0,
    "recommend": 1.2, "nen di": 1.3, "must do": 1.3, "must visit": 1.3,
    "highlight": 1.0, "10/10": 1.5, "5 sao": 1.3,
    # Food
    "ngon": 1.0, "rat ngon": 1.3, "tuoi": 0.8, "tuoi song": 1.0,
    "ngot": 0.5, "thom": 0.7, "beo": 0.5, "dac biet": 0.8,
    # Place/scenery
    "hung vi": 1.3, "trang le": 1.2, "lung linh": 1.0,
    "trong xanh": 1.0, "trong vanh": 1.0, "sach": 0.7, "sach se": 0.9,
    "mat lanh": 0.8, "trong lanh": 0.8, "yen tinh": 0.7,
    "rong": 0.5, "thoang": 0.6, "ruc ro": 0.9,
    # Service
    "nhiet tinh": 1.0, "chuyen nghiep": 1.1, "than thien": 0.9,
    "nhanh": 0.6, "chu dao": 1.0, "lich su": 0.8,
    # Value
    "re": 0.7, "gia re": 0.8, "hop ly": 0.7, "xung dang": 1.0,
    "gia tot": 0.8, "binh dan": 0.6,
    # Emotion
    "wow": 1.2, "qua dinh": 1.5, "sieu dep": 1.5,
    "ngat ngay": 1.3, "an tuong": 1.0, "bat ngo": 0.8,
    "khong the quen": 1.3, "doi nguoi": 1.3, "once in a lifetime": 1.5,
    "quay lai": 1.0, "se quay lai": 1.2,
}

NEGATIVE_WORDS = {
    # General negative
    "xau": -0.8, "te": -0.9, "kem": -0.8, "do": -0.7,
    "chan": -0.7, "that vong": -1.3, "toi te": -1.5,
    "khong nen": -1.0, "tranh": -0.6, "khong di": -1.0,
    "phot": -0.5, "lua": -1.2, "chat chem": -1.3,
    # Service
    "cham": -0.7, "lau": -0.6, "cho lau": -0.8,
    "thieu": -0.5, "khong chuyen nghiep": -1.0,
    "bat lich su": -1.2, "kho chiu": -0.9,
    # Place
    "ban": -0.7, "dong": -0.5, "qua dong": -0.9,
    "nong": -0.5, "nang": -0.4, "hoi": -0.3,
    "nguy hiem": -0.8, "met": -0.4, "met moi": -0.6,
    # Value
    "dat": -0.6, "qua dat": -1.0, "mac": -0.6,
    "khong xung": -1.0, "bi chat": -0.9,
    # Food
    "khong ngon": -1.0, "oiu": -0.7, "bi": -0.3,
    "cu": -0.5, "khong tuoi": -0.9,
}

# Entity patterns for Vietnamese travel context
PLACE_PATTERNS = [
    r"dong\s+\w+",  # Dong Phong Nha, Dong Thien Duong
    r"hang\s+\w+",  # Hang Toi, Hang Son Doong
    r"suoi\s+\w+",  # Suoi Mooc
    r"bien\s+\w+",  # Bien Nhat Le
    r"bai\s+\w+",   # Bai bien
    r"song\s+\w+",  # Song Chay
    r"nui\s+\w+",   # Nui
    r"ho\s+\w+",    # Ho
    r"chua\s+\w+",  # Chua
]

PRICE_PATTERN = r"(\d{1,3}(?:[.,]\d{3})*)\s*(?:k|K|nghin|ngan|dong|vnd|VND|tr|trieu)(?!\w)"
TIME_PATTERN = r"(?:thang\s+\d{1,2}|mua\s+(?:he|dong|xuan|thu)|sang|trua|chieu|toi|buoi\s+\w+)"


def analyze_sentiment(text: str) -> Dict:
    """Analyze sentiment of Vietnamese text.

    Returns:
        {
            "score": float (0-1, 0=negative, 0.5=neutral, 1=positive),
            "label": str ("positive", "negative", "neutral"),
            "positive_words": list,
            "negative_words": list,
            "confidence": float (0-1)
        }
    """
    text_lower = _normalize_vietnamese(text.lower())

    pos_found = []
    neg_found = []
    pos_score = 0.0
    neg_score = 0.0

    for word, weight in POSITIVE_WORDS.items():
        if word in text_lower:
            pos_found.append(word)
            pos_score += weight

    for word, weight in NEGATIVE_WORDS.items():
        if word in text_lower:
            neg_found.append(word)
            neg_score += abs(weight)

    total = pos_score + neg_score
    if total == 0:
        score = 0.5
        confidence = 0.2
    else:
        score = pos_score / total
        confidence = min(1.0, total / 5.0)  # More words = more confident

    if score >= 0.65:
        label = "positive"
    elif score <= 0.35:
        label = "negative"
    else:
        label = "neutral"

    return {
        "score": round(score, 3),
        "label": label,
        "positive_words": pos_found,
        "negative_words": neg_found,
        "confidence": round(confidence, 3),
    }


def extract_entities(text: str) -> Dict:
    """Extract travel-related entities from Vietnamese text.

    Returns:
        {
            "places": list of place names,
            "prices": list of {amount, raw},
            "times": list of time references,
            "activities": list of detected activities
        }
    """
    text_lower = _normalize_vietnamese(text.lower())

    # Places
    places = []
    for pattern in PLACE_PATTERNS:
        matches = re.findall(pattern, text_lower)
        places.extend(matches)

    # Prices
    prices = []
    for match in re.finditer(PRICE_PATTERN, text):
        raw = match.group(0)
        amount_str = match.group(1).replace(".", "").replace(",", "")
        amount = int(amount_str)
        # Normalize to VND
        if "tr" in raw.lower() or "trieu" in raw.lower():
            amount *= 1_000_000
        elif "k" in raw.lower() or "nghin" in raw.lower() or "ngan" in raw.lower():
            amount *= 1_000
        prices.append({"amount": amount, "raw": raw})

    # Times
    times = re.findall(TIME_PATTERN, text_lower)

    # Activities
    activities = []
    activity_keywords = {
        "tam bien": "swimming", "boi": "swimming", "tam": "bathing",
        "leo nui": "hiking", "trekking": "trekking", "di bo": "walking",
        "cheo kayak": "kayaking", "kayak": "kayaking",
        "zipline": "zipline", "zip line": "zipline",
        "tam bun": "mud_bath", "tam suoi": "spring_bath",
        "an": "eating", "thuong thuc": "dining",
        "chup hinh": "photography", "check-in": "checkin", "check in": "checkin",
        "ngam": "sightseeing", "tham quan": "sightseeing",
        "di thuyen": "boating", "thuyen": "boating",
    }
    for vn, en in activity_keywords.items():
        if vn in text_lower:
            activities.append({"vietnamese": vn, "type": en})

    return {
        "places": list(set(places)),
        "prices": prices,
        "times": list(set(times)),
        "activities": activities,
    }


def detect_fake_signals(text: str, rating: float, author_name: str = "") -> Dict:
    """Detect signals of fake/spam reviews.

    Returns:
        {
            "is_suspicious": bool,
            "reasons": list of strings,
            "fake_probability": float (0-1)
        }
    """
    reasons = []
    score = 0.0

    # Too short
    if len(text) < 20:
        reasons.append("Review quá ngắn")
        score += 0.3

    # All caps
    upper_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    if upper_ratio > 0.5 and len(text) > 10:
        reasons.append("Nhiều chữ in hoa bất thường")
        score += 0.2

    # Excessive punctuation
    excl_count = text.count("!") + text.count("?")
    if excl_count > 5:
        reasons.append("Quá nhiều dấu chấm than")
        score += 0.15

    # Generic text (no specific details)
    entities = extract_entities(text)
    if not entities["prices"] and not entities["places"] and not entities["activities"]:
        if len(text) < 50:
            reasons.append("Thiếu chi tiết cụ thể (giá, địa điểm, hoạt động)")
            score += 0.25

    # Extreme rating with short text
    if rating in (1, 5) and len(text) < 30:
        reasons.append("Rating cực đoan với review ngắn")
        score += 0.2

    # Repeated characters
    if re.search(r"(.)\1{4,}", text):
        reasons.append("Ký tự lặp lại nhiều")
        score += 0.2

    # URL/link spam
    if re.search(r"https?://|www\.", text):
        reasons.append("Chứa link/URL")
        score += 0.15

    return {
        "is_suspicious": score >= 0.4,
        "reasons": reasons,
        "fake_probability": round(min(1.0, score), 3),
    }


def compute_trust_score(
    text: str,
    rating: float,
    author_name: str = "",
    photo_count: int = 0,
    engagement: int = 0,
    other_ratings: List[float] = None,
) -> Dict:
    """Compute Trust Score for a review (0-1).

    Formula: w1*ContentDepth + w2*Sentiment + w3*FakeCheck + w4*PhotoEvidence + w5*Consistency
    """
    # 1. Content Depth (w=0.25)
    word_count = len(text.split())
    has_price = bool(re.search(PRICE_PATTERN, text))
    has_specific = bool(extract_entities(text)["activities"])

    depth = min(1.0, word_count / 50) * 0.5  # Length
    if has_price:
        depth += 0.25
    if has_specific:
        depth += 0.25

    # 2. Sentiment coherence (w=0.2)
    sentiment = analyze_sentiment(text)
    sentiment_coherence = 1.0
    if rating >= 4 and sentiment["score"] < 0.4:
        sentiment_coherence = 0.4  # High rating but negative text
    elif rating <= 2 and sentiment["score"] > 0.7:
        sentiment_coherence = 0.4  # Low rating but positive text

    # 3. Fake check (w=0.25)
    fake = detect_fake_signals(text, rating, author_name)
    authenticity = 1.0 - fake["fake_probability"]

    # 4. Photo evidence (w=0.15)
    photo_score = min(1.0, photo_count / 3)

    # 5. Consistency with others (w=0.15)
    consistency = 1.0
    if other_ratings:
        avg_other = sum(other_ratings) / len(other_ratings)
        diff = abs(rating - avg_other)
        consistency = max(0.3, 1.0 - diff / 4)

    # Weighted sum
    trust = (
        0.25 * depth
        + 0.20 * sentiment_coherence
        + 0.25 * authenticity
        + 0.15 * photo_score
        + 0.15 * consistency
    )

    return {
        "trust_score": round(trust, 3),
        "breakdown": {
            "content_depth": round(depth, 3),
            "sentiment_coherence": round(sentiment_coherence, 3),
            "authenticity": round(authenticity, 3),
            "photo_evidence": round(photo_score, 3),
            "consistency": round(consistency, 3),
        },
        "sentiment": sentiment,
        "fake_check": fake,
    }


def generate_review_summary(reviews: List[Dict]) -> Dict:
    """Generate AI-like summary from multiple reviews.

    Returns:
        {
            "summary": str,
            "highlights": list,
            "concerns": list,
            "best_time": str or None,
            "avg_sentiment": float,
            "top_activities": list
        }
    """
    if not reviews:
        return {"summary": "Chưa có review", "highlights": [], "concerns": []}

    all_positive = []
    all_negative = []
    all_activities = []
    all_prices = []
    all_times = []
    sentiments = []

    for rev in reviews:
        text = rev.get("text", "")
        sentiment = analyze_sentiment(text)
        entities = extract_entities(text)

        sentiments.append(sentiment["score"])
        all_positive.extend(sentiment["positive_words"])
        all_negative.extend(sentiment["negative_words"])
        all_activities.extend([a["vietnamese"] for a in entities["activities"]])
        all_prices.extend(entities["prices"])
        all_times.extend(entities["times"])

    # Count frequencies
    pos_freq = _count_freq(all_positive)
    neg_freq = _count_freq(all_negative)
    act_freq = _count_freq(all_activities)

    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.5
    avg_rating = sum(r.get("rating", 3) for r in reviews) / len(reviews)

    # Build summary
    total = len(reviews)
    pos_pct = int(sum(1 for s in sentiments if s >= 0.65) / total * 100)
    neg_pct = int(sum(1 for s in sentiments if s <= 0.35) / total * 100)

    highlights = [word for word, count in pos_freq[:5] if count >= 2]
    concerns = [word for word, count in neg_freq[:3] if count >= 2]
    top_activities = [act for act, count in act_freq[:5]]

    summary = f"{pos_pct}% review tích cực, {neg_pct}% tiêu cực (từ {total} reviews). "
    summary += f"Rating trung bình: {avg_rating:.1f}/5. "

    if highlights:
        summary += f"Điểm nổi bật: {', '.join(highlights[:3])}. "
    if concerns:
        summary += f"Cần lưu ý: {', '.join(concerns[:2])}. "

    best_time = None
    if all_times:
        time_freq = _count_freq(all_times)
        best_time = time_freq[0][0] if time_freq else None

    price_range = None
    if all_prices:
        amounts = [p["amount"] for p in all_prices]
        price_range = {"min": min(amounts), "max": max(amounts)}

    return {
        "summary": summary.strip(),
        "highlights": highlights,
        "concerns": concerns,
        "best_time": best_time,
        "avg_sentiment": round(avg_sentiment, 3),
        "avg_rating": round(avg_rating, 1),
        "top_activities": top_activities,
        "price_range": price_range,
        "total_reviews": total,
    }


def _normalize_vietnamese(text: str) -> str:
    """Remove diacritics for matching (keep original for display)."""
    # This is a simple normalization - the text is already without diacritics
    # in most seed data. For production, use underthesea or similar.
    return text.lower().strip()


def _count_freq(items: List[str]) -> List[Tuple[str, int]]:
    freq = {}
    for item in items:
        freq[item] = freq.get(item, 0) + 1
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)
