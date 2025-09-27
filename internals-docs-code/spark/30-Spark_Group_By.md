### Lecture 23: Group By In Spark

Sample Data

![image](https://github.com/user-attachments/assets/17c9a1dd-b003-4c67-8b1f-3f4e8fb6a556)

#### Questions

![image](https://github.com/user-attachments/assets/60d2d30b-c2c9-4e3f-9544-b8ab7eece55c)

Salary per department using groupBy()
![image](https://github.com/user-attachments/assets/b90a254d-1aac-46f1-8e2e-c66e8d99c0ad)

#### Where do we use window functions?

Suppose we need to find out the percentage of total salary from a particular dept that the person is earning. we can use window function to specify the total salary per department in the particular record itself like I've shown below.
![image](https://github.com/user-attachments/assets/6c328d14-bf1e-4059-83d5-618f6c7a0ec0)

This way we dont need to perform a join.

![image](https://github.com/user-attachments/assets/c6ababa6-3031-4147-887e-1b0b80a7fc13)

#### Grouping by two columns

![image](https://github.com/user-attachments/assets/0822535b-c50a-433a-bd1e-67b9ee6b9dcc)