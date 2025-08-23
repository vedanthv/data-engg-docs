## Bicep Templates in Azure

Bicep is the modern, cleaner alternative to ARM JSON templates. It’s declarative, easier to read, and natively compiles to ARM templates.

```
// Parameters
param storageAccountName string {
  metadata: {
    description: 'Unique name for the storage account.'
  }
}

param location string = 'eastus' {
  metadata: {
    description: 'Azure region for deployment.'
  }
}

param skuName string = 'Standard_LRS' {
  allowed: [
    'Standard_LRS'
    'Standard_GRS'
    'Standard_ZRS'
    'Premium_LRS'
  ]
  metadata: {
    description: 'Performance and replication type.'
  }
}

// Resource: Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: skuName
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    isHnsEnabled: true  // Hierarchical namespace for ADLS Gen2
    networkAcls: {
      defaultAction: 'Deny'   // Block public access
      bypass: 'AzureServices'
    }
  }
}
```

### Deployment

```
# Create resource group (if needed)
az group create --name MyResourceGroup --location eastus

# Deploy Bicep file
az deployment group create \
  --resource-group MyResourceGroup \
  --template-file storage.bicep \
  --parameters storageAccountName=mystorageacctbicep
```
// Output: Storage Account Resource ID
output storageAccountId string = storageAccount.id
