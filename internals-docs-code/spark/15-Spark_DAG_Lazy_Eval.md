### Lecture 10 : DAG and Lazy Evaluation in Spark

![image](https://github.com/user-attachments/assets/b323161d-5dcf-4a01-ad70-05b11c4e811f)

- For every action there is a new job, here there are three actions : read,inferSchema,sum and show
- When used with groupBy().sum(): It is considered an action because it triggers computation to aggregate data across partitions and produce a result. This operation forces Spark to execute the transformations leading up to it, effectively creating a job.
- When used as a column expression df.select(sum("value")): It acts more like a transformation in Spark's context, especially if part of a larger query or pipeline that does not immediately trigger execution. In this case, it only defines the operation and does not create a job until an action (like show() or collect()) is called.

1. Job for reading file
![image](https://github.com/user-attachments/assets/c568a81e-dfa8-4637-bf22-637605286140)
Whole Stage Codegen - generate Java ByteCode

2. Inferschema
![image](https://github.com/user-attachments/assets/c79751a7-ea04-444a-8940-61eb0d144a5f)

3. GroupBy and Count
As explained above this is an action.

4. Show
Final action to display df

![image](https://github.com/user-attachments/assets/925397f9-c1e6-4662-ba01-a52d8bcc04ab)
After we read the csv and inferSchema there are no jobs created since filter and repartition both are transformations not actions.

When there are two filters on same dataset

![image](https://github.com/user-attachments/assets/a05bb675-508b-42bb-8128-f38a5e0d21fa)

This is the job
![image](https://github.com/user-attachments/assets/272cea9a-7570-4716-b831-1883472cc4be)

##### Optimizations on the Filter
Both the filters are on the same task
![image](https://github.com/user-attachments/assets/2682b8b3-3f31-4d5e-ba6a-b2ea32ea2246)
The optimizations can be applied because Spark is lazily evaluated.