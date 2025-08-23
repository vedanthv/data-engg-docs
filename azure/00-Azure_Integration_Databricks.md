<img width="1919" height="690" alt="image" src="https://github.com/user-attachments/assets/5a01752e-73bd-4778-9449-134efba7ab2c" />## Azure Integration with Databricks

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
