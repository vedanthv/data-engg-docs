## How to tune executors in Spark?

### Example of Sizing an Executor

![alt text](https://snipboard.io/JcrGLg.jpg)

We need to optimally decide how many executors to create, how much memory and cores must be allocated to the executor.

### Structure 

![alt text](https://snipboard.io/uPYdW3.jpg)

There are 5 nodes, each has 12 cores and 48 GB RAM.

We need to calculate number of cores and executors.

### Fat Executors

**Fat executors** are executors that have **very large memory and many cores assigned to each executor**, instead of spreading the resources across many smaller executors.

They are the opposite of “thin executors.”

---

# Definition

### Fat executors

Executors that have:

* high memory (20–64 GB or more)
* many CPU cores (8–32 cores)
* fewer total executors per node

Example:

```
1 executor per node
32 cores
64 GB RAM
```

This is a fat executor.

---

# Thin executors

Executors that have:

* small memory (4–8 GB)
* few cores (2–5 cores)
* many executors per node

Example:

```
4 executors per node
8 cores each
8 GB RAM each
```

---

# When do we use fat executors?

You use fat executors **only in specific situations**, mainly when your workload or library *demands* it.

---

# 1) When using Pandas UDFs, Python UDFs, PySpark heavy workloads

Python is single-threaded (GIL).
But each executor needs **more overhead**, **more worker memory**, and fewer processes.

If thin executors are used, Python overhead may kill them due to container limits.

Fat executors help because:

* fewer Python worker processes
* more memory for Arrow buffers
* less shuffle pressure

---

# 2) When handling extremely large broadcast variables

If your broadcast variable is 3–8 GB, thin executors (with 4–8GB heap) may OOM.

Fat executors allow:

* larger heap for broadcast
* fewer executor JVMs → lower duplication of broadcast

Remember: each executor gets one full copy of the broadcast variable.

---

# 3) When working with large in-memory datasets (caching heavy DataFrames)

If your job requires extensive caching:

* machine learning iterative algorithms
* graph processing (GraphX)
* window functions with wide datasets

Fat executors reduce spill and improve in-memory performance.

---

# 4) When using RDD-based, memory-intensive libraries

Libraries like:

* GraphX
* MLlib older algorithms
* iterative RDD transformations

These perform better with large heap sizes, hence fat executors.

---

# 5) When node hardware is extremely powerful

Some nodes come with:

* 32–64 cores
* 256–512GB RAM

In such cases:

* having many small executors increases JVM overhead and shuffle connections
* fat executors reduce management overhead and maximize single JVM performance

---

# When NOT to use fat executors (default case)

Most workloads work best with **thin executors**, because:

* tasks parallelize better with more executors
* GC times are shorter on smaller heaps
* scheduling is more flexible
* shuffle is more balanced

Thin executors follow the typical guideline:

```
4–5 cores per executor
8–16GB memory per executor
```

---

# Perfect interview one-liner

> Fat executors are executors with very high memory and many cores. They are used for Python-heavy jobs, large broadcasts, huge in-memory workloads, or when the cluster nodes themselves are very large. However, for most workloads thin executors perform better due to less GC pressure and better parallelism.

![alt text](https://snipboard.io/bg0dwe.jpg)

We leave out 1 GB,1 core for the OS/YARN/K8s deamons to run at node level.

Imagine each node is a building, we would have lifts, electricity rooms, DG backup facilities, wieing etc...

So for these to operate we would need some space and people, hence some resources are allocated for that.

## Thin Executors

![alt text](https://snipboard.io/OVRzly.jpg)

Thin executors are less heavy but are more in number.

### Advantages and Disadvantages of Fat Executors

![alt text](https://snipboard.io/YBvSpU.jpg)

HDFS Throughput drasticallly reduces because during garbage collection the entire executor needs to stop and there is lot of delay / latency.

### Advantages and Disadvantages of Thin Executors

![alt text](https://snipboard.io/TY4lNs.jpg)

For smaller and lightweight tasks we can use Thin Executors.

### Rules for sizing an optimal executor

![alt text](https://snipboard.io/lMg51n.jpg)

```
Node (Building)
│
├── OS & daemons (security guard, lift room)                <-- leave 1 core, 1–4GB for OS
│
├── Application Master (Project Manager's Office)           <-- leave 1 core, 1GB for AM
│
└── Executors (Workers)
      ├── Desk (heap)
      └── AC + space (memory overhead)
```

While the other deductions (like 1 core and 1 GB RAM for OS/YARN) are done per node, the Application Master itself runs at the cluster level. It manages the overall resource allocation for your entire Spark job across all nodes in the cluster. Therefore, the resources for the Application Master are deducted from the total available resources of the cluster, not from each individual node.

The video suggests subtracting 1 core and 1 GB of RAM for the Application Master at the cluster level because it's a small, fixed overhead that applies to the entire job, regardless of how many nodes or executors you have.

The "cluster" is defined as a group of five nodes (or machines).

![alt text](https://snipboard.io/l5IevP.jpg)

So the final spark submit command includes the following:

```
--num-executors 10
-- executor-cores 5
-- executor-memory 20gb
```

## How does size of data affect the processes?

We have total of 20GB for the executor and 5 cores, so its 4gb per core.

1 core can work on 1 partition so as long as the partition is within 4gb it can perform operations seamlessly.

