from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("biglake-iceberg-rest-catalog-test")
    .getOrCreate()
)

print("Spark catalogs:")
spark.sql("SHOW CATALOGS").show(truncate=False)


# Create namespace in BigLake catalog
spark.sql("""
CREATE NAMESPACE IF NOT EXISTS gaurav_catalog.demo
""")


# Create Iceberg table registered in BigLake catalog
spark.sql("""
CREATE TABLE IF NOT EXISTS gaurav_catalog.demo.customer (
    customer_id BIGINT,
    customer_name STRING,
    city STRING
)
USING ICEBERG
""")


# Insert test data
spark.sql("""
INSERT INTO gaurav_catalog.demo.customer VALUES
(1, 'Gaurav', 'Bangalore'),
(2, 'Alice', 'London'),
(3, 'Bob', 'New York')
""")


# Read back using Spark
print("Reading table from BigLake catalog:")
spark.sql("""
SELECT *
FROM gaurav_catalog.demo.customer
""").show()


# Show table metadata
print("Table metadata:")
spark.sql("""
DESCRIBE TABLE EXTENDED gaurav_catalog.demo.customer
""").show(truncate=False)


spark.stop()