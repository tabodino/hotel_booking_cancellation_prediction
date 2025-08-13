FROM python:3.10-slim

ARG JUPYTER_PORT=8888

# Java install (necessary for Spark)
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV JUPYTER_PORT=${JUPYTER_PORT}
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV SPARK_VERSION=4.0.0
ENV HADOOP_VERSION=3

# Spark install
RUN wget -q https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV SPARK_HOME=/opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV PATH=$PATH:$SPARK_HOME/bin

WORKDIR /app

COPY requirements.txt .

# Install necessary packages
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . .

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser"]
