# 🧪 Demo: Event Grid + Blob Storage + Azure Function

## 1️⃣ Create a Storage Account

```bash
az group create --name demo-rg --location eastus

az storage account create \
  --name demoeventgridstore \
  --resource-group demo-rg \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2
```

Create a container:

```bash
az storage container create \
  --name demo-container \
  --account-name demoeventgridstore
```

---

## 2️⃣ Create a Function App (event handler)

Install extension if not installed:

```bash
az extension add --name functionapp
```

Create resources:

```bash
az storage account create \
  --name demofunctionstore \
  --resource-group demo-rg \
  --location eastus \
  --sku Standard_LRS

az functionapp create \
  --resource-group demo-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --functions-version 4 \
  --name demo-eventgrid-func \
  --storage-account demofunctionstore
```

---

## 3️⃣ Create an Event Grid Subscription

Hook Blob Storage events to the Function:

```bash
az eventgrid event-subscription create \
  --name demo-subscription \
  --source-resource-id $(az storage account show \
    --name demoeventgridstore \
    --resource-group demo-rg \
    --query id -o tsv) \
  --endpoint-type azurefunction \
  --endpoint $(az functionapp show \
    --name demo-eventgrid-func \
    --resource-group demo-rg \
    --query id -o tsv)
```

---

## 4️⃣ Add Function Code

Inside your Function App (can be done in VS Code or portal):

**`__init__.py`**

```python
import logging
import json

import azure.functions as func

def main(event: func.EventGridEvent):
    logging.info('Event received: %s', event.get_json())
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type
    })
    logging.info('Processed Event: %s', result)
```

This will log the event payload whenever triggered.

---

## 5️⃣ Trigger the Event

Upload a test file:

```bash
az storage blob upload \
  --account-name demoeventgridstore \
  --container-name demo-container \
  --name hello.txt \
  --file hello.txt \
  --auth-mode login
```

---

## 6️⃣ Verify

Check logs of the Function App:

```bash
az functionapp log tail --name demo-eventgrid-func --resource-group demo-rg
```

You should see Event Grid delivering the event with metadata like:

```json
{
  "id": "abcd-1234",
  "data": {
    "api": "PutBlob",
    "clientRequestId": "...",
    "requestId": "...",
    "contentType": "text/plain",
    "blobType": "BlockBlob",
    "url": "https://demoeventgridstore.blob.core.windows.net/demo-container/hello.txt"
  },
  "topic": "/subscriptions/.../resourceGroups/demo-rg/providers/Microsoft.Storage/storageAccounts/demoeventgridstore",
  "subject": "/blobServices/default/containers/demo-container/blobs/hello.txt",
  "event_type": "Microsoft.Storage.BlobCreated"
}
```
## 🔑 Why do we need an Event Grid subscription?

* **Event Grid itself is just an event router**.

  * It listens to event sources (like Blob Storage, IoT Hub, custom topics).
  * But it doesn’t know *where* to send events unless you explicitly tell it.

* **An Event Grid subscription is the “routing rule”**:

  * Defines *which events* you care about (filters by event type, subject, prefix/suffix).
  * Defines *where to send them* (endpoint like Function, Logic App, Event Hub, Webhook).

Without a subscription, the events are generated but simply **dropped** — nothing consumes them.

---

## 📌 Example (Blob Storage → Function)

1. **Blob Storage** generates an event: *“BlobCreated”*.
2. Event Grid sees it but needs a subscription.
3. The **Event Grid subscription** says:

   * Source = `demoeventgridstore` (Blob Storage).
   * Event Type = `Microsoft.Storage.BlobCreated`.
   * Target = Function `demo-eventgrid-func`.
4. Now, when a blob is uploaded → Event Grid matches subscription → delivers event to Function.

---

## 🧠 Analogy

Think of it like **YouTube**:

* Blob Storage (publisher) = YouTube channel.
* Event Grid (event router) = YouTube platform.
* Event Grid Subscription = you clicking “Subscribe + Notify” to a channel.
* Function/Logic App = your phone getting the notification.

If you don’t subscribe, the channel is still publishing videos (events), but *you’ll never see them*.

---
✅ So, you need to **create a subscription** every time you want to connect an **event source** to an **event handler**.

### Example

---

# 🔹 Architecture Overview

1. **Blob Storage** → file lands (raw data).
2. **Event Grid (system topic)** → automatically emits `BlobCreated` event.
3. **Event Subscription** → routes event to an **Azure Function**.
4. **Azure Function** → parses event payload (which blob was uploaded) and calls **Databricks Jobs API**.
5. **Databricks Job** → runs notebook/ETL to process the file.

---

# 🔹 Step 1. Create Storage Account

This is the **event source**.

```bash
az storage account create \
  --name mydatalake123 \
  --resource-group myResourceGroup \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2 \
  --hierarchical-namespace true
```

---

# 🔹 Step 2. Create an Event Handler (Azure Function)

This Function will receive BlobCreated events and trigger Databricks.

```bash
az functionapp create \
  --resource-group myResourceGroup \
  --consumption-plan-location eastus \
  --runtime python \
  --functions-version 4 \
  --name databrickstriggerfunc \
  --storage-account mydatalake123
```

---

# 🔹 Step 3. Create Event Subscription

Connect Blob Storage → Event Grid → Function.

```bash
az eventgrid event-subscription create \
  --name blobCreatedToDatabricks \
  --source-resource-id /subscriptions/<subId>/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/mydatalake123 \
  --endpoint-type azurefunction \
  --endpoint /subscriptions/<subId>/resourceGroups/myResourceGroup/providers/Microsoft.Web/sites/databrickstriggerfunc/functions/<functionName>
```

---

# 🔹 Step 4. Function Code (Python)

This Function will:

1. Receive BlobCreated event.
2. Extract blob URL.
3. Call Databricks Jobs API (authenticated with **Personal Access Token** or **Managed Identity**).

```python
import logging
import os
import requests
import azure.functions as func

# Databricks config
DATABRICKS_INSTANCE = os.environ["DATABRICKS_INSTANCE"]   # e.g. https://adb-123456789012.12.azuredatabricks.net
DATABRICKS_TOKEN = os.environ["DATABRICKS_TOKEN"]         # Store securely in Key Vault
DATABRICKS_JOB_ID = os.environ["DATABRICKS_JOB_ID"]       # Job you want to trigger

def main(event: func.EventGridEvent):
    result = event.get_json()
    logging.info(f"Received event: {result}")

    # Check for blob created event
    if event.event_type == "Microsoft.Storage.BlobCreated":
        blob_url = result.get("url")
        logging.info(f"New blob detected: {blob_url}")

        # Trigger Databricks job via REST API
        url = f"{DATABRICKS_INSTANCE}/api/2.1/jobs/run-now"
        headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
        payload = {
            "job_id": DATABRICKS_JOB_ID,
            "notebook_params": {
                "input_blob": blob_url
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            logging.info("Databricks job triggered successfully")
        else:
            logging.error(f"Failed to trigger job: {response.text}")
```

---

# 🔹 Step 5. Databricks Job

1. Create a **Job** in Databricks (pointing to a Notebook/Delta Live Table).
2. Add a parameter `input_blob` so the notebook knows which file to process.

Example Notebook:

```python
dbutils.widgets.text("input_blob", "")
blob_url = dbutils.widgets.get("input_blob")

print(f"Processing file: {blob_url}")

# Example: Read from Blob/ADLS into Spark
df = spark.read.text(blob_url)
# Do ETL...
```

---

# 🔹 Step 6. Test It

Upload a file to Blob Storage:

```bash
az storage blob upload \
  --account-name mydatalake123 \
  --container-name raw \
  --name testdata.csv \
  --file ./testdata.csv
```

Event Grid → Function → Databricks job → Notebook runs with the blob path.

---

# 🔹 Extras (Production Ready)

* **Secure secrets** → Store `DATABRICKS_TOKEN` in **Azure Key Vault** and integrate with Function.
* **Retries** → Event Grid automatically retries delivery (with exponential backoff).
* **Dead-letter destination** → configure a Blob container to store undelivered events.
* **Monitoring** → Use **Application Insights** on the Function + Event Grid metrics.

---

✅ With this setup, every time a new file lands in storage, your Databricks pipeline kicks in automatically — no polling needed, fully event-driven.

---