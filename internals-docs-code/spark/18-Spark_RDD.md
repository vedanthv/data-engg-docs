### Lecture 13: Resilient Distributed Dataset

![image](https://github.com/user-attachments/assets/9f092749-7050-4067-9b9f-4e19e3527a18)

#### Data Storage of List
![image](https://github.com/user-attachments/assets/023e8304-b40a-40a6-8f61-516efe301635)

#### Data Storage in RDD

Suppose we have 500MB of data and 128MB partition, so we will have 4 partitions.

The data is scattered on various executors.
![image](https://github.com/user-attachments/assets/4c99e784-5366-4ee4-b1ac-c7baa0a49f34)

Its not in single contiguous location like elements of a list. The data structure used ot process this data is called RDD
![image](https://github.com/user-attachments/assets/99aac217-5141-4c6b-bcbe-0873e7a9bbbd)

![image](https://github.com/user-attachments/assets/01a10422-cb78-42a3-bb95-db643950b621)

Why is RDD recoverable?

- RDD is immutable. If we apply multiple filters each dataset after filtering is a different dataset
![image](https://github.com/user-attachments/assets/ff872b52-f89f-406e-b8e1-30edd48624cf)

- In below case if rdd2 fails then we can restore rdd1 because of the lineage.
![image](https://github.com/user-attachments/assets/9497cf7a-7646-4dc1-ba2b-790e524572f5)

#### Disadvantage of RDD

- No optimization done by Spark on RDD. The dev must specify explicitly on how to optimize RDD.

#### Advantage

- Works well with unstructured data where there are no columns and rows / key-value pairs
- RDD is type safe, we get error on compile time rather than runtime which happens with Dataframe API.

#### Avoiding RDDs

![image](https://github.com/user-attachments/assets/7dcd2caa-fac8-478f-9ba2-e99370c3fb44)

- RDD : How to do? Dataframe API: Just specify what to do?

![image](https://github.com/user-attachments/assets/a028ab4e-b35e-4ead-9c04-a5cdbbf7f228)
You can see in above case that we have a join and filter but we are specifically saying that first join then filter so it triggers a shuffle first and then filter which is not beneficial.