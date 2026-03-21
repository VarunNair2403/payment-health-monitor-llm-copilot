# Payment Health Monitor — LLM Copilot

## The Problem

Payment teams at companies like Stripe, Adyen, and Plaid deal with thousands to millions of transactions per day. When something goes wrong — a spike in declines, a region underperforming, a surge in disputes — the data exists in dashboards and SQL tables, but translating that into a clear, actionable summary takes time and manual effort.

PMs and ops teams often have to:
- Pull multiple queries across regions, methods, and time windows
- Manually interpret what the numbers mean
- Write up summaries for stakeholders

This tool automates that entire workflow.

---

## Why I Built This

I built this as a portfolio project to simulate the kind of internal tooling a payments PM would actually use day-to-day. The goal was to combine:

- **Real payments domain knowledge** — KPIs that Stripe, Adyen, and Plaid actually track (success rate, decline codes, dispute rate, refund rate)
- **LLM-powered narrative generation** — instead of raw numbers, get a 4-5 sentence health summary with a recommended action
- **Anomaly detection** — proactive alerting when metrics fall below configurable thresholds
- **Production-ready API** — FastAPI layer so this could be consumed by a dashboard, Slack bot, or internal tool

This project demonstrates how AI can augment a PM's workflow — not replace judgment, but eliminate the grunt work of translating data into language.

---

## How It Works

1. `payments_raw.csv` is loaded into a SQLite database via `ingestion.py`
2. `metrics.py` computes KPIs globally and broken down by region, method, and failure code with optional time-window filtering
3. `anomaly.py` checks those KPIs against configurable thresholds and fires alerts
4. `reporter.py` builds a structured prompt and sends it to GPT to generate a plain-English health summary
5. `cli.py` or `api.py` delivers the output — either via terminal or REST API

---

## Project Structure and File Explanations

**data/payments_raw.csv** — Raw payments data (synthetic, 500 rows). In production this would be replaced by a Kafka stream or data warehouse pull.

**scripts/generate_synthetic_data.py** — Generates 500 realistic payment rows with randomized regions, methods, failure codes, dispute rates, and amounts. Used to simulate a real payments dataset for local development.

**src/ingestion.py** — Loads the CSV into a local SQLite database. Simulates an ETL step; in production this would be an Airflow job or dbt pipeline pulling from Snowflake or BigQuery.

**src/metrics.py** — Computes all KPIs with time-window support (24h, 7d, 30d, all-time). Centralizes metric logic so both the CLI and API use identical calculations.

**src/anomaly.py** — Fires alerts when metrics breach thresholds. Mimics PagerDuty-style alerting. Thresholds are configurable per business context directly in the file.

**src/reporter.py** — Builds a structured LLM prompt from the snapshot data and calls the OpenAI client. Prompt is designed to produce a PM-quality narrative with a concrete recommendation.

**src/llm_client.py** — OpenAI API wrapper. Isolated so you can swap GPT for Claude, Gemini, or an internal model without touching any other file.

**src/cli.py** — CLI entrypoint. Lets you run health checks locally or from a cron job without spinning up a server.

**src/api.py** — FastAPI REST API. Makes the tool consumable by dashboards, Slack bots, or other internal services.

---

## Quickstart (Local)

**1. Clone and set up environment**

```bash
git clone https://github.com/VarunNair2403/payment-health-monitor-llm-copilot.git
cd payment-health-monitor-llm-copilot
python -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv fastapi uvicorn
```

**2. Add your OpenAI key**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
```

**3. Generate data and load DB**

```bash
python scripts/generate_synthetic_data.py
python -m src.ingestion
```

**4. Run via CLI**

```bash
python -m src.cli           # all-time data
python -m src.cli 24h       # last 24 hours
python -m src.cli 7d        # last 7 days
python -m src.cli 30d       # last 30 days
```

**5. Run via API**

```bash
uvicorn src.api:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

---

## API Endpoints

- `GET /health` — Service health check
- `GET /kpis?window=7d` — Raw KPIs with breakdowns
- `GET /alerts?window=7d` — Anomaly alerts only
- `GET /report?window=7d` — Full report: KPIs + alerts + LLM narrative

---

## KPIs Tracked

- **Success rate** — global, by region, by payment method
- **Volume** — total transaction count and dollar amount
- **Top failure codes** — top 5 decline reasons (e.g. do_not_honor, insufficient_funds)
- **Dispute rate** — percentage of transactions disputed
- **Refund rate** — percentage of transactions refunded

---

## Anomaly Detection Thresholds

- Global success rate below 80% → Critical
- Region success rate below 70% → Warning
- Method success rate below 70% → Warning

Thresholds are configurable in `src/anomaly.py`.

---

## Taking This to Production

| Current (Local) | Production Equivalent |
|---|---|
| CSV file | Kafka stream or data warehouse (Snowflake, BigQuery) |
| SQLite | PostgreSQL or Redshift |
| Manual ingestion script | Airflow or dbt pipeline on a schedule |
| Local uvicorn server | Dockerized container on AWS ECS or Cloud Run |
| .env file | AWS Secrets Manager or Azure Key Vault |
| OpenAI GPT-4o-mini | Fine-tuned internal model or Azure OpenAI private endpoint |
| CLI output | Slack bot or internal dashboard (Retool, Grafana) |
| Hardcoded thresholds | Dynamically configured per merchant or product vertical |

---

## Tech Stack

- Python 3.7+
- SQLite — lightweight local data store
- OpenAI GPT-4o-mini — narrative generation
- FastAPI + Uvicorn — REST API layer
- python-dotenv — environment config
