FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.airflow.txt .
RUN pip install --no-cache-dir -r requirements.airflow.txt

ENV AIRFLOW_HOME=/usr/local/airflow
RUN useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow

WORKDIR ${AIRFLOW_HOME}

COPY dags/ ${AIRFLOW_HOME}/dags/
COPY scripts/ ${AIRFLOW_HOME}/scripts/
COPY config/ ${AIRFLOW_HOME}/config/
COPY plugins/  ${AIRFLOW_HOME}/plugins/
COPY logs/  ${AIRFLOW_HOME}/logs/

COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

EXPOSE 8888

ENTRYPOINT ["/bin/bash", "-c"]
RUN airflow db reset -y && airflow db init && airflow users create \
    --username airflow \
    --password airflow \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com

CMD ["airflow webserver --port 8888"]
