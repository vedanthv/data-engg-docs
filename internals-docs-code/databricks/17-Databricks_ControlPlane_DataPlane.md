## Databricks Control Plane and Data Plane

---

## 🚀 What is Databricks Lakehouse Architecture?

Traditionally, companies had **two separate systems**:

* **Data Lake** 🪣 (cheap storage, e.g., Azure Data Lake, S3, Blob): stores raw structured, semi-structured, unstructured data → flexible but lacks strong data management (ACID, governance, BI).
* **Data Warehouse** 🏢 (expensive but fast): optimized for SQL queries, BI, and analytics → great schema enforcement and governance but limited flexibility and costly.

🔹 The **Lakehouse** combines both in one system:

* The **low-cost, flexible storage** of a **data lake**
* The **governance, ACID transactions, performance** of a **warehouse**

---

## 🏗️ Core Components of Databricks Lakehouse

1. **Storage Layer (Data Lake foundation)**

   * Data stored in **open formats** like Parquet, ORC, Avro, Delta.
   * Uses **cloud object storage** (e.g., Azure Data Lake Storage Gen2, AWS S3, GCS).

2. **Delta Lake (the secret sauce 🧂)**

   * Adds **ACID transactions** on top of data lake storage.
   * Provides **schema enforcement, schema evolution, time travel, data versioning**.
   * Solves problems like “eventual consistency” and corrupted files in raw data lakes.

3. **Unified Governance (Unity Catalog)**

   * Centralized **metadata & permissions** for files, tables, ML models, dashboards.
   * Manages security, lineage, and data discovery across the Lakehouse.

4. **Compute Layer (Databricks Runtime / Spark + Photon)**

   * Uses Apache Spark + Photon execution engine for **batch, streaming, ML, BI**.
   * Same engine for **ETL, streaming, AI, SQL queries** → no silos.

5. **Data Management Features**

   * **Streaming + Batch = One Pipeline** (via Delta Live Tables).
   * **Materialized Views, Incremental Processing, Change Data Capture (CDC)**.
   * MLflow integration for **machine learning lifecycle management**.

---

## 📊 Architecture Diagram (Conceptual Flow)

```
                ┌───────────────────────┐
                │   Business Apps / BI  │
                │ (Power BI, Tableau)   │
                └─────────▲─────────────┘
                          │
                ┌─────────┴─────────────┐
                │   Databricks SQL      │
                │   & Photon Engine     │
                └─────────▲─────────────┘
                          │
   ┌──────────────────────┴────────────────────────┐
   │          Delta Lake (ACID, Schema, CDC)       │
   │   (Open Storage Format on Parquet + Log)      │
   └──────────────────────▲────────────────────────┘
                          │
                ┌─────────┴─────────────┐
                │   Cloud Object Store  │
                │ (ADLS, S3, GCS)       │
                └───────────────────────┘
```

---

## ⚡ Benefits of Lakehouse

* ✅ **One platform** → no need for separate warehouse + lake.
* ✅ **Cost efficient** → cheap storage, scalable compute.
* ✅ **Flexibility** → structured + semi-structured + unstructured.
* ✅ **ACID reliability** → transactions, schema enforcement.
* ✅ **End-to-end** → supports ETL, real-time streaming, ML/AI, BI in the same system.

---

## 🌐 In Databricks Azure Context

* Storage → **Azure Data Lake Storage (ADLS Gen2)**
* Security/Governance → **Azure Key Vault + Unity Catalog**
* Compute → **Databricks Clusters with Photon**
* Serving → **Power BI (Direct Lake Mode)**

---
## Data Plane vs Control Plane
---

# 🚦 1. Simple Analogy

Think of Databricks like **Uber**:

* **Control Plane = Uber App** 📱 → handles **where you go, who drives, billing, monitoring**.
* **Data Plane = The Car** 🚗 → where the **actual ride happens** (your data processing).

So, Databricks separates **management functions (control)** from **execution functions (data)**.

---

# 🏗️ 2. Databricks Architecture

### 🔹 **Control Plane**

* Managed by **Databricks itself** (runs in Databricks’ own AWS/Azure/GCP accounts).
* Contains:

  1. **Web UI / REST API** → you log in here, create clusters, manage jobs.
  2. **Cluster Manager** → decides how to spin up VMs/compute.
  3. **Job Scheduler** → triggers pipelines, notebooks, workflows.
  4. **Metadata Storage** → notebooks, workspace configs, Unity Catalog metadata.
  5. **Monitoring / Logging** → cluster health, job logs, error reporting.

⚠️ **Important**: Your **raw data does not go here**. This plane is about orchestration, configs, and metadata.

---

### 🔹 **Data Plane**

* Runs inside **your cloud account** (your subscription/project).
* Contains:

  1. **Clusters/Compute** (Spark Executors, Driver, Photon) → where the data is processed.
  2. **Your Data** → stored in ADLS, S3, or GCS.
  3. **Networking** → VNETs, Private Endpoints, Peering.
  4. **Libraries / Runtime** → Spark, Delta Lake, MLflow, etc.

⚠️ **Key Point**: The **actual data never leaves your cloud account**. Processing happens within your boundary.

---

# 🔐 3. Security Perspective

* **Control Plane**:

  * Managed by Databricks.
  * Contains **metadata, credentials, configs**, but not raw data.
  * Can be hardened with **SCIM, SSO, RBAC, IP Access Lists**.

* **Data Plane**:

  * Fully inside **your cloud subscription**.
  * Your **sensitive data** (PII, transactions, crypto, etc.) never touches Databricks’ account.
  * You control networking:

    * Private Link / VNET Injection → ensures traffic never goes over the public internet.
    * Key Vault / KMS for secrets.
    * Storage firewalls.

---

# 🖼️ 4. Architecture Diagram

```
               ┌──────────────────────────────────────┐
               │           CONTROL PLANE              │
               │  (Databricks-managed account)        │
               │                                      │
               │  - Web UI / API                      │
               │  - Cluster Manager                   │
               │  - Job Scheduler                     │
               │  - Unity Catalog Metadata            │
               │  - Logs / Monitoring                 │
               └───────────────▲──────────────────────┘
                               │
                               │ Secure REST/API Calls
                               │
               ┌───────────────┴──────────────────────┐
               │             DATA PLANE                │
               │   (Your cloud subscription/project)   │
               │                                       │
               │  - Spark Driver & Executors           │
               │  - Photon Engine                      │
               │  - Data in ADLS/S3/GCS                │
               │  - Networking (VNET, Firewall, PEs)   │
               │  - Secrets from Key Vault/KMS         │
               └───────────────────────────────────────┘
```

---

# ⚡ 5. Why This Separation?

✅ **Security** → Your data never leaves your account.
✅ **Scalability** → Databricks manages orchestration, you manage compute.
✅ **Multi-cloud** → Same control plane works across AWS, Azure, GCP.
✅ **Compliance** → Helps with HIPAA, GDPR, financial regulations.

---

# 🔑 6. Special Feature: **Databricks Serverless SQL**

* Here, the **data plane compute is managed by Databricks** too (not your account).
* Good for quick BI queries (like Power BI), but some enterprises avoid it for sensitive data.

---
