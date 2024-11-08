import re
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Create a SparkSession
spark = SparkSession.Builder().enableHiveSupport().getOrCreate()

# Get sparkContext object and set log level to warnings, in order that there's not
# too much output in the console that it's not necessary.
sc = spark.sparkContext
sc.setLogLevel("WARN")

bucket = "alec"
sales_bronze_path = f"s3a://{bucket}/bronze/tb_sales"

"""
Load data from S3/MinIO landing path into bronze layer using delta format.
Args:
filename (str): Name of the file to be readed from landing.
"""

try:
    # Get name of file to be processed from application arguments
    filename = sys.argv[1]
    print(f"Loading file: {filename}")
    file_path = f"s3a://{bucket}/landing/{filename}"
    df_sales = spark.read.format("csv").option("header", True).option("sep", ",").load(file_path)
    print("File loaded successfully")
except Exception as e:
    raise ValueError(f"Error when trying to load file from S3/MinIO landing path:\n{e}") from e

try:
    # Names with some special symbols crash command, so we're going to replace them.
    print("Removing special symbols from column names and adding metadata columns")
    cols_cleaned = {
        col: re.sub(r"[ ,;{}()\n\t=]", "", col)
        for col in df_sales.columns
        if any(char in col for char in " ,;{}()\n\t=")
    }

    df_sales_bronze = df_sales.withColumns(
        {"sys_imported_at": F.current_timestamp(), "sys_imported_from": F.lit(file_path)}
    ).withColumnsRenamed(cols_cleaned)
    print("Data cleaned and metadata added successfully")
except Exception as e:
    raise ValueError(f"Error when trying to clean column names:\n{e}") from e

try:
    print("Writing data to bronze layer")
    df_sales_bronze.write.format("delta").mode("overwrite").option("overwriteSchema", True).save(
        sales_bronze_path
    )
    spark.sql(
        f"CREATE TABLE IF NOT EXISTS alec_bronze.tb_sales USING DELTA LOCATION '{sales_bronze_path}'"
    ).show(1, False)
except Exception as e:
    raise ValueError(f"Error when trying to write data to bronze layer:\n{e}") from e
else:
    print("Data successfully loaded into bronze layer\n-------------------------------------------")
