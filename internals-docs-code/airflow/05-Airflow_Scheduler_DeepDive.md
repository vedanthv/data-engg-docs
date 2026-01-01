## Airflow Scheduler — Deep Dive (Internals & Mental Model)

### In **Apache Airflow**

![Image](https://airflow.apache.org/docs/apache-airflow/2.2.4/_images/arch-diag-basic.png)

![Image](https://imgix.datadoghq.com/img/blog/key-metrics-for-airflow-monitoring/airflow-arch-diagram.png?auto=compress%2Cformat\&cs=origin\&dpr=1\&fit=max\&h=\&lossless=true\&q=75\&w=)

![Image](https://airflow.apache.org/docs/apache-airflow/stable/_images/diagram_basic_airflow_architecture.png)

The **Scheduler** is the **most complex and critical component** of Airflow.
If the scheduler is unhealthy, Airflow *looks alive* but **nothing runs**.

---

# 1) What the Scheduler Really Does (Not Marketing Version)

The scheduler is **not a simple cron**.
It is a **continuous decision engine** that:

1. Parses DAGs
2. Decides **when DAG runs should exist**
3. Decides **which task instances can run**
4. Enforces **dependencies, limits, and policies**
5. Persists every decision to the **metadata database**

It does **zero execution** itself.

---

# 2) Scheduler Core Loop (Very Important)

The scheduler runs an **infinite loop** called the **scheduling heartbeat**.

Conceptually:

```
while True:
    parse_dags()
    create_dag_runs()
    create_task_instances()
    evaluate_dependencies()
    queue_tasks()
    sleep(heartbeat)
```

Every iteration:

* Reads from metadata DB
* Writes scheduling decisions back

---

# 3) DAG Parsing Phase (Why Parsing Is Expensive)

## What Happens

* Scheduler scans DAG folder
* Imports each DAG file
* Executes top-level Python code
* Extracts DAG objects

### Writes to DB

* Updates `dag` table
* Updates `serialized_dag` table (Airflow 2.x)

---

## Why Heavy DAG Files Kill Scheduler

Bad DAG file:

```python
df = spark.read.parquet("s3://...")
```

This runs **every parse cycle**.

Impact:

* CPU spikes
* Scheduler lag
* DAGs appear missing or delayed

Rule:

> DAG files define structure, not work

---

# 4) DAG Run Creation Logic (Critical)

Scheduler checks for each DAG:

* `start_date`
* `schedule_interval`
* `catchup`
* `max_active_runs`
* last `dag_run.execution_date`

### If a run is needed:

* Inserts row into `dag_run`
* Sets state = `RUNNING`

Important insight:

> DAG runs are created **before** any task is eligible to run

---

# 5) Task Instance Materialization

For every DAG run:

* Scheduler creates **TaskInstance rows**
* One row per task per logical date

Initial state:

```
task_instance.state = NONE
```

This is **pure bookkeeping**, not execution.

---

# 6) Dependency Resolution (The Real Scheduler Work)

This is where most CPU time goes.

For each TaskInstance, scheduler checks:

### Task Dependencies

* Upstream task states
* Trigger rules
* `depends_on_past`

### DAG-Level Limits

* `max_active_runs`
* `concurrency`

### Global Limits

* Pools
* Parallelism
* Executor slots

Only if **all checks pass**:

```
task_instance.state = SCHEDULED
```

---

# 7) Queuing Tasks

Scheduler hands off runnable tasks to the **executor**.

### Metadata DB transition

```
SCHEDULED → QUEUED
```

At this point:

* Scheduler responsibility ends
* Executor responsibility begins

Scheduler never waits for execution.

---

# 8) Scheduler Heartbeat & Locking

Scheduler runs with a **heartbeat**:

* Default: a few seconds
* Every heartbeat:

  * Acquire DB lock
  * Make scheduling decisions
  * Release lock

### Why Locking Exists

* Prevent multiple schedulers from scheduling the same task
* Ensure consistency in HA mode

If DB is slow:

* Heartbeats miss
* Scheduling stalls
* Tasks remain queued

---

# 9) High Availability Scheduler (Multiple Schedulers)

In Airflow HA:

* Multiple scheduler processes run
* Only **one scheduler instance** makes a scheduling decision for a task
* DB-level locks enforce safety

Important:

> Scaling schedulers helps parsing and decision throughput, not execution speed

---

# 10) Scheduler Bottlenecks (Real Production Issues)

### 1) Metadata DB Latency

* Slow `task_instance` queries
* Long scheduling cycles
* DAGs appear “stuck”

### 2) Too Many DAGs

* Parse time dominates
* Scheduler never catches up

### 3) Too Many Small Tasks

* Millions of state transitions
* DB write amplification

### 4) Sensors

* Long-running sensor tasks block worker slots
* Increase scheduler bookkeeping

---

# 11) Scheduler vs Executor Responsibilities

| Scheduler               | Executor                 |
| ----------------------- | ------------------------ |
| Creates DAG runs        | Executes tasks           |
| Resolves dependencies   | Assigns workers          |
| Enforces limits         | Manages worker lifecycle |
| Writes scheduling state | Updates execution state  |

If tasks are queued but not running:

* Executor issue

If tasks never get queued:

* Scheduler issue

---

# 12) Why Scheduler Is State-Driven (Not Event-Driven)

Scheduler does **not react to events**.

Instead:

* Polls metadata DB
* Recomputes state
* Makes idempotent decisions

This design enables:

* Restarts without loss
* Backfills
* Partial reruns

But costs:

* High DB load
* Slower reaction time

---

# 13) Mental Model (Internal Truth)

Think of scheduler as:

```
A loop that repeatedly asks:
"Given everything I know from the DB,
what is allowed to run right now?"
```

Then it updates the DB accordingly.

---

## One-Line Summary

**The Airflow scheduler is a state-driven decision engine that continuously parses DAGs, creates DAG runs, resolves dependencies, and queues task instances using the metadata database as its single source of truth.**

---
