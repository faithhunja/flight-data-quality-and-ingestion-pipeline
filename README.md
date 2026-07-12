# Flight Data Quality and Ingestion Pipeline

A self-orchestrated data pipeline that ingests live aircraft telemetry data, validates it against a strict data contract, and only stores data that passes the validation. This project runs on **GitHub Actions**, uses `uv` for environment management, and enforces data quality using **Great Expectations (GX) Core 1.0**.

## System Architecture

The pipeline follows the following design:

1. **Orchestration:** Through a manual dispatch, GitHub Actions provisions a Linux runner.

2. **Environment setup:** A composite action installs Python, uv and the required dependencies.

3. **Ingestion:** The OpenSky Network API is queried for live aircraft telemetry data within the Kenyan airspace.

4. **Validation:** A Great Expectations checkpoint is run against the new batch of incoming data to enforce strict data contracts.

5. **Validation outcome:**
- **Pass:** the data batch is automatically committed to a csv file in the repository.
- **Fail:** the pipeline is halted and a Great Expectations Data Docs HTML report is exported as a workflow artifact, showing exactly where the data contract failed.

## Tech Stack and Tools

* **Orchestration:** GitHub Actions
* **Environment management:** uv
* **Data quality framework:** Great Expectations Core 1.0
* **Language & core libraries:** Python 3.12, pandas, requests
* **Data source:** [OpenSky Network REST API](https://openskynetwork.github.io/opensky-api/)

## Repository Structure

```text
├── .github/
│   ├── actions/
│   │   └── setup-python-env/
│   │       └── action.yml        # Composite action: Python & uv setup
│   └── workflows/
│       └── data_pipeline.yml     # Main GitHub Actions workflow
├── data/
│   └── live_flights.csv          # Validated telemetry storage
├── gx/                           # Great Expectations configuration root
│   ├── checkpoints/              # Quality gate execution rules
│   └── expectations/             # Data contract definitions
├── src/
│   └── fetch_data.py             # Flight data ingestion script
├── pyproject.toml                # Project dependency definitions
├── uv.lock                       # Locked environment dependency versions
└── run_validation.py             # Great Expectations checkpoint runner
```

## Getting started

### Prerequisites

* Python 3.12
* `uv` installed locally

### Setup

```bash
git clone https://github.com/faithhunja/flight-data-quality-and-ingestion-pipeline

cd light-data-quality-and-ingestion-pipeline

uv sync --frozen
```

### Run locally

```bash
# Fetch the latest telemetry batch
uv run src/fetch_data.py

# Validate it against the data contract
uv run run_validation.py
```

A successful validation exits `0` and leaves the new batch ready to persist. A failed validation exits `1`. Both instances generate a report at `gx/uncommitted/data_docs/local_site/index.html`.

### Run in GitHub Actions

Trigger the pipeline manually from the **Actions** tab (`workflow_dispatch`) on GitHub. Download the `data-docs` artifact from the workflow run summary to view the diagnostic report.

## Data contract

The Great Expectations suite enforces:

* `icao24` (aircraft identifier), `latitude` and `longitude` must never be null.
* `velocity` must be a float type.
