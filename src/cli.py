from datetime import datetime
from .metrics import (
    get_global_kpis,
    get_breakdown_by_method,
    get_breakdown_by_region,
    get_top_failure_codes,
    get_dispute_refund_rates,
)
from .reporter import generate_narrative


def main():
    snapshot = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "window": "all_data",
        "global_kpis": get_global_kpis(),
        "by_method": get_breakdown_by_method(),
        "by_region": get_breakdown_by_region(),
        "top_failures": get_top_failure_codes(),
        "dispute_refund": get_dispute_refund_rates(),
    }

    narrative = generate_narrative(snapshot)

    print("SNAPSHOT:", snapshot)
    print("\nNARRATIVE:")
    print(narrative)


if __name__ == "__main__":
    main()
