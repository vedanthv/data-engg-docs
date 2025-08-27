# 🔹 What is Blob Storage?

Blob = **Binary Large Object** → any file (text, image, video, parquet, JSON, etc.)
Azure Blob Storage is Microsoft’s **object storage solution** for unstructured data.

It’s **cheap, scalable, durable** → you can store petabytes of data and pay only for what you use.

---

# 🔹 Types of Blobs

Azure Blob storage supports **3 types**:

1. **Block Blob (most common)**

   * Optimized for **streaming and storing files**.
   * Stores data as **blocks** → you can upload in chunks.
   * Used for: documents, CSV, Parquet, images, logs.

2. **Append Blob**

   * Optimized for **append operations**.
   * Great for logs → you can only **add** to the end, not modify existing content.

3. **Page Blob**

   * Optimized for **random read/write**.
   * Used for **VM disks** (VHD files).

👉 For Data Engineering / Delta Lake → you’ll almost always use **Block Blobs**.

---

# 🔹 Storage Account + Containers

* A **Storage Account** = the root of your blob storage.
* Inside it, you create **containers** → logical groups of blobs.
* Inside containers, you can have **folders** (if Hierarchical Namespace is enabled = ADLS Gen2).

Example path:

```
abfss://bronze@mydatalake.dfs.core.windows.net/2025/08/data.csv
```

Breakdown:

* `abfss` → protocol for ADLS Gen2 secure access.
* `bronze` → container.
* `mydatalake` → storage account.
* `dfs.core.windows.net` → ADLS Gen2 endpoint.
* `2025/08/data.csv` → folder path + file.

---

# 🔹 Access Tiers (Cost Optimization)

Blob storage offers **3 main tiers**:

1. **Hot** – frequently accessed, higher cost per GB, lower access cost.
2. **Cool** – infrequently accessed, cheaper storage, higher access charges.
3. **Archive** – very cheap storage, but must be “rehydrated” before use (hours).

Example:

* Store last 30 days of logs in **Hot**.
* Move logs > 30 days old to **Cool**.
* Move logs > 1 year old to **Archive**.

---

# 🔹 Security & Access

1. **Authentication options**:

   * Azure AD (recommended) → RBAC roles, Managed Identity.
   * Shared Key (account key) → full access, risky.
   * SAS Tokens → temporary, limited access (e.g., read-only link valid for 1 hour).

2. **Authorization**:

   * RBAC roles:

     * `Storage Blob Data Reader` → read only.
     * `Storage Blob Data Contributor` → read/write.
     * `Storage Blob Data Owner` → full control.

3. **Networking**:

   * Private endpoints (VNet integration).
   * Firewalls + IP restrictions.

---

# 🔹 Features for Data Engineering

* **Hierarchical Namespace (HNS)** → required for Data Lake Gen2.

  * Allows directories + POSIX-like permissions.
  * Needed for Delta Lake + Databricks UC.
* **Soft delete / versioning** → recover accidentally deleted blobs.
* **Lifecycle rules** → auto-move data across tiers.
* **Event Grid integration** → trigger pipelines when new data arrives.
* **Immutable blobs (WORM)** → compliance, can’t be modified/deleted.

---

# 🔹 Example Scenario (ETL Pipeline with Blob Storage)

1. Raw CSV files land in `bronze` container.
2. Azure Function + Event Grid detects new files.
3. Data Factory (ADF) or Databricks picks up files → transforms → saves as Delta in `silver`.
4. Aggregated tables saved in `gold`.
5. Access controlled via **Unity Catalog external location** with **Managed Identity**.

---

# 🔹 Quick Analogy

* **Block Blob** = Lego blocks (you can build files in chunks).
* **Append Blob** = notebook (you can only keep adding pages).
* **Page Blob** = hard disk (you can jump to any page and edit).

---
