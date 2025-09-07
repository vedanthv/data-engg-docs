## Delta Live Tables Code Walkthrough

1. Create Streaming Table for Orders

```python
@dlt.table(
  table_properties = {"quality":"bronze"},
  comment = "Orders Bronze Table"
)
def orders_bronze():
  df = spark.readStream.table("dev.bronze.orders_raw")
  return df
```

2. Create Materialized View for Customers

```python
@dlt.table(
  table_properties = {"quality":"bronze"},
  comment = "Customers Materialized View"
)
def customers_bronze():
  df = spark.read.table("dev.bronze.customers_raw")
  return df
```

3. Create a view that joins above streaming table and materialized view

```python
@dlt.view(
  comment = 'Joined View'
)
def joined_vw():
  df_c = spark.read.table("LIVE.customers_bronze")
  df_o = spark.read.table("LIVE.orders_bronze")

  df_join = df_o.join(df_c,how = "left_outer",on = df_c.c_custkey==df_o.o_custkey)

  return df_join  
```

4. Add a new column to the view

```python
@dlt.table(
  table_properties = {"quality":"silver"},
  comment = "joined table",
  name = 'joined_silver'
)
def joined_silver():
  df = spark.read.table("LIVE.joined_vw").withColumn("_insertdate",current_timestamp())
  return df
```

5. Create gold level aggregation

```python
@dlt.table(
  table_properties = {"quality":"gold"},
  comment = "orders aggregated table",
)
def joined_silver():
  df = spark.read.table("LIVE.joined_silver")

  df_final = df.groupBy('c_mktsegment').agg(count('o_orderkey').alias('sum_orders').withColumn('_insertdate',current_timestamp()))
  return df_final
```

<img width="960" height="185" alt="image" src="https://github.com/user-attachments/assets/b7ef8b2d-499e-4e3f-a1ef-414da15c6871" />

### Deleting DLT Pipeline

The tables / datasets in DLT are managed and linked to DLT pipelines. So if we delete a pipleine all fo them get dropped.

### Incremental Load in DLT

When we inserted 10k records into orders_bronze, only those got ingested not the entire table.

<img width="1077" height="282" alt="image" src="https://github.com/user-attachments/assets/bf98534a-12ae-4b33-9d54-06b94de34abc" />

### Adding New Column

```python
@dlt.table(
  table_properties = {"quality":"gold"},
  comment = "orders aggregated table",
)
def joined_silver():
  df = spark.read.table("LIVE.joined_silver")

  df_final = df.groupBy('c_mktsegment').agg(count('o_orderkey').alias('sum_orders').agg(sum('o_totalprice').alias('sum_price').withColumn('_insertdate',current_timestamp()))
  return df_final
```

We dont have to manipulate ddl, the dlt pipeline will auto detect addition of new column.

### Renaming Tables

We just change the name of the function in the table declaration and the table name will be renamed. The catalog will also reflect this.

### DLT Internals

Every streaming table, MV is supported by underlying tables in ```_databricks_internal``` schema.

<img width="384" height="162" alt="image" src="https://github.com/user-attachments/assets/97490445-99ec-4afb-b2bf-8b27ba785c7d" />

and they have a table_id associated with it.

If we go to these tables in storage account, we can see checkpoints that keep track of incremental data changes.

<img width="1084" height="339" alt="image" src="https://github.com/user-attachments/assets/4d9fe83a-f523-4769-b28d-235b279070c9" />

### Data Lineage

<img width="969" height="432" alt="image" src="https://github.com/user-attachments/assets/b1eaa4ae-7ad2-46f6-8c7e-052536ceb9fa" />

### DLT Append Flow and Autoloader

```python
@dlt.table(
  table_properties = {"quality":"bronze"},
  comment = "orders autoloader",
  name = "orders_autoloader_bronze"
)
def func():
  df = (
      spark.readStream
      .format("cloudFiles")
      .option("cloudFilesFormat","CSV")
      .option("cloudFiles.schemaLocation","...")
      .option("pathGlobFilter","*.csv")
      .option("cloudFiles.schemaEvolutionMode","none")
      .load("/Volumes/etl/landing/files"
)
return df
```

```python
dlt.createStreamingTable("order_union_bronze")

@dlt.append_flow(
  target = "orders_union_bronze"
)
def order_delta_append():
  df = spark.readStream.table("LIVE.orders_bronze")
  return df

@dlt.append_flow(
  target = "orders_union_bronze"
)
def order_autoloader_append():
  df = spark.readStream.table("LIVE.orders_autoloader_bronze")
  return df
```

```python
@dlt.view(
  comment = 'Joined View'
)
def joined_vw():
  df_c = spark.read.table("LIVE.customers_bronze")
  df_o = spark.read.table("LIVE.orders_union_bronze")

  df_join = df_o.join(df_c,how = "left_outer",on = df_c.c_custkey==df_o.o_custkey)

  return df_join  
```

<img width="854" height="247" alt="image" src="https://github.com/user-attachments/assets/4a7b209b-6920-4123-823d-61db5a1055df" />

### Custom Configuration

<img width="796" height="137" alt="image" src="https://github.com/user-attachments/assets/04ae9b25-f370-4fa9-abd6-9e8864a3fbf9" />

Use this param in code

```python
_order_status = spark.conf.get("custom.orderStatus","_NA")
```

```python
for _status in _order_status.split(","):
    # create gold table
    @dlt.table(
        table_properties = {"quality":"gold"},
        comment = "order aggregated table",
        name = f"orders_agg_{_status}_gold"
    )
    def orders_aggregated_gold():
        df = spark.read.table("LIVE.joined_silver")
        df_final = df.where(f"o_orderstatus = '{_status}'").groupBy("c_mktsegment").agg(count('o_orderkey').alias("count_of_orders"),sum("o_totalprice").alias('sum_totalprice')).withColumn("_insert_date", current_timestamp())

        return df_final
```

<img width="819" height="279" alt="image" src="https://github.com/user-attachments/assets/ea50584f-8c08-49fa-b42c-f74dbb700486" />

### DLT SCD1 and SCD2

**Pre Requisites**

<img width="760" height="312" alt="image" src="https://github.com/user-attachments/assets/f5bd0301-6538-46e9-8bd3-3baf8fb7d643" />

Input Source Table

```python
@dlt.view(
  comment = "Customer Bronze streaming view"
)
def customer_bronze():
  df = spark.readStream.table("dev.bronze.customers_raw")
  return df
```

**SCD Type1 Table**

```python
dlt.create_streaming_table('customer_sdc1_bronze')

dlt.apply_changes(
  target = "customer_scd1_bronze",
  source = "customer_bronze_vw",
  keys = ['c_custkey'],
  stored_as_scd_type = 1,
  apply_as_deletes = expr("__src_action = 'D'"),
  apply_as_truncates = expr("__src_action = 'T'"),
  sequence_by = "__src_insert_dt"
)
```

**SCD Type 2 Table**

```python
dlt.create_streaming_table('customer_sdc2_bronze')

dlt.apply_changes(
  target = "customer_scd1_bronze",
  source = "customer_bronze_vw",
  keys = ['c_custkey'],
  stored_as_scd_type = 2,
  except_column_list = ['__src_action','__src_insert_dt']
  sequence_by = "__src_insert_dt"
)
```

Changes in view to make SCD2 applicable

```python
@dlt.view(
  comment = 'Joined View'
)
def joined_vw():
  df_c = spark.read.table("LIVE.customers_scd2_bronze").where("__END_AT is null")
  df_o = spark.read.table("LIVE.orders_union_bronze")

  df_join = df_o.join(df_c,how = "left_outer",on = df_c.c_custkey==df_o.o_custkey)

  return df_join  
```

<img width="521" height="504" alt="image" src="https://github.com/user-attachments/assets/081c237f-d603-4388-a308-28d65236e90d" />

After inserting record with update the ```__END_AT``` for the new update is null signifying its the latest update

<img width="1354" height="433" alt="image" src="https://github.com/user-attachments/assets/4c2a71ae-d31d-4022-857a-cc26e76836fe" />

In SCD Type1 just the update is captured.

<img width="1372" height="455" alt="image" src="https://github.com/user-attachments/assets/b2441097-b38f-4084-aba2-3dde938275d6" />

### Insert Old Timestamp record

<img width="1039" height="571" alt="image" src="https://github.com/user-attachments/assets/afa79129-7c78-4624-8546-8bad61511f19" />

### SCD Type1 vs SCD Type2 Delete Records

<img width="1101" height="340" alt="image" src="https://github.com/user-attachments/assets/535c9268-243f-4363-83db-0a5c7a171fd4" />

<img width="1113" height="326" alt="image" src="https://github.com/user-attachments/assets/7e508692-86ec-428c-a2c5-765015d779d0" />
