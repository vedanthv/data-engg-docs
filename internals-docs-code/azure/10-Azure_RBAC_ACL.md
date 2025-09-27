# RBAC (Role Based Access Control) vs ACL (Access Control List)

---

# 🔹 RBAC (Role-Based Access Control)

* **Scope:** At the **Azure Resource level** (Subscription → Resource Group → Storage Account → Container/File System).
* **Purpose:** Controls **management and broad access** to resources.
* **Assigned via:** Azure Active Directory (Azure AD).
* **Examples of RBAC roles:**

  * Storage Blob Data Reader → can read blobs/files.
  * Storage Blob Data Contributor → can read/write/delete.
  * Storage Blob Data Owner → full control.

✅ **Strengths:**

* Centralized (assign once at container level, applies to all).
* Great for **coarse-grained permissions**.
* Easy to manage across thousands of users.

❌ **Limitations:**

* Not file/folder level → If you grant access to a file system, users see *everything inside*.
* Cannot express “User A can only read `/raw/sales/2025` but not `/raw/hr`.”

---

# 🔹 ACL (Access Control Lists)

* **Scope:** At the **data level** (directory and file).
* **Purpose:** Provides **fine-grained, POSIX-like permissions** within the hierarchical namespace.
* **Assigned via:** Set on directories/files using ADLS Gen2 APIs, CLI, or Databricks/Spark.
* **ACLs have three types:**

  1. **Read (r)** – view file contents, list directory.
  2. **Write (w)** – modify contents.
  3. **Execute (x)** – traverse directory / access child objects.

✅ **Strengths:**

* Very **granular** (control at file/folder level).
* Mimics traditional file systems (POSIX model).
* Perfect for **multi-team data lakes** where each team should only see their zone.

❌ **Limitations:**

* Can get **complex to manage** if you have thousands of folders.
* Inheritance isn’t automatic unless you set **default ACLs**.

---

# 🔹 How RBAC and ACL Work Together in ADLS Gen2

👉 Think of it as **two layers of security**:

1. **RBAC** decides: *Can this user access this storage account / file system at all?*
2. **ACLs** decide: *Within that file system, what directories and files can they actually read/write?*

🔑 Rule: **RBAC grants the door key, ACLs decide which rooms inside you can enter.**

---

# 🔹 Example

### Scenario:

* Storage account: `datalakeprod`
* File system: `finance`
* Directory: `/finance/reports/2025/`

### User: Alice (Finance Analyst)

1. **RBAC**: Assign *Storage Blob Data Reader* at the `finance` file system level → Alice can access the file system.
2. **ACL**:

   * `/finance/reports/2025/` → grant Alice **read + execute**
   * `/finance/raw/` → deny access

👉 Result: Alice can **see and read reports from 2025**, but she cannot even list or open files in the `raw` folder.

---

# 🔹 Summary

| Feature      | RBAC                                                | ACL                                                         |
| ------------ | --------------------------------------------------- | ----------------------------------------------------------- |
| Scope        | Azure resource level                                | File system (directory/file)                                |
| Granularity  | Broad                                               | Fine-grained                                                |
| Assigned via | Azure AD                                            | POSIX-like model                                            |
| Use case     | “Who can access this storage account or container?” | “Within the container, what files/folders can they access?” |
| Best for     | Coarse access control                               | Detailed data lake permissions                              |

---

👉 In short:

* **RBAC = Door access to the building.**
* **ACL = Which rooms and drawers inside you can open.**

---

### Practical : How to setup RBAC and ACLs?

```
az role assignment create \
  --assignee <userObjectIdOrEmail> \
  --role "Storage Blob Data Reader" \
  --scope /subscriptions/<subId>/resourceGroups/<rgName>/providers/Microsoft.Storage/storageAccounts/<storageAccountName>
```

```
az storage fs access set \
  --account-name <storageAccountName> \
  --file-system <containerName> \
  --path <folderName> \
  --acl "user:<userObjectId>:r-x"
```

