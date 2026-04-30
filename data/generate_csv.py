#!/usr/bin/env python3
"""
Generate sample CSV data files for the AI Insights Assistant.

Produces 6 CSV files in data/csv/ with realistic entertainment industry data
that supports the 6 required example questions:
1. Which titles performed best in 2025?
2. Why is Stellar Run trending recently?
3. Compare Dark Orbit vs Last Kingdom
4. Which city had the strongest engagement last month?
5. What explains weak comedy performance?
6. What recommendations would you give for leadership?

Uses a fixed random seed for reproducibility.
"""

import csv
import os
import random
from datetime import date, timedelta

# Fixed seed for reproducibility
random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv")


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def random_date(start: date, end: date) -> date:
    """Return a random date between start and end (inclusive)."""
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 0)))


def write_csv(filename: str, headers: list[str], rows: list[list]):
    """Write rows to a CSV file inside OUTPUT_DIR."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"  Written {len(rows)} rows -> {filepath}")


# ---------------------------------------------------------------------------
# 1. movies.csv  (50+ movies)
# ---------------------------------------------------------------------------

GENRES = ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller", "Horror", "Romance", "Animation"]
STUDIOS = ["Apex Studios", "Horizon Films", "Pinnacle Entertainment", "Nova Pictures", "Crescent Media"]
DIRECTORS = [
    "James Carter", "Sophia Lin", "Marcus Webb", "Elena Ruiz", "David Park",
    "Olivia Chen", "Ryan Mitchell", "Priya Sharma", "Lucas Fernandez", "Mia Johnson",
]

def generate_movies() -> list[dict]:
    """Generate 55 movies with specific entries to support required questions."""
    movies = []
    movie_id = 1

    # --- Key movies required by the example questions ---

    # Q1: Top performers in 2025 – several 2025 movies with varying revenue
    key_movies_2025 = [
        {"title": "Stellar Run",       "genre": "Sci-Fi",    "release_date": "2025-01-15", "duration": 138, "rating": 8.7, "budget": 95_000_000,  "revenue": 420_000_000, "director": "Sophia Lin",      "studio": "Apex Studios"},
        {"title": "Neon Horizon",      "genre": "Action",    "release_date": "2025-02-20", "duration": 125, "rating": 8.2, "budget": 110_000_000, "revenue": 380_000_000, "director": "James Carter",    "studio": "Horizon Films"},
        {"title": "The Last Ember",    "genre": "Drama",     "release_date": "2025-03-10", "duration": 142, "rating": 8.9, "budget": 45_000_000,  "revenue": 310_000_000, "director": "Elena Ruiz",      "studio": "Pinnacle Entertainment"},
        {"title": "Velocity",          "genre": "Action",    "release_date": "2025-04-05", "duration": 118, "rating": 7.8, "budget": 130_000_000, "revenue": 290_000_000, "director": "Marcus Webb",     "studio": "Nova Pictures"},
        {"title": "Echoes of Tomorrow","genre": "Sci-Fi",    "release_date": "2025-05-01", "duration": 155, "rating": 8.4, "budget": 100_000_000, "revenue": 350_000_000, "director": "David Park",      "studio": "Apex Studios"},
        {"title": "Midnight Bloom",    "genre": "Romance",   "release_date": "2025-01-28", "duration": 112, "rating": 7.5, "budget": 30_000_000,  "revenue": 150_000_000, "director": "Olivia Chen",     "studio": "Crescent Media"},
    ]

    # Q3: Dark Orbit vs Last Kingdom – different profiles
    comparison_movies = [
        {"title": "Dark Orbit",        "genre": "Sci-Fi",    "release_date": "2024-09-12", "duration": 148, "rating": 7.9, "budget": 120_000_000, "revenue": 340_000_000, "director": "James Carter",    "studio": "Apex Studios"},
        {"title": "Last Kingdom",      "genre": "Drama",     "release_date": "2024-11-05", "duration": 160, "rating": 8.6, "budget": 55_000_000,  "revenue": 260_000_000, "director": "Elena Ruiz",      "studio": "Pinnacle Entertainment"},
    ]

    # Q5: Weak comedy movies
    weak_comedies = [
        {"title": "Laugh Track",       "genre": "Comedy",    "release_date": "2024-06-15", "duration": 98,  "rating": 5.2, "budget": 25_000_000,  "revenue": 35_000_000,  "director": "Ryan Mitchell",   "studio": "Crescent Media"},
        {"title": "Funny Business",    "genre": "Comedy",    "release_date": "2024-08-20", "duration": 105, "rating": 4.8, "budget": 30_000_000,  "revenue": 28_000_000,  "director": "Mia Johnson",     "studio": "Nova Pictures"},
        {"title": "Joke's On You",     "genre": "Comedy",    "release_date": "2025-02-14", "duration": 92,  "rating": 5.5, "budget": 20_000_000,  "revenue": 22_000_000,  "director": "Ryan Mitchell",   "studio": "Crescent Media"},
        {"title": "Sitcom Dreams",     "genre": "Comedy",    "release_date": "2025-03-22", "duration": 100, "rating": 5.0, "budget": 18_000_000,  "revenue": 19_000_000,  "director": "Mia Johnson",     "studio": "Horizon Films"},
        {"title": "Punchline",         "genre": "Comedy",    "release_date": "2024-12-01", "duration": 95,  "rating": 5.8, "budget": 22_000_000,  "revenue": 30_000_000,  "director": "Lucas Fernandez", "studio": "Nova Pictures"},
    ]

    # Additional filler movies across genres and years
    filler_movies = [
        {"title": "Iron Veil",         "genre": "Action",    "release_date": "2024-01-20", "duration": 130, "rating": 7.4, "budget": 90_000_000,  "revenue": 220_000_000, "director": "Marcus Webb",     "studio": "Horizon Films"},
        {"title": "Crimson Tide II",   "genre": "Thriller",  "release_date": "2024-03-15", "duration": 122, "rating": 7.1, "budget": 70_000_000,  "revenue": 180_000_000, "director": "James Carter",    "studio": "Apex Studios"},
        {"title": "Whispers in Dark",  "genre": "Horror",    "release_date": "2024-10-25", "duration": 108, "rating": 6.8, "budget": 15_000_000,  "revenue": 95_000_000,  "director": "Priya Sharma",    "studio": "Crescent Media"},
        {"title": "Love in Paris",     "genre": "Romance",   "release_date": "2024-02-14", "duration": 115, "rating": 7.0, "budget": 28_000_000,  "revenue": 120_000_000, "director": "Olivia Chen",     "studio": "Pinnacle Entertainment"},
        {"title": "Pixel World",       "genre": "Animation", "release_date": "2024-07-04", "duration": 95,  "rating": 8.0, "budget": 80_000_000,  "revenue": 300_000_000, "director": "David Park",      "studio": "Nova Pictures"},
        {"title": "Shadow Protocol",   "genre": "Thriller",  "release_date": "2024-05-18", "duration": 128, "rating": 7.3, "budget": 65_000_000,  "revenue": 170_000_000, "director": "Sophia Lin",      "studio": "Apex Studios"},
        {"title": "Frozen Hearts",     "genre": "Drama",     "release_date": "2024-12-20", "duration": 135, "rating": 8.1, "budget": 40_000_000,  "revenue": 200_000_000, "director": "Elena Ruiz",      "studio": "Pinnacle Entertainment"},
        {"title": "Turbo Charge",      "genre": "Action",    "release_date": "2025-06-01", "duration": 115, "rating": 7.6, "budget": 100_000_000, "revenue": 250_000_000, "director": "Marcus Webb",     "studio": "Horizon Films"},
        {"title": "Nightmare Lane",    "genre": "Horror",    "release_date": "2025-04-18", "duration": 102, "rating": 6.5, "budget": 12_000_000,  "revenue": 80_000_000,  "director": "Priya Sharma",    "studio": "Crescent Media"},
        {"title": "Starlight Serenade","genre": "Romance",   "release_date": "2025-05-20", "duration": 120, "rating": 7.2, "budget": 35_000_000,  "revenue": 130_000_000, "director": "Olivia Chen",     "studio": "Nova Pictures"},
        {"title": "Toy Galaxy",        "genre": "Animation", "release_date": "2025-06-15", "duration": 90,  "rating": 8.3, "budget": 85_000_000,  "revenue": 320_000_000, "director": "David Park",      "studio": "Nova Pictures"},
        {"title": "Code Red",          "genre": "Thriller",  "release_date": "2025-03-05", "duration": 118, "rating": 7.7, "budget": 55_000_000,  "revenue": 190_000_000, "director": "Sophia Lin",      "studio": "Apex Studios"},
        {"title": "Desert Storm",      "genre": "Action",    "release_date": "2024-04-10", "duration": 140, "rating": 7.0, "budget": 95_000_000,  "revenue": 210_000_000, "director": "James Carter",    "studio": "Horizon Films"},
        {"title": "Haunted Manor",     "genre": "Horror",    "release_date": "2024-10-31", "duration": 100, "rating": 6.2, "budget": 10_000_000,  "revenue": 70_000_000,  "director": "Priya Sharma",    "studio": "Crescent Media"},
        {"title": "Summer Fling",      "genre": "Romance",   "release_date": "2024-06-21", "duration": 110, "rating": 6.9, "budget": 25_000_000,  "revenue": 90_000_000,  "director": "Olivia Chen",     "studio": "Pinnacle Entertainment"},
        {"title": "Robot Uprising",    "genre": "Sci-Fi",    "release_date": "2024-08-08", "duration": 132, "rating": 7.5, "budget": 110_000_000, "revenue": 280_000_000, "director": "David Park",      "studio": "Apex Studios"},
        {"title": "Silent Witness",    "genre": "Drama",     "release_date": "2024-09-30", "duration": 145, "rating": 8.0, "budget": 38_000_000,  "revenue": 175_000_000, "director": "Elena Ruiz",      "studio": "Pinnacle Entertainment"},
        {"title": "Blaze Runner",      "genre": "Action",    "release_date": "2024-11-15", "duration": 126, "rating": 7.2, "budget": 85_000_000,  "revenue": 195_000_000, "director": "Marcus Webb",     "studio": "Horizon Films"},
        {"title": "Phantom Menace II", "genre": "Sci-Fi",    "release_date": "2025-07-04", "duration": 150, "rating": 7.8, "budget": 140_000_000, "revenue": 360_000_000, "director": "Sophia Lin",      "studio": "Apex Studios"},
        {"title": "Tiny Adventures",   "genre": "Animation", "release_date": "2024-04-20", "duration": 88,  "rating": 7.9, "budget": 75_000_000,  "revenue": 270_000_000, "director": "David Park",      "studio": "Nova Pictures"},
        {"title": "The Verdict",       "genre": "Drama",     "release_date": "2025-02-01", "duration": 138, "rating": 8.5, "budget": 42_000_000,  "revenue": 230_000_000, "director": "Elena Ruiz",      "studio": "Pinnacle Entertainment"},
        {"title": "Night Crawlers",    "genre": "Horror",    "release_date": "2025-01-10", "duration": 96,  "rating": 6.7, "budget": 14_000_000,  "revenue": 88_000_000,  "director": "Priya Sharma",    "studio": "Crescent Media"},
        {"title": "Rapid Fire",        "genre": "Action",    "release_date": "2025-05-15", "duration": 112, "rating": 7.4, "budget": 78_000_000,  "revenue": 215_000_000, "director": "James Carter",    "studio": "Horizon Films"},
        {"title": "Galactic Drift",    "genre": "Sci-Fi",    "release_date": "2024-06-30", "duration": 144, "rating": 7.6, "budget": 105_000_000, "revenue": 295_000_000, "director": "Sophia Lin",      "studio": "Apex Studios"},
        {"title": "Broken Strings",    "genre": "Drama",     "release_date": "2024-07-22", "duration": 128, "rating": 7.8, "budget": 32_000_000,  "revenue": 155_000_000, "director": "Elena Ruiz",      "studio": "Pinnacle Entertainment"},
        {"title": "Chill Factor",      "genre": "Thriller",  "release_date": "2024-02-28", "duration": 116, "rating": 6.9, "budget": 50_000_000,  "revenue": 140_000_000, "director": "James Carter",    "studio": "Apex Studios"},
        {"title": "Wedding Crashers 2","genre": "Comedy",    "release_date": "2024-05-10", "duration": 108, "rating": 5.4, "budget": 35_000_000,  "revenue": 45_000_000,  "director": "Mia Johnson",     "studio": "Nova Pictures"},
        {"title": "Pranksters",        "genre": "Comedy",    "release_date": "2025-01-05", "duration": 96,  "rating": 5.1, "budget": 15_000_000,  "revenue": 18_000_000,  "director": "Ryan Mitchell",   "studio": "Crescent Media"},
        {"title": "Ocean Deep",        "genre": "Thriller",  "release_date": "2025-04-25", "duration": 134, "rating": 7.5, "budget": 60_000_000,  "revenue": 200_000_000, "director": "Marcus Webb",     "studio": "Horizon Films"},
        {"title": "Dreamscape",        "genre": "Animation", "release_date": "2025-03-15", "duration": 92,  "rating": 8.1, "budget": 70_000_000,  "revenue": 280_000_000, "director": "David Park",      "studio": "Nova Pictures"},
        {"title": "Eternal Flame",     "genre": "Romance",   "release_date": "2024-12-25", "duration": 118, "rating": 7.3, "budget": 30_000_000,  "revenue": 110_000_000, "director": "Olivia Chen",     "studio": "Pinnacle Entertainment"},
        {"title": "Steel Horizon",     "genre": "Action",    "release_date": "2024-03-08", "duration": 124, "rating": 7.1, "budget": 88_000_000,  "revenue": 205_000_000, "director": "Marcus Webb",     "studio": "Horizon Films"},
        {"title": "Mind Games",        "genre": "Thriller",  "release_date": "2025-06-10", "duration": 110, "rating": 7.6, "budget": 48_000_000,  "revenue": 175_000_000, "director": "Sophia Lin",      "studio": "Apex Studios"},
        {"title": "Wanderlust",        "genre": "Romance",   "release_date": "2025-04-12", "duration": 106, "rating": 7.0, "budget": 22_000_000,  "revenue": 95_000_000,  "director": "Olivia Chen",     "studio": "Crescent Media"},
        {"title": "Byte Me",           "genre": "Comedy",    "release_date": "2024-09-05", "duration": 94,  "rating": 5.3, "budget": 18_000_000,  "revenue": 24_000_000,  "director": "Mia Johnson",     "studio": "Nova Pictures"},
        {"title": "Aftershock",        "genre": "Drama",     "release_date": "2024-05-25", "duration": 136, "rating": 7.7, "budget": 36_000_000,  "revenue": 160_000_000, "director": "Elena Ruiz",      "studio": "Pinnacle Entertainment"},
        {"title": "Creature Feature",  "genre": "Horror",    "release_date": "2024-10-15", "duration": 104, "rating": 6.4, "budget": 11_000_000,  "revenue": 65_000_000,  "director": "Priya Sharma",    "studio": "Crescent Media"},
        {"title": "Orbit Station",     "genre": "Sci-Fi",    "release_date": "2025-05-28", "duration": 140, "rating": 7.9, "budget": 115_000_000, "revenue": 310_000_000, "director": "David Park",      "studio": "Apex Studios"},
        {"title": "Color Splash",      "genre": "Animation", "release_date": "2024-08-15", "duration": 86,  "rating": 7.8, "budget": 65_000_000,  "revenue": 245_000_000, "director": "David Park",      "studio": "Nova Pictures"},
    ]

    all_movie_defs = key_movies_2025 + comparison_movies + weak_comedies + filler_movies

    for m in all_movie_defs:
        movies.append({
            "id": movie_id,
            "title": m["title"],
            "genre": m["genre"],
            "release_date": m["release_date"],
            "duration_minutes": m["duration"],
            "rating": m["rating"],
            "budget": m["budget"],
            "revenue": m["revenue"],
            "director": m["director"],
            "studio": m["studio"],
        })
        movie_id += 1

    return movies



# ---------------------------------------------------------------------------
# 2. viewers.csv  (200+ viewers)
# ---------------------------------------------------------------------------

FIRST_NAMES = [
    "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason",
    "Isabella", "Logan", "Mia", "Lucas", "Charlotte", "Aiden", "Amelia",
    "James", "Harper", "Benjamin", "Evelyn", "Alexander", "Abigail", "Daniel",
    "Emily", "Henry", "Ella", "Sebastian", "Scarlett", "Jack", "Grace", "Owen",
    "Chloe", "Samuel", "Victoria", "Ryan", "Riley", "Nathan", "Aria", "Leo",
    "Lily", "Isaac", "Zoey", "Caleb", "Nora", "Dylan", "Hannah", "Luke",
    "Addison", "Gabriel", "Eleanor", "Julian",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson",
]

GENDERS = ["Male", "Female", "Non-binary"]
# Q4 needs city-level regions for engagement comparison
REGIONS = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin",
    "London", "Toronto", "Sydney", "Mumbai", "Tokyo",
]
SUBSCRIPTION_TIERS = ["Free", "Basic", "Premium", "VIP"]


def generate_viewers(count: int = 220) -> list[dict]:
    """Generate viewer records."""
    viewers = []
    for i in range(1, count + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        viewers.append({
            "id": i,
            "viewer_id": f"V{i:04d}",
            "name": f"{first} {last}",
            "age": random.randint(16, 72),
            "gender": random.choice(GENDERS),
            "region": random.choice(REGIONS),
            "subscription_tier": random.choice(SUBSCRIPTION_TIERS),
            "signup_date": str(random_date(date(2022, 1, 1), date(2025, 6, 1))),
        })
    return viewers


# ---------------------------------------------------------------------------
# 3. watch_activity.csv  (1000+ records)
# ---------------------------------------------------------------------------

DEVICES = ["Mobile", "Tablet", "Smart TV", "Desktop", "Gaming Console"]


def generate_watch_activity(movies: list[dict], viewers: list[dict], count: int = 1200) -> list[dict]:
    """Generate watch activity records.

    Ensures Stellar Run (movie_id=1) has high recent activity to support Q2.
    """
    records = []
    movie_ids = [m["id"] for m in movies]
    viewer_ids = [v["viewer_id"] for v in viewers]

    stellar_run_id = None
    for m in movies:
        if m["title"] == "Stellar Run":
            stellar_run_id = m["id"]
            break

    record_id = 1

    # --- Boost Stellar Run with heavy recent watch activity (Q2) ---
    recent_start = date(2025, 5, 1)
    recent_end = date(2025, 6, 30)
    for _ in range(150):
        vid = random.choice(viewer_ids)
        duration = random.randint(100, 138)
        records.append({
            "id": record_id,
            "viewer_id": vid,
            "movie_id": stellar_run_id,
            "watch_date": str(random_date(recent_start, recent_end)),
            "watch_duration_minutes": duration,
            "completed": random.random() < 0.85,  # high completion
            "device": random.choice(DEVICES),
        })
        record_id += 1

    # --- Generate remaining activity ---
    remaining = count - len(records)
    # Weight movie selection: comedies get fewer watches to support Q5
    comedy_ids = {m["id"] for m in movies if m["genre"] == "Comedy"}

    for _ in range(remaining):
        # Lower probability for comedies
        mid = random.choice(movie_ids)
        if mid in comedy_ids and random.random() < 0.5:
            mid = random.choice([x for x in movie_ids if x not in comedy_ids])

        vid = random.choice(viewer_ids)
        movie_data = next(m for m in movies if m["id"] == mid)
        max_dur = movie_data["duration_minutes"]
        completed = random.random() < 0.65
        watch_dur = max_dur if completed else random.randint(10, max(11, max_dur - 10))

        records.append({
            "id": record_id,
            "viewer_id": vid,
            "movie_id": mid,
            "watch_date": str(random_date(date(2024, 1, 1), date(2025, 6, 30))),
            "watch_duration_minutes": watch_dur,
            "completed": completed,
            "device": random.choice(DEVICES),
        })
        record_id += 1

    return records


# ---------------------------------------------------------------------------
# 4. reviews.csv  (500+ reviews)
# ---------------------------------------------------------------------------

POSITIVE_SNIPPETS = [
    "Absolutely loved it! A must-watch.",
    "Great storyline and amazing visuals.",
    "One of the best films this year.",
    "Incredible performances by the entire cast.",
    "Kept me on the edge of my seat the whole time.",
    "A masterpiece of modern cinema.",
    "Beautifully directed and well-paced.",
    "Highly recommend to everyone.",
    "Exceeded all my expectations.",
    "A thrilling ride from start to finish.",
]

NEUTRAL_SNIPPETS = [
    "It was okay, nothing special.",
    "Decent movie but could have been better.",
    "Some good moments but overall average.",
    "Not bad, but I expected more.",
    "Watchable but forgettable.",
    "Had its moments but dragged in places.",
    "A solid effort but not groundbreaking.",
]

NEGATIVE_SNIPPETS = [
    "Very disappointing. Would not recommend.",
    "Poor writing and predictable plot.",
    "Waste of time and money.",
    "The worst movie I have seen this year.",
    "Boring and uninspired.",
    "Terrible pacing and weak characters.",
    "Not worth the hype at all.",
]


def generate_reviews(movies: list[dict], viewers: list[dict], count: int = 550) -> list[dict]:
    """Generate review records.

    Stellar Run gets many positive reviews (Q2).
    Comedies get mostly negative/neutral reviews (Q5).
    """
    reviews = []
    movie_ids = [m["id"] for m in movies]
    viewer_ids = [v["viewer_id"] for v in viewers]
    comedy_ids = {m["id"] for m in movies if m["genre"] == "Comedy"}

    stellar_run_id = next(m["id"] for m in movies if m["title"] == "Stellar Run")

    review_id = 1

    # --- Stellar Run positive reviews (Q2) ---
    for _ in range(60):
        vid = random.choice(viewer_ids)
        rating = round(random.uniform(7.5, 10.0), 1)
        reviews.append({
            "id": review_id,
            "viewer_id": vid,
            "movie_id": stellar_run_id,
            "rating": rating,
            "review_text": random.choice(POSITIVE_SNIPPETS),
            "review_date": str(random_date(date(2025, 4, 1), date(2025, 6, 30))),
        })
        review_id += 1

    # --- Comedy negative reviews (Q5) ---
    for cid in comedy_ids:
        for _ in range(random.randint(8, 15)):
            vid = random.choice(viewer_ids)
            rating = round(random.uniform(2.0, 5.5), 1)
            text = random.choice(NEGATIVE_SNIPPETS + NEUTRAL_SNIPPETS)
            reviews.append({
                "id": review_id,
                "viewer_id": vid,
                "movie_id": cid,
                "rating": rating,
                "review_text": text,
                "review_date": str(random_date(date(2024, 1, 1), date(2025, 6, 30))),
            })
            review_id += 1

    # --- Remaining reviews ---
    remaining = count - len(reviews)
    for _ in range(remaining):
        mid = random.choice(movie_ids)
        vid = random.choice(viewer_ids)
        movie_data = next(m for m in movies if m["id"] == mid)
        base_rating = movie_data["rating"]
        # Vary around the movie's base rating
        rating = round(max(1.0, min(10.0, base_rating + random.uniform(-2.0, 2.0))), 1)

        if rating >= 7.0:
            text = random.choice(POSITIVE_SNIPPETS)
        elif rating >= 5.0:
            text = random.choice(NEUTRAL_SNIPPETS)
        else:
            text = random.choice(NEGATIVE_SNIPPETS)

        reviews.append({
            "id": review_id,
            "viewer_id": vid,
            "movie_id": mid,
            "rating": rating,
            "review_text": text,
            "review_date": str(random_date(date(2024, 1, 1), date(2025, 6, 30))),
        })
        review_id += 1

    return reviews



# ---------------------------------------------------------------------------
# 5. marketing_spend.csv  (100+ campaigns)
# ---------------------------------------------------------------------------

CHANNELS = ["Social Media", "TV", "Search Ads", "Email", "Influencer", "Display Ads", "Streaming Ads"]
CAMPAIGN_TEMPLATES = [
    "Launch Campaign", "Awareness Push", "Retargeting Wave", "Holiday Special",
    "Pre-Release Buzz", "Opening Weekend Blitz", "Sustained Reach", "Viral Challenge",
    "Cross-Promo", "Loyalty Reward",
]


def generate_marketing_spend(movies: list[dict], count: int = 120) -> list[dict]:
    """Generate marketing spend records.

    Stellar Run gets significant marketing spend (Q2).
    Comedies get lower marketing spend (Q5).
    Different channels show different ROI for leadership insights (Q6).
    """
    campaigns = []
    campaign_id = 1

    stellar_run_id = next(m["id"] for m in movies if m["title"] == "Stellar Run")
    comedy_ids = {m["id"] for m in movies if m["genre"] == "Comedy"}

    # --- Stellar Run heavy marketing (Q2) ---
    for channel in ["Social Media", "Influencer", "Streaming Ads", "Search Ads", "TV"]:
        spend = random.randint(800_000, 3_000_000)
        start = random_date(date(2025, 3, 1), date(2025, 4, 15))
        end = start + timedelta(days=random.randint(14, 45))
        impressions = spend * random.randint(8, 15)
        clicks = int(impressions * random.uniform(0.02, 0.06))
        conversions = int(clicks * random.uniform(0.05, 0.15))
        campaigns.append({
            "id": campaign_id,
            "movie_id": stellar_run_id,
            "campaign_name": f"Stellar Run {random.choice(CAMPAIGN_TEMPLATES)}",
            "channel": channel,
            "spend_amount": spend,
            "start_date": str(start),
            "end_date": str(end),
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
        })
        campaign_id += 1

    # --- Generate campaigns for other movies ---
    non_stellar_movies = [m for m in movies if m["id"] != stellar_run_id]
    remaining = count - len(campaigns)

    for _ in range(remaining):
        movie = random.choice(non_stellar_movies)
        mid = movie["id"]
        channel = random.choice(CHANNELS)

        # Comedies get lower spend (Q5)
        if mid in comedy_ids:
            spend = random.randint(50_000, 400_000)
            impressions = spend * random.randint(3, 8)
            clicks = int(impressions * random.uniform(0.005, 0.02))
        else:
            spend = random.randint(200_000, 2_500_000)
            impressions = spend * random.randint(6, 14)
            clicks = int(impressions * random.uniform(0.015, 0.05))

        conversions = int(clicks * random.uniform(0.03, 0.12))
        rel_date = date.fromisoformat(movie["release_date"])
        start = rel_date - timedelta(days=random.randint(14, 60))
        end = rel_date + timedelta(days=random.randint(7, 30))

        campaigns.append({
            "id": campaign_id,
            "movie_id": mid,
            "campaign_name": f"{movie['title']} {random.choice(CAMPAIGN_TEMPLATES)}",
            "channel": channel,
            "spend_amount": spend,
            "start_date": str(start),
            "end_date": str(end),
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
        })
        campaign_id += 1

    return campaigns


# ---------------------------------------------------------------------------
# 6. regional_performance.csv  (200+ records)
# ---------------------------------------------------------------------------

# City-level regions for Q4
CITY_REGIONS = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin",
    "London", "Toronto", "Sydney", "Mumbai", "Tokyo",
]


def generate_regional_performance(movies: list[dict], count: int = 240) -> list[dict]:
    """Generate regional performance records.

    Ensures city-level data with varying engagement for Q4.
    Shows clear regional trends for Q6 leadership recommendations.
    """
    records = []
    record_id = 1

    # Define engagement multipliers per city (Q4: one city clearly strongest)
    city_engagement = {
        "New York": 1.8,
        "Los Angeles": 1.5,
        "Chicago": 1.2,
        "Houston": 1.0,
        "Phoenix": 0.9,
        "Philadelphia": 0.85,
        "San Antonio": 0.7,
        "San Diego": 0.95,
        "Dallas": 1.1,
        "Austin": 1.3,
        "London": 1.6,
        "Toronto": 1.15,
        "Sydney": 1.05,
        "Mumbai": 1.4,
        "Tokyo": 1.35,
    }

    # Generate records for recent months to support "last month" queries
    periods = [
        (date(2025, 5, 1), date(2025, 5, 31)),
        (date(2025, 6, 1), date(2025, 6, 30)),
        (date(2025, 4, 1), date(2025, 4, 30)),
        (date(2025, 3, 1), date(2025, 3, 31)),
        (date(2025, 2, 1), date(2025, 2, 28)),
        (date(2025, 1, 1), date(2025, 1, 31)),
        (date(2024, 10, 1), date(2024, 12, 31)),
        (date(2024, 7, 1), date(2024, 9, 30)),
    ]

    comedy_ids = {m["id"] for m in movies if m["genre"] == "Comedy"}

    # Ensure we cover all cities in recent periods
    for period_start, period_end in periods:
        for city in CITY_REGIONS:
            # Pick a subset of movies for this city/period
            sample_movies = random.sample(movies, min(len(movies), random.randint(3, 6)))
            for movie in sample_movies:
                mid = movie["id"]
                multiplier = city_engagement.get(city, 1.0)

                base_views = random.randint(5000, 50000)
                views = int(base_views * multiplier)

                # Comedies get lower views/revenue (Q5)
                if mid in comedy_ids:
                    views = int(views * 0.4)

                revenue = round(views * random.uniform(3.0, 8.0), 2)
                avg_rating = round(max(1.0, min(10.0, movie["rating"] + random.uniform(-1.5, 1.5))), 1)

                records.append({
                    "id": record_id,
                    "movie_id": mid,
                    "region": city,
                    "views": views,
                    "revenue": revenue,
                    "avg_rating": avg_rating,
                    "period_start": str(period_start),
                    "period_end": str(period_end),
                })
                record_id += 1

                if len(records) >= count:
                    break
            if len(records) >= count:
                break
        if len(records) >= count:
            break

    # If we still need more records, add extras
    while len(records) < count:
        movie = random.choice(movies)
        city = random.choice(CITY_REGIONS)
        period_start, period_end = random.choice(periods)
        multiplier = city_engagement.get(city, 1.0)
        base_views = random.randint(5000, 50000)
        views = int(base_views * multiplier)
        if movie["id"] in comedy_ids:
            views = int(views * 0.4)
        revenue = round(views * random.uniform(3.0, 8.0), 2)
        avg_rating = round(max(1.0, min(10.0, movie["rating"] + random.uniform(-1.5, 1.5))), 1)

        records.append({
            "id": record_id,
            "movie_id": movie["id"],
            "region": city,
            "views": views,
            "revenue": revenue,
            "avg_rating": avg_rating,
            "period_start": str(period_start),
            "period_end": str(period_end),
        })
        record_id += 1

    return records


# ---------------------------------------------------------------------------
# Main: generate all CSV files
# ---------------------------------------------------------------------------

def main():
    print("Generating sample CSV data files...")
    print(f"Output directory: {OUTPUT_DIR}\n")

    # 1. Movies
    movies = generate_movies()
    write_csv("movies.csv",
              ["id", "title", "genre", "release_date", "duration_minutes", "rating", "budget", "revenue", "director", "studio"],
              [[m["id"], m["title"], m["genre"], m["release_date"], m["duration_minutes"],
                m["rating"], m["budget"], m["revenue"], m["director"], m["studio"]] for m in movies])

    # 2. Viewers
    viewers = generate_viewers()
    write_csv("viewers.csv",
              ["id", "viewer_id", "name", "age", "gender", "region", "subscription_tier", "signup_date"],
              [[v["id"], v["viewer_id"], v["name"], v["age"], v["gender"],
                v["region"], v["subscription_tier"], v["signup_date"]] for v in viewers])

    # 3. Watch Activity
    watch_activity = generate_watch_activity(movies, viewers)
    write_csv("watch_activity.csv",
              ["id", "viewer_id", "movie_id", "watch_date", "watch_duration_minutes", "completed", "device"],
              [[w["id"], w["viewer_id"], w["movie_id"], w["watch_date"],
                w["watch_duration_minutes"], w["completed"], w["device"]] for w in watch_activity])

    # 4. Reviews
    reviews = generate_reviews(movies, viewers)
    write_csv("reviews.csv",
              ["id", "viewer_id", "movie_id", "rating", "review_text", "review_date"],
              [[r["id"], r["viewer_id"], r["movie_id"], r["rating"],
                r["review_text"], r["review_date"]] for r in reviews])

    # 5. Marketing Spend
    marketing = generate_marketing_spend(movies)
    write_csv("marketing_spend.csv",
              ["id", "movie_id", "campaign_name", "channel", "spend_amount", "start_date", "end_date", "impressions", "clicks", "conversions"],
              [[c["id"], c["movie_id"], c["campaign_name"], c["channel"], c["spend_amount"],
                c["start_date"], c["end_date"], c["impressions"], c["clicks"], c["conversions"]] for c in marketing])

    # 6. Regional Performance
    regional = generate_regional_performance(movies)
    write_csv("regional_performance.csv",
              ["id", "movie_id", "region", "views", "revenue", "avg_rating", "period_start", "period_end"],
              [[r["id"], r["movie_id"], r["region"], r["views"], r["revenue"],
                r["avg_rating"], r["period_start"], r["period_end"]] for r in regional])

    print(f"\nDone! All CSV files generated in {OUTPUT_DIR}")

    # Print summary stats
    print(f"\nSummary:")
    print(f"  Movies:              {len(movies)} rows")
    print(f"  Viewers:             {len(viewers)} rows")
    print(f"  Watch Activity:      {len(watch_activity)} rows")
    print(f"  Reviews:             {len(reviews)} rows")
    print(f"  Marketing Spend:     {len(marketing)} rows")
    print(f"  Regional Performance:{len(regional)} rows")


if __name__ == "__main__":
    main()
