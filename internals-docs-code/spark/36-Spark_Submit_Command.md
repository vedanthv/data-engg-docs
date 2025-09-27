### Lecture 27: Spark Submit

![image](https://github.com/user-attachments/assets/8e499b3f-7e55-420e-a94b-c5099948ff18)

Spark submit is a command line tool to run spark applications, it packages the spark code and runs on cluster.

The spark cluster can be standalone,local,K8s or YARN.

#### Spark Submit Command

![image](https://github.com/user-attachments/assets/d1074716-4dc8-4469-b126-1bfc949dc58d)

![image](https://github.com/user-attachments/assets/0cb56a47-03c2-4068-b6b8-69f97237225b)

![image](https://github.com/user-attachments/assets/e269e312-fcab-4f07-9a5b-2202ce1e785b)

Master can run on ```yarn```,```local``` or ```k8s```

```deploy-mode``` -> specifies where driver runs

```--class``` -> not required for python, just scala or java

```--jars``` -> my sql connector jar files

```spark.dynamicAllocation.enabled``` -> free's up some memory if we are not using it

![image](https://github.com/user-attachments/assets/a19795ba-4d5e-4012-90f8-db8d58a2a2e3)

We provide two arguments to ```main.py``` file. 

![image](https://github.com/user-attachments/assets/5c42be36-179e-44d4-a215-41e059c127ca)

We can provide syntax to generate log file.
![image](https://github.com/user-attachments/assets/9e162712-9fc4-42a9-a7e1-40a8da4d69c6)

The local system computer from where we run the command is called edge node.