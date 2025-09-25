## Deletion Vectors in Delta Lake

### 🔹 What are Deletion Vectors?

Normally, when you delete rows in a Delta table, Delta rewrites entire Parquet files without those rows.

This is called copy-on-write → expensive for big tables.

Deletion Vectors (DVs) are a new optimization:

Instead of rewriting files, Delta just marks the deleted rows with a bitmap (a lightweight “mask”).
The data is still physically there, but readers skip the “deleted” rows.

Think of it like putting a red X mark ❌ on rows instead of erasing them immediately.

### 🔹 Why are they useful?

🚀 Much faster deletes/updates/merges (because files aren’t rewritten).

⚡ Less I/O → good for big data tables.

✅ Efficient for streaming + time travel.

### Example Without deletion vectors

1. Create a sales table

```sql
CREATE TABLE dev.bronze.sales as 
select * from 
read_files(
  'dbfs:/databricks-datasets/online_retail/data-001/data.csv',
  header => true,
  format => 'csv'
)
```

2. Set Deletion Vectors false

```sql
ALTER TABLE dev.bronze.sales SET TBLPROPERTIES (delta.enableDeletionVectors = false);
```

<img width="977" height="112" alt="image" src="https://github.com/user-attachments/assets/7a685589-c484-45b0-b9d7-992e36cb0bbc" />

3. Delete some rows

```sql
-- delete InvoiceNo = '540644'
delete from dev.bronze.sales
where InvoiceNo = '540644'
```

4. Describe history

<img width="1343" height="333" alt="image" src="https://github.com/user-attachments/assets/3a2f3c1e-c5e1-4122-b4f6-c1389908bbed" />

Observe that all rows (65000+) are removed and rewritten.

### Example with deletion vectors

<img width="1337" height="427" alt="image" src="https://github.com/user-attachments/assets/62bd9425-3930-4943-b667-c5c517718dc5" />

We can see that one deletion vector is added no files are rewritten.

Running optimize would remove those files / records.
