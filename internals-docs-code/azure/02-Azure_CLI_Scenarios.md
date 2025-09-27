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
echo "id,name,age
1,Alice,30
2,Bob,25
3,Charlie,28" > sample.csv
```



```
az storage blob upload --account-name storageaccountfromclivb \
--container-name clidatacontainer --name sample.csv --file ./sample.csv
```

**List blobs**

```
az storage blob list \
  --account-name storageaccountfromclivb --container-name clidatacontainer \
  --output table
```

### 🔹 Exercise 3: SQL Database

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

### `basename $file`

* `basename` is a Unix command.
* It strips the **directory path** from a file and returns only the filename.
* Example:

  ```bash
  file="/home/user/docs/report.pdf"
  basename $file
  ```

  Output:

  ```
  report.pdf
  ```

### `--name $(basename $file)`

* The `$(...)` syntax means **command substitution**: run the command inside and replace it with its output.
* So `$(basename $file)` gets replaced by the filename (without path).
* If `file="/home/user/docs/report.pdf"`, then:

  ```
  --name $(basename $file)
  ```

  becomes:

  ```
  --name report.pdf
  ```

---

### Why it’s used

Often, scripts loop through files in directories. Instead of passing full paths, they just want the **filename** for naming a resource, argument, or output.

Example in Azure CLI:

```bash
for file in /path/to/files/*; do
  az storage blob upload \
    --account-name mystorage \
    --container-name mycontainer \
    --file $file \
    --name $(basename $file)
done
```

Here:

* `--file $file` → full path to the file.
* `--name $(basename $file)` → just the filename in the blob storage.

---

**Verify using query:**

```
az storage blob list \
  --account-name mydatalake123 --container-name raw \
  --query "[].{Name:name, Size:properties.contentLength}" --output table
```

That syntax is from the **Azure CLI**, and specifically it uses **JMESPath** (a JSON query language) to filter and reshape JSON output from Azure commands.

Let’s break it down:

---

### The context

Most `az` CLI commands return **JSON objects**. For example, listing blobs:

```bash
az storage blob list \
  --account-name mystorage \
  --container-name mycontainer \
  --output json
```

Might return something like:

```json
[
  {
    "name": "file1.txt",
    "properties": {
      "contentLength": 1234,
      "contentType": "text/plain"
    }
  },
  {
    "name": "file2.csv",
    "properties": {
      "contentLength": 5678,
      "contentType": "text/csv"
    }
  }
]
```

---

### The query explained

`--query "[].{Name:name, Size:properties.contentLength}"`

1. `[]`

   * Means "go through each item in the JSON array".

2. `{Name:name, Size:properties.contentLength}`

   * Reshapes each object to keep only:

     * `Name` → mapped from the field `name`.
     * `Size` → mapped from nested field `properties.contentLength`.

So the output would look like:

```json
[
  {
    "Name": "file1.txt",
    "Size": 1234
  },
  {
    "Name": "file2.csv",
    "Size": 5678
  }
]
```

---

### Why it’s useful

* Avoids huge JSON output.
* Lets you extract just the fields you care about.
* Works with `--output table` for nice tabular summaries:

```bash
az storage blob list \
  --account-name mystorage \
  --container-name mycontainer \
  --query "[].{Name:name, Size:properties.contentLength}" \
  --output table
```

Gives:

```
Name       Size
---------  -----
file1.txt  1234
file2.csv  5678
```

---