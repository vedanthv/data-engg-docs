## CTAS | Deep Clone | Shallow Clone

### Create Table As Select (CTAS)

```sql
CREATE TABLE dev.bronze.sales_ctas 
AS 
SELECT * FROM dev.bronze.sales_managed
```

A new physical location is created and data is now stored in that for the new table.

```sql
-- location is different from original table, the physical location is changed.
desc extended dev.bronze.sales_ctas
```

### Deep Clone

```sql
CREATE TABLE dev.bronze.sales_deep_clone DEEP CLONE dev.bronze.sales_managed;
select * from dev.bronze.sales_deep_clone;
desc extended dev.bronze.sales_deep_clone;
```

This copies both table data and metadata.

The data is created in new locaiton.

<img width="1089" height="419" alt="image" src="https://github.com/user-attachments/assets/00ebeae0-8170-461f-97fc-1a4478402db0" />

Both delta logs and data copied over

<img width="1556" height="265" alt="image" src="https://github.com/user-attachments/assets/008d68de-05f5-44f5-a971-1df0f15e46e8" />

We can see latest version of source from where data from table is copied.

<img width="1113" height="160" alt="image" src="https://github.com/user-attachments/assets/64ed3b77-c5e2-4cfc-9cae-75847e647d4b" />

### Shallow Clone

The table is created at a new location

<img width="1320" height="611" alt="image" src="https://github.com/user-attachments/assets/e6189f87-c8e4-426a-b1d1-d61796ed7a83" />

Only Delta Log copied over the physical data stored at original location.

<img width="1573" height="279" alt="image" src="https://github.com/user-attachments/assets/7bf88c13-f068-4e9c-b80e-0fcf0328b8af" />

### Inserting Data into original table and see if it reflects in Shallow Clone

```sql
select * from dev.bronze.sales_shallow_clone
```

<img width="1345" height="274" alt="image" src="https://github.com/user-attachments/assets/bf50349e-fd9b-48db-81db-ef8e28bc3ab0" />

Insert data into main table

<img width="1358" height="499" alt="image" src="https://github.com/user-attachments/assets/b5c72310-2212-4d2c-a3d0-c2d615c69ea8" />

Requery shallow clone

<img width="1368" height="411" alt="image" src="https://github.com/user-attachments/assets/98be94a4-7186-42f1-8bca-48a87e207a76" />

We can see only one row the 2nd row inserted is not visible.

Shallow Clone points to the source version of original table when created and does not update the data.

When we do the vice versa and insert new record in shallow table, it does not impact the original table. The new data is stored in the shallow table's own location.

Only when we VACUUM the main table, all records from shallow table also gets deleted.
