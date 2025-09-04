## Shared Access Signatures in Azure

---

## 🔹 What is a SAS?

A **Shared Access Signature (SAS)** is like a **temporary key with limited permissions** that you can give to someone (or an app) so they can access your Azure Storage resources **without sharing your account keys**.

* Your **storage account keys** = the **master key** to the whole house.
* A **SAS token** = a **guest pass** to just one room, for a limited time.

---

## 🔹 Types of SAS

1. **Account SAS**

   * Grants access to services at the **account level**.
   * Can apply to: Blob, File, Queue, Table.
   * Example: “Give read/write to all blob containers for 2 hours.”

2. **Service SAS**

   * Grants access to a **specific resource** (like one blob, or one file share).
   * Example: “User can download just this one blob until midnight.”

3. **User Delegation SAS**

   * Created using **Azure AD credentials** instead of account key.
   * More secure because you avoid using storage account keys.
   * Example: “An app logged in with Azure AD gets a SAS for one blob.”

---

## 🔹 What can you control with a SAS?

* **Permissions**

  * Read (`r`), Write (`w`), Delete (`d`), List (`l`), Add, Create, Update.
* **Start time and expiry time**

  * Define when the SAS is valid.
* **Resource scope**

  * Container, Blob, File, Queue, Table.
* **IP address restrictions**

  * Limit access to certain IP ranges.
* **Protocol restrictions**

  * Allow HTTPS only (recommended).

---

## 🔹 SAS Structure

A SAS is basically a **token string** you append to a resource URL.
Example:

```
https://mystorageaccount.blob.core.windows.net/mycontainer/myfile.txt?sv=2023-11-14&ss=b&srt=o&sp=r&se=2025-09-05T10:00Z&st=2025-09-05T08:00Z&spr=https&sig=abcd1234
```

Parts:

* `sv` → Storage version.
* `ss` → Services.
* `srt` → Resource types.
* `sp` → Permissions.
* `st` / `se` → Start/Expiry time.
* `sig` → The cryptographic signature.

---

## 🔹 How to create SAS

### Option 1: **Azure Portal**

* Go to your Storage Account → **Shared access signature** → Choose permissions, expiry, allowed IP → Generate SAS token.

### Option 2: **Azure Storage Explorer**

* Right-click container/blob → Get Shared Access Signature.

### Option 3: **Azure CLI**

```sh
az storage blob generate-sas \
  --account-name mystorageaccount \
  --container-name mycontainer \
  --name myfile.txt \
  --permissions r \
  --expiry 2025-09-05T10:00Z \
  --https-only \
  --output tsv
```

### Option 4: **SDK (Python example)**

```python
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

sas_token = generate_blob_sas(
    account_name="mystorageaccount",
    container_name="mycontainer",
    blob_name="myfile.txt",
    account_key="your_storage_key",
    permission=BlobSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)

print("SAS Token:", sas_token)
```

---

## 🔹 Best Practices

* Use **User Delegation SAS** with Azure AD when possible.
* Keep expiry times short (principle of least privilege).
* Use **stored access policies** if you need to revoke SAS without waiting for expiry.
* Restrict to HTTPS and specific IP ranges.

---

## 🔹 Shared Access Signatures (SAS)

* **What it is**: A **signed token** you append to a storage resource URL (e.g., blob, file, queue).
* **How it works**:

  * Signed with the storage account key (or via Azure AD for user delegation SAS).
  * Grants specific **permissions (R/W/D/L)** for a **time window**.
  * Passed around as part of a URL.

👉 Think: “Here’s a **temporary guest pass** to this file/container.”

**Pros:**

* Very flexible (can be scoped down to one blob, for 5 minutes).
* Easy to share (just a URL).
* No need for caller to authenticate with Azure AD.

**Cons:**

* Hard to revoke (unless you use **stored access policies**).
* If leaked, anyone with the token can use it until it expires.
* Still relies on account keys (for Service SAS / Account SAS).

---

## 🔹 Managed Identities (MI)

* **What it is**: An **Azure AD identity** automatically managed by Azure for your resource (VM, Function, App Service, Databricks, etc.).
* **How it works**:

  * Resource (e.g., Databricks cluster) has a system-assigned or user-assigned identity.
  * Identity is trusted by Azure AD.
  * When the resource needs to access storage, it requests a token from Azure AD using its MI.
  * Access is controlled via **Azure RBAC** (e.g., “Blob Data Reader”).

👉 Think: “The **building security system** recognizes you because you’re wearing your office badge.”

**Pros:**

* No secrets, no SAS tokens, no keys to manage.
* Access controlled centrally by **Azure RBAC**.
* Tokens are short-lived and auto-rotated.
* More secure for long-running apps (no risk of token leaks in code).

**Cons:**

* Less flexible for **fine-grained sharing** (you can’t say “give access to just this one blob for 15 minutes”).
* Requires the caller to run inside Azure (VM, Function, App Service, Databricks, etc.).

---

## 🔹 When to use what

| Scenario                                               | Use SAS | Use Managed Identity |
| ------------------------------------------------------ | ------- | -------------------- |
| Share a file with an external partner                  | ✅ Yes   | ❌ No                 |
| Grant temporary access to a single blob/container      | ✅ Yes   | ❌ No                 |
| Long-running Azure app accessing storage               | ❌ No    | ✅ Yes                |
| Secure, keyless access with automatic token rotation   | ❌ No    | ✅ Yes                |
| Fine-grained, time-limited access without RBAC changes | ✅ Yes   | ❌ No                 |

---

✅ **Summary**:

* **SAS** = best for **short-term, fine-grained, external sharing** (like “download this blob until tonight”).
* **Managed Identity** = best for **apps running in Azure** that need **ongoing secure access** without key management.

---
