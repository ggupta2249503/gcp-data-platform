
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("retail-etl") \
    .getOrCreate()

BUCKET_RAW = "de-learning-raw-510018"
TEMP_BUCKET = "de-learning-bq-staging-510018"
PROJECT = "de-learning-project-510018"

datasets = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "stores": "stores.csv",
    "suppliers": "suppliers.csv",
    "inventory": "inventory.csv",
    "promotions": "promotions.csv"
}

for table_name, file_name in datasets.items():

    print(f"Processing {file_name}")

    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(f"gs://{BUCKET_RAW}/rystore/{file_name}")

    print(f"{table_name} schema:")
    df.printSchema()

    df.write \
        .format("bigquery") \
        .option(
            "table",
            f"{PROJECT}.raw.{table_name}"
        ) \
        .option(
            "temporaryGcsBucket",
            TEMP_BUCKET
        ) \
        .mode("overwrite") \
        .save()

    print(f"Completed {table_name}")

