## Azure Integration with Databricks

<img width="1919" height="690" alt="image" src="https://github.com/user-attachments/assets/5a01752e-73bd-4778-9449-134efba7ab2c" />


### Managed Resource Group

<img width="1509" height="635" alt="image" src="https://github.com/user-attachments/assets/bd037017-c504-4a9d-af10-571d89e3049c" />

We can see:

- Identity
- Managed Storage Account : DBFS is stored here.
- Access Connector : Used to connect to storage account from databricks.

Blob Containers inside the storage account

<img width="1919" height="690" alt="image" src="https://github.com/user-attachments/assets/1be62561-92c3-4a6d-87b1-4760c67e47d0" />

### Creating Compute in Databricks

When we create compute in databricks we can see VM created. One VM for each driver and worker node

<img width="1132" height="555" alt="image" src="https://github.com/user-attachments/assets/03747e99-6120-46af-90d5-0199fb2c6e4b" />

When compute is terminated the VM is deleted.

### Unity Catalog

- Metadata is stored in control plane and data is stored in data plane. One region is adviced to have single metastore.

- Only catalog is securable object, others are non securable.

<img width="1304" height="507" alt="image" src="https://github.com/user-attachments/assets/784481af-b046-43c6-bd2f-1abd3f0e2787" />

Location in Managed Tables

<img width="1345" height="533" alt="image" src="https://github.com/user-attachments/assets/e2575471-1c4b-4a3c-bc36-228e705ab2dc" />

### Detailed Steps to Setup

---

## 1. Create an Azure Databricks Workspace

* Go to the **Azure Portal**.
* Create a new resource → search **Azure Databricks** → click *Create*.
* Fill in:

  * **Workspace name**
  * **Region**
  * **Pricing tier** (Standard, Premium, or Trial)
* Under *Networking*, choose whether to deploy into a **VNet (VNet Injection)** or let Databricks create a managed VNet.
* Deploy the workspace.

---

## 2. Understand the Storage Setup

When you create a Databricks workspace, Azure automatically provisions:

* **Managed Storage Account**:

  * A hidden, Microsoft-managed storage account that Databricks uses for workspace metadata (notebooks, cluster logs, ML models, job configs).
  * You **don’t manage** or see this storage directly.
  * This is different from your **customer-managed storage account**, where you store your actual data (e.g., in ADLS Gen2, Blob).

So you’ll normally integrate Databricks with your own **Azure Data Lake Storage (ADLS Gen2)** for raw and processed data.

---

## 3. Grant Access Using an Access Connector

To allow Databricks to access your storage securely:

1. Create a resource called **Azure Databricks Access Connector**.

   * This acts like a bridge between Databricks and Azure services.
   * It’s assigned a **Managed Identity** (system-assigned).
2. Assign **RBAC roles** to this Access Connector on your storage account.
   Example:

   * `Storage Blob Data Contributor` → read/write data in ADLS Gen2.
   * `Storage Blob Data Reader` → read-only.
3. Go to your Databricks workspace → *Advanced Settings* → *Access Connector* → attach the Access Connector you created.

---

## 4. Use Managed Identity in Databricks

* The **Access Connector’s managed identity** is used by Databricks clusters and jobs to authenticate to Azure services **without secrets**.
* Benefits:

  * No need to store SAS tokens, keys, or service principal secrets in Databricks.
  * Authentication happens via Azure AD automatically.
* When you mount ADLS or connect to other services (like Key Vault, Synapse, Event Hub), Databricks uses this managed identity.

Example for mounting ADLS with managed identity:

```python
spark.conf.set("fs.azure.account.auth.type.<storage_account>.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.<storage_account>.dfs.core.windows.net",
               "org.apache.hadoop.fs.azurebfs.oauth2.ManagedIdentityTokenProvider")

df = spark.read.format("parquet").load("abfss://container@storage_account.dfs.core.windows.net/data/")
```

---

## 5. Typical Flow in Production

1. **Create Databricks workspace** → Managed storage account provisioned automatically.
2. **Create Access Connector** → acts as Databricks’ identity in Azure.
3. **Assign roles on your ADLS storage account** to Access Connector’s identity.
4. **Enable Access Connector in Databricks workspace**.
5. **Access ADLS data** from notebooks or jobs using managed identity authentication.

---
