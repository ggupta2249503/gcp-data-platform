from pyspark.sql import SparkSession
from pyspark.sql.functions import *

PROJECT = "de-learning-project-510018"

spark = SparkSession.builder \
    .appName("create-iceberg-table") \
    .config(
        "spark.sql.extensions",
        "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
    ) \
    .config(
        "spark.sql.catalog.gaurav_gcp_catalog",
        "org.apache.iceberg.spark.SparkCatalog"
    ) \
    .config(
        "spark.sql.catalog.gaurav_gcp_catalog.type",
        "hadoop"
    ) \
    .config(
        "spark.sql.catalog.gaurav_gcp_catalog.warehouse",
        "gs://de-learning-curated-510018/iceberg-hadoop/"
    ) \
    .getOrCreate()

print(spark.version)


# Read BigQuery native table

orders = spark.read \
    .format("bigquery") \
    .option(
        "table",
        f"{PROJECT}.raw.orders"
    ) \
    .load()


orders.printSchema()


# Transformation

daily_sales = orders \
    .withColumn(
        "order_date",
        to_date("order_datetime")
    ) \
    .groupBy(
        "order_date"
    ) \
    .agg(
        sum("total_amount").alias("daily_sales"),
        count("order_id").alias("total_orders")
    )




# Create Iceberg table

daily_sales.writeTo(
    "gaurav_gcp_catalog.retail.daily_sales"
).using(
    "iceberg"
).createOrReplace()

daily_sales_df=spark.sql("""
SELECT *
FROM gaurav_gcp_catalog.retail.daily_sales
""")

daily_sales_df.show(5,truncate=False)


print("Iceberg table created successfully")