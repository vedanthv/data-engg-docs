### Lecture 28 : Deployment Modes in Spark

![image](https://github.com/user-attachments/assets/96b5edab-c2fe-4d71-898a-58193e94ff0f)

Below is the normal Spark Architecture

![image](https://github.com/user-attachments/assets/4360bf36-7807-4c69-9a9d-5adc87df9f3d)

Here we have a separate EC2 instance called edge node. Its configuration is not as much as the other nodes.

![image](https://github.com/user-attachments/assets/6a9e92f6-ac2e-4dbb-b6f9-d7f2df99e2cc)

User does not connect directly to the cluster rather connects to the edge node now.

They can login to the edge node and perform tasks. Kerberos is used for Authentication and Authorization.

Any data that needs to be submitted to cluster also goes through edge node.

The /bin/spark-submit folder is on the edge node, it contains hadoop client libaries YARN is not installed here.

![image](https://github.com/user-attachments/assets/6ed26628-b3c2-41fd-8d70-cd1b0c515cab)

#### client mode deployment

![image](https://github.com/user-attachments/assets/8a127c39-ec56-4d10-b751-8cb8598305f9)

Driver is made on the edge node.

#### cluster mode

![image](https://github.com/user-attachments/assets/64afeed7-0803-46b5-b748-6dd0ff9d5305)

In cluster mode, the driver is created on the cluster.

#### pros and cons of client mode

Pro : 

- The user can see the cluster logs on their own system.
  
Con : 

- Once the driver in the local system shuts down, the executors also go down.
- When we submit on client mode we will have network latency. Two way communication creates lot of delay.
  
![image](https://github.com/user-attachments/assets/0c4adda6-86ad-4b60-9deb-b14b0f6b2012)

In cluster mode, we are given an application id and using that we can see the spark ui details.

![image](https://github.com/user-attachments/assets/bbb7665c-960c-4b3c-bfd2-eaecab4611be)