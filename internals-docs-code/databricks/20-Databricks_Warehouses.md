## Databricks SQL Warehouses

### Types of SQL Warehouses

<img width="1539" height="717" alt="image" src="https://github.com/user-attachments/assets/4b048109-ea35-48c0-bcdb-356e9571c3e5" />

### Sample SQL Query and Monitoring

```sql
SELECT c.c_mktsegment,count(o.o_orderkey) total_orders
FROM
dev.etl.orders_bronze o
LEFT JOIN dev.etl.customer_scd2_bronze c
ON o.o_custkey = c.c_custkey
WHERE c.__END_AT is null
group by c.c_mktsegment
```

**Query Monitoring**

<img width="1659" height="756" alt="image" src="https://github.com/user-attachments/assets/f947afa5-15a0-4278-b55f-20f7943253d9" />
