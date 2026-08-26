from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator


with DAG(
    dag_id="tokopedia_etl",
    start_date=datetime(2026, 8, 25),
    schedule=None,
    catchup=False,
    tags=["tokopedia", "etl"],
) as dag:

    run_etl = DockerOperator(
        task_id="run_tokopedia_etl",

        image="tokopedia-etl-pipeline-etl",

        command="python /app/main.py",

        docker_url="unix://var/run/docker.sock",

        network_mode="tokopedia-etl-pipeline_default",

        environment={
            "POSTGRES_HOST": "postgres",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "tokopedia_db",
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
        },

        auto_remove="success",
	mount_tmp_dir=False,
    )