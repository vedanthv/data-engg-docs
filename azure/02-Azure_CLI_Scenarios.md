## Azure CLI Scenarios

###🔹 Exercise 1: Setup & Resource Groups

**Login to Azure CLI**

```
az login
```

**Set your active subscription**

```
az account list --output table
az account set --subscription "<your-subscription-id>"
```

**Create a resource group**

```
az group create --name MyRG --location eastus
```

**Verify it**

```
az group list --output table
```

### 🔹 Exercise 2: Storage Account + Blob

**Create a storage account**
```
az storage account create \
  --name mystorage123xyz --resource-group MyRG \
  --location eastus --sku Standard_LRS --kind StorageV2
```

**Create a container**

```
az storage container create \
  --account-name mystorage123xyz --name rawdata
```

**Upload a CSV file**

```
az storage blob upload \
  --account-name mystorage123xyz --container-name rawdata \
  --name sample.csv --file ./sample.csv
```

**List blobs**

```
az storage blob list \
  --account-name mystorage123xyz --container-name rawdata \
  --output table
```

3## 🔹 Exercise 3: SQL Database

**Create a SQL server**

```
az sql server create \
  --name my-sql-server123 --resource-group MyRG \
  --location eastus --admin-user myadmin --admin-password MyP@ssw0rd!
```

**Create a database**

```
az sql db create \
  --resource-group MyRG --server my-sql-server123 \
  --name mydb --service-objective S0
```

**Show details**

```
az sql db show --resource-group MyRG --server my-sql-server123 --name mydb
```

### 🔹 Exercise 4: Virtual Machine

**Create a Linux VM**

```
az vm create \
  --resource-group MyRG --name MyVM \
  --image UbuntuLTS --admin-username azureuser --generate-ssh-keys
```

**Check running VMs**

```
az vm list --output table
```

**Stop the VM**

```
az vm stop --resource-group MyRG --name MyVM
```

**Start it again**

```
az vm start --resource-group MyRG --name MyVM
```

### 🔹 Exercise 5: Build a Mini Data Lake Pipeline

**Goal: Create a Data Lake storage, upload raw data, then use queries to check it.**

1. Create a storage account with hierarchical namespace (Data Lake Gen2):

```
az storage account create \
  --name mydatalake123 --resource-group MyRG \
  --location eastus --sku Standard_LRS --kind StorageV2 \
  --hierarchical-namespace true
```

**Create a container for raw data:**

```
az storage container create \
  --account-name mydatalake123 --name raw
```

**Upload multiple files (CSV, JSON):**

```
for file in ./data/*; do
  az storage blob upload \
    --account-name mydatalake123 \
    --container-name raw \
    --name $(basename $file) \
    --file $file
done
```

**Verify using query:**

```
az storage blob list \
  --account-name mydatalake123 --container-name raw \
  --query "[].{Name:name, Size:properties.contentLength}" --output table
```
