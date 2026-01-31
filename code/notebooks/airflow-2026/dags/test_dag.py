import requests
import json
from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

API_URL = "http://fastapi-app:5000/getAll"   # <--- Container-to-container hostname

def call_api_and_save(**kwargs):
    payload = {
        "start_date": "2025-12-01",
        "end_date": "2025-12-05",
        "limit": 50
    }

    response = requests.post(API_URL, json=payload, auth=("admin", "manish"))
    response.raise_for_status()
    data = response.json()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = f"/opt/airflow/output_files/dag_result_{timestamp}.json"

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved API output to: {output_path}")


dag = DAG(
    dag_id="save_api_output",
    start_date=datetime(2025, 12, 5),
    catchup=False
)

task = PythonOperator(
    task_id="call_api_and_save",
    python_callable=call_api_and_save,
    dag=dag
)
