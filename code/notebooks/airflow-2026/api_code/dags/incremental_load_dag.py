import requests
import json
import os
from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.timetables.interval import CronDataIntervalTimetable
import pendulum


def call_api_and_save(**context):
    url = context['templates_dict']['url']
    output_path = context['templates_dict']['output_path']
    start_date=context['ds']
    end_date=context['ds']
    payload = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": 50
    }

    response = requests.post(url, json=payload, auth=("admin", "manish"))
    response.raise_for_status()
    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_path = os.path.join(output_path, f"dag_result_{timestamp}.json")

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved API output to: {output_path}")


dag = DAG(
    dag_id="incremental_load_dag_v2",
    start_date=datetime(2025, 12, 5),
    schedule=CronDataIntervalTimetable(
        cron="0 * * * *",
        timezone=pendulum.timezone("Asia/Kolkata")
    ),
    catchup=False
)

task = PythonOperator(
    task_id="call_api_and_save",
    python_callable=call_api_and_save,
    templates_dict={
        "output_path":"/opt/airflow/output_files/dag_result_{{ ds }}.json",
        "url":"http://fastapi-app:5000/getAll"
    },
    dag=dag
)
