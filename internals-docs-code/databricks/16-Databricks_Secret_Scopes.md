## Databricks Secret Scopes Using Azure Key Vault

---

# 🔹 1. Prerequisites

* An **Azure Databricks workspace** (Premium or above recommended).
* An **Azure Key Vault** created.
* Appropriate RBAC permissions (Owner/Contributor + Key Vault Administrator).
* Networking planned: VNet injection or secure workspace.

---

# 🔹 2. Create an Azure Key Vault

1. Go to **Azure Portal → Create a resource → Key Vault**.
2. Set:

   * **Resource Group**: choose existing/new.
   * **Region**: same as your Databricks workspace (recommended for latency & compliance).
   * **Pricing tier**: Standard.
3. In **Access configuration**:

   * Choose **RBAC** (recommended) OR **Vault access policy**.
   * For Databricks, RBAC is simpler to manage at scale.
4. Finish creation.

---

# 🔹 3. Configure Networking on Key Vault

* In **Key Vault → Networking**:

  1. Set **Public access**:

     * Choose *Disabled* if you want **private access only**.
     * Or choose *Selected networks* and allow only your Databricks subnets.
  2. If you’re using **Private Endpoints**:

     * Click *+ Private Endpoint*.
     * Link it to your Databricks VNet subnet.
     * Approve the private endpoint connection in Key Vault.

---

# 🔹 4. Store Secrets in Key Vault

1. In Key Vault → **Objects → Secrets** → *+ Generate/Import*.
2. Add secrets, e.g.:

   * `db-password`
   * `api-key`

---

# 🔹 5. Create a Databricks Secret Scope Backed by Key Vault

In Databricks workspace:

1. Open **Azure Databricks → Manage Account → User Settings → Access Tokens**.

   * Generate a **personal access token** if you’ll use the CLI.
2. Run Databricks CLI (or REST API) to create the scope:

```bash
databricks secrets create-scope \
  --scope my-keyvault-scope \
  --scope-backend-type AZURE_KEYVAULT \
  --resource-id "/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/Microsoft.KeyVault/vaults/<kv-name>" \
  --dns-name "https://<kv-name>.vault.azure.net/"
```

✅ Now, secrets in Key Vault are accessible from Databricks under the scope `my-keyvault-scope`.

---

# 🔹 6. Access Secrets in Databricks Notebook

```python
# Example: get db-password stored in Key Vault
db_password = dbutils.secrets.get(scope="my-keyvault-scope", key="db-password")

print("Fetched secret length:", len(db_password))  # don’t print actual secret!
```

---

# 🔹 7. Networking Configurations (Important)

You have two secure options for Key Vault ↔ Databricks:

### Option A: VNet Injection (most common for secure workspaces)

* Deploy Databricks workspace in **your own VNet**.
* Add **service endpoints** for Key Vault:

  * Go to **Databricks VNet → Subnets → Service endpoints → Add KeyVault**.
* In Key Vault **Networking**, allow that subnet.

### Option B: Private Endpoint

* Create a **private endpoint** for Key Vault in the Databricks VNet.
* Approve the connection in Key Vault.
* Disable public network access for maximum security.

---

# 🔹 8. Permissions

* In **Key Vault → Access Control (IAM)**:

  * Assign your Databricks workspace managed identity:

    * **Key Vault Secrets User** role.
    * Or **Key Vault Reader** role (depending on setup).

---

# ✅ Summary

1. Create Key Vault → Add secrets.
2. Configure networking (service endpoint or private endpoint).
3. Assign RBAC so Databricks can access Key Vault.
4. Create secret scope in Databricks (backed by Key Vault).
5. Access secrets inside notebooks with `dbutils.secrets.get`.

---

Would you like me to also draw you a **network diagram** (Databricks → VNet → Key Vault with private endpoint) so you can visualize the traffic flow?
