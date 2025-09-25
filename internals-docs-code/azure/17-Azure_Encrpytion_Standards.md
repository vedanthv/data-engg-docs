# 🔒 1. Types of Encryption in Azure Storage

### **a. Encryption at Rest (Server-Side Encryption, SSE)**

* All data written to Azure Storage (Blob, File, Queue, Table, Disk) is **automatically encrypted**.
* Uses **256-bit AES encryption** (FIPS 140-2 compliant).
* Happens **before persisting data** to disk and is transparent to you.
* **No extra cost**.

You can choose key management options:

1. **Microsoft-managed keys (default)** → Azure manages keys automatically.
2. **Customer-managed keys (CMK)** → You provide keys in **Azure Key Vault** or **Managed HSM**.

   * Useful for compliance and rotation policies.

---

### **b. Encryption in Transit**

* All communications to Azure Storage use **HTTPS/TLS**.
* You can enforce **HTTPS-only traffic** by disabling HTTP at the storage account level.
* SMB 3.0 encryption is used for Azure Files.

---

### **c. Client-Side Encryption**

* Optional, you encrypt data **before uploading** to Azure.
* You manage keys and encryption.
* Useful for very sensitive scenarios where you want full control.

---

# 🛠 2. How to Enable / Configure

### By default:

* Encryption at rest (SSE with Microsoft-managed keys) is **always on**, you don’t have to do anything.

### To use Customer-Managed Keys (CMK):

1. Create or use an **Azure Key Vault**.
2. Generate or import your encryption key.
3. Grant the Storage Account **access permissions** to the key.
4. Configure the Storage Account to use that key for encryption.

---

# 📂 3. Example – Azure CLI

Enable CMK with a Key Vault key:

```bash
az storage account update \
  --name mystorageaccount \
  --resource-group myResourceGroup \
  --encryption-key-source Microsoft.Keyvault \
  --encryption-key-vault https://mykeyvault.vault.azure.net/ \
  --encryption-key-name myKey
```

---

# ✅ 4. Quick Summary

* **At Rest** → Always encrypted with AES-256.
* **In Transit** → Encrypted with TLS (HTTPS/SMB).
* **Keys** → Microsoft-managed by default, or CMK via Key Vault/HSM.
* **Extra** → You can do client-side encryption for max control.

---

👉 Do you want me to also show you how **Spark / Databricks** integrates with **Azure Storage encryption** (e.g., when reading/writing to ADLS Gen2)?
