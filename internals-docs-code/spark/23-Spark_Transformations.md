### Lecture 17: Dataframe Transformations in Spark Part 1

![image](https://github.com/user-attachments/assets/b3c9d9a3-b664-4cde-868f-d8d9c508ed9f)
Data gets stored in Row() format in the form of bytes

![image](https://github.com/user-attachments/assets/fccd78ab-d343-41dd-9a48-77122a4447d9)

Columns are expressions. Expressions are set of transformations on more than one value in a record.

#### Ways to select values / columns

![image](https://github.com/user-attachments/assets/3bb9ee25-d1d2-42e9-bb8b-22cb7c1030d3)

![image](https://github.com/user-attachments/assets/ccd538cb-5122-4ca4-ae8f-0e1d46a56996)

Column Manipulations

![image](https://github.com/user-attachments/assets/be26f027-5ef2-4475-8fd9-2e520be44dab)

Other methods
![image](https://github.com/user-attachments/assets/705819f1-fb56-4024-a3f1-4590706a58f7)

**selectExpr**
![image](https://github.com/user-attachments/assets/7ccf1d62-4834-43b8-84ae-7727a159eccc)

**Aliasing Columns**
![image](https://github.com/user-attachments/assets/e9710673-c2b4-476f-8296-fd1ee25681b5)

### Lecutre 18 : Dataframe Transformations in Spark Part II

#### ```filter()``` / ```where()``` no difference

![image](https://github.com/user-attachments/assets/ccdb523c-04bb-490a-bd54-e051dc0d221b)

![image](https://github.com/user-attachments/assets/19d178e5-086e-41c1-908f-689badb24df8)

#### Multiple filter conditions 

![image](https://github.com/user-attachments/assets/baa7134d-e151-404e-98d6-5dc8b010fc5d)

#### Literals in spark
Used to pass same value in all the columns
![image](https://github.com/user-attachments/assets/b96c60d9-754f-450d-bc46-7aaf6848c095)

#### Adding Columns
If the column already exists then it gets overwritten.
![image](https://github.com/user-attachments/assets/32f4d415-9685-4329-acfd-41ee7a7fd720)

#### Renaming Columns
![image](https://github.com/user-attachments/assets/6fa9577a-c0f3-4e54-b756-d24cb6fb6eda)