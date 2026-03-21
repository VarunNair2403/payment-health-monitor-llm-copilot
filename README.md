# Payment Health Monitor — LLM Copilot

An AI-powered payment health monitoring tool that ingests transaction data, computes KPIs, detects anomalies, and generates natural language health narratives using GPT.

Built as a portfolio project simulating the kind of tooling a payments PM at Stripe, Adyen, or Plaid would use to monitor product health.

---

## What It Does

- Ingests raw payment transaction data (CSV → SQLite)
- Computes global and breakdown KPIs (by region, method, failure code)
- Supports time-windowed analysis: `24h`, `7d`, `30d`, or all-time
- Detects anomalies against configurable thresholds (success rate, dispute rate, refund rate)
- Generates a concise LLM narrative summarizing health, risks, and recommended actions
- Exposes everything via a FastAPI REST API with Swagger UI

---

## Project Structure

payment-health-monitor-llm-copilot/
├── data/
│ └── payments_raw.csv # Raw payments data (synthetic)
├── scripts/
│ └── generate_synthetic_data.py # Generates 500 realistic payment rows
├── src/
│ ├── ingestion.py # Loads CSV into SQLite
│ ├── metrics.py # KPI computations with time-window support
│ ├── anomaly.py # Threshold-based anomaly detection
│ ├── reporter.py # LLM prompt builder + narrative generator
│ ├── llm_client.py # OpenAI API client
│ ├── cli.py # CLI entrypoint
│ └── api.py # FastAPI REST API
├── .env # API keys (not committed)
├── .gitignore
└── README.md


---

## Quickstart

### 1. Clone and set up environment

```bash
git clone https://github.com/VarunNair2403/payment-health-monitor-llm-copilot.git
cd payment-health-monitor-llm-copilot
python -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv fastapi uvicorn

### 2. Add your OpenAI key
Create a .env file in the project root:

text
OPENAI_API_KEY=sk-...

### 3. Generate data and load DB
bash
python scripts/generate_synthetic_data.py
python -m src.ingestion
### 4. Run via CLI
bash
python -m src.cli           # all-time
python -m src.cli 24h       # last 24 hours
python -m src.cli 7d        # last 7 days
python -m src.cli 30d       # last 30 days

### 5. Run via API
bash
uvicorn src.api:app --reload
Open http://127.0.0.1:8000/docs for the interactive Swagger UI.

### API Endpoints
Method	Endpoint	Description
GET	/health	Service health check
GET	/kpis?window=7d	Raw KPIs with breakdowns
GET	/alerts?window=7d	Anomaly alerts only
GET	/report?window=7d	Full report: KPIs + alerts + LLM narrative

### KPIs Tracked
Success rate — global, by region, by payment method

Volume — total transaction count and amount

Failure codes — top 5 failure drivers (e.g. do_not_honor, insufficient_funds)

Dispute rate — % of transactions disputed

Refund rate — % of transactions refunded

### Anomaly Thresholds
Metric	Threshold	Alert Level
Global success rate	< 80%	Critical
Region success rate	< 70%	Warning
Method success rate	< 70%	Warning

### Tech Stack
Python 3.7+
SQLite — lightweight local data store
OpenAI GPT-4o-mini — narrative generation
FastAPI + Uvicorn — REST API layer
python-dotenv — environment config