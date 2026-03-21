from typing import Optional, List, Dict
from .metrics import get_global_kpis, get_breakdown_by_region, get_breakdown_by_method

# --- Thresholds ---
GLOBAL_SUCCESS_RATE_MIN = 0.80       # alert if below 80%
REGION_SUCCESS_RATE_MIN = 0.70       # alert if any region below 70%
METHOD_SUCCESS_RATE_MIN = 0.70       # alert if any method below 70%
DISPUTE_RATE_MAX = 0.02              # alert if above 2%
REFUND_RATE_MAX = 0.15               # alert if above 15%


def check_anomalies(window: Optional[str] = None) -> List[Dict]:
    alerts = []

    # 1. Global success rate
    kpis = get_global_kpis(window)
    if kpis["success_rate"] < GLOBAL_SUCCESS_RATE_MIN:
        alerts.append({
            "level": "critical",
            "type": "global_success_rate",
            "message": f"Global success rate {kpis['success_rate']:.1%} is below threshold {GLOBAL_SUCCESS_RATE_MIN:.1%}",
        })

    # 2. Region success rate
    for r in get_breakdown_by_region(window):
        if r["success_rate"] is not None and r["success_rate"] < REGION_SUCCESS_RATE_MIN:
            alerts.append({
                "level": "warning",
                "type": "region_success_rate",
                "message": f"Region {r['region']} success rate {r['success_rate']:.1%} is below threshold {REGION_SUCCESS_RATE_MIN:.1%}",
            })

    # 3. Method success rate
    for m in get_breakdown_by_method(window):
        if m["success_rate"] is not None and m["success_rate"] < METHOD_SUCCESS_RATE_MIN:
            alerts.append({
                "level": "warning",
                "type": "method_success_rate",
                "message": f"Method {m['method']} success rate {m['success_rate']:.1%} is below threshold {METHOD_SUCCESS_RATE_MIN:.1%}",
            })

    return alerts
