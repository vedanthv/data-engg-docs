## Types of Storage in Azure

---

## **1. Azure File Storage**

**Definition:**
Azure File Storage provides **fully managed file shares in the cloud**, accessible via SMB (Server Message Block) or NFS protocols. It’s like having a network drive in the cloud.

**Key Features:**

| Feature               | Details                                                                                   |
| --------------------- | ----------------------------------------------------------------------------------------- |
| **Access Protocol**   | SMB 3.0 (for Windows/Linux), NFS 4.1 (premium tier).                                      |
| **Structure**         | Folders and files (like a traditional file system).                                       |
| **Persistence**       | Fully persistent, replicated.                                                             |
| **Mounting**          | Can mount directly to VMs, Azure Kubernetes, or local machines.                           |
| **Typical Use Cases** | Lift-and-shift apps, shared storage for VMs, legacy apps needing a file system interface. |

**Example Use Case:**

* Shared logs folder for multiple Azure VMs.
* Migrating on-premises applications that rely on file shares.

---

## **2. Azure Queue Storage**

**Definition:**
Azure Queue Storage provides a **messaging queue for asynchronous communication** between components of an application. Each message is stored for up to 7 days by default.

**Key Features:**

| Feature                | Details                                                                                   |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| **Structure**          | A queue is a collection of messages. Each message is up to 64 KB.                         |
| **Access**             | REST API or Azure SDKs.                                                                   |
| **Persistence**        | Messages are durably stored until dequeued or expired.                                    |
| **Processing Pattern** | **FIFO-ish** (first-in, first-out), but not guaranteed.                                   |
| **Typical Use Cases**  | Decoupling application components, task scheduling, background jobs, buffering workloads. |

**Example Use Case:**

* A web app pushes tasks into a queue; a worker VM dequeues and processes them asynchronously.
* Event-driven data pipelines.

---

## **3. Azure Table Storage**

**Definition:**
Azure Table Storage is a **NoSQL key-value store** for structured, semi-structured data. It’s highly scalable, low-latency, and schema-less.

**Key Features:**

| Feature               | Details                                                                 |
| --------------------- | ----------------------------------------------------------------------- |
| **Structure**         | Tables → PartitionKey + RowKey + properties (columns).                  |
| **Schema**            | Schema-less; each row can have different properties.                    |
| **Access**            | REST API, SDKs, or OData.                                               |
| **Querying**          | Efficient on PartitionKey + RowKey; limited secondary indexing.         |
| **Typical Use Cases** | Storing metadata, logs, IoT telemetry, lightweight structured datasets. |

**Example Use Case:**

* Storing IoT device readings (temperature, humidity) with timestamp.
* Metadata store for blobs or files.
* User session data in web applications.

---

## **4. Quick Comparison**

| Feature            | File Storage                        | Queue Storage                    | Table Storage                                   |
| ------------------ | ----------------------------------- | -------------------------------- | ----------------------------------------------- |
| **Type**           | File system                         | Messaging queue                  | NoSQL key-value store                           |
| **Access**         | SMB/NFS                             | REST API / SDK                   | REST API / SDK                                  |
| **Data Structure** | Files & directories                 | Messages                         | Rows (PartitionKey + RowKey)                    |
| **Use Case**       | Shared storage, lift-and-shift apps | Decoupled messaging, async tasks | Structured/semi-structured data, logs, metadata |
| **Persistence**    | Durable                             | Durable until read/expire        | Durable                                         |

---

✅ **Summary / Guidance:**

* **File Storage** → Use when you need a traditional file system in the cloud.
* **Queue Storage** → Use for decoupling components, async processing, or buffering workloads.
* **Table Storage** → Use for scalable NoSQL storage with structured/semi-structured data.

---

## **1. What is Immutable Blob Storage?**

**Immutable Blob Storage** is a **type of Azure Storage account or configuration that prevents modification or deletion of blobs for a specified retention period**.

* Once a blob is **written**, it **cannot be changed or deleted** until the retention period expires.
* Useful for **compliance, regulatory, and audit requirements**, e.g., finance, healthcare, or legal data.

---

## **2. Key Concepts**

| Concept                          | Description                                                               |
| -------------------------------- | ------------------------------------------------------------------------- |
| **Immutability Policy**          | Rules that define how long a blob is protected (e.g., 30 days, 365 days). |
| **Legal Hold**                   | Option to indefinitely prevent deletion until explicitly removed.         |
| **Retention Period**             | Duration (in days) for which blobs cannot be modified or deleted.         |
| **Write Once, Read Many (WORM)** | The blob can be read many times, but written only once.                   |

---

## **3. Types of Immutable Policies**

1. **Time-based retention**

   * Blobs cannot be modified or deleted for a fixed period.
   * Example: 90-day retention for financial transactions.

2. **Legal hold**

   * Prevents modification/deletion indefinitely until legal hold is cleared.
   * Often used in audits or legal investigations.

---

## **4. How it Works in Azure Blob Storage**

* Create a **container** in a storage account that supports **immutability** (must be a **general-purpose v2 storage account**).
* Enable **immutable storage** on the container.
* Apply a **policy**:

  * **Time-based retention** → specify days.
  * **Legal hold** → optionally apply.
* Once a blob is uploaded:

  * It **cannot be deleted or overwritten** until the retention period expires.
  * Reads are allowed.

**Important:** Only **newly uploaded blobs** are protected. Existing blobs can be migrated into immutable containers if needed.

---

## **5. Use Cases**

| Scenario                   | Why Immutable Storage?                   |
| -------------------------- | ---------------------------------------- |
| Financial transaction logs | Regulatory compliance (SOX, SEC, FINRA)  |
| Healthcare records         | HIPAA compliance                         |
| Legal or audit archives    | Prevent tampering or accidental deletion |
| Backup data                | Ensure backups are safe from ransomware  |

---

## **6. Creating Immutable Blob Storage (Azure Portal)**

1. Go to **Storage Account → Containers → + Container**.
2. Set **Access level** (private / blob).
3. After creating the container:

   * Go to **Container → Immutable blob storage → Policies**.
   * Add **Time-based retention** (e.g., 365 days).
   * Optionally, add a **Legal hold**.
4. Upload blobs → they are now **write-once, read-many (WORM)**.

---

## **7. Creating via Azure CLI**

```bash
# Create a container
az storage container create \
    --name immutable-container \
    --account-name mystorageacct

# Set time-based immutability policy (e.g., 90 days)
az storage container immutability-policy create \
    --account-name mystorageacct \
    --container-name immutable-container \
    --period 90 \
    --allow-protected-append-writes true
```

> `--allow-protected-append-writes` allows **append operations** (for logs) without breaking immutability.

---

✅ **Summary**

* **Immutable Blob Storage** ensures **write-once, read-many (WORM)** behavior.
* Supports **time-based retention** or **legal hold**.
* Protects critical data from **accidental or malicious deletion**.
* Common in **compliance-heavy industries**.

---
