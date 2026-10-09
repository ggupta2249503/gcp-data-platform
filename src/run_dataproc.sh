#!/bin/bash

set -e

PROJECT_ID="de-learning-project-510018"
REGION="us-central1"

BUCKET="de-learning-raw-510018"

SCRIPT="create_iceberg_lakehouse_table.py"

GCS_SCRIPT_PATH="gs://${BUCKET}/scripts/${SCRIPT}"

CATALOG_ID="gaurav-lakehouse-catalog"
CATALOG_NAME="gaurav_catalog"


echo "Uploading Python files..."

gcloud storage cp *.py gs://${BUCKET}/scripts/


echo "Submitting Dataproc Serverless Spark job..."


gcloud dataproc batches submit pyspark \
    ${GCS_SCRIPT_PATH} \
    --project=${PROJECT_ID} \
    --region=${REGION} \
    --version=2.2 \
    --properties="\
spark.sql.defaultCatalog=${CATALOG_NAME},\
spark.sql.catalog.${CATALOG_NAME}=org.apache.iceberg.spark.SparkCatalog,\
spark.sql.catalog.${CATALOG_NAME}.type=rest,\
spark.sql.catalog.${CATALOG_NAME}.uri=https://biglake.googleapis.com/iceberg/v1/restcatalog,\
spark.sql.catalog.${CATALOG_NAME}.warehouse=bl://projects/${PROJECT_ID}/catalogs/${CATALOG_ID},\
spark.sql.catalog.${CATALOG_NAME}.header.X-Iceberg-Access-Delegation=vended-credentials,\
spark.sql.catalog.${CATALOG_NAME}.header.x-goog-user-project=${PROJECT_ID},\
spark.sql.catalog.${CATALOG_NAME}.rest.auth.type=org.apache.iceberg.gcp.auth.GoogleAuthManager,\
spark.sql.catalog.${CATALOG_NAME}.io-impl=org.apache.iceberg.gcp.gcs.GCSFileIO,\
spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"


echo "Done"