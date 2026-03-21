from fastapi import FastAPI, Query
from datetime import datetime
from typing import Optional

from .metrics import (
    get_global_kpis,
    get_breakdown_by_method,
    get_breakdown_by_region,
    get_top_failure_codes,
    get_dispute_refund_rates,
)
from .reporter import generate_narrative
from .anomaly import check_anomalies

app = FastAPI(
    title="Payment Health Monitor",
    description="LLM-powered payment health reporting API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/report")
def get_report(window: Optional[str] = Query(None, enum=["24h", "7d", "30d"])):
    snapshot = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "window": window or "all_data",
        "global_kpis": get_global_kpis(window),
        "by_method": get_breakdown_by_method(window),
        "by_region": get_breakdown_by_region(window),
        "top_failures": get_top_failure_codes(window),
        "dispute_refund": get_dispute_refund_rates(window),
    }
    narrative = generate_narrative(snapshot)
    alerts = check_anomalies(window)

    return {
        "snapshot": snapshot,
        "alerts": alerts,
        "narrative": narrative,
    }


@app.get("/alerts")
def get_alerts(window: Optional[str] = Query(None, enum=["24h", "7d", "30d"])):
    alerts = check_anomalies(window)
    return {
        "window": window or "all_data",
        "alert_count": len(alerts),
        "alerts": alerts,
    }


@app.get("/kpis")
def get_kpis(window: Optional[str] = Query(None, enum=["24h", "7d", "30d"])):
    return {
        "window": window or "all_data",
        "global_kpis": get_global_kpis(window),
        "by_method": get_breakdown_by_method(window),
        "by_region": get_breakdown_by_region(window),
        "top_failures": get_top_failure_codes(window),
        "dispute_refund": get_dispute_refund_rates(window),
    }
