### Lecture 22 : Aggregate functions

#### Count as both Action and Transformation

![image](https://github.com/user-attachments/assets/d2cd9647-fc8a-4247-b04e-539a48331f76)

⚠️ When we are doing count on a single column and there is a null in it, its not considered in the count. But for all columns we have nulls in the count.
![image](https://github.com/user-attachments/assets/1ae8b278-3675-439c-9b12-8853064c9f3a)

<img width="887" height="510" alt="image" src="https://github.com/user-attachments/assets/63d7afe9-10ab-4392-8f1a-5fc87eb50eaa" />

Above case when we do ```df.count()``` the rows that have all duplicates are counted and we get 10 records but when we do ```df.select('name').count()``` then we get 8 because there are two nulls in name column.


Job created in first case and its not created in second case below.
![image](https://github.com/user-attachments/assets/8a771986-85e2-465d-a2c4-d4a2bd86dfca)