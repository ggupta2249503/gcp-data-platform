# GCP Data Platform — Learning Project

A production-style Python project for building data pipelines on GCP.

## Services Covered

- **Cloud Storage** — Data lake (raw, curated, analytics layers)
- **BigQuery** — Data warehouse (external tables, native tables, Iceberg)
- **Dataproc Serverless** — Spark jobs (batch ETL)

## Project Structure

```
gcp-data-platform/
├── config/
│   └── settings.py          # GCP clients & env vars
├── src/
│   ├── bigquery_ops.py      # BigQuery operations
│   ├── gcs_ops.py           # Cloud Storage operations
│   └── dataproc_ops.py      # Dataproc Serverless operations
├── tests/
│   └── test_bigquery.py     # Unit tests
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md
```

## Setup

```bash
cd gcp-data-platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables (.env)

```
GCP_PROJECT_ID=de-learning-project-510018
GCP_REGION=us-central1
GCP_BUCKET_RAW=de-learning-raw-510018
GCP_BUCKET_CURATED=de-learning-curated-510018
BQ_DATASET_RAW=raw
BQ_DATASET_CURATED=curated
BQ_DATASET_ICEBERG=iceberg
```

## Usage

```python
from src.bigquery_ops import run_query

result = run_query("SELECT * FROM `de-learning-project-510018.raw.apple_stock` LIMIT 10")
for row in result:
    print(row)
```
