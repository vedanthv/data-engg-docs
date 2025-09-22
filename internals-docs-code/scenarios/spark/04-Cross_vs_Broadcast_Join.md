## What is the difference between Cross Join and Broadcast Join?

At first glance, a Cartesian Product (a.k.a. Shuffle-and-Replication Nested Loop) join may look similar to a Broadcast Join since data ends up being available across executors. But there is a crucial difference:

In a Broadcast Join, the driver first collects the smaller dataset and then broadcasts a full copy of it to every executor. Each executor then joins its local partition of the larger dataset with this broadcasted copy, i.e. there is no shuffle step involved in this process!
In a Cartesian Product (Cross Join), the data is not broadcasted by the driver. Instead, Spark performs a shuffle-and-replication, where all partitions of both datasets are exchanged and replicated across executors, ensuring that every partition of one dataset is matched with every partition of the other.

👉 In short: Broadcast Join = driver-based broadcast of a small dataset without any shuffle vs. Cross Join = shuffle-driven replication of all partitions across executors.

<img width="1100" height="645" alt="image" src="https://github.com/user-attachments/assets/f8f25232-ff2f-454f-964c-4b3ecb7054e6" />
