FROM apache/airflow:2.3.4

USER root
RUN apt-get update && \
    apt-get install -y wget gnupg unzip

# Install Python dependencies
COPY requirements.txt /requirements.txt
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt
