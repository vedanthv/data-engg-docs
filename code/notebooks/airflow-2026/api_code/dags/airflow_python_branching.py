from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import BranchPythonOperator
from datetime import datetime

dag = DAG(
    dag_id = "Pipeline_Layout_Example",
    start_date = datetime(2026,1,31),
    schedule="*/2 * * * *"
)

def decide_flow(**context):
    checkout_amount = 50
    if checkout_amount < 100:
        return "checkout"
    else:
        return "merged"
    
start = EmptyOperator(task_id='start',dag=dag)
end = EmptyOperator(task_id='end',dag=dag,trigger_rule='none_failed')

product_page = BashOperator(
    task_id = 'product_page',
    bash_command = "echo 'This is the product page task'",
    dag = dag,
)

checkout_page = BashOperator(
    task_id = 'checkout_page',
    bash_command = "echo 'This is the checkout page task'"
)

user_login_page = BashOperator(
    task_id = 'useR_login_page',
    bash_command = "echo 'This is the user login page'"
)

read_raw = BranchPythonOperator(
    task_id = 'read_raw',
    python_callable=decide_flow,
    dag = dag,
)

checkout = BashOperator(
    task_id = 'checkout',
    bash_command = "echo 'This is the checkout task'"
)

merge = BashOperator(
    task_id = 'merge',
    bash_command = "echo 'This is the merged task'"
)

alarming_situation = BashOperator(
    task_id = 'alarming_situation',
    bash_command = "echo 'This is the alarming situation task.'"
)

notify = BashOperator(
    task_id = "notify",
    bash_command = "echo 'This is notify task'",
    dag=dag,
)

start >> [product_page,user_login_page,checkout_page]
[product_page,user_login_page,checkout_page] >> read_raw
read_raw >> [checkout,merge]
checkout >> alarming_situation
merge >> notify
[alarming_situation,notify] >> end