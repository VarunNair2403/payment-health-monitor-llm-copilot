from typing import Dict
from .llm_client import generate_health_narrative

def build_llm_prompt(snapshot: Dict) -> str:
    kpis = snapshot["global_kpis"]
    return (
        "You are a payments product manager.\n"
        "Given these KPIs, write a concise 3-sentence health summary.\n"
        "Mention success rate, volume, and any obvious concerns.\n\n"
        f"Payments count: {kpis['payments_count']}\n"
        f"Volume (cents): {kpis['volume_cents']}\n"
        f"Success rate: {kpis['success_rate']:.3f}\n"
    )

def generate_narrative(snapshot: Dict) -> str:
    prompt = build_llm_prompt(snapshot)
    return generate_health_narrative(prompt)
