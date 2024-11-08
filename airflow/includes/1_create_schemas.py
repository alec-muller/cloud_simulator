from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.Builder().enableHiveSupport().getOrCreate()

# Get sparkContext object and set log level to warnings, in order that there's not
# too much output in the console that it's not necessary.
sc = spark.sparkContext
sc.setLogLevel("WARN")

bucket = "alec"
sales_bronze_path = f"s3a://{bucket}/bronze/tb_sales"

"""
Create databases in S3/MinIO using medallion schema.
"""

try:
    print("Creating schema in delta using each layer location.")
    spark.sql(
        f"""
        CREATE SCHEMA IF NOT EXISTS {bucket}_bronze LOCATION 's3a://{bucket}/bronze/'
        """
    ).show(10, False)

    spark.sql(
        f"""
        CREATE SCHEMA IF NOT EXISTS {bucket}_silver LOCATION 's3a://{bucket}/silver/'
        """
    ).show(10, False)

    spark.sql(
        f"""
        CREATE SCHEMA IF NOT EXISTS {bucket}_gold LOCATION 's3a://{bucket}/gold/'
        """
    ).show(10, False)
except Exception as e:
    raise ValueError(f"Error when trying to create databases on S3/MinIO:\n{e}") from e
else:
    print(
        f"""Databases created successfully on S3/MinIO:
        {bucket}_bronze, {bucket}_silver, {bucket}_gold
        {spark.sql('show databases').show(10, False)}

        ---------------------------------------------------"""
    )
