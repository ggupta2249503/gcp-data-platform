from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("bq-to-parquet") \
    .getOrCreate()


tables = [
    "order_items"  
]

PROJECT = "de-learning-project-510018"


for table in tables:

    print(f"Processing {table}")

    df = spark.read \
        .format("bigquery") \
        .option(
            "table",
            f"{PROJECT}.raw.{table}"
        ) \
        .load()

    df.write \
        .mode("overwrite") \
        .parquet(
            f"gs://de-learning-curated-510018/parquet/{table}/"
        )

    print(f"Completed {table}")