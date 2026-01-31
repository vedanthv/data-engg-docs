import requests
import json
from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.timetables.interval import CronDataIntervalTimetable
import pendulum

dag = DAG(
    dag_id='my_first_dag_v2',
    start_date=datetime(2026, 1, 24),
    schedule=CronDataIntervalTimetable(
        cron="0 * * * *",
        timezone=pendulum.timezone("Asia/Kolkata")
    ),
    catchup=True
)

def print_context(**kwargs):
    print("\n===== AIRFLOW CONTEXT =====")
    for key, value in kwargs.items():
        print(f"{key:25} : {value}")
    print("===== END CONTEXT =====\n")

copy_file = BashOperator(
    dag=dag,
    task_id="copy_file",
    bash_command="echo copyop"
)

task2 = PythonOperator(
    task_id='task_2',
    python_callable=print_context,
    dag=dag
)

copy_file >> task2
