import sqlite3
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "payments.db"
CSV_PATH = DATA_DIR / "payments_raw.csv"

DDL = """
CREATE TABLE IF NOT EXISTS payments (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  amount INTEGER NOT NULL,
  currency TEXT NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_vertical TEXT NOT NULL,
  country TEXT NOT NULL,
  region TEXT,
  payment_method_type TEXT NOT NULL,
  card_brand TEXT,
  wallet_type TEXT,
  status TEXT NOT NULL,
  failure_code TEXT,
  failure_category TEXT,
  auth_outcome TEXT,
  risk_level TEXT,
  is_disputed INTEGER NOT NULL,
  is_refunded INTEGER NOT NULL,
  latency_ms INTEGER,
  channel TEXT,
  experiment_bucket TEXT
);
"""

def load_csv_to_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(DDL)

    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        rows = [tuple(r[h] or None for h in reader.fieldnames) for r in reader]
        placeholders = ",".join(["?"] * len(reader.fieldnames))
        sql = f"INSERT OR REPLACE INTO payments VALUES ({placeholders})"
        cur.executemany(sql, rows)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    load_csv_to_db()
    print("Loaded payments_raw.csv into payments.db")
