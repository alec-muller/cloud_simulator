FROM bitnami/spark:3.5.3

USER root

# Instalar dependências e SSH server
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    # openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Definir variáveis de ambiente
ENV SPARK_HOME=/opt/bitnami/spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Diretório para armazenar JARs
RUN mkdir -p $SPARK_HOME/jars

# Baixar JARs necessários
RUN wget -P $SPARK_HOME/jars/ \
    https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.2.1/delta-spark_2.12-3.2.1.jar \
    && wget -P $SPARK_HOME/jars/ \
    https://repo1.maven.org/maven2/io/delta/delta-hive_2.12/3.2.1/delta-hive_2.12-3.2.1.jar \
    && wget -P $SPARK_HOME/jars/ \
    https://jdbc.postgresql.org/download/postgresql-42.7.4.jar \
    && wget -P $SPARK_HOME/jars/ \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar \
    && wget -P $SPARK_HOME/jars/ \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.2/hadoop-common-3.3.2.jar

# Adicionar JARs do Hadoop AWS (dependências do Hadoop)
RUN wget -P $SPARK_HOME/jars/ \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.361/aws-java-sdk-bundle-1.12.361.jar \
    && wget -P $SPARK_HOME/jars/ \
    https://repo1.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.13/httpclient-4.5.13.jar

# Definir o diretório de trabalho
WORKDIR $SPARK_HOME

# Voltar para o usuário não root
USER 1001
