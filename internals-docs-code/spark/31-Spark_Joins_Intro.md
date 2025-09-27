### Lecture 24 : Joins in Spark part 1

![image](https://github.com/user-attachments/assets/442da83f-1447-4834-ba6b-6195fb5e775c)

Which customers joined platform but never brought anything?

![image](https://github.com/user-attachments/assets/9d0f578f-a02a-4da1-b8c4-3d88767b5fb7)

Whenever we need information from another table, we use joins and there should be some common column.

Join is a costly wide dependency operation.

#### How do joins work?

How many records do we get after inner joining the below two tables.
![image](https://github.com/user-attachments/assets/6e83fe11-578b-4590-9a89-43c98ca482a8)

We get a total of 9 records.
![image](https://github.com/user-attachments/assets/d706afb9-74bf-4c99-bceb-ed9327a2357d)

Sometimes data gets duplicated when we do joins, so we should use distinct() but remember distinct is wide dependency transform.

### Lecture 25 : Types of Join in Spark

![image](https://github.com/user-attachments/assets/e5e441c3-c64d-40ed-8646-89afcecc0be1)

#### Inner Join
![image](https://github.com/user-attachments/assets/641aa365-9493-46ff-9cb3-518805fda892)

#### Left Join
![image](https://github.com/user-attachments/assets/295cadda-2a97-41bb-a02d-997dfafd3a5b)
All records in left table + those that join with right table, whereever we dont get match on right table the columns become null.

#### Right Join
![image](https://github.com/user-attachments/assets/0e0c88d6-a290-42a7-901c-eae316262a44)

#### Full Outer Join
![image](https://github.com/user-attachments/assets/b49eb89d-829a-44f5-a30a-4ab08a89a289)

#### Left Semi Join 
![image](https://github.com/user-attachments/assets/acf7fb6a-d939-4b80-9bb7-7b411e43ac2e)

![image](https://github.com/user-attachments/assets/fc790260-df75-470a-8c91-795095ce72b2)

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("LeftSemiJoinExample").getOrCreate()

# Left DataFrame: Orders
orders = spark.createDataFrame([
    (1, "iPhone"),
    (2, "Pixel"),
    (3, "OnePlus"),
    (4, "Nokia")
], ["customer_id", "product"])

# Right DataFrame: Valid Customers
valid_customers = spark.createDataFrame([
    (1,), (3,)
], ["customer_id"])

# Perform left semi join
filtered_orders = orders.join(valid_customers, on="customer_id", how="left_semi")
filtered_orders.show()
```

**Output**

```
+-----------+--------+
|customer_id|product |
+-----------+--------+
|          1|iPhone  |
|          3|OnePlus |
+-----------+--------+
```

#### Left Anti Join

![image](https://github.com/user-attachments/assets/108e662c-63c8-4115-8181-928f66a0665c)

Find out all customers who have never purchased any product.

#### Cross Join

Never use cross join!
![image](https://github.com/user-attachments/assets/4d9b51bd-9a07-476c-a53c-3166bceec0b8)

![image](https://github.com/user-attachments/assets/10038361-8d23-4adb-9b1c-23095ae05aab)