## 🚀 Unity Catalog Setup from Scratch (Azure + Databricks)

**Using UC Connector as Managed Identity**

### 🔹 Part 1: Azure Setup

**1. Create a Storage Account**

In Azure Portal, search Storage Accounts → Create.

Important settings:

Performance: Standard
Redundancy: LRS (for testing)
Enable Hierarchical Namespace (HNS) ✅ (must be ON for Unity Catalog).
Create a container inside it (e.g. uc-data).

**2. Assign Permissions to UC Managed Identity**

In Azure Portal → Storage Account → Access Control (IAM) → Add Role Assignment.
Assign these roles to the UC Managed Identity (the connector):
- Storage Blob Data Owner (read/write access).
- Storage Blob Delegator (needed for ABFS driver).

Scope: Storage Account level (recommended).

👉 Tip: You can find the UC managed identity name in Databricks → Admin Console → Identity Federation.

### 🔹 Part 2: Databricks Setup (UI + SQL)

**3. Verify Metastore**

Go to Databricks Admin Console → Unity Catalog → Metastores.

If you don’t have one, click Create Metastore.
Region = same as Storage Account.
Assign this metastore to your workspace.

👉 Do not skip this. Unity Catalog won’t work without a metastore.

**4. Create Storage Credential (UI or SQL)**

This ties the Azure Managed Identity to Unity Catalog.

UI:
Go to Catalog → Storage Credentials → Create.
Select Azure Managed Identity.
Enter a name (e.g., uc-cred).
Paste the UC Connector Managed Identity ID.

```sql
CREATE STORAGE CREDENTIAL uc_cred
WITH AZURE_MANAGED_IDENTITY 'your-managed-identity-client-id'
COMMENT 'UC Connector credential for ADLS';
```

**5. Register an External Location**

This points Unity Catalog to your ADLS container/folder.

UI:
Go to Catalog → External Locations → Create.
Name: ext_loc_dev
Path: abfss://uc-data@<storageaccount>.dfs.core.windows.net/
Storage credential: uc-cred (Storage Credential is at Storage Account level so for one cred is enough)

```
CREATE EXTERNAL LOCATION ext_loc_dev
URL 'abfss://uc-data@<storageaccount>.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL uc_cred)
COMMENT 'External location for dev data';
```

**6. Create Catalog**

Decide whether it will use:

Metastore root storage (if defined), OR
Catalog-level managed location (recommended).

UI:

Go to Catalog Explorer → Create Catalog.
Name: dev
Managed Location:
```
abfss://uc-data@<storageaccount>.dfs.core.windows.net/dev
```
Storage credential: uc-cred.

SQL equivalent:

```
CREATE CATALOG dev
MANAGED LOCATION 'abfss://uc-data@<storageaccount>.dfs.core.windows.net/dev';
```

<img width="515" height="404" alt="image" src="https://github.com/user-attachments/assets/da261099-f7a5-41b1-925b-066cc2f84125" />


**7. Create Schema**

Schemas can also have their own managed locations (if needed).

```
CREATE SCHEMA dev.bronze
MANAGED LOCATION 'abfss://uc-data@<storageaccount>.dfs.core.windows.net/dev/bronze';
```

**9. Grant Permissions**

For yourself or a group (like account users):

```
-- Catalog usage
GRANT USAGE ON CATALOG dev TO `account users`;

-- Schema usage
GRANT USAGE ON SCHEMA dev.bronze TO `account users`;

-- External location permissions
GRANT READ FILES, WRITE FILES ON EXTERNAL LOCATION ext_loc_dev TO `account users`;

-- Table level
GRANT SELECT, MODIFY ON TABLE dev.bronze.trades TO `account users`;
```

**10. Create Tables at Different Levels**

```
CREATE SCHEMA dev.bronze
COMMENT 'This is schema in dev catalog without external location'
```

This gets created in metastore level container because its managed and we havent specified external location at catalog level.

```
-- CREATE A TABLE UNDER ALL THREE SCHEMA
CREATE TABLE IF NOT EXISTS dev.bronze.raw_sales (
  id INT,
  name STRING,
  invoice_no INT,
  price double
);

INSERT INTO dev_ext.bronze.raw_sales VALUES (1,'Cookies',1,200.50);
```

This gets created in catalog level container because the catalog associated to the schema is external.

```
-- CREATE A TABLE UNDER ALL THREE SCHEMA
CREATE TABLE IF NOT EXISTS dev_ext.bronze.raw_sales (
  id INT,
  name STRING,
  invoice_no INT,
  price double
);

INSERT INTO dev_ext.bronze.raw_sales VALUES (1,'Cookies',1,200.50);
```

Creating schema in external location.

```
CREATE EXTERNAL LOCATION 'ext_schema'
MANAGED LOCATION 'https://adbvedanthnew.databricks.net/adb/schema/bronze_ext'
```

This gets created in schema level since we specified external location at schema level.

```sql
-- CREATE A TABLE UNDER ALL THREE SCHEMA
CREATE TABLE IF NOT EXISTS dev_ext.bronze_ext.raw_sales (
  id INT,
  name STRING,
  invoice_no INT,
  price double
);

INSERT INTO dev_ext.bronze_Ext.raw_sales VALUES (1,'Cookies',1,200.50);
```

<img width="1351" height="621" alt="image" src="https://github.com/user-attachments/assets/0a6847fb-ef66-4bc9-9bc7-2b0c6d7317a7" />

### Where data is stored?

1. Stored in metastore root location

<img width="663" height="291" alt="image" src="https://github.com/user-attachments/assets/2d2bf8cd-3986-4a19-87db-8d456f9146f0" />

<img width="676" height="274" alt="image" src="https://github.com/user-attachments/assets/e9be7b1d-699c-41ed-ae5b-215181611c44" />

2. Store in Catalog Level Ext Location

```sql
DESC EXTENDED DEV_EXT.BRONZE.RAW_SALE;
```

<img width="686" height="284" alt="image" src="https://github.com/user-attachments/assets/2adc41ef-11fb-4994-8818-d3780d411c43" />

3. Store in Schema Level External Location

```sql
DESC EXTENDED DEV_EXT.BRONZE_EXT.RAW_SALE
```

<img width="675" height="287" alt="image" src="https://github.com/user-attachments/assets/eb572613-c2e1-41f6-a47a-d0d1251e4a82" />


## Summary

---

## 🔹 1. **Managed Table (no LOCATION specified)**

```sql
CREATE SCHEMA finance
MANAGED LOCATION 'abfss://finance@companydatalake.dfs.core.windows.net/schemas/finance';

CREATE TABLE finance.transactions (
  id INT,
  amount DECIMAL(10,2)
);
```

* Since you didn’t give a `LOCATION` for the table:

  * Unity Catalog treats this as a **managed table**.
  * UC stores the data under the **schema’s managed location**.

✅ Path =
`abfss://finance@companydatalake.dfs.core.windows.net/schemas/finance/transactions/`

So in your example, you are exactly right.

---

## 🔹 2. **External Table (explicit LOCATION specified)**

```sql
CREATE TABLE finance.transactions_ext (
  id INT,
  amount DECIMAL(10,2)
)
LOCATION 'abfss://raw@companydatalake.dfs.core.windows.net/landing/transactions/';
```

* Here you told UC exactly where the data lives.
* This is an **external table**.
* UC does not move or manage the files — it just registers metadata pointing at that path.

✅ Path =
`abfss://raw@companydatalake.dfs.core.windows.net/landing/transactions/`

---

## 🔹 What If Schema Has No Managed Location?

If you do:

```sql
CREATE SCHEMA finance;
```

* No schema location defined.
* A managed table like:

  ```sql
  CREATE TABLE finance.transactions (id INT, amount DECIMAL(10,2));
  ```

  will fall back to the **metastore’s root storage location** (the one you defined when setting up Unity Catalog).

✅ Path example:
`abfss://uc-metastore@companydatalake.dfs.core.windows.net/finance/transactions/`

---

## 🔹 Summary Table

| Case                                                         | Table Type     | Storage Path                                                              |
| ------------------------------------------------------------ | -------------- | ------------------------------------------------------------------------- |
| Schema has `MANAGED LOCATION`, table has no `LOCATION`       | Managed table  | Inside schema’s managed location (e.g., `/schemas/finance/transactions/`) |
| Schema has `MANAGED LOCATION`, table has explicit `LOCATION` | External table | Exact path you provided                                                   |
| Schema has **no location**, table has no `LOCATION`          | Managed table  | Falls back to **metastore root storage**                                  |

---

✅ So in your example (`schema has managed location` + `table no LOCATION`) → **yes, data files are stored under schema’s storage location.**

---

<img src = 'https://docs.databricks.com/aws/en/assets/images/managed-storage-0fe299ce1b4c32afce5845652093c124.png'>

## Real Case Study : Employee Data Sensitivity

For example, let's say your organization has a company compliance policy that requires production data relating to human resources to reside in the bucket s3://mycompany-hr-prod. In Unity Catalog, you can achieve this requirement by setting a location on a catalog level, creating a catalog called, for example hr_prod, and assigning the location s3://mycompany-hr-prod/unity-catalog to it. This means that managed tables or volumes created in the hr_prod catalog (for example, using CREATE TABLE hr_prod.default.table …) store their data in s3://mycompany-hr-prod/unity-catalog. Optionally, you can choose to provide schema-level locations to organize data within the hr_prod catalog at a more granular level.

If storage isolation is not required for some catalogs, you can optionally set a storage location at the metastore level. This location serves as a default location for managed tables and volumes in catalogs and schemas that don't have assigned storage. Typically, however, Databricks recommends that you assign separate managed storage locations for each catalog.