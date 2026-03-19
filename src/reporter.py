from typing import Dict

def build_llm_prompt(snapshot: Dict) -> str:
    kpis = snapshot["global_kpis"]
    return (
        "You are a payments PM.\n"
        "Given these KPIs, write a 2–3 sentence health summary.\n\n"
        f"Payments count: {kpis['payments_count']}\n"
        f"Volume (cents): {kpis['volume_cents']}\n"
        f"Success rate: {kpis['success_rate']:.3f}\n"
    )

def fake_llm_call(prompt: str) -> str:
    # placeholder until we wire a real LLM client
    return "Payment health looks stable based on the current KPIs."
