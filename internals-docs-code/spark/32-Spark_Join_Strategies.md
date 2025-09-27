### Lecture 26 : Join Strategies in Spark

![image](https://github.com/user-attachments/assets/45d79335-9f31-43d8-9a04-93d48ec3a918)

Joins are expensive due to shuffling.

4 partitions are there in each dataframe.

![image](https://github.com/user-attachments/assets/cae9e337-7d63-4134-8df1-964847c351e4)

Executors in the cluster

![image](https://github.com/user-attachments/assets/267e6dd1-b981-441d-a2dd-693e2e013c7d)

Now we need to join employee and salary df to get the output but they are on different executors, so we need to do data shuffling.

Each executor has 200 partitions. Goal is to get all same keys in one executor.
![image](https://github.com/user-attachments/assets/80daa55e-8dce-4e3e-839d-8f6b2b2bee16)

![image](https://github.com/user-attachments/assets/e37dd852-daa4-4f1c-be91-83d01451cb57)

![image](https://github.com/user-attachments/assets/9266d9fb-9dee-486a-9e38-ffcd00658fcf)

- Since we want to get id for 1 we divide 1/200 = 1 and then send all the data to that executor 1.

![image](https://github.com/user-attachments/assets/69e73f9b-f7af-461e-8ac9-65f2d279a1c3)

Suppose we want to map the salary for id = 7 so the data from the employee df with id = 7 and also salary df with id=7 will come into the executor 7.

Similarly id = 201 will go into 201/200 = executor no 1.

#### Types of Join Strategies

![image](https://github.com/user-attachments/assets/58ea7594-9378-4fd6-b0f7-a16b77c88d4c)

![image](https://github.com/user-attachments/assets/9d1c2231-bc9a-41e2-8cbf-3137570acfe0)

Joins generally result in shuffling

There are two dataframes df1 and df2 each with 4 partitions.

![image](https://github.com/user-attachments/assets/fde4638b-d6a4-46d1-926b-fd7f20cabf2d)

We have two executors.

In join goal is to join with same keys.

![image](https://github.com/user-attachments/assets/12274ff6-b7a6-4e32-8cca-7d4409b5dd75)

We can see that red P1 has corresponding id for salary in the other executor.

![image](https://github.com/user-attachments/assets/6339f3f0-2e8e-4e48-aa22-69ce46a2ac5c)

We need to get same keys fetched from other executors.

When a dataframe is sent to executors by default 200 partitions are created per dataframe.

![image](https://github.com/user-attachments/assets/8465bc0e-5f80-4c19-8697-14f03e889c9f)

Now let's say we want to find salary for id = 1 we can divide 1/200 on blue = 1 and 1/200 on red = 1, so both data will come into executor 1 in the partition 1.

![image](https://github.com/user-attachments/assets/574fd6aa-aa86-49ab-a23c-28fa37c2f351)

Similarly for id = 7 also we will send the data on blue and red P7

But if id = 201 then 201/200 = 1 so this id will come into P1 only.

If we have id = 102 then 102/200 = 102 partition on 2nd executor.

![image](https://github.com/user-attachments/assets/d4e6056c-bb9f-4c9c-8e78-c19b3684e536)

The executors can be on different worker nodes also, we need to then move data across from one worker node to other.

### Strategies

![image](https://github.com/user-attachments/assets/22526c97-ddd0-4088-aefa-fbb29a599efb)

Broadcast nested loop join is costly because we dont do a straight join, rather its based on < an > conditions, its O(n^2)

#### Shuffle Sort Merge Join

![image](https://github.com/user-attachments/assets/3fb09974-e5a1-400c-9871-f0e748e65216)

TC : O(nlogn)

#### Shuffle Hash Join

The smaller table gets a hash table created with hashed keys in memory.

Now from df1 we checked which keys match with O(1) lookup using the hash table.

![image](https://github.com/user-attachments/assets/e2a95ff0-5c94-4871-830d-585cc23c868b)

### Broadcast Join

![image](https://github.com/user-attachments/assets/96982a15-f0dd-4b08-97ca-663ed9d63459)

The tables that are less than 100mb can be broadcast.

Scenario : Suppose one table is 1GB size so we will have 1000MB / 128MB = 8 partitions and there is another table of size 5mb.

So if we dont broadcast, then the df with 100gb should be shuffled around with 5mb data across executors for joining. Instead of that we will just send the small df in all the executors so that there is no shuffling.

![image](https://github.com/user-attachments/assets/20369a8d-d88f-42fb-8c33-3372c78d74ac)

The amount of data that can be broadcast depends on the memory of executor and driver. Make sure that there is no case where driver memory is 2GB and we are trying to broadcast 1GB data.

#### Demo

There are total 200 partitions when we join 

![image](https://github.com/user-attachments/assets/a426fb92-a489-4532-8184-56ffad0c77a6)

**Normal Sort Merge Join Execution Plan**

```
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- == Initial Plan ==
   Project [sale_id#10484L, sale_date#10485, amount#10486L, country_name#10514]
   +- SortMergeJoin [country_id#10487L], [country_id#10513L], Inner
      :- ColumnarToRow
      :  +- PhotonResultStage
      :     +- PhotonSort [country_id#10487L ASC NULLS FIRST]
      :        +- PhotonShuffleExchangeSource
      :           +- PhotonShuffleMapStage
      :              +- PhotonShuffleExchangeSink hashpartitioning(country_id#10487L, 1024)
      :                 +- PhotonFilter isnotnull(country_id#10487L)
      :                    +- PhotonRowToColumnar
      :                       +- LocalTableScan [sale_id#10484L, sale_date#10485, amount#10486L, country_id#10487L]
      +- ColumnarToRow
         +- PhotonResultStage
            +- PhotonSort [country_id#10513L ASC NULLS FIRST]
               +- PhotonShuffleExchangeSource
                  +- PhotonShuffleMapStage
                     +- PhotonShuffleExchangeSink hashpartitioning(country_id#10513L, 1024)
                        +- PhotonFilter isnotnull(country_id#10513L)
                           +- PhotonRowToColumnar
                              +- LocalTableScan [country_id#10513L, country_name#10514]

== Photon Explanation ==
Photon does not fully support the query because:
		Unsupported node: SortMergeJoin [country_id#10487L], [country_id#10513L], Inner.

Reference node:
	SortMergeJoin [country_id#10487L], [country_id#10513L], Inner
```

**Spark UI Diagram**

![image](https://github.com/user-attachments/assets/e2f11398-cd8e-4020-8487-32d3d5bce576)

![image](https://github.com/user-attachments/assets/5a0406e0-6f35-4f57-8f3d-93dd3623bc31)

**Broadcast Join Execution Plan**

```
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- == Initial Plan ==
   ColumnarToRow
   +- PhotonResultStage
      +- PhotonProject [sale_id#10484L, sale_date#10485, amount#10486L, country_name#10514]
         +- PhotonBroadcastHashJoin [country_id#10487L], [country_id#10513L], Inner, BuildRight, false, true
            :- PhotonFilter isnotnull(country_id#10487L)
            :  +- PhotonRowToColumnar
            :     +- LocalTableScan [sale_id#10484L, sale_date#10485, amount#10486L, country_id#10487L]
            +- PhotonShuffleExchangeSource
               +- PhotonShuffleMapStage
                  +- PhotonShuffleExchangeSink SinglePartition
                     +- PhotonFilter isnotnull(country_id#10513L)
                        +- PhotonRowToColumnar
                           +- LocalTableScan [country_id#10513L, country_name#10514]

== Photon Explanation ==
The query is fully supported by Photon.
```

![image](https://github.com/user-attachments/assets/116ece89-7dbc-43f2-9477-ceea6fe3238f)