import sys
from datetime import datetime
from .metrics import (
    get_global_kpis,
    get_breakdown_by_method,
    get_breakdown_by_region,
    get_top_failure_codes,
    get_dispute_refund_rates,
)
from .reporter import generate_narrative
from .anomaly import check_anomalies


def main():
    window = sys.argv[1] if len(sys.argv) > 1 else None

    snapshot = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "window": window or "all_data",
        "global_kpis": get_global_kpis(window),
        "by_method": get_breakdown_by_method(window),
        "by_region": get_breakdown_by_region(window),
        "top_failures": get_top_failure_codes(window),
        "dispute_refund": get_dispute_refund_rates(window),
    }

    alerts = check_anomalies(window)
    narrative = generate_narrative(snapshot)

    print("SNAPSHOT:", snapshot)

    print(f"\nALERTS ({len(alerts)} found):")
    if alerts:
        for a in alerts:
            print(f"  [{a['level'].upper()}] {a['message']}")
    else:
        print("  No anomalies detected.")

    print("\nNARRATIVE:")
    print(narrative)


if __name__ == "__main__":
    main()
