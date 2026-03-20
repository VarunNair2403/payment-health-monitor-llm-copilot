from typing import Dict
from .llm_client import generate_health_narrative
from .metrics import (
    get_breakdown_by_method,
    get_breakdown_by_region,
    get_top_failure_codes,
    get_dispute_refund_rates,
)


def build_llm_prompt(snapshot: Dict) -> str:
    kpis = snapshot["global_kpis"]
    methods = snapshot["by_method"]
    regions = snapshot["by_region"]
    failures = snapshot["top_failures"]
    rates = snapshot["dispute_refund"]

    method_lines = "\n".join(
        f"  {m['method']}: {m['count']} txns, {m['success_rate'] or 0:.1%} success" for m in methods
    ) or "  No data"

    region_lines = "\n".join(
        f"  {r['region']}: {r['count']} txns, {r['success_rate'] or 0:.1%} success" for r in regions
    ) or "  No data"

    failure_lines = "\n".join(
        f"  {f['failure_code']}: {f['count']} occurrences" for f in failures
    ) or "  No data"

    dispute_rate = rates["dispute_rate"] or 0
    refund_rate = rates["refund_rate"] or 0

    return (
        "You are a payments product manager at a fintech company.\n"
        "Write a concise 4-5 sentence health summary covering: overall health, "
        "worst performing region or method, top failure drivers, and one recommended action.\n\n"
        f"=== Global KPIs ===\n"
        f"Total payments: {kpis['payments_count']}\n"
        f"Volume: ${kpis['volume_cents']/100:,.2f}\n"
        f"Success rate: {kpis['success_rate']:.1%}\n"
        f"Dispute rate: {dispute_rate:.1%}\n"
        f"Refund rate: {refund_rate:.1%}\n\n"
        f"=== By Payment Method ===\n{method_lines}\n\n"
        f"=== By Region ===\n{region_lines}\n\n"
        f"=== Top Failure Codes ===\n{failure_lines}\n"
    )

def generate_narrative(snapshot: Dict) -> str:
    prompt = build_llm_prompt(snapshot)
    return generate_health_narrative(prompt)
