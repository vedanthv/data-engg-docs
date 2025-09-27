### Lecture 12: Spark SQL Engine

![image](https://github.com/user-attachments/assets/ffb137d5-5a71-427d-b411-1493925ed6a4)

#### How is code converted into Byte Code?

<img width="1036" height="423" alt="image" src="https://github.com/user-attachments/assets/208cf61e-6d22-4ad0-af86-eb27433b7c15" />

#### How is Spark Code compiled?

- The catalyst optimizer creates a plan and creates RDD lineage

#### Phases in Catalyst Optimizer

![image](https://github.com/user-attachments/assets/4dcb1108-768c-4c28-aa21-732e93fda646)

##### Workflow Diagram

- Unresolved Logical Plan : Bunch of crude steps to execute the SQL code
- Catalog : The table, files and database metadata information si stored in the catalog. Suppose we call read.csv on file that doesnt exist. The procedure that gives / throws the error is assisted via the catalog. In Analysis phase, we go through these steps. If some file/table is not found then we get **Analysis Exception** This error occurs when the Logical plan provided is not able to be resolved.
- Reoslved Logical Plan : This is the phase when we finished analysing the catalog objects.
- Logical Optimization: There are many examples. Suppose we need just two columns in select output, the spark engine does not fetch all the columns rather jsut fetches the two columns from memory that we need. Another example is when we use multiple filters on the same column in different lines of code. When we execute this code, we see that all of it is executed with **or** statements in one single line of code.
- Physical Plan: This involves taking decision like the type of join to use: Broadcast Join is one example. From the logical plan, we can build multiple physical plans.
Thebest Physical Plan is a set of RDDs to be run on different executors on the cluster.

![image](https://github.com/user-attachments/assets/7931f705-5d53-45d0-8bdc-407e2b3426a7)
