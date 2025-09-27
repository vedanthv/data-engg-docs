### Lecture 7 : Schema in Spark

#### StructType and StructField
![image](https://github.com/user-attachments/assets/c5adae79-16fa-4643-80ea-88c538407c9d)

Example:

![image](https://github.com/user-attachments/assets/bb98a403-21d9-4721-9d48-442bc6bd5006)

![image](https://github.com/user-attachments/assets/a042b2de-561a-4863-a85e-6bf589c385c3)

How to skip the header row?

```python
df = spark.read.option("skipRows", 2).csv("file.csv")
```