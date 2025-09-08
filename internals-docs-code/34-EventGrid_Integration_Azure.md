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

Great question 👌 — the **subscription** is the key piece that makes **Event Grid actually deliver events** to something.

---

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


Would you like me to extend this demo to show **routing events to multiple consumers** (like Function + Logic App + Event Hub) the way AWS EventBridge fan-outs events?
