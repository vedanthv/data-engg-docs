## Managed and External Tables in Hive Metastore

---

### 1️⃣ Your command

```sql
CREATE TABLE IF NOT EXISTS dev.bronze.table_1
LOCATION 'dbfs:/tmp/tmp_ext'
```

* You are explicitly setting a **LOCATION**.
* You are creating the table in the **Hive Metastore** (because you didn’t specify Unity Catalog).
* That means: **this is an *external table***, *not* a managed one.

---

### 2️⃣ Where does the data go?

* If you **don’t specify a LOCATION** and use Hive Metastore → the data is stored in the **Databricks-managed DBFS root (a hidden storage account in the Databricks Managed Resource Group)**. That’s the “managed table” case.
* Since you **did specify `LOCATION dbfs:/tmp/tmp_ext`** → the data is stored in **DBFS**, which itself is backed by **the same hidden storage account** unless you mounted another storage.
* So in your case, yes — it is still in the **Databricks-managed storage account**, but specifically under the **DBFS `/tmp` folder**, not the default warehouse root (`/user/hive/warehouse`).

---

### 3️⃣ Important distinction: Hive Metastore vs Unity Catalog

* **Hive Metastore tables**:

  * Data goes to DBFS (Databricks-managed storage account).
  * Security is weaker (workspace-scoped, not account-scoped).

* **Unity Catalog tables**:

  * Data must go to a customer-managed **external storage account** (ADLS Gen2 / S3 / GCS).
  * Databricks does **not** put UC data into its hidden resource group storage.

---

### 4️⃣ Managed vs External recap

* **Managed table (no LOCATION)** → Hive Metastore puts data in Databricks-managed DBFS root.
* **External table (with LOCATION)** → Data goes exactly where you point it (`dbfs:/...` → Databricks storage, `abfss:/...` → your ADLS).

---

✅ So, in your example:
Yes — the data **is still stored in the Databricks managed resource group storage account**, because `dbfs:/tmp/...` points to DBFS root, which is Databricks-managed storage.

---

### Data Retention?

- In Hive Metastore once a managed table is deleted its whole data is also purged forever.
- This is not the case with UC, unless we do VACUUM even if we drop the table we still can see data in storage account for 7 days by default.
