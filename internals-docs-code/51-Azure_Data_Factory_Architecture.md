# 🏗 Azure Data Factory Architecture (In Depth)

<img width="960" height="540" alt="image" src="https://github.com/user-attachments/assets/091c52f3-b672-4c7d-a490-40a0c7bcb804" />

At a high level, ADF has **5 core building blocks**:

1. **Pipelines**
2. **Activities**
3. **Datasets**
4. **Linked Services**
5. **Integration Runtimes**

Let’s explore step by step.

---

## 🔹 1. Control Plane vs Data Plane

ADF runs on a **serverless architecture** inside Azure.
It is split into two planes:

* **Control Plane**:

  * Manages *metadata, pipelines, triggers, monitoring*.
  * What you see in the ADF Studio (the UI).
  * Stores JSON definitions of pipelines in Azure.

* **Data Plane**:

  * Where the **actual data movement/processing** happens.
  * Uses Integration Runtime (IR) to copy or transform data.
  * Example: Copying a file from On-prem SQL → Blob storage.

---

## 🔹 2. Core Components

### ✅ **Pipelines**

* A **pipeline = workflow**.
* Groups multiple **activities** into a sequence/graph.
* Example:

  * Step 1: Copy sales data from SQL → Data Lake
  * Step 2: Run Databricks transformation
  * Step 3: Load into Synapse

---

### ✅ **Activities**

* Steps inside a pipeline.
* Types:

  1. **Data Movement** → Copy Activity (move data between stores).
  2. **Data Transformation** → Mapping Data Flows, Databricks, Synapse SQL, HDInsight.
  3. **Control Activities** → If/Else, ForEach loops, Web calls, Execute pipeline.

---

### ✅ **Datasets**

* Definition of **data structure** you want to read/write.
* Think of it as a **pointer to data** inside a storage system.
* Example:

  * A dataset for "SalesTable in SQL DB".
  * A dataset for "CSV file in Data Lake folder".

---

### ✅ **Linked Services**

* **Connection info** (credentials + endpoints).
* Similar to **connection strings**.
* Examples:

  * Linked Service for Azure SQL DB
  * Linked Service for Blob Storage
  * Linked Service for On-prem SQL via Self-hosted IR

---

### ✅ **Integration Runtime (IR)**

This is the **engine** that actually runs ADF activities.
Types of IR:

1. **Azure IR** → Managed, serverless compute (default). Used for copying data in the cloud.
2. **Self-Hosted IR** → Installed on your on-prem VM. Used for hybrid (on-prem ↔ cloud).
3. **Azure SSIS IR** → Run legacy SSIS packages in Azure.

📌 Example:

* If your data is in **on-prem SQL Server**, you must install **Self-hosted IR** in your data center to move data to Azure.
* If your data is in **Azure Blob → Synapse**, then **Azure IR** handles it.

---

## 🔹 3. Orchestration Layer

* Pipelines are **triggered** by:

  * Schedule (daily, hourly)
  * Event-based (new file arrives in Blob)
  * Manual/REST API call
* Pipelines can **branch, loop, or run in parallel**.

---

## 🔹 4. Monitoring Layer

* Built-in monitoring in **ADF Studio**.
* Shows pipeline runs, activity runs, duration, errors.
* Integrated with **Azure Monitor** & **Log Analytics** for alerts.

---

## 🔹 5. Security Layer

* Authentication: **Managed Identity, Service Principal, Key Vault**.
* Data never passes through control plane → only through IR.
* Network isolation possible with VNet integration.

---

## 🔹 6. Typical Data Flow Example

**Scenario**: Ingest daily sales data from On-prem SQL to Synapse

1. **Trigger** fires daily.
2. **Pipeline** starts.
3. **Copy Activity** (using Self-hosted IR) moves data → Azure Data Lake.
4. **Mapping Data Flow Activity** cleans & transforms data.
5. **Copy Activity** loads transformed data → Synapse DW.
6. **Monitoring** logs success/failure.

---

## 🔹 Architecture Diagram (Explained in Words)

Imagine:

* **Top Layer (UI + Control Plane)** → ADF Studio where you design pipelines.
* **Middle Layer (Orchestration)** → Pipelines + Triggers + Activities.
* **Bottom Layer (Execution via IR)** → Data is copied/transformed by IR across data sources.

So:

* **Control Plane** = Think "Blueprint + Control Room".
* **Integration Runtime (Data Plane)** = Think "Workers doing the job".

---

✅ In short:
ADF is an **orchestrator + integration engine** with **pipelines** as workflows, **activities** as tasks, **linked services** as connections, **datasets** as pointers, and **IR** as the worker that executes jobs.

---
