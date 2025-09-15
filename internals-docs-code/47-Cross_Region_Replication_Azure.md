# Cross Region Replication

---

## 🔑 1. Built-in Redundancy Options (Storage Account Level)

When you create an ADLS Gen2 account, you choose a **redundancy type**. Azure handles replication under the hood.

### ✅ Options:

1. **LRS (Locally Redundant Storage)**

   * 3 copies within a single datacenter in one region.
   * Cheapest but **no cross-region replication**.

2. **ZRS (Zone-Redundant Storage)**

   * 3 copies across 3 availability zones in one region.
   * Provides resilience against **zone failures**, but **not region-wide outages**.

3. **GRS (Geo-Redundant Storage)**

   * 6 copies: 3 in primary region + 3 in a paired secondary region.
   * Replication is **asynchronous**.

4. **RA-GRS (Read-Access Geo-Redundant Storage)**

   * Same as GRS, but **read access** to the secondary region is available.
   * Useful for **disaster recovery** and **read-heavy workloads**.

5. **GZRS (Geo-Zone Redundant Storage)**

   * Combines ZRS (in primary region) + asynchronous replication to a paired secondary region.
   * High durability + regional disaster recovery.

6. **RA-GZRS (Read-Access GZRS)**

   * Same as GZRS but with **read access to secondary** region.
   * Best option for **mission-critical cross-region replication**.

---

## 🔑 2. Asynchronous Data Movement (Custom Replication)

Sometimes built-in GRS/RA-GRS may not meet your **latency, cost, or compliance** requirements. In that case, you build **custom cross-region replication**:

### Approaches:

* **Azure Data Factory (ADF) Copy Activity**

  * Schedule pipelines to copy data from ADLS in Region A → ADLS in Region B.
  * Flexible (supports filtering, transformations, scheduling).
  * Good for **batch replication**.

* **Azure Data Share**

  * For sharing snapshots of datasets across regions.
  * Suited for **read-only scenarios**.

* **AzCopy / Azure Storage Sync Service**

  * AzCopy CLI can sync containers across regions.
  * Best for **ad-hoc or bulk replication**.

* **Event-Driven Replication with Event Grid + Functions**

  * Trigger on BlobCreated/Updated events → replicate object to another region.
  * Provides **near real-time cross-region replication**.

* **Third-party tools** (Databricks, Apache NiFi, Informatica, etc.)

  * For more complex pipelines involving **CDC (Change Data Capture)** or **multi-cloud replication**.

---

## 🔑 3. Strategy Selection (When to Use What)

* **Mission-critical, zero-downtime needs** → Use **RA-GZRS** for built-in cross-region replication with read access.
* **Compliance requirements (regulatory control over region)** → Use **custom ADF/Event Grid pipelines** to replicate only selected data.
* **Disaster recovery only (cold standby)** → Use **GRS/RA-GRS** with failover enabled.
* **Performance optimization (local reads in multiple geographies)** → Use **RA-GRS or RA-GZRS** so consumers in another geography can read from the secondary.

---

## 🔑 4. Failover Considerations

* For **GRS/RA-GRS/GZRS/RA-GZRS**, failover to secondary is **manual**.
* When you trigger failover, the secondary becomes primary.
* Important: **failover breaks replication** (you must reconfigure after).

---

✅ **Summary:**

* Use **RA-GZRS** if you want the best balance of availability + performance with cross-region reads.
* Use **ADF/Event Grid/AzCopy** if you need **fine-grained control** over what, when, and how data is replicated across regions.
* Always align your choice with **RPO (Recovery Point Objective)**, **RTO (Recovery Time Objective)**, and **compliance** needs.
