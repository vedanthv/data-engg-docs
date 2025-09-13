# Streaming and Materialized Views in Databricks SQL

There is no auto option for incremental load while developing streaming tables and views in SQL, hence additional option has to be provided.

```sql
CREATE OR REFRESH STREAMING TABLE dev.bronze.orders_st
AS
SELECT * FROM 
STREAM read_files(
  "/Volumes/dev/bronze/landing/input/",
  format => 'csv',
  includeExistingFiles => false
)
```

```sql
CREATE OR REPLACE MATERIALIZED VIEW dev.bronze.ordes_mv 
-- SCHEDULE EVERY 4 HOURS
AS
SELECT Country,sum(UnitPrice) as agg_total_price FROM dev.bronze.orders_st 
group by Country
```

Replacing the materialized view does not refresh entire data, just incrementally. The group aggregate is also calculated incrementally.

```sql
CREATE OR REPLACE MATERIALIZED VIEW dev.bronze.ordes_mv 
-- SCHEDULE EVERY 4 HOURS
AS
SELECT Country,sum(UnitPrice) as agg_total_price FROM dev.bronze.orders_st 
group by Country
```

Every run of the query on Serverless Warehouse spins up DLT job in background.

<img width="1676" height="811" alt="image" src="https://github.com/user-attachments/assets/f2b79903-6945-4b29-912f-244741ae6664" />
