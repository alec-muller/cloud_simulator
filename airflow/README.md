# Airflow

This directory contains the configuration and files required for Apache Airflow in the Data-Infrastructure Challenge project.

## Structure

- **Dockerfile**: Configures the Apache Airflow image, including dependencies and custom configurations.
- **dags/**: Contains the Directed Acyclic Graphs (DAGs) that define Airflow workflows.
- `load_transactional_data.py`: Main DAG to load and process transactional data, using scripts from the includes folder to submit the job to Spark.
    - This DAG expected to receive a param named "filename_sftp" in non-scheduled runs.
    - Creates schemas in the data lake.
    - Loads raw data to the bronze tier.
    - Processes data from the bronze tier to the silver tier.
    - Feeds the gold tier with refined and summarized data.
    - Uploads data to Postgres.
- **airflow.cfg**: Airflow configuration file, defining parameters such as connections and email settings.
- **webserver_config.py**: Configures sqlite as Airflow's default database.