#!/usr/bin/env python3
"""
TravelMind — Automated Test Suite
===================================
Self-contained test: starts servers, runs all tests, reports, cleans up.

Usage:
    python3 test_all.py              # Run all tests
    python3 test_all.py --skip-start # Skip server start (if already running)
    python3 test_all.py --verbose    # Show detailed output
"""

import sys
import os
import json
import time
import signal
import subprocess
import re
import urllib.request
import urllib.error
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_DIR, "backend")
FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
DB_PATH = os.path.join(BACKEND_DIR, "travelmind.db")

VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv
SKIP_START = "--skip-start" in sys.argv

# ─── Colors ───────────────────────────────────────────────────────────
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# ─── Test Results ─────────────────────────────────────────────────────
results = {"passed": 0, "failed": 0, "errors": [], "warnings": []}
processes = []


def log(msg, color=RESET):
    print(f"{color}{msg}{RESET}")


def log_test(name, passed, detail=""):
    if passed:
        results["passed"] += 1
        symbol = f"{GREEN}✓{RESET}"
    else:
        results["failed"] += 1
        results["errors"].append(f"{name}: {detail}")
        symbol = f"{RED}✗{RESET}"
    extra = f" — {detail}" if detail and (not passed or VERBOSE) else ""
    print(f"  {symbol} {name}{extra}")


def warn(msg):
    results["warnings"].append(msg)
    print(f"  {YELLOW}⚠ {msg}{RESET}")


# ─── HTTP Helpers ─────────────────────────────────────────────────────
def http_get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode(), json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except:
            return e.code, {"raw": body}
    except Exception as e:
        return 0, {"error": str(e)}


def http_post(url, data, headers=None):
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.getcode(), json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except:
            return e.code, {"raw": raw}
    except Exception as e:
        return 0, {"error": str(e)}


def http_delete(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {}, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode(), json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())
    except Exception as e:
        return 0, {"error": str(e)}


def http_status(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except:
        return 0


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


# ─── Server Management ────────────────────────────────────────────────
def start_servers():
    log("\n🔧 Starting servers...", CYAN)

    # Clean DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Init DB + seed
    subprocess.run([sys.executable, "-c",
        "from database import engine, Base; from models import *; Base.metadata.create_all(bind=engine)"],
        cwd=BACKEND_DIR, capture_output=True)
    subprocess.run([sys.executable, "seed_data.py"], cwd=BACKEND_DIR, capture_output=True)
    subprocess.run([sys.executable, "seed_destinations.py"], cwd=BACKEND_DIR, capture_output=True)
    log("  DB seeded", GREEN)

    # Start backend
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=BACKEND_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    processes.append(backend)

    # Wait for backend
    for i in range(20):
        try:
            urllib.request.urlopen(f"{BACKEND_URL}/health", timeout=2)
            log("  Backend started ✓", GREEN)
            break
        except:
            time.sleep(0.5)
    else:
        log("  Backend FAILED to start", RED)
        sys.exit(1)

    # Check frontend (assume already running via npm run dev)
    try:
        urllib.request.urlopen(FRONTEND_URL, timeout=3)
        log("  Frontend detected ✓", GREEN)
    except:
        log("  Frontend not running — skipping frontend tests", YELLOW)
        return False

    return True


def stop_servers():
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=5)
        except:
            p.kill()


# ═══════════════════════════════════════════════════════════════════════
# TEST SUITES
# ═══════════════════════════════════════════════════════════════════════

def test_health():
    log("\n📋 Health & Root", BOLD)
    code, data = http_get(f"{BACKEND_URL}/health")
    log_test("GET /health", code == 200 and data.get("status") == "ok")

    code, data = http_get(f"{BACKEND_URL}/")
    log_test("GET /", code == 200 and "TravelMind" in data.get("message", ""))


def test_waitlist():
    log("\n📧 Waitlist", BOLD)

    code, data = http_post(f"{BACKEND_URL}/api/waitlist/", {"email": "test-wl@qa.com", "name": "QA"})
    log_test("POST valid email", code == 200 and data.get("id"))

    code, data = http_post(f"{BACKEND_URL}/api/waitlist/", {"email": "test-wl@qa.com"})
    log_test("Duplicate email → 400", code == 400)

    code, data = http_post(f"{BACKEND_URL}/api/waitlist/", {"email": ""})
    log_test("Empty email → 400", code == 400)

    code, data = http_post(f"{BACKEND_URL}/api/waitlist/", {"email": "invalid"})
    log_test("Invalid email → 400", code == 400)

    code, data = http_post(f"{BACKEND_URL}/api/waitlist/", {})
    log_test("Missing email → 422", code == 422)


def test_auth():
    log("\n🔐 Auth", BOLD)

    # Register
    code, data = http_post(f"{BACKEND_URL}/api/auth/register",
        {"email": "auth@qa.com", "password": "test123", "name": "QA Auth"})
    log_test("Register", code == 200 and data.get("token"))
    token = data.get("token", "")

    # Register duplicate
    code, data = http_post(f"{BACKEND_URL}/api/auth/register",
        {"email": "auth@qa.com", "password": "test123"})
    log_test("Register duplicate → 400", code == 400)

    # Validation
    code, _ = http_post(f"{BACKEND_URL}/api/auth/register", {"email": "bad", "password": "123456"})
    log_test("Invalid email → 400", code == 400)

    code, _ = http_post(f"{BACKEND_URL}/api/auth/register", {"email": "a@b.com", "password": "12"})
    log_test("Short password → 400", code == 400)

    # Login
    code, data = http_post(f"{BACKEND_URL}/api/auth/login",
        {"email": "auth@qa.com", "password": "test123"})
    log_test("Login", code == 200 and data.get("token"))

    code, _ = http_post(f"{BACKEND_URL}/api/auth/login",
        {"email": "auth@qa.com", "password": "wrong"})
    log_test("Wrong password → 401", code == 401)

    # Me
    code, data = http_get(f"{BACKEND_URL}/api/auth/me", auth_header(token))
    log_test("GET /me with token", code == 200 and data.get("email") == "auth@qa.com")
    log_test("Has referral_code", bool(data.get("referral_code")))

    code, _ = http_get(f"{BACKEND_URL}/api/auth/me")
    log_test("GET /me no token → 401", code == 401)

    code, _ = http_get(f"{BACKEND_URL}/api/auth/me", auth_header("invalid.token"))
    log_test("Invalid token → 401", code == 401)

    return token


def test_referral(token_a):
    log("\n🎁 Referral", BOLD)
    code, data = http_get(f"{BACKEND_URL}/api/auth/me", auth_header(token_a))
    ref_code = data.get("referral_code", "")

    code, data = http_post(f"{BACKEND_URL}/api/auth/register",
        {"email": "referred@qa.com", "password": "123456", "referral_code": ref_code})
    log_test("Register with referral", code == 200)

    code, data = http_get(f"{BACKEND_URL}/api/auth/me", auth_header(token_a))
    log_test("Referrer count incremented", data.get("referral_count", 0) == 1)


def test_profile(token):
    log("\n🧬 Travel DNA Profile", BOLD)

    dna = {
        "persona": "couple", "budget_range": "medium",
        "energy_level": "chill", "food_preferences": ["seafood"],
        "accommodation_style": "homestay", "deal_breakers": ["no_crowds"]
    }

    code, data = http_post(f"{BACKEND_URL}/api/profile/travel-dna",
        {"email": "auth@qa.com", "travel_dna": dna}, auth_header(token))
    log_test("Save Travel DNA", code == 200 and data.get("message"))

    code, data = http_get(f"{BACKEND_URL}/api/profile/travel-dna/auth@qa.com")
    log_test("Get Travel DNA", code == 200 and data.get("travel_dna", {}).get("persona") == "couple")

    # Auth check: can't modify others
    code, _ = http_post(f"{BACKEND_URL}/api/profile/travel-dna",
        {"email": "other@qa.com", "travel_dna": dna}, auth_header(token))
    log_test("Modify other profile → 403", code == 403)

    code, _ = http_get(f"{BACKEND_URL}/api/profile/travel-dna/nonexistent@qa.com")
    log_test("Unknown user → 404", code == 404)


def test_itinerary(token):
    log("\n🗺 Itinerary", BOLD)

    destinations = ["Quang Binh", "Da Lat", "Phu Quoc", "Hoi An"]
    itinerary_id = None

    for dest in destinations:
        code, data = http_post(f"{BACKEND_URL}/api/itinerary/generate",
            {"destination": dest, "num_days": 3, "budget": 3000000, "email": "auth@qa.com"})
        ok = code == 200 and data.get("itinerary_data", {}).get("days")
        log_test(f"Generate {dest}", ok)
        if dest == destinations[0]:
            itinerary_id = data.get("id")

    # Get by ID
    code, data = http_get(f"{BACKEND_URL}/api/itinerary/{itinerary_id}")
    log_test("Get itinerary by ID", code == 200 and data.get("destination"))

    code, _ = http_get(f"{BACKEND_URL}/api/itinerary/99999")
    log_test("Get nonexistent → 404", code == 404)

    # Itinerary has review_summaries
    code, data = http_get(f"{BACKEND_URL}/api/itinerary/{itinerary_id}")
    has_reviews = bool(data.get("itinerary_data", {}).get("review_summaries"))
    log_test("Itinerary includes review summaries", has_reviews)

    # Save/unsave
    code, data = http_post(f"{BACKEND_URL}/api/auth/save-itinerary/{itinerary_id}", {}, auth_header(token))
    log_test("Save itinerary", code == 200 and itinerary_id in data.get("saved", []))

    code, data = http_get(f"{BACKEND_URL}/api/auth/my-itineraries", auth_header(token))
    log_test("My itineraries (created)", len(data.get("created", [])) >= 1)
    log_test("My itineraries (saved)", len(data.get("saved", [])) >= 1)

    code, data = http_delete(f"{BACKEND_URL}/api/auth/save-itinerary/{itinerary_id}", auth_header(token))
    log_test("Unsave itinerary", code == 200 and itinerary_id not in data.get("saved", []))

    return itinerary_id


def test_reviews():
    log("\n⭐ Reviews", BOLD)

    code, data = http_get(f"{BACKEND_URL}/api/reviews/places/all")
    place_count = len(data.get("places", []))
    log_test(f"List places ({place_count})", code == 200 and place_count >= 10)

    code, data = http_get(f"{BACKEND_URL}/api/reviews/dark_cave")
    log_test("Get reviews by place", code == 200 and data.get("total_reviews", 0) > 0)
    log_test("Has avg_rating", data.get("avg_rating", 0) > 0)
    log_test("Has avg_trust_score", data.get("avg_trust_score", 0) > 0)

    code, data = http_get(f"{BACKEND_URL}/api/reviews/dark_cave/summary")
    log_test("Review summary (NLP)", code == 200 and data.get("summary"))
    log_test("Summary has highlights", len(data.get("highlights", [])) > 0)

    code, data = http_get(f"{BACKEND_URL}/api/reviews/dark_cave/analyze")
    log_test("Review NLP analyze", code == 200 and len(data.get("analysis", [])) > 0)
    if data.get("analysis"):
        a = data["analysis"][0]
        log_test("Has trust_score", "trust_score" in a)
        log_test("Has sentiment", "sentiment" in a)
        log_test("Has fake_check", "fake_check" in a)
        log_test("Has entities", "entities" in a)

    # Submit review
    code, data = http_post(f"{BACKEND_URL}/api/reviews/submit", {
        "place_id": "dark_cave", "place_name": "Hang Toi",
        "rating": 5, "text": "Trai nghiem tuyet voi! Zipline rat dep, tam bun vui. Gia 450k xung dang!"
    })
    log_test("Submit review", code == 200 and data.get("trust_score", 0) > 0)
    log_test("Auto NLP sentiment", data.get("sentiment", {}).get("label") == "positive")

    # Validation
    code, _ = http_post(f"{BACKEND_URL}/api/reviews/submit",
        {"place_id": "x", "place_name": "X", "rating": 0, "text": "valid text here"})
    log_test("Rating 0 → 400", code == 400)

    code, _ = http_post(f"{BACKEND_URL}/api/reviews/submit",
        {"place_id": "x", "place_name": "X", "rating": 5, "text": "short"})
    log_test("Short review → 400", code == 400)


def test_search():
    log("\n🔍 Search", BOLD)

    code, data = http_get(f"{BACKEND_URL}/api/search?q=phong+nha")
    log_test("Search 'phong nha'", code == 200 and data.get("total", 0) > 0)

    code, data = http_get(f"{BACKEND_URL}/api/search?q=quang+binh")
    has_dest = len(data.get("destinations", [])) > 0
    log_test("Search finds destination", has_dest)

    code, data = http_get(f"{BACKEND_URL}/api/search?q=xyznonexistent")
    log_test("Search no results", code == 200 and data.get("total", 0) == 0)


def test_concierge():
    log("\n💬 AI Concierge", BOLD)

    topics = [
        ("an gi o quang binh?", "food", ["Bánh", "sản"]),
        ("thoi tiet thang 5?", "weather", ["tháng", "mùa"]),
        ("hang toi co gi?", "dark_cave", ["Hang Tối", "Dark Cave"]),
        ("o dau khi di quang binh?", "accommodation", ["Phong Nha", "Đồng Hới"]),
        ("phong nha the nao?", "phong_nha", ["Phong Nha"]),
        ("di quang binh may ngay?", "itinerary", ["Ngày"]),
        ("hello", "fallback", ["Concierge", "giúp"]),
    ]

    for msg, topic, keywords in topics:
        code, data = http_post(f"{BACKEND_URL}/api/concierge/chat",
            {"message": msg})
        reply = data.get("reply", "")
        has_keyword = any(k.lower() in reply.lower() for k in keywords)
        log_test(f"Chat '{msg}' → {topic}", code == 200 and has_keyword,
                 f"missing keywords" if not has_keyword else "")

    # Has suggestions
    code, data = http_post(f"{BACKEND_URL}/api/concierge/chat", {"message": "hello"})
    log_test("Chat has suggestions", len(data.get("suggestions", [])) > 0)


def test_group(token):
    log("\n👥 Group Planning", BOLD)

    # Create
    code, data = http_post(f"{BACKEND_URL}/api/group/create",
        {"name": "QA Trip", "destination": "Quang Binh", "num_days": 3}, auth_header(token))
    log_test("Create group", code == 200 and data.get("code"))
    group_code = data.get("code", "")

    # Get
    code, data = http_get(f"{BACKEND_URL}/api/group/{group_code}")
    log_test("Get group", code == 200 and data.get("member_count", 0) >= 1)
    log_test("Has votable places", len(data.get("places", [])) > 0)

    # Join
    code, data = http_post(f"{BACKEND_URL}/api/group/{group_code}/join", {"name": "Guest"})
    log_test("Join group", code == 200 and len(data.get("members", [])) >= 2)

    # Vote
    code, data = http_post(f"{BACKEND_URL}/api/group/{group_code}/vote",
        {"place_id": "dark_cave"}, auth_header(token))
    log_test("Vote place", code == 200)

    # Verify vote persisted
    code, data = http_get(f"{BACKEND_URL}/api/group/{group_code}")
    dark_cave = next((p for p in data.get("places", []) if p["id"] == "dark_cave"), {})
    log_test("Vote persisted", dark_cave.get("votes", 0) >= 1)

    # Toggle vote off
    code, _ = http_post(f"{BACKEND_URL}/api/group/{group_code}/vote",
        {"place_id": "dark_cave"}, auth_header(token))
    code, data = http_get(f"{BACKEND_URL}/api/group/{group_code}")
    dark_cave = next((p for p in data.get("places", []) if p["id"] == "dark_cave"), {})
    log_test("Vote toggle off", dark_cave.get("votes", 0) == 0)

    # 404
    code, _ = http_get(f"{BACKEND_URL}/api/group/nonexistent")
    log_test("Unknown group → 404", code == 404)


def test_payment():
    log("\n💳 Payment", BOLD)

    code, data = http_get(f"{BACKEND_URL}/api/payment/pricing")
    tiers = data.get("tiers", [])
    log_test(f"Pricing tiers ({len(tiers)})", code == 200 and len(tiers) == 4)

    tier_names = [t["name"] for t in tiers]
    log_test("Has Free tier", "Free" in tier_names)
    log_test("Has Premium tier", "Premium" in tier_names)

    code, data = http_post(f"{BACKEND_URL}/api/payment/create-session",
        {"email": "test@qa.com", "tier": "explorer"})
    log_test("Create payment session (mock)", code == 200 and data.get("checkout_url"))

    code, _ = http_post(f"{BACKEND_URL}/api/payment/create-session",
        {"email": "test@qa.com", "tier": "invalid"})
    log_test("Invalid tier → 400", code == 400)


def test_admin():
    log("\n📊 Admin", BOLD)

    code, data = http_get(f"{BACKEND_URL}/api/admin/stats")
    overview = data.get("overview", {})
    log_test("Admin stats", code == 200)
    log_test("Has waitlist count", "waitlist" in overview)
    log_test("Has review count", overview.get("reviews", 0) > 0)
    log_test("Has places count", overview.get("places", 0) > 0)
    log_test("Has review_stats", len(data.get("review_stats", [])) > 0)


def test_frontend(has_frontend):
    if not has_frontend:
        log("\n🌐 Frontend — SKIPPED (not running)", YELLOW)
        return

    log("\n🌐 Frontend Pages", BOLD)

    pages = [
        ("/", "Landing"), ("/explore", "Explore"), ("/login", "Login"),
        ("/dashboard", "Dashboard"), ("/faq", "FAQ"), ("/reviews", "Reviews"),
        ("/compare", "Compare"), ("/profile", "Profile"), ("/itinerary", "Itinerary"),
        ("/chat", "Chat"), ("/pricing", "Pricing"), ("/admin", "Admin"),
        ("/destination/quang-binh", "Dest: QB"), ("/destination/da-lat", "Dest: DL"),
        ("/destination/phu-quoc", "Dest: PQ"), ("/destination/hoi-an", "Dest: HA"),
        ("/sitemap.xml", "Sitemap"), ("/robots.txt", "Robots"),
    ]

    for path, name in pages:
        code = http_status(f"{FRONTEND_URL}{path}")
        log_test(f"{name} ({path})", code == 200)

    # 404
    code = http_status(f"{FRONTEND_URL}/nonexistent-page-xyz")
    log_test("404 page", code == 404)

    # Manifest
    code = http_status(f"{FRONTEND_URL}/manifest.json")
    log_test("PWA manifest", code == 200)


def test_nlp():
    log("\n🧠 NLP Pipeline", BOLD)

    sys.path.insert(0, BACKEND_DIR)
    from services.nlp_vietnamese import analyze_sentiment, detect_fake_signals, compute_trust_score, extract_entities

    # Sentiment
    cases = [
        ("Dep tuyet voi, xung dang di!", "positive"),
        ("That vong, te, dat qua", "negative"),
        ("Wow sieu dep 10/10 se quay lai", "positive"),
        ("Toi te, ban, khong bao gio quay lai", "negative"),
    ]
    for text, expected in cases:
        result = analyze_sentiment(text)
        log_test(f"Sentiment '{text[:30]}...' → {expected}", result["label"] == expected)

    # Fake detection
    result = detect_fake_signals("tot", 5)
    log_test("Fake: short review", result["is_suspicious"])

    result = detect_fake_signals("Dong dep, di thuyen 1 tieng, ve 150k. Nen di sang som.", 5)
    log_test("Legit: detailed review", not result["is_suspicious"])

    # Entity extraction
    entities = extract_entities("Gia ve 150k, nen di thang 5")
    log_test("Extract prices", len(entities["prices"]) > 0)
    log_test("Extract times", len(entities["times"]) > 0)

    # Trust score
    result = compute_trust_score("Dong dep tuyet voi, thach nhu lung linh. Gia 150k. Nen di sang som.", 5)
    log_test("Trust score high for good review", result["trust_score"] > 0.6)

    result = compute_trust_score("tot", 5)
    log_test("Trust score low for short review", result["trust_score"] < 0.6)


def test_concurrent():
    log("\n⚡ Concurrent Requests", BOLD)
    import concurrent.futures

    def make_request(url):
        return http_status(url)

    urls = [f"{BACKEND_URL}/api/reviews/dark_cave"] * 20
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results_list = list(executor.map(make_request, urls))

    all_200 = all(c == 200 for c in results_list)
    log_test(f"20 concurrent review reads", all_200, f"codes: {set(results_list)}")

    urls = [f"{BACKEND_URL}/api/search?q=phong"] * 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results_list = list(executor.map(make_request, urls))
    all_200 = all(c == 200 for c in results_list)
    log_test(f"10 concurrent searches", all_200)


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    start_time = datetime.now()

    log(f"""
{'='*60}
  {BOLD}TravelMind — Automated Test Suite{RESET}
  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}""")

    try:
        if SKIP_START:
            log("\n⏭ Skipping server start (--skip-start)", YELLOW)
            has_frontend = http_status(FRONTEND_URL) == 200
        else:
            has_frontend = start_servers()

        # Run all test suites
        test_health()
        test_waitlist()
        token = test_auth()
        test_referral(token)
        test_profile(token)
        test_itinerary(token)
        test_reviews()
        test_search()
        test_concierge()
        test_group(token)
        test_payment()
        test_admin()
        test_nlp()
        test_concurrent()
        test_frontend(has_frontend)

    except KeyboardInterrupt:
        log("\n⚠ Interrupted", YELLOW)
    except Exception as e:
        log(f"\n💥 FATAL: {e}", RED)
        import traceback
        traceback.print_exc()
    finally:
        if not SKIP_START:
            stop_servers()

    # ─── Report ───
    elapsed = (datetime.now() - start_time).total_seconds()
    total = results["passed"] + results["failed"]

    log(f"""
{'='*60}
  {BOLD}TEST RESULTS{RESET}
{'='*60}

  {GREEN}Passed: {results['passed']}{RESET}
  {RED if results['failed'] else GREEN}Failed: {results['failed']}{RESET}
  Total:  {total}
  Time:   {elapsed:.1f}s
""")

    if results["warnings"]:
        log("  Warnings:", YELLOW)
        for w in results["warnings"]:
            log(f"    ⚠ {w}", YELLOW)
        print()

    if results["errors"]:
        log("  Failed tests:", RED)
        for e in results["errors"]:
            log(f"    ✗ {e}", RED)
        print()

    if results["failed"] == 0:
        log(f"  {GREEN}{BOLD}✓✓✓ ALL TESTS PASSED ✓✓✓{RESET}\n")
    else:
        log(f"  {RED}{BOLD}✗ {results['failed']} TESTS FAILED{RESET}\n")

    sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
