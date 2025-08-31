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

```
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "storageAccountName": {
      "type": "string",
      "metadata": {
        "description": "Unique name for the storage account."
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "eastus",
      "metadata": {
        "description": "Azure region to deploy the storage account."
      }
    },
    "skuName": {
      "type": "string",
      "defaultValue": "Standard_LRS",
      "allowedValues": [
        "Standard_LRS",
        "Standard_GRS",
        "Standard_ZRS",
        "Premium_LRS"
      ],
      "metadata": {
        "description": "Storage account performance and replication type."
      }
    }
  },
  "variables": {
    "storageAccountType": "[parameters('skuName')]"
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2023-01-01",
      "name": "[parameters('storageAccountName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "[variables('storageAccountType')]"
      },
      "kind": "StorageV2",
      "properties": {
        "accessTier": "Hot"
      }
    }
  ],
  "outputs": {
    "storageAccountId": {
      "type": "string",
      "value": "[resourceId('Microsoft.Storage/storageAccounts', parameters('storageAccountName'))]"
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

