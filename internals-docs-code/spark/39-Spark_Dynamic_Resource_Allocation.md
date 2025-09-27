### Lecture 31 : Dynamic Resource Allocation

![image](https://github.com/user-attachments/assets/bc67607d-ac0c-4c7d-8198-b3be42d4aa59)

#### Cluster Configuration

![image](https://github.com/user-attachments/assets/d0283700-c961-4c84-b7e8-99186341e2bf)

There is no problem with above configuration.

But let's say another user comes and asks for more resources...

![image](https://github.com/user-attachments/assets/b95ac3f3-fece-4475-8f9e-af22ec6eae01)

The red person can't get assigned any more memory since cluster is already full.

The resource manager works on FIFO process.

Now this small process that needs only 25GB may have to wait for hours.

![image](https://github.com/user-attachments/assets/31eff3b8-5804-4833-ba2d-44fbe173952a)

In dynamic memory allocation, the data that is not used is released.

Resource Manager has no role, spark internal algo does this.

![image](https://github.com/user-attachments/assets/052cdcb7-9b36-442c-b2b9-5e07d152707e)

Let's say we have free 750GB and driver demands 500GB from resource manager but there might be other processes waiting for the memory so it may not get it.

We can use min executors and max executors to get around this. We set min executors in such a way that process does not fail.

Now let's say there is a process which has completed execution and so Dynamic Resource Allocator frees the data. But we want it for further calculations. Do we calculate it again? No.

We can use **External Shuffle Service**. This works independently on every worker node and data in this doesnt get deleted.

![image](https://github.com/user-attachments/assets/c3e41033-dc01-4925-87df-05417b63786f)

If executors idle from 60s then we release the data.

#### How does executor ask for resources?

If the executor does not get its required memory within 1 sec then it starts asking in two fold manner.

![image](https://github.com/user-attachments/assets/37d347d0-0db3-479c-92e2-bc08e600062b)

First it asks for 1GB then 2GB then 4GB and so on...

```spark.scheduler.backlogTimeout``` = 2s the executor waits till 2s before asking for memory.

#### Parallel Execution and Multi Threading

![image](https://github.com/user-attachments/assets/51543a7e-2c23-467f-bcbd-f2d9383ba20a)

#### When to avoid dynamic resource allocation?

For critical jobs that needs to be run within certain SLA avoid it.