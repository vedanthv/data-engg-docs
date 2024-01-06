## Core Airflow for Data Pipelines

This is the notes for Airflow tool from coder2j channel on YouTube.

A quick note, you can refer this [link](https://vedanthv.github.io/data-engg-docs/astronomer/). It has most of the details from here but the installation steps are much more clear here!!

### Installation

#### Using pip package

1. Python 3.6 is the min version required.

2. Create a Python Virtual Environment ```python3 -m venv py_env```

3. Activate the Python Environment **py_env** ```source py_env/bin/activate```

4. Install airflow using ```pip install apache-airflow```

5. Now before creating a db, we have to set the path ```export AIRFLOW_HOME = .```

6. Initialize the db with ```airflow db init```

7. Start Airflow Web Server using ```airflow webserver -p 8080```

8. Create a username and password ```airflow users create --username admin --firstname ved --lastname baliga --role admin --email vedanthvbaliga@gmail.com``` and set the password.

9. Run ```airflow scheduler``` to start the scheduler.

#### Using Docker for Installation

1. For Windows, first setup and setup WSL2. Check out the [video](https://www.youtube.com/watch?v=YByZ_sOOWsQ&pp=ygUdaW5zdGFsbGluZyB3c2wyIG9uIHdpbmRvd3MgMTE%3D) here.

2. Now download Docker Desktop from the [website](https://docs.docker.com/desktop/install/windows-install/)

3. Use this curl command to dowload Airflow yaml file via Docker Compose.[```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml'```]

4. Change the core executor in yaml file to LocalExecutor. Remove the Celery flower and celery-worker.

5. Initialize the Environment : ```mkdir -p ./dags ./logs ./plugins ./config echo -e "AIRFLOW_UID=$(id -u)" > .env```

6. Start the docker environment : ```docker compose up airflow-init```

7. Run Airflow : ```docker compose up```

### Core Concepts

What is Airflow?
![image](https://github.com/vedanthv/data-engg/assets/44313631/8edfa98b-7119-4d66-b0fd-e6e6687a952a)

What is a workflow?
![image](https://github.com/vedanthv/data-engg/assets/44313631/48ef6fce-07e4-422c-9e63-022ec686cbfd)

DAG, Task and Operator
![image](https://github.com/vedanthv/data-engg/assets/44313631/3fc46745-e852-4007-bf76-820ae2c48c5a)

Here A is the downstream task of C and B is the upstream task of A. Task implements an operator and DAG is a collection of operators working together.

![image](https://github.com/vedanthv/data-engg/assets/44313631/dd4617c9-1145-4b5a-9aae-72b84e72343a)

### Task Architecture

![image](https://github.com/vedanthv/data-engg/assets/44313631/c4861188-b5cf-4523-bf80-51079ca3f94e)

### Complete Task Lifecycle

![image](https://github.com/vedanthv/data-engg/assets/44313631/caebdbb0-96ff-4ec2-9361-f8621135425b)

### Complete Airflow Architecture Design

![image](https://github.com/vedanthv/data-engg/assets/44313631/898d4868-0e23-4111-aae6-976e4c35ba01)

**How does Data Engineer help in the process**

![image](https://github.com/vedanthv/data-engg/assets/44313631/ad4ff9f1-05f7-48c1-852f-20c9fcd81b6c)

### Creating DAGs

Downstream and Upstream Tasks with DAG
![image](https://github.com/vedanthv/data-engg/assets/44313631/526fb6cd-ef73-496d-8aef-2512dc22e85d)

### Airflow XComs For Information Sharing

Airflow XCom allows us to push info from one task to other and another task can pull information from the XCon.

Every Function's return value goes to XCom by default.

Here is the [code](https://github.com/vedanthv/data-engg/blob/main/airflow/02-pythonOperator.py) for one value push into XComs.

Here is the [code](https://github.com/vedanthv/data-engg/blob/main/airflow/03-xcom.py) for pushing two or more values with keys into XComs.


