### Lecture 19: Repartitioning and Coalesce

Suppose we have 5 partitions and one of them is skewed a lot 100MB, let's say this is the best selling product records. This partition takes lot of time to compute. So the other executors have to wait until this executor finishes processing.
![image](https://github.com/user-attachments/assets/2a5567b0-486c-4b8b-aa91-41d077281e91)

#### Repartitioning vs Coalesce

##### Repartitioning

Suppose we have the above partitions and total data is 100mb. let's say we do repartition(5) so we will have 5 partitions now for the data with 40mb per partition.

##### Coalesce

In case of coalesce there is no equal splitting of partition memory, rather the already existing partitions get merged together.
![image](https://github.com/user-attachments/assets/85f6803b-6905-49e4-b3b3-3a896cde668f)

There is no shuffling in coalesce but in repartitioning there is shuffling of data.

#### Pros and Cons in repartitioning

- There is evenly distributed data.
- Con is that IO operations are more, its expensive.
- Con of coalesce is that the data is unevenly distributed.

Repartitioning can increase or decrease the partitions but coalescing can only decrease the partitions.

#### How to get number of partitions?

```flight_df.rdd.getNumPartitions()``` gets the initial number of partitions and then we can repartition ```flight_df.repartition(4)```. Data is evenly distributed.

![image](https://github.com/user-attachments/assets/00bd0cfe-e61a-4826-b978-b6c02924a363)

**Repartitioning based on columns**

![image](https://github.com/user-attachments/assets/9d39f248-2be8-4520-a57a-4084bcfc297f)

Since we asked for 300 partitions and we have 255 records some partitions will have null record.
![image](https://github.com/user-attachments/assets/c59615d8-65c1-44e8-85c4-3e1833a4cb60)

#### Coalescing

![image](https://github.com/user-attachments/assets/210eb04d-80b3-4cce-a7dd-1b7757b3bd1c)
Suppose we have 8 partitions and we coalesce into 3 partitions. Coalesce has only one arg.

Uneven distribution of data in partitions.
![image](https://github.com/user-attachments/assets/bc136007-2ae3-4df1-90b4-625352a81809)