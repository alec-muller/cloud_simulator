from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Create a SparkSession
spark = SparkSession.Builder().enableHiveSupport().getOrCreate()

# Get sparkContext object and set log level to warnings, in order that there's not
# too much output in the console that it's not necessary.
sc = spark.sparkContext
sc.setLogLevel("WARN")

bucket = "alec"
sales_silver_path = f"s3a://{bucket}/silver/tb_sales"
sales_gold_path = f"s3a://{bucket}/gold/tb_fact_sales"

"""
This function is responsible for transforming and loading data into the gold layer.
"""

try:
    print("Reading data from silver table")
    df_silver = spark.read.format("delta").load(sales_silver_path)
    print("Data read successfully")
except Exception as e:
    raise ValueError(f"Error when trying to read data from silver table:\n{e}") from e

try:
    print("Adding columns to partition table in gold layer and control update date.")
    df_fact_sales = (
        df_silver.withColumn("Year", F.date_format("order_date", "yyyy"))
        .withColumn("Month", F.date_format("order_date", "MM"))
        .withColumn("sys_updated_at", F.lit(None).cast("timestamp"))
    )
    df_fact_sales.show(10, False)
    print("Columns added successfully")
except Exception as e:
    raise ValueError(
        f"Error when trying to add columns to partition table in gold layer:\n{e}"
    ) from e

try:
    # We need to create delta table on gold layer if it not exists, because
    # we're going to perform a merge command, that will insert/update data on it.
    print("Creating table in gold layer if not exists")
    (
        DeltaTable.createIfNotExists(spark)
        .tableName("alec_gold.tb_fact_sales")
        .location(sales_gold_path)
        .addColumns(df_fact_sales.schema)
        .partitionedBy("Year", "Month")
        .execute()
    )
    print("Table created successfully")
except Exception as e:
    raise ValueError(f"Error when trying to create table in gold layer:\n{e}") from e

try:
    print("Executing merge into gold layer")
    fact_sales_delta = DeltaTable.forPath(spark, sales_gold_path)
    (
        fact_sales_delta.alias("old")
        .merge(
            df_fact_sales.withColumn("sys_updated_at", F.lit(None)).alias("new"),
            """
                    old.order_id = new.order_id
                AND old.customer_id = new.customer_id
                AND old.product_id = new.product_id
            """,
        )
        .whenNotMatchedInsertAll()
        .whenMatchedUpdate(
            set={
                "quantity": "new.quantity",
                "price": "new.price",
                "total_price": "new.total_price",
                "order_date": "new.order_date",
                "sys_hash": "new.sys_hash",
                "sys_updated_at": "new.sys_imported_at",
            }
        )
        .execute()
    )
    fact_sales_delta.toDF().show(10, False)
except Exception as e:
    raise ValueError(f"Error when trying to merge into gold layer:\n{e}") from e
else:
    print("Merge executed successfully.\n----------------------------------------------")
