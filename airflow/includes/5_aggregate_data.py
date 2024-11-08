from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.Builder().enableHiveSupport().getOrCreate()

# Get sparkContext object and set log level to warnings, in order that there's not
# too much output in the console that it's not necessary.
sc = spark.sparkContext
sc.setLogLevel("WARN")

bucket = "alec"
gold_path = f"s3a://{bucket}/gold"


df_sales = spark.read.format("delta").load(f"{gold_path}/tb_fact_sales")
df_sales.createOrReplaceTempView("tb_sales")

try:
    print("Summarizing data in customer_id level")
    df_customer_summary = spark.sql("""
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        AVG(price) AS avg_price,
        SUM(quantity) AS total_quantity,
        SUM(total_price) AS revenue,
        SUM(quantity) / COUNT(DISTINCT order_id) avg_items_per_order,
        AVG(total_price) AS avg_price_per_order,
        AVG(total_price / quantity) AS avg_price_per_product
    FROM tb_sales
    GROUP BY customer_id
    ORDER BY SUM(total_price) DESC
    """)
except Exception as e:
    raise ValueError(f"Error when trying to summarize customer data.\n:{e}") from e

try:
    print("Summarizing data in product_id level")
    df_product_summary = spark.sql("""
    SELECT
        product_id,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS total_customers,
        SUM(quantity) AS total_quantity, 
        AVG(quantity) AS avg_quantity,
        AVG(price) AS avg_price,
        SUM(total_price) / SUM(quantity) AS avg_price_per_order, 
        SUM(total_price) AS total_revenue,
        AVG(total_price) AS avg_revenue_per_order,
        AVG(total_price / quantity) AS avg_revenue_per_unit
    FROM tb_sales
    GROUP BY product_id
    ORDER BY SUM(total_price) DESC
    """)
except Exception as e:
    raise ValueError(f"Error when trying to summarize product data.\n:{e}") from e

try:
    print("Writing summary tables to gold layer")
    df_customer_summary.write.format("delta").mode("overwrite").save(
        f"{gold_path}/tb_customer_summary"
    )
    df_product_summary.write.format("delta").mode("overwrite").save(
        f"{gold_path}/tb_product_summary"
    )
except Exception as e:
    raise ValueError(f"Error when trying to write summary tables to gold layer.\n:{e}") from e
else:
    print("Summary tables successfully written to gold layer.")
