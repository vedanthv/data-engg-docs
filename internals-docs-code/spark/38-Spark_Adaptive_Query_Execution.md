### Lecture 29: Adaptive Query Execution

#### Features of AQE

![image](https://github.com/user-attachments/assets/6d312c6b-2983-4ebc-a3fb-9fef5647bced)

##### Dynamically Coalescing Shuffle Partitions

Sugar is best selling product it has highest data in the partition.

![image](https://github.com/user-attachments/assets/6302df14-6abb-4f8e-ac1a-63aee3154957)

Now there is a GroupBy / Shuffling of data. All the Sugar data comes to one partition.

![image](https://github.com/user-attachments/assets/419528eb-2d4a-4a90-b302-436c9ace1277)

By default there are 200 partitions, but 195 are empty.

The resources are getting wasted because these 195 partitions also need to be shuffled.

The 5 partitions become 5 tasks but Partition 1 takes lot of time to run.

![image](https://github.com/user-attachments/assets/60d3d490-b566-4f3d-a8eb-22d2c530197e)

Now AQE coalesces the partitions.

![image](https://github.com/user-attachments/assets/0cee3eda-96db-44fd-a000-a31ef5273174)

Two tasks are now reduced and also 2 cores become free.

But even after coalescing we may end up with data skew.

![image](https://github.com/user-attachments/assets/bffc1b5f-8afd-4557-9cc3-2f8b260771b0)

![image](https://github.com/user-attachments/assets/8a18642b-4448-455a-9a55-8a545930ae30)

Once we coalesce we end up with 2 partitions and 1/2 completes fast, the one with sugar takes time.

#### Data Splitting 

![image](https://github.com/user-attachments/assets/49399787-322c-452e-9e91-17d650a8b84c)

If median is 5MB and one partition is > 25MB then the data splits.

#### Dynamically Switching Join Strategy

![image](https://github.com/user-attachments/assets/48da944e-f024-4e2c-b31a-d79015f0d356)

By default spark does sort merge join.

Now if we compress table2 to become 10mb, even though sort merge join DAG is built, if AQE is enabled, we can check runtime statistics.

![image](https://github.com/user-attachments/assets/77901eba-47b2-4eec-b199-68deee0b3b3a)

Since data is only 10MB we can broadcast the data but shuffling still happens only sorting and merging is avoided.

#### Dynamically Optimizing Skew Join

![image](https://github.com/user-attachments/assets/aae53785-bad9-4399-8094-ba636234f4c3)

We are considering two tables where key = Sugar and just 128MB of data.

Let's show other partitions also

![image](https://github.com/user-attachments/assets/6d1eca97-aa29-4534-838b-8d177b868ab9)

Now when we do the Sort Merge Join and get all keys together the Sugar partition size increases.

![image](https://github.com/user-attachments/assets/f56d8ded-a4cc-495a-8606-176bda358233)

All tasks except the one with Sugar completes fast.

![image](https://github.com/user-attachments/assets/535c4cf4-c3b9-4076-8241-9133d673721a)

This leads to OOM error.

##### Solutions

- Salting
- AQE

AQE has ShuffleReader, it has statistics on the memory and size of each partition. This parttion gets automatically split in both tables.

![image](https://github.com/user-attachments/assets/77e35131-03a6-4ad0-898f-b705f935d2e4)