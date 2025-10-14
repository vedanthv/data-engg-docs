## ACID Guarantees in Databricks

Databricks uses Delta Lake by default for all reads and writes and builds upon the ACID guarantees provided by the open source Delta Lake protocol. ACID stands for atomicity, consistency, isolation, and durability.

- Atomicity means that all transactions either succeed or fail completely.

- Consistency guarantees relate to how a given state of the data is observed by simultaneous operations.

- Isolation refers to how simultaneous operations potentially conflict with one another.

- Durability means that committed changes are permanent.

While many data processing and warehousing technologies describe having ACID transactions, specific guarantees vary by system, and transactions on Databricks might differ from other systems you've worked with.

### How are Transactions scoped on Databricks

Databricks manages transactions at the **table level**, meaning each transaction only affects one table at a time.

It uses **optimistic concurrency control**, which means:

* There are **no locks** on reads or writes.
* Multiple users can read or write at the same time without blocking each other.
* Because locks are not used, **deadlocks cannot occur**.

### Isolation Levels

* **Snapshot isolation** applies to reads.
  This means each read operation sees a consistent snapshot of the table as it was when the read began — even if other users are modifying the table at the same time.

* **Write-serializable isolation** applies to writes.
  This is stronger than snapshot isolation because Databricks ensures that concurrent write operations produce a consistent final state, as if they happened one after another in sequence.

### Multi-table Reads

When a query reads from multiple tables, Databricks:

* Reads the **current version** of each table at the moment it is accessed.
* Does **not block** other transactions that are writing to those tables.

### Multi-table Transactions

Databricks does **not support** `BEGIN` and `END` statements to group multiple operations into a single transaction across tables.
If an application needs to modify multiple tables, it must **commit changes to each table separately** — one after another.

### Combining Multiple Operations

Within a single table, you can combine **inserts, updates, and deletes** into one atomic write operation by using the **`MERGE INTO`** statement.
This ensures that all those changes happen together as a single transaction.

Sure. Here is a clear explanation without emojis.

---

### Scenario

Suppose you have two Delta tables:

* `orders`
* `customers`

You want to:

1. Insert a new order into `orders`
2. Update the customer’s last order date in `customers`

You want both changes to behave like one transaction.

---

### Key Point

Databricks does not support true multi-table transactions.
Each operation on a table is committed independently.
If one operation fails, Databricks will not automatically roll back the others.

---

### Example: Sequential Multi-table Operations

```sql
-- Step 1: Insert a new order
INSERT INTO orders (order_id, customer_id, amount, order_date)
VALUES (101, 1, 250.00, current_timestamp());

-- Step 2: Update the customer’s last order date
UPDATE customers
SET last_order_date = current_timestamp()
WHERE customer_id = 1;
```

Each of these statements is its own transaction.
If the first succeeds but the second fails, the first will still be committed.

---

### Handling Multi-table Consistency

#### Option 1: Application-level Control

You can manage multi-table logic at the application or notebook level.
For example, in Python:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

try:
    # Table 1: Insert new order
    spark.sql("""
        INSERT INTO orders (order_id, customer_id, amount, order_date)
        VALUES (101, 1, 250.00, current_timestamp())
    """)

    # Table 2: Update customer info
    spark.sql("""
        UPDATE customers
        SET last_order_date = current_timestamp()
        WHERE customer_id = 1
    """)

except Exception as e:
    print("Transaction failed:", e)
    # Optionally run manual rollback logic, such as deleting the new order
```

This way, you can control what happens if one statement fails.
For instance, if the update fails, you could delete the order that was just inserted.

---

#### Option 2: Using a Staging Table

You can use a staging table to stage changes before applying them to multiple tables.

```sql
-- Stage combined changes
CREATE OR REPLACE TABLE staging_orders AS
SELECT 101 AS order_id, 1 AS customer_id, 250.00 AS amount, current_timestamp() AS order_date;

-- Merge into the orders table
MERGE INTO orders AS o
USING staging_orders AS s
ON o.order_id = s.order_id
WHEN NOT MATCHED THEN INSERT *;

-- Merge into the customers table
MERGE INTO customers AS c
USING staging_orders AS s
ON c.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET last_order_date = s.order_date;
```

This approach helps you track progress and retry failed steps, but it still does not provide atomicity across both tables.

---

### Summary

| Concept                                    | Databricks Behavior                       |
| ------------------------------------------ | ----------------------------------------- |
| Atomic transactions across multiple tables | Not supported                             |
| Atomic operations on a single table        | Supported                                 |
| Sequential multi-table updates             | Supported, but managed by the application |
| Rollback for multi-table transactions      | Must be handled manually                  |
| MERGE INTO for combined operations         | Supported per table                       |

---

## How does Databricks Implement Atomicity?

The transaction log controls commit atomicity. During a transaction, data files are written to the file directory backing the table. When the transaction completes, a new entry is committed to the transaction log that includes the paths to all files written during the transaction. Each commit increments the table version and makes new data files visible to read operations. The current state of the table comprises all data files marked valid in the transaction logs.

Data files are not tracked unless the transaction log records a new version. If a transaction fails after writing data files to a table, these data files will not corrupt the table state, but the files will not become part of the table. The VACUUM operation deletes all untracked data files in a table directory, including remaining uncommitted files from failed transactions.

## How does Databricks Implement Durability?

Databricks uses cloud object storage to store all data files and transaction logs. Cloud object storage has high availability and durability. Because transactions either succeed or fail completely and the transaction log lives alongside data files in cloud object storage, tables on Databricks inherit the durability guarantees of the cloud object storage on which they're stored.

## How does Databricks ensure consistency?

Delta Lake uses optimistic concurrency control to provide transactional guarantees between writes. Under this mechanism, writes operate in three stages:

- Read: Reads (if needed) the latest available version of the table to identify which files need to be modified (that is, rewritten).
    - Writes that are append-only do not read the current table state before writing. Schema validation leverages metadata from the transaction log.
- Write: Writes data files to the directory used to define the table.
- Validate and commit:
Checks whether the proposed changes conflict with any other changes that may have been concurrently committed since the snapshot that was read.

If there are no conflicts, all the staged changes are committed as a new versioned snapshot, and the write operation succeeds.

If there are conflicts, the write operation fails with a concurrent modification exception. This failure prevents corruption of data.

## How does Databricks Implement Isolation?

Databricks uses write serializable isolation by default for all table writes and updates. Snapshot isolation is used for all table reads.

Write serializability and optimistic concurrency control work together to provide high throughput for writes. The current valid state of a table is always available, and a write can be started against a table at any time. Concurrent reads are only limited by throughput of the metastore and cloud resources.

