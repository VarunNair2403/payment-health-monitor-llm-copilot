import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CSV_PATH = DATA_DIR / "payments_raw.csv"

# --- Config ---
NUM_ROWS = 500
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 3, 18)

MERCHANTS = ["m_001", "m_002", "m_003", "m_004", "m_005"]
VERTICALS = ["ecommerce", "saas", "marketplace", "fintech", "gaming"]
COUNTRIES = ["US", "GB", "IN", "BR", "DE", "CA", "SG", "AU"]
REGIONS = {"US": "NA", "CA": "NA", "BR": "LATAM", "GB": "EU",
           "DE": "EU", "IN": "APAC", "SG": "APAC", "AU": "APAC"}
METHODS = ["card", "card", "card", "ach", "wallet", "rtp"]
CARD_BRANDS = ["visa", "mastercard", "amex", "discover"]
WALLET_TYPES = ["apple_pay", "google_pay"]
STATUSES = ["succeeded", "succeeded", "succeeded", "succeeded", "failed", "pending", "refunded"]
FAILURE_CODES = ["insufficient_funds", "do_not_honor", "network_error", "expired_card", "fraud_detected"]
FAILURE_CATEGORIES = {"insufficient_funds": "bank_decline", "do_not_honor": "bank_decline",
                      "network_error": "technical", "expired_card": "customer", "fraud_detected": "fraud"}
RISK_LEVELS = ["normal", "normal", "normal", "elevated", "highest"]
CHANNELS = ["web", "mobile", "api"]
EXPERIMENTS = ["control", "control", "auth_opt_v1", "routing_v2"]

FIELDNAMES = [
    "id", "created_at", "amount", "currency", "merchant_id", "merchant_vertical",
    "country", "region", "payment_method_type", "card_brand", "wallet_type",
    "status", "failure_code", "failure_category", "auth_outcome", "risk_level",
    "is_disputed", "is_refunded", "latency_ms", "channel", "experiment_bucket"
]


def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def generate_row():
    method = random.choice(METHODS)
    card_brand = random.choice(CARD_BRANDS) if method == "card" else ""
    wallet_type = random.choice(WALLET_TYPES) if method == "wallet" else ""
    country = random.choice(COUNTRIES)
    status = random.choice(STATUSES)
    failure_code = random.choice(FAILURE_CODES) if status == "failed" else ""
    failure_category = FAILURE_CATEGORIES.get(failure_code, "") if failure_code else ""
    auth_outcome = "authorized" if status == "succeeded" else ("declined" if status == "failed" else "not_attempted")
    risk_level = random.choice(RISK_LEVELS)
    is_disputed = 1 if (status == "succeeded" and random.random() < 0.03) else 0
    is_refunded = 1 if status == "refunded" else 0
    merchant_id = random.choice(MERCHANTS)

    return {
        "id": "pmt_" + uuid.uuid4().hex[:10],
        "created_at": random_date(START_DATE, END_DATE).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "amount": random.randint(199, 49999),
        "currency": "usd",
        "merchant_id": merchant_id,
        "merchant_vertical": random.choice(VERTICALS),
        "country": country,
        "region": REGIONS[country],
        "payment_method_type": method,
        "card_brand": card_brand,
        "wallet_type": wallet_type,
        "status": status,
        "failure_code": failure_code,
        "failure_category": failure_category,
        "auth_outcome": auth_outcome,
        "risk_level": risk_level,
        "is_disputed": is_disputed,
        "is_refunded": is_refunded,
        "latency_ms": random.randint(200, 3000),
        "channel": random.choice(CHANNELS),
        "experiment_bucket": random.choice(EXPERIMENTS),
    }


if __name__ == "__main__":
    rows = [generate_row() for _ in range(NUM_ROWS)]
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {NUM_ROWS} rows → {CSV_PATH}")
