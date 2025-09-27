### Lecture 9 : Transformations and Actions in Spark

![image](https://github.com/user-attachments/assets/347c73e6-2cdb-491b-85b8-a98797df7b5f)

#### Types of Transformations

- Narrow Transformation
- Wide Transformation

![image](https://github.com/user-attachments/assets/7fa407aa-fe59-4b90-a5f4-d1cb969e06e0)

Example:
![image](https://github.com/user-attachments/assets/c7b44c1b-5e48-4728-9a24-93fe42762bf0)

Suppose data is of 200MB. 200MB / 128MB = 2 partitions

![image](https://github.com/user-attachments/assets/0c74472a-ec82-4241-a236-2ed3c2e35ea2)

Let's say both partitions go to separate executors.

Q1 : Filtering Records
![image](https://github.com/user-attachments/assets/5bbf61d7-1116-4d0d-b860-f5410f12c1b8)
There is no data movement here.

Q2: Find Total Income of each employee
![image](https://github.com/user-attachments/assets/3524bd45-9d80-43d7-a134-2a43460fae5b)

One id = 2 record is in one partition and the other is in the second partition so we need to do wide transformation
![image](https://github.com/user-attachments/assets/060eb0d1-a8fc-44b5-843e-738ebd87e42e)

Data needs to be shuffled and records with same id must be moved to same partition.

- filter,select,union etc are narrow transformations
- join,groupby,distinct