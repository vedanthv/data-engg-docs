# Azure Storage Rest APIs

## 🔑 1. What It Is

The **Azure Storage REST API** allows you to programmatically perform operations on:

* **Blob storage** (block, append, page blobs → includes ADLS Gen2)
* **Queue storage**
* **Table storage** (legacy, use Cosmos DB Table API now)
* **File shares (Azure Files)**

Instead of SDKs (Python, .NET, Java, etc.), you can call storage endpoints directly via HTTPS.

---

## 🔑 2. REST API Endpoint Pattern

Every request goes to:

```
https://<account_name>.blob.core.windows.net/<container>/<blob>?<optional_parameters>
```

Example (reading a file in ADLS Gen2):

```http
GET https://mystorageaccount.blob.core.windows.net/mycontainer/myfolder/myfile.csv HTTP/1.1
x-ms-date: Mon, 15 Sep 2025 18:00:00 GMT
x-ms-version: 2023-11-03
Authorization: SharedKey mystorageaccount:<signature>
```

---

## 🔑 3. Authentication Methods

You must authenticate every REST API request. Options:

1. **Shared Key (HMAC)**

   * Uses your storage account name + access key.
   * You compute an HMAC signature for each request (`Authorization: SharedKey <account>:<signature>`).
   * Very low-level but powerful.

2. **SAS (Shared Access Signature)**

   * Pre-signed URL with limited permissions (read/write/list/delete).
   * Example:

     ```
     https://mystorageaccount.blob.core.windows.net/mycontainer/myfile.csv?sv=2023-11-03&ss=b&srt=o&sp=rw&se=2025-09-16T18:00Z&sig=<signature>
     ```
   * Great for **temporary access** (e.g., users, apps, third parties).

3. **OAuth 2.0 / Azure AD (Recommended)**

   * Use **Azure AD service principal or managed identity**.
   * Add bearer token in header:

     ```
     Authorization: Bearer <access_token>
     ```

---

## 🔑 4. Common REST Operations (Blobs / ADLS Gen2)

### Container Operations

* **Create Container**

  ```http
  PUT https://<account>.blob.core.windows.net/<container>?restype=container
  ```
* **List Containers**

  ```http
  GET https://<account>.blob.core.windows.net/?comp=list
  ```

### Blob/File Operations

* **Upload Blob**

  ```http
  PUT https://<account>.blob.core.windows.net/<container>/<blob>
  x-ms-blob-type: BlockBlob
  ```

  (Body contains file data)

* **Download Blob**

  ```http
  GET https://<account>.blob.core.windows.net/<container>/<blob>
  ```

* **Delete Blob**

  ```http
  DELETE https://<account>.blob.core.windows.net/<container>/<blob>
  ```

### ADLS Gen2-Specific (Hierarchical Namespace enabled)

* **Create Directory**

  ```http
  PUT https://<account>.dfs.core.windows.net/<filesystem>/<directory>?resource=directory
  ```

* **Create File**

  ```http
  PUT https://<account>.dfs.core.windows.net/<filesystem>/<directory>/<file>?resource=file
  ```

* **Append Data**

  ```http
  PATCH https://<account>.dfs.core.windows.net/<filesystem>/<directory>/<file>?action=append&position=0
  ```

* **Flush Data (commit)**

  ```http
  PATCH https://<account>.dfs.core.windows.net/<filesystem>/<directory>/<file>?action=flush&position=<length>
  ```

---

## 🔑 5. Versioning

* Each request must specify an **API version** in the `x-ms-version` header.
* Example: `x-ms-version: 2023-11-03`
* This ensures consistent behavior as Azure evolves.

---

## 🔑 6. Tools for Testing

* **Postman / Insomnia** → manually call REST APIs.
* **cURL** for CLI-based requests.
* **AzCopy** (built on REST API).
* **Azure Storage Explorer** (GUI built on REST API).

---

✅ **Summary**:
The **Azure Storage REST API** is the backbone of ADLS & Blob operations. You can:

* Authenticate with Shared Key, SAS, or Azure AD.
* Use Blob endpoints for standard blob storage.
* Use DFS endpoints (`.dfs.core.windows.net`) for ADLS Gen2 hierarchical namespace features.
* Issue standard HTTP verbs (`GET`, `PUT`, `PATCH`, `DELETE`) with required headers.

### Python Example

```python
import requests
from azure.identity import ClientSecretCredential

# Azure AD app registration
tenant_id = "<tenant-id>"
client_id = "<client-id>"
client_secret = "<client-secret>"

# Authenticate
cred = ClientSecretCredential(tenant_id, client_id, client_secret)
token = cred.get_token("https://storage.azure.com/.default").token

# Storage details
account_name = "mystorageaccount"
filesystem = "mycontainer"
file_path = "demo_folder/test2.txt"
base_url = f"https://{account_name}.dfs.core.windows.net/{filesystem}/{file_path}"

# Create file
headers = {"Authorization": f"Bearer {token}", "x-ms-version": "2023-11-03"}
resp = requests.put(f"{base_url}?resource=file", headers=headers)
print("Create:", resp.status_code, resp.text)

# Append
data = b"Secure upload via Azure AD!"
resp = requests.patch(f"{base_url}?action=append&position=0",
                      headers={**headers, "Content-Length": str(len(data))},
                      data=data)
print("Append:", resp.status_code, resp.text)

# Flush
resp = requests.patch(f"{base_url}?action=flush&position={len(data)}",
                      headers={**headers, "Content-Length": "0"})
print("Flush:", resp.status_code, resp.text)
```
