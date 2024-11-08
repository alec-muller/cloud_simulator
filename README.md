# Data-Infrastructure Challenge

This project implements a data lake architecture using Apache Airflow, Apache Spark, MinIO, and PostgreSQL.

## Project Structure

- `docker-compose.yml`: Main configuration file to orchestrate all services.
- `airflow/`: Contains configurations and code related to Apache Airflow.
- `minio/`: Configurations for the MinIO service (S3-compatible object storage).
- `postgres/`: Configurations for the PostgreSQL database.
- `spark/`: Configurations for Apache Spark.

## How to Use

1. Ensure that Docker and Docker Compose are installed on your machine.
2. In the root directory of the project, run:

```
docker-compose up -d
```

3. Access Airflow web interface in `http://localhost:8080`.

## Services

- Airflow Webserver: <http://localhost:8080> - AWS similar: Amazon Managed Workflows for Apache Airflow (MWAA)
- MinIO Console: <http://localhost:9001> - AWS Similar: Amazon Simple Storage Service (S3)
- PostgreSQL: localhost:5432 - AWS Similar: AWS Similar: Amazon Relational Database Service (RDS) and Amazon Redshift
- Spark Master WebUI: <http://localhost:8081> - AWS Similar: Amazon Elastic MapReduce (EMR)

PS: Docker can be related to some AWS as well, like Amazon EKS, Amazon ECS, AWS Fargate
For more details on each component, see the READMEs in their respective directories.

---------------------------------------

# Docker Compose Configuration

This `docker-compose.yml` file defines and configures all the services required for the Data-Infrastructure Challenge project.

## Instances

- **minio**: S3-compatible object storage service.
- **createbuckets**: Temporary service for creating initial buckets in MinIO.
- **airflow-webserver**: Apache Airflow web interface.
- **airflow-scheduler**: Airflow job scheduler.
- **airflow-init**: Airflow initialization service.
- **postgres**: PostgreSQL database.
- **spark-master**: Spark cluster master node.
- **spark-worker**: Spark cluster worker node.

## Volumes

- **minio_data**: Stores MinIO data.
- **postgres_data**: Stores PostgreSQL data.

## Networks

- A standard bridge network is used for communication between services.

## Usage

To start all services:

```bash
docker-compose up -d
```

To stop all services:

```bash
docker-compose down
```
