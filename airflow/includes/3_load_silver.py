from delta.tables import DeltaTable
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.Builder().enableHiveSupport().getOrCreate()

# Get sparkContext object and set log level to warnings, in order that there's not
# too much output in the console that it's not necessary.
sc = spark.sparkContext
sc.setLogLevel("WARN")

bucket = "alec"
sales_bronze_path = f"s3a://{bucket}/bronze/tb_sales"
sales_silver_path = f"s3a://{bucket}/silver/tb_sales"

"""
Load data from bronze layer into silver layer using delta format.
"""

try:
    print("Loading data from bronze layer")
    df_bronze = DeltaTable.forPath(spark, sales_bronze_path).toDF()
    df_bronze.createOrReplaceTempView("sales")
    print("Data loaded successfully")
except Exception as e:
    raise ValueError(f"Error when trying to load data from bronze layer:\n{e}") from e

try:
    print("Transforming data for silver layer")
    df_silver = spark.sql(
        """
        WITH sales_refined AS (
            SELECT
                CAST(TRIM(order_id) AS LONG) order_id,
                CAST(TRIM(customer_id) AS LONG) customer_id,
                CAST(TRIM(product_id) AS LONG) product_id,
                CAST(TRIM(quantity) AS INT) quantity,
                CAST(TRIM(price) AS DOUBLE) price,
                CAST(
                    REGEXP_REPLACE(order_date, '[^0-9\-]', '')
                    AS DATE
                ) order_date,
                sys_imported_at,
                sys_imported_from
            FROM sales
        )
        SELECT
            order_id,
            customer_id,
            product_id,
            quantity,
            price,
            ROUND((quantity * price), 2) total_price,
            order_date,
            SHA2(
                CONCAT_WS(
                    ',',
                    order_id, customer_id, product_id, quantity,
                    price, ROUND(quantity * price, 2), order_date
                ),
                256
            ) sys_hash,
            sys_imported_at,
            sys_imported_from
        FROM sales_refined
        """
    )
    df_silver.show(10, False)
    print("Data transformed successfully")
except Exception as e:
    raise ValueError(f"Error when trying to transform data for silver layer:\n{e}") from e

try:
    print("Loading data into silver layer")
    df_silver.write.format("delta").mode("overwrite").save(sales_silver_path)
    spark.sql(
        f"CREATE TABLE IF NOT EXISTS alec_silver.tb_sales USING DELTA LOCATION '{sales_silver_path}'"
    ).show(10, False)
except Exception as e:
    raise ValueError(f"Error when trying to load data into silver layer:\n{e}") from e
else:
    print("Data loaded successfully into silver layer\n-------------------------------------------")
