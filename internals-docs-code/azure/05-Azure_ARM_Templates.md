**📌 What are ARM Templates?**

ARM (Azure Resource Manager) templates are JSON files that define the infrastructure and configuration you want to deploy in Azure.

Think of them as Infrastructure as Code (IaC) for Azure.
Instead of manually creating resources in the portal or using CLI/PowerShell, you write a template once and deploy it repeatedly.

**🔹 Key Points**

Format: JSON file (.json)

- Declarative: You describe what you want (VM, Storage, SQL, etc.), Azure figures out how to create it.

- Idempotent: You can deploy the same template multiple times, Azure won’t create duplicates – it ensures the desired state.

- Repeatable: Use the same template for dev, test, prod environments.

- Automation: Works well with CI/CD (e.g., GitHub Actions, Azure DevOps).

**Custom Template to Create Storage Account**

```json
@description('Unique Name for Storage Account')
param storageAccountName string

@description('Azure Region for Deployment')
param location string = 'eastus2'

@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_ZRS'
  'Premium_LRS'
])
@description('Performance and replication type.')
param skuName string = 'Standard_LRS'

// Resource: Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2025-06-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: skuName
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    isHnsEnabled: true  // Hierarchical namespace for ADLS Gen2
    networkRuleSet: {
      defaultAction: 'Deny'   // Block public access
      bypass: [
        'AzureServices'
      ]
    }
  }
}


```

<img width="1879" height="708" alt="image" src="https://github.com/user-attachments/assets/ca40d84c-787e-41eb-ac15-2ab4f5bba65f" />

<img width="1398" height="535" alt="image" src="https://github.com/user-attachments/assets/16ff3847-08d1-4c5f-a447-9eef4cb15ff4" />

### Deploying using az

```
az deployment group create \
  --resource-group MyResourceGroup \
  --template-file storage-gen2.json \
  --parameters storageAccountName=mystorageacctgen2
```

This is an **Azure Resource Manager (ARM) template**. It defines how to deploy a **Storage Account** in Azure. Let me walk you through every section in depth:

---

Okay, let me explain your **fixed Bicep template** in a simple way, step by step:

---

### 1. Parameters

Parameters let you **pass values** when you deploy, so the template is reusable.

* **storageAccountName** → The unique name of the storage account.
* **location** → The Azure region (default is `eastus2`).
* **skuName** → The storage account’s performance/replication option. Allowed values are:

  * `Standard_LRS` → locally redundant
  * `Standard_GRS` → geo-redundant
  * `Standard_ZRS` → zone redundant
  * `Premium_LRS` → premium performance

---

### 2. Resource Definition

This creates the **storage account** itself.

```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-01-01' = {
```

* Tells Azure: “I want to create a storage account using API version 2022-01-01.”

---

### 3. Storage Account Settings

Inside the resource block, you configure:

* **name** → uses the `storageAccountName` parameter.
* **location** → uses the `location` parameter.
* **sku** → set to whatever you passed in `skuName`.
* **kind: 'StorageV2'** → makes it a modern storage account that supports all services.
* **properties**:

  * `accessTier: 'Hot'` → assumes data is accessed frequently.
  * `isHnsEnabled: true` → turns on **Hierarchical Namespace**, required for Data Lake Gen2.
  * `networkRuleSet`:

    * `defaultAction: 'Deny'` → blocks public access by default.
    * `bypass: ['AzureServices']` → allows trusted Azure services (like Databricks, Synapse) to still connect.

---

### 4. What happens when you deploy

* Azure will create a new **StorageV2 account**.
* It will use the name, location, and SKU you provided (or the defaults).
* The account will support **Data Lake Gen2**.
* Public access is blocked, but Azure services can still use it.

---

### In one line:

This Bicep template **deploys a secure StorageV2 account with ADLS Gen2 enabled**, parameterized for name, location, and redundancy type, and blocks public access except for trusted Azure services.

---