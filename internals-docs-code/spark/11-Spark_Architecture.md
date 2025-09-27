### Lecture 6 : Spark Architecture

#### Spark Cluster

![image](https://github.com/user-attachments/assets/58ee64d9-0105-453c-97a6-9888b804c98a)

- 20 core per machine and 100 GB RAM / each machine
- Total Cluster : 200 cores and 1TB RAM

![image](https://github.com/user-attachments/assets/aaaca550-af99-41ba-bbd3-158a83941819)

- The master is controlled by Resource Manager and the workers are controlled by Node Manager.

#### What happens when user submits code?
![image](https://github.com/user-attachments/assets/1cea605b-f750-406a-ae44-819bc06ccea3)

- The user submits some Spark code for execution to the Resource Manager. It needs 20 GB RAM, 25 GB executor, 5 total executors and 5 CPU cores.
- So the manager goes to W5 and asks to create 20GB container as the driver node.

#### What happens inside the container?

##### Driver Allocation

Now this 20 GB driver is called Application Master
![image](https://github.com/user-attachments/assets/a85199e1-0036-4e51-842a-39faab13adab)

There are two main() functions inside the master, one is for PySpark and other is for JVM like Java,Scala etc...

The JVM main() is called Application Driver.

The Spark Core has a Java Wrapper and the Java Wrapper has a Python Wrapper.

When we write code in PySpark it gets converted to Java Wrapper.

The PySpark driver is not a requirement but the Java Wrapper is required to run any code.

##### Worker Allocation

![image](https://github.com/user-attachments/assets/6fccdb87-a254-4bc2-9c50-38c9a9d26a02)

- Now the Application master asks for the executors to be assigned and the resource manager allocates.

#### Executor Container

![image](https://github.com/user-attachments/assets/1ee66178-03be-474c-8b02-ec1cc8f73a01)

Each executor has 5 core CPU and 25GB RAM. Each one of them runs on separate container.

THe above is when we have pure Java code and dont use Python UDF.

But what if we use Python UDF functions?

![image](https://github.com/user-attachments/assets/69057cb6-f0f7-40c5-86ab-ab06689bcd08)
We need a Python worker inside the executor to be able to run the code.