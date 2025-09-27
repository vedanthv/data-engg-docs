### Lecture 4 : Spark Ecosystem

![image](https://github.com/user-attachments/assets/1790b682-10ba-4c47-8594-d743fbe54650)

High Level API : We cna write any SQL queries in python,java etc... there are ML and GraphX librries also.

We can write code in many languages. Low Level API : we can make RDD's and work on them.

![image](https://github.com/user-attachments/assets/452c4dc0-20d7-45e3-89f6-fb53719f75b9)

#### Where does Spark run?

![image](https://github.com/user-attachments/assets/d2c11530-6dc3-485e-98c7-10e7bafac25b)

Spark Engine would need some memory for transformation.

- suppose it needs 4 worker nodes each 20 GB and a driver node of 20 gb.
- it goes to the cluster manager and asks for total 100 GB of memory, if available then the manager will assign that muuch storage.
- cluster manager is also called YARN, K8S, Standalone managers