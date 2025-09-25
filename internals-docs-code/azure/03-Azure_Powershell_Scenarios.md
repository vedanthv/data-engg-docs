## ⚡ Azure PowerShell Basics

### 1. Install & Setup

```
# Install the Az module (latest version)
Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force

# Import the module
Import-Module Az

# Login
Connect-AzAccount

# Check current subscription
Get-AzContext

# Switch subscription
Set-AzContext -Subscription "SUBSCRIPTION-ID"

```

### 🔹 Scenario 1: Create Resource Groups for Data Projects

```
# Create resource groups for different environments
New-AzResourceGroup -Name DataRG-Dev -Location eastus
New-AzResourceGroup -Name DataRG-Test -Location eastus
New-AzResourceGroup -Name DataRG-Prod -Location eastus
```

### 🔹 Scenario 2: Deploy a Data Lake Storage Account

```
# Create a Data Lake Gen2 Storage Account
New-AzStorageAccount `
  -ResourceGroupName DataRG-Dev `
  -Name datalakeps123 `
  -Location eastus `
  -SkuName Standard_LRS `
  -Kind StorageV2 `
  -EnableHierarchicalNamespace $true
```

### 🔹 Scenario 3: Upload Raw Data to Data Lake

```
# Connect to storage account
$ctx = New-AzStorageContext -StorageAccountName datalakeps123 -UseConnectedAccount

# Create container
New-AzStorageContainer -Name raw -Context $ctx

# Upload file
Set-AzStorageBlobContent -File "./sales.csv" -Container raw -Blob "sales.csv" -Context $ctx

```

### 🔹 Scenario 5: Secure Secrets in Key Vault

```
# Create Key Vault
New-AzKeyVault -Name MyVault123 -ResourceGroupName DataRG-Dev -Location eastus

# Store SQL password
$secret = ConvertTo-SecureString "StrongP@ssword123!" -AsPlainText -Force
Set-AzKeyVaultSecret -VaultName MyVault123 -Name SqlPassword -SecretValue $secret
```
