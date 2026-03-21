# PRD: Payment Health Monitor — LLM Copilot

**Author:** Varun Nair
**Status:** v1.0 — Complete
**Last Updated:** March 2026

---

## Problem Statement

Payment operations teams at fintech companies monitor hundreds of KPIs daily — success rates, decline codes, dispute rates, refund rates — broken down by region, payment method, merchant, and time window. The data exists, but extracting signal from it requires manual SQL queries, dashboard interpretation, and stakeholder writeups.

This creates three compounding problems:

1. **Speed** — by the time a human notices a decline spike and writes it up, the issue has already impacted revenue or user trust
2. **Consistency** — different analysts frame the same data differently, leading to inconsistent narratives across teams
3. **Accessibility** — not every stakeholder (PM, executive, support lead) can read raw dashboards fluently

There is no tool today that takes payment transaction data and automatically produces a plain-English health summary with anomaly alerts and a recommended action — the way a senior payments PM would.

---

## Target Users

- **Payments PM** — needs a daily health snapshot without pulling SQL manually
- **Engineering On-Call** — needs an anomaly alert with context, not just a raw metric breach
- **Finance / Risk Lead** — needs refund and dispute rate summaries across time windows
- **Executive Stakeholder** — needs a plain-English narrative they can act on without reading dashboards

---

## Goals

**Primary Goals**
- Automate the generation of a payment health narrative from raw transaction data
- Surface anomalies proactively before they require human detection
- Support time-windowed analysis (24h, 7d, 30d) to catch both spikes and trends

**Secondary Goals**
- Build a reusable API layer so this can plug into dashboards, Slack bots, or internal tools
- Demonstrate a production-ready architecture pattern for LLM-augmented data products

**Non-Goals for v1**
- Real-time streaming — this is batch/on-demand, not sub-second
- Multi-tenant support — single data source for now
- User authentication or access control on the API
- Fine-tuning the LLM on proprietary payments data

---

## Success Metrics

- **Narrative relevance** — output references correct KPIs and failure codes from the actual data
- **Anomaly precision** — no false positives on clean synthetic data
- **API response time** — /report endpoint returns in under 5 seconds
- **Time saved** — replaces 15-20 minutes of manual querying and writeup per health check

---

## Scope — What Is In v1

- CSV ingestion into SQLite with schema validation
- Global KPIs: success rate, volume, dispute rate, refund rate
- Breakdown KPIs: by region (NA, EU, APAC, LATAM) and by payment method (card, ACH, wallet, RTP)
- Top 5 failure code analysis
- Time-window filtering: 24h, 7d, 30d, all-time
- Threshold-based anomaly detection with critical and warning levels
- LLM-generated narrative via OpenAI GPT-4o-mini
- CLI entrypoint for local and cron use
- FastAPI REST API with four endpoints: /health, /kpis, /alerts, /report
- Synthetic data generator for development and testing

## Scope — What Is Out of v1

- Real data pipeline (Kafka, Airflow, dbt)
- Merchant-level or product-vertical-level breakdowns
- Slack or email alerting integration
- Frontend dashboard UI
- Historical trend comparison such as WoW or MoM delta
- Authentication and rate limiting on the API

---

## Feature Breakdown

**1. Data Ingestion**
Loads a CSV of payment transactions into a local SQLite database. Schema covers all standard payments fields: transaction ID, timestamp, amount, currency, merchant, region, payment method, status, failure code, dispute and refund flags, latency, channel, and experiment bucket.

**2. KPI Computation**
Computes the following metrics, all filterable by time window: global success rate and volume, success rate by region and payment method, top 5 failure codes by frequency, dispute rate and refund rate.

**3. Anomaly Detection**
Checks computed KPIs against configurable thresholds and returns structured alerts. Critical alert fires when global success rate falls below 80%. Warning alerts fire when any region or method success rate falls below 70%. Each alert includes level, type, and a plain-English message.

**4. LLM Narrative Generation**
Builds a structured prompt from the full KPI snapshot and sends it to GPT-4o-mini. The prompt instructs the model to act as a payments PM and produce a 4-5 sentence summary covering overall health, worst performing segment, top failure drivers, and one recommended action.

**5. REST API**
Four endpoints exposed via FastAPI. GET /health for liveness check. GET /kpis?window=7d for raw KPI breakdown. GET /alerts?window=7d for anomaly alerts only. GET /report?window=7d for the full report with KPIs, alerts, and narrative.

**6. CLI**
Single command entrypoint: python -m src.cli [window]. Prints snapshot, alerts, and narrative to terminal. Suitable for local use or scheduled cron jobs.

---

## Technical Architecture

Data flows in one direction:

payments_raw.csv → ingestion.py → payments.db → metrics.py → KPI dict → anomaly.py → alerts → reporter.py → LLM prompt → llm_client.py → OpenAI API → narrative → cli.py or api.py → output

Stack: Python 3.7+, SQLite, OpenAI GPT-4o-mini, FastAPI, Uvicorn, python-dotenv

---

## Production Roadmap

- **Data source** — replace CSV with Kafka stream or Snowflake/BigQuery
- **Database** — replace SQLite with PostgreSQL or Redshift
- **Pipeline** — replace manual script with Airflow or dbt on a schedule
- **Hosting** — replace local uvicorn with Docker container on AWS ECS or Cloud Run
- **Secrets** — replace .env file with AWS Secrets Manager or Azure Key Vault
- **LLM** — replace OpenAI direct call with Azure OpenAI private endpoint
- **Alerting** — extend API alerts to Slack bot or PagerDuty integration
- **Thresholds** — make configurable per merchant or product vertical rather than hardcoded
- **Auth** — add OAuth2 or API key middleware to the FastAPI layer

---

## Open Questions

1. Should anomaly thresholds be static or dynamically set based on rolling baselines?
2. Should the narrative be cached per time window to avoid redundant LLM calls?
3. At what transaction volume does SQLite become a bottleneck and require migration?
4. Should the /report endpoint support webhook delivery so consumers do not need to poll?
5. How do we handle multi-currency volume aggregation in a production setting?
