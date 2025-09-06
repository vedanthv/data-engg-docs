## Spark Architecture on YARN

---

### 1. Key Components

#### **a) Master Node / Cluster Manager**

* YARN ResourceManager (when Spark runs on YARN)
* Responsible for **resource allocation** (CPU, memory across cluster).
* It doesn’t run Spark code itself, but decides **where** and **how many** containers to start.

---

#### **b) Worker Nodes**

* The machines that actually **execute Spark tasks**.
* Each worker hosts YARN NodeManager.
* Containers are launched here to run parts of Spark applications.

---

#### **c) Driver Node**

* The **process that runs your main Spark application code** (`SparkContext`).
* Responsible for:

  * Creating the DAG of transformations and actions.
  * Submitting tasks to executors.
  * Collecting results.
* In YARN:

  * **Cluster mode** → Driver runs inside an ApplicationMaster container on a worker node.
  * **Client mode** → Driver runs on your local machine (the edge node / laptop) while executors run in cluster.

---

#### **d) Executors**

* JVM processes on worker nodes.
* Run tasks assigned by the Driver.
* Store data in memory/disk for caching/shuffles.
* Communicate with Driver throughout the job’s life.

---

#### **e) Application Master (AM)**

* A **YARN-specific concept**.
* Every YARN application (including Spark) gets its own AM.
* Responsibilities:

  * Request containers from YARN ResourceManager.
  * Monitor health of containers.
* For Spark-on-YARN, the **ApplicationMaster often hosts the Driver (in cluster mode)**.

---

---

# 2️⃣ What Happens When You Run `spark-submit`

Let’s assume you run:

```bash
spark-submit --master yarn --deploy-mode cluster my_app.py
```

---

### Step-by-Step Flow:

1. **spark-submit starts**

   * The client (edge node or local machine) contacts **YARN ResourceManager**.
   * Submits your application (including JARs, Python files, configs).

---

2. **YARN allocates ApplicationMaster container**

   * ResourceManager picks a worker node and starts the **ApplicationMaster (AM)**.
   * For Spark, this AM **bootstraps the Driver** inside itself (in cluster mode).

---

3. **Driver starts inside AM**

   * `SparkContext` is created.
   * Driver:

     * Builds logical execution plan (DAG).
     * Asks AM to request executor containers.

---

4. **AM requests Executors**

   * AM communicates with ResourceManager → “I need N executors with X cores & Y memory each.”
   * ResourceManager talks to NodeManagers on workers → allocates containers.
   * Executors are launched on those workers.

---

5. **Executors register with Driver**

   * Each executor JVM contacts Driver:
     “I’m alive and ready.”
   * Driver now knows how many executors it has and their resources.

---

6. **Tasks scheduled**

   * Driver divides DAG into **stages** → **tasks**.
   * Tasks are shipped to executors.
   * Executors run the tasks, fetch data (HDFS, S3, Delta, etc.), cache/shuffle results.

---

7. **Execution & Results**

   * Executors send status & results back to Driver.
   * Driver coordinates retries on failure.

---

8. **Job Completion**

   * Once all actions complete, Driver tells AM to stop executors.
   * AM unregisters with ResourceManager.
   * Job is marked as **finished**.

---

---

# 3️⃣ Cluster Mode vs Client Mode (Big Interview Question!)

* **Cluster Mode**

  * Driver runs inside the cluster (in AM container).
  * Good for production (doesn’t depend on client machine).

* **Client Mode**

  * Driver runs on submitting machine (edge node).
  * Executors still in cluster.
  * Good for development / debugging.

---

# 4️⃣ Quick Visual

```
+-----------------+          +-----------------+
| spark-submit    |          | YARN RM         |
| (client)        |          | (ResourceManager)|
+--------+--------+          +--------+--------+
         |                            |
         | Submit App                 |
         v                            |
+--------+--------+                   |
| App Master (AM) | <-----------------+
| (hosts Driver)  |
+--------+--------+
         |
         | Request Executors
         v
+--------+--------+     +--------+--------+
| Executor (Node) | ... | Executor (Node) |
+-----------------+     +-----------------+
```

---

# 5️⃣ In Summary

* **Driver** = Brain of Spark App (DAG, task scheduling).
* **Executors** = Workers that do actual computation.
* **ApplicationMaster** = YARN-specific agent that negotiates resources and may host Driver.
* **spark-submit** = Entry point that asks YARN to spin everything up.
* **Cluster Mode** = Driver in cluster (recommended for prod).
* **Client Mode** = Driver on local machine.

---
