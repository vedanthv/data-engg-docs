### Lecture 15 : How to write data on the disk?

![image](https://github.com/user-attachments/assets/a22d1931-1b95-4515-9311-5c53883b47ba)

![image](https://github.com/user-attachments/assets/03f8e132-9ead-4ae4-9d59-ad339ebcf615)

#### Modes to write data

![image](https://github.com/user-attachments/assets/1ecedad1-043a-49d9-be96-d1ba66d062c3)

Create three files
![image](https://github.com/user-attachments/assets/5e28b1b7-af47-4cb6-ac24-45d0a64b03a7)

```python
  write_df = read_df.repartition(3).write.format("csv")\
    .option("header", "True")\
    .mode("overwrite")\  # Using .mode() instead of .option() for overwrite mode
    .option("path", "/FileStore/tables/Write_Data/")\
    .save()
```