### Lecture 5 : Read Modes in Spark

![image](https://github.com/user-attachments/assets/7ab22f33-3951-45d7-849e-83f693e5bf4b)

**format**
data file format : csv,json,jdbc and odbc connection. Format is optional parameter, by default its parquet format

**option** 
inferschema, mode and header [**optional field**]

**schema**
manual schema can be passed here

**load**
path from where we need to read the data [**not optional**]

#### DataframeReader API

Access it using 'spark.read' in the spark session

![image](https://github.com/user-attachments/assets/0ba45b86-8921-41dc-8453-ebc4298184ab)

#### `mode` in Spark

![image](https://github.com/user-attachments/assets/8ef66ae0-5f09-4610-8ae4-120aa9ecd673)