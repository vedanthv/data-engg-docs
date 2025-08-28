### ```COPY INTO``` in Databricks

COPY INTO feature is used to load files from volumes to Databricks tables and has feature of idempotency ie the data does not get duplicated in the table.

#### Steps

1. Create Volume

```sql
CREATE VOLUME dev.bronze.landing
```

2. Create folder inside volume

```sql
dbutils.fs.mkdirs("/Volumes/dev/bronze/landing/input")
```

3. Copy sample dataset into volume

```python
dbutils.fs.cp("/databricks-datasets/definitive-guide/data/retail-data/by-day/2010-12-01.csv","/Volumes/dev/bronze/landing/input")

dbutils.fs.cp("/databricks-datasets/definitive-guide/data/retail-data/by-day/2010-12-02.csv","/Volumes/dev/bronze/landing/input")
```

4. Create bronze table

```sql
COPY INTO dev.bronze.invoice_cp
FROM '/Volumes/dev/bronze/landing/input'
FILEFORMAT = CSV
PATTERN = '*.csv'
FORMAT_OPTIONS ( -- for the files, if they are different format one has 3 cols other has 5 then merge them
  'mergeSchema' = 'true',
  'header' = 'true'
)
COPY_OPTIONS ( -- at table level meerge Schema
  'mergeSchema' = 'true'
)
```

5. Select from table

We can see 5217 rows.

<img width="1322" height="564" alt="image" src="https://github.com/user-attachments/assets/f4058ce6-74df-4608-ab03-24fc8fd1013f" />

6. Run COPY INTO again

<img width="1345" height="618" alt="image" src="https://github.com/user-attachments/assets/ce26f8ea-8cb8-478e-b7bf-4ed14d744da0" />

No affected rows so copy into does not duplicate. Its idempotent.

### How does copy into maintain the log of data files ingested?

The delta log maintains json version tracking that has information and path of files processed.

<img width="1564" height="614" alt="image" src="https://github.com/user-attachments/assets/17755221-552f-443e-a762-81f65fb50b93" />

### Custom Transformations while loading

```
COPY INTO dev.bronze.invoice_cp_alt
FROM 
(
  SELECT InvoiceNo,StockCode,cast(Quantity as DOUBLE),current_timestamp() as _insert_date 
  FROM 
  '/Volumes/dev/bronze/landing/input'
)

FILEFORMAT = CSV
PATTERN = '*.csv'
FORMAT_OPTIONS ( -- for the files, if they are different format one has 3 cols other has 5 then merge them
  'mergeSchema' = 'true',
  'header' = 'true'
)
COPY_OPTIONS ( -- at table level meerge Schema
  'mergeSchema' = 'true'
)
```

<img width="1356" height="660" alt="image" src="https://github.com/user-attachments/assets/82d55458-9072-481d-bf3c-71a349cb59a2" />
