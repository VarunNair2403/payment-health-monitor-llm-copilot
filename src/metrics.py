import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "payments.db"


def _window_filter(window: Optional[str]) -> str:
    """Returns a SQL WHERE clause fragment for the given window."""
    if window == "24h":
        cutoff = (datetime.utcnow() - timedelta(hours=24)).isoformat() + "Z"
    elif window == "7d":
        cutoff = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"
    elif window == "30d":
        cutoff = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    else:
        return ""  # all_data — no filter
    return f"WHERE created_at >= '{cutoff}'"


def get_global_kpis(window: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    wf = _window_filter(window)

    cur.execute(f"SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM payments {wf}")
    total_count, total_amount = cur.fetchone()

    cur.execute(
        f"""
        SELECT
          SUM(CASE WHEN status = 'succeeded' THEN 1 ELSE 0 END),
          SUM(CASE WHEN status IN ('succeeded','failed') THEN 1 ELSE 0 END)
        FROM payments {wf}
        """
    )
    succeeded, attempted = cur.fetchone() or (0, 0)
    success_rate = (succeeded / attempted) if attempted else 0.0

    conn.close()
    return {
        "payments_count": total_count,
        "volume_cents": total_amount,
        "success_rate": round(success_rate, 4),
    }


def get_breakdown_by_method(window: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    wf = _window_filter(window)
    cur.execute(
        f"""
        SELECT payment_method_type,
               COUNT(*) as count,
               ROUND(AVG(CASE WHEN status='succeeded' THEN 1.0 ELSE 0.0 END), 4) as success_rate
        FROM payments {wf}
        GROUP BY payment_method_type
        ORDER BY count DESC
        """
    )
    rows = [{"method": r[0], "count": r[1], "success_rate": r[2]} for r in cur.fetchall()]
    conn.close()
    return rows


def get_breakdown_by_region(window: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    wf = _window_filter(window)
    cur.execute(
        f"""
        SELECT region,
               COUNT(*) as count,
               ROUND(AVG(CASE WHEN status='succeeded' THEN 1.0 ELSE 0.0 END), 4) as success_rate
        FROM payments {wf}
        GROUP BY region
        ORDER BY count DESC
        """
    )
    rows = [{"region": r[0], "count": r[1], "success_rate": r[2]} for r in cur.fetchall()]
    conn.close()
    return rows


def get_top_failure_codes(window: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    wf = _window_filter(window)
    and_filter = wf.replace("WHERE", "AND") if wf else ""
    cur.execute(
        f"""
        SELECT failure_code, COUNT(*) as count
        FROM payments
        WHERE failure_code != '' AND failure_code IS NOT NULL
        {and_filter}
        GROUP BY failure_code
        ORDER BY count DESC
        LIMIT 5
        """
    )
    rows = [{"failure_code": r[0], "count": r[1]} for r in cur.fetchall()]
    conn.close()
    return rows


def get_dispute_refund_rates(window: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    wf = _window_filter(window)
    cur.execute(
        f"""
        SELECT
          ROUND(AVG(is_disputed), 4) as dispute_rate,
          ROUND(AVG(is_refunded), 4) as refund_rate
        FROM payments {wf}
        """
    )
    row = cur.fetchone()
    conn.close()
    return {"dispute_rate": row[0], "refund_rate": row[1]}
