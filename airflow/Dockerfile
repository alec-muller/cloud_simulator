FROM apache/airflow:latest-python3.12

# Copy DAGs and includes folders
COPY --chown=airflow:root ./dags ${AIRFLOW_HOME}/dags
COPY --chown=airflow:root ./includes ${AIRFLOW_HOME}/includes

# Copy airflow.cfg custom file
COPY --chown=airflow:root ./airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

# Copy requirements.txt file
COPY --chown=airflow:root ./requirements.txt ${AIRFLOW_HOME}/requirements.txt

# Switch to root user
USER root

# Update repositories and install needed packages
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk ant procps wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Define JAVA_HOME and PATH
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Back to airflow user to install dependencies
USER airflow

# Install dependencies
RUN pip install --no-cache-dir -r ${AIRFLOW_HOME}/requirements.txt

# Define Airflow's environment variables
ENV AIRFLOW__CORE__DAGS_FOLDER=${AIRFLOW_HOME}/dags
ENV AIRFLOW__CORE__PLUGINS_FOLDER=${AIRFLOW_HOME}/plugins
ENV AIRFLOW__LOGGING__BASE_LOG_FOLDER=${AIRFLOW_HOME}/logs

# Define workspace
WORKDIR ${AIRFLOW_HOME}