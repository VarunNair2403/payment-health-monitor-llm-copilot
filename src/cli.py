from datetime import datetime
from .metrics import get_global_kpis
from .reporter import generate_narrative

def main():
    snapshot = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "window": "all_data",
        "global_kpis": get_global_kpis(),
    }

    narrative = generate_narrative(snapshot)

    print("SNAPSHOT:", snapshot)
    print("\nNARRATIVE:")
    print(narrative)

if __name__ == "__main__":
    main()
