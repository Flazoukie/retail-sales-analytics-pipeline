import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql.functions import (
    col, trim, when, to_timestamp, year, month
)

from awsglue.dynamicframe import DynamicFrame

# --------------------------------------------------------------------------------
# Glue boilerplate
# --------------------------------------------------------------------------------
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# --------------------------------------------------------------------------------
# READ RAW DATA FROM GLUE CATALOG
# --------------------------------------------------------------------------------
raw_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="retail_raw_db",
    table_name="online_retail",
)

df = raw_dyf.toDF()

# --------------------------------------------------------------------------------
# DATA CLEANING & TRANSFORMATIONS
# --------------------------------------------------------------------------------

# Cast proper types
df = (
    df
    .withColumn("invoice_no", col("invoiceno").cast("string"))
    .withColumn("stock_code", col("stockcode").cast("string"))
    .withColumn("description", trim(col("description")))
    .withColumn("quantity", col("quantity").cast("int"))
    .withColumn("invoice_date", to_timestamp(col("invoicedate"), "yyyy-MM-dd HH:mm:ss"))
    .withColumn("unit_price", col("unitprice").cast("double"))
    .withColumn("customer_id", col("customerid").cast("string"))
    .withColumn("country", col("country"))
)

# Handle missing customer IDs
df = df.withColumn("customer_id",
    when(col("customer_id").isNull(), "UNKNOWN").otherwise(col("customer_id"))
)

# Add revenue
df = df.withColumn("revenue", col("quantity") * col("unit_price"))

# Add date parts
df = (
    df
    .withColumn("year", year(col("invoice_date")))
    .withColumn("month", month(col("invoice_date")))
)

# Add return flag
df = df.withColumn("is_return", col("quantity") < 0)

# Drop original messy column names
df = df.drop("invoiceno", "stockcode", "invoicedate", "unitprice", "customerid")

# Convert back to DynamicFrame
curated_dyf = DynamicFrame.fromDF(df, glueContext, "curated")


# --------------------------------------------------------------------------------
# WRITE PARTITIONED PARQUET TO S3
# --------------------------------------------------------------------------------

glueContext.write_dynamic_frame.from_options(
    frame=curated_dyf,
    connection_type="s3",
    connection_options={
        "path": "s3://retail-demo-flavia/curated/online_retail/",
        "partitionKeys": ["year", "month"]
    },
    format="parquet"
)

job.commit()
