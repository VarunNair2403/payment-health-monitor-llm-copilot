from datetime import datetime
from .metrics import get_global_kpis
from .reporter import build_llm_prompt, fake_llm_call

def main():
    snapshot = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "window": "all_data",
        "global_kpis": get_global_kpis(),
    }

    prompt = build_llm_prompt(snapshot)
    narrative = fake_llm_call(prompt)

    print("SNAPSHOT:", snapshot)
    print("\nNARRATIVE:")
    print(narrative)

if __name__ == "__main__":
    main()
