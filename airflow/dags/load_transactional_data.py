from datetime import datetime, timedelta

# from include.etl_pipeline_deltawarehouse import Data-Infrastructure Challenge
from airflow.decorators import dag, task
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {"owner": "Alec", "retries": 1, "retry_delay": timedelta(minutes=2)}


@dag(
    dag_id="load_transactional_data",
    start_date=datetime(2024, 10, 20),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
)
def main():
    """
    This DAG is responsible for loading transactional data into delta warehouse
    """
    # Get the date from when this DAG is expected to run
    v_today = "{{ data_interval_end }}"

    ## Tasks definition session

    # Below task is just an example of how would be used an Operator to bring a daily file from FTP
    # to S3. This task is not used in this DAG because there isn't a FTP server to simulate.
    # @task()
    # def upload_to_landing(today, **context):
    #     today_date = datetime.fromisoformat(today).strftime("%Y%m%d")
    #     filename = f"sales_data_{today_date}.csv"
    #     upload_cmd = FTPToS3Operator(
    #         ftp_path=f"some/ftp/path/{filename}",
    #         s3_bucket="alec",
    #         s3_key=f"landing/{filename}",
    #         ftp_conn_id="ftp_default",
    #         aws_conn_id="aws_default",
    #     )
    #     upload_cmd.execute(context)

    create_schemas = SparkSubmitOperator(
        task_id="create_schemas",
        application="./includes/1_create_schemas.py",
        conn_id="spark_default",
        deploy_mode="client",
        name="create_schemas",
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.access.key": "root",
            "spark.hadoop.fs.s3a.secret.key": "12345678",
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "true",
            "spark.hadoop.fs.s3a.connection.timeout": "600000",
        },
        packages="io.delta:delta-spark_2.12:3.2.1,org.apache.hadoop:hadoop-aws:3.3.2",
    )

    @task()
    def get_filename(today, **context):
        f_name = context["dag_run"].conf.get("filename_sftp")
        if f_name:
            return f_name
        else:
            today_date = datetime.fromisoformat(today).strftime("%Y%m%d")
            return f"sales_data_{today_date}.csv"

    load_bronze = SparkSubmitOperator(
        task_id="load_bronze",
        application="./includes/2_load_bronze.py",
        conn_id="spark_default",
        deploy_mode="client",
        name="load_bronze",
        application_args=["{{ ti.xcom_pull(task_ids='get_filename') }}"],
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.access.key": "root",
            "spark.hadoop.fs.s3a.secret.key": "12345678",
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "true",
            "spark.hadoop.fs.s3a.connection.timeout": "600000",
        },
        packages="io.delta:delta-spark_2.12:3.2.1,org.apache.hadoop:hadoop-aws:3.3.2",
    )

    load_silver = SparkSubmitOperator(
        task_id="load_silver",
        application="./includes/3_load_silver.py",
        conn_id="spark_default",
        deploy_mode="client",
        name="load_silver",
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.access.key": "root",
            "spark.hadoop.fs.s3a.secret.key": "12345678",
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "true",
            "spark.hadoop.fs.s3a.connection.timeout": "600000",
        },
        packages="io.delta:delta-spark_2.12:3.2.1,org.apache.hadoop:hadoop-aws:3.3.2",
    )

    load_gold = SparkSubmitOperator(
        task_id="load_gold",
        application="./includes/4_load_gold.py",
        conn_id="spark_default",
        deploy_mode="client",
        name="load_gold",
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.access.key": "root",
            "spark.hadoop.fs.s3a.secret.key": "12345678",
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "true",
            "spark.hadoop.fs.s3a.connection.timeout": "600000",
        },
        packages="io.delta:delta-spark_2.12:3.2.1,org.apache.hadoop:hadoop-aws:3.3.2",
    )

    aggregate_data = SparkSubmitOperator(
        task_id="aggregate_data",
        application="./includes/5_aggregate_data.py",
        conn_id="spark_default",
        deploy_mode="client",
        name="aggregate_data",
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.access.key": "root",
            "spark.hadoop.fs.s3a.secret.key": "12345678",
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "true",
            "spark.hadoop.fs.s3a.connection.timeout": "600000",
        },
        packages="io.delta:delta-spark_2.12:3.2.1,org.apache.hadoop:hadoop-aws:3.3.2",
    )

    load_postgres = SparkSubmitOperator(
        task_id="load_postgres",
        application="./includes/6_load_postgres.py",
        conn_id="spark_default",
        deploy_mode="client",
        name="load_postgres",
        application_args=[
            "{{ conn.postgres_default.schema }}",
            "{{ conn.postgres_default.host }}",
            "{{ conn.postgres_default.port }}",
            "{{ conn.postgres_default.login }}",
            "{{ conn.postgres_default.password }}",
        ],
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.access.key": "root",
            "spark.hadoop.fs.s3a.secret.key": "12345678",
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "true",
            "spark.hadoop.fs.s3a.connection.timeout": "600000",
        },
        packages="io.delta:delta-spark_2.12:3.2.1,org.apache.hadoop:hadoop-aws:3.3.2,org.postgresql:postgresql:42.7.4",
    )

    (
        create_schemas
        >> get_filename(v_today)
        >> load_bronze
        >> load_silver
        >> load_gold
        >> aggregate_data
        >> load_postgres
    )


main()
