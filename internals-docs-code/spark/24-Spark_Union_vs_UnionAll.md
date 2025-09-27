### Lecture 19: union vs unionAll()

![image](https://github.com/user-attachments/assets/3e649ae8-6b69-4fa9-b687-109e4ede5615)

We can see that here we have a duplicate id
![image](https://github.com/user-attachments/assets/3680c897-59c2-4f04-963d-3ce99981f3b4)

In PySpark union and unionAll behaves in the same way, both retain duplicates
![image](https://github.com/user-attachments/assets/041e31d1-017f-45f7-aa7e-3c7db513d617)

But in Spark SQL when we do union it drops the duplicate records
![image](https://github.com/user-attachments/assets/05af5b19-9963-4581-a71d-77fe42f739cf)

![image](https://github.com/user-attachments/assets/00fde583-6538-4cc3-b275-97d8c5d620b2)

#### Selecting data and unioning the same table

![image](https://github.com/user-attachments/assets/f9226608-4b77-40db-91e1-82072e8cd14b)

#### What happens when we change the order of the columns?

```wrong_manager_df``` actually has the wrong order of columns but still we get the union output but in a wrong column values.
![image](https://github.com/user-attachments/assets/3db3d2c8-3008-4930-b223-6f7bb31da477)

If we give different number of columns an exception is thrown.
![image](https://github.com/user-attachments/assets/ece32bd0-6ea3-45f1-8919-721ef783c65b)

If we use unionByName then the column names on both dfs must be the same.
![image](https://github.com/user-attachments/assets/fd3659ae-703f-42bc-bd4a-49c9c427cd9e)