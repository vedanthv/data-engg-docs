## Soft Deletes and Point in Time Restore

---

## 🔹 1. Soft Delete

Soft delete = **"safety net" for accidental deletion**.
When enabled, deleted data isn’t immediately removed - instead, it’s kept for a **retention period** so you can restore it.

### Where it applies

* **Azure Blob Storage / Data Lake Storage Gen2**

  * When you delete a blob or snapshot, it goes into a soft-delete state.
  * Retention period: **1-365 days** (configurable).
  * You can list and restore these blobs from the portal, PowerShell, or CLI.

* **Azure Files**

  * Protects deleted file shares.

* **Azure SQL Database / Managed Instance**

  * Soft delete applies to **backups**. Deleted database backups are retained for **7 days by default**.

📌 Example (Blob Storage):

* Delete a blob at `container1/data.csv`.
* It’s recoverable for (say) 30 days.
* After 30 days, it’s permanently purged.

---

## 🔹 2. Point-in-Time Restore (PITR)

PITR = **restore database to a specific time within a retention period**.
It uses **continuous transaction log backups + full/differential backups**.

### Where it applies

* **Azure SQL Database**

  * Default retention: **7–35 days** (depending on service tier).
  * You can restore to any second within that window.
  * PITR creates a **new database** (it doesn’t overwrite the original).

* **Cosmos DB**

  * Continuous backup with **PITR up to 30 days**.

* **Azure Blob Storage**

  * Versioning + change feed + soft delete together simulate PITR at object level.

📌 Example (SQL Database):

* Retention set to 14 days.
* A DROP TABLE happened at `2025-08-25 10:00:00`.
* You can restore the database to `2025-08-25 09:59:59` and recover data.

---

## 🔑 Difference

| Feature         | Purpose                                           | Retention                 |
| --------------- | ------------------------------------------------- | ------------------------- |
| **Soft Delete** | Recover deleted data (blob, file share, backups). | 1–365 days (configurable) |
| **PITR**        | Restore entire DB/container to any time in past.  | SQL: 7–35 days (default)  |

---

## ✅ When to Use

* **Soft delete** → accidental object deletion (blob/file/share/backup).
* **PITR** → logical corruption, dropped table, wrong update query, ransomware attack.

---

