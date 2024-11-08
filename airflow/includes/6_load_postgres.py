import sys

from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.Builder().enableHiveSupport().getOrCreate()

# Get sparkContext object and set log level to warnings, in order that there's not
# too much output in the console that it's not necessary.
sc = spark.sparkContext
sc.setLogLevel("WARN")

bucket = "alec"
gold_path = f"s3a://{bucket}/gold"

# Using airflow connection to define jdbc_url
print("Looking for postgres variables")
database = sys.argv[1]
host = sys.argv[2]
port = sys.argv[3]
user = sys.argv[4]
password = sys.argv[5]

# Create jdbc_url and properties from variables
jdbc_url = f"jdbc:postgresql://{host}:{port}/{database}"
properties = {"user": user, "password": password, "driver": "org.postgresql.Driver"}
print("Connections settings to Postgres defined.\nStarting write command.")

tables = [
    "tb_fact_sales",
    "tb_customer_summary",
    "tb_product_summary",
]

for table in tables:
    try:
        print(f"Reading table from gold: {table}")
        df = spark.read.format("delta").load(f"{gold_path}/{table}")
        print("Table read successfully. Starting writing into Postgres.")
        df.write.jdbc(
            url=jdbc_url,
            table=f"alec_warehouse.{table}",
            mode="overwrite",
            properties=properties,
        )
        print("Dataframe written to Postgres")
    except Exception as e:
        print(f"Erro ao gravar no postgres: {e}")

print("All tables were written into Postgres!\n----------------------------------")
