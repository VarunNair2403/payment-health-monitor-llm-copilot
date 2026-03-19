import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "payments.db"


def get_global_kpis():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM payments")
    total_count, total_amount = cur.fetchone()

    cur.execute(
        """
        SELECT
          SUM(CASE WHEN status = 'succeeded' THEN 1 ELSE 0 END),
          SUM(CASE WHEN status IN ('succeeded','failed') THEN 1 ELSE 0 END)
        FROM payments
        """
    )
    succeeded, attempted = cur.fetchone() or (0, 0)

    conn.close()

    success_rate = (succeeded / attempted) if attempted else 0.0

    return {
        "payments_count": total_count,
        "volume_cents": total_amount,
        "success_rate": success_rate,
    }


if __name__ == "__main__":
    kpis = get_global_kpis()
    print(kpis)
