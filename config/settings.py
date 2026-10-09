import os
from dotenv import load_dotenv
from google.cloud import bigquery, storage

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "de-learning-project-510018")
REGION = os.getenv("GCP_REGION", "us-central1")
BUCKET_RAW = os.getenv("GCP_BUCKET_RAW", "de-learning-raw-510018")
BUCKET_CURATED = os.getenv("GCP_BUCKET_CURATED", "de-learning-curated-510018")

BQ_CLIENT = bigquery.Client(project=PROJECT_ID)
GCS_CLIENT = storage.Client(project=PROJECT_ID)


def get_bq_client():
    return BQ_CLIENT


def get_gcs_client():
    return GCS_CLIENT
