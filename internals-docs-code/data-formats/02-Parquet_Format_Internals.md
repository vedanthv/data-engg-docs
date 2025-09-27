### Lecture 14 : Parquet File Internals

![image](https://github.com/user-attachments/assets/50def6a3-7bfa-4b14-881d-46710762a06b)

There are two types of file formats:

- Columnar Based and Row Based

#### Physical Storage of Data on Disk
![image](https://github.com/user-attachments/assets/76e40279-29f0-43b3-80ec-fd4c3e9e4894)

#### Write Once Read Many

The funda of big data is write once read many.

- We dont need all the columns for analytics of big data, so columnar storage is the best.
- If we store in row based format then we need to jump many memory racks to be able to get the data we need.

![image](https://github.com/user-attachments/assets/4fb9d3cc-541e-4b28-a818-5be35e211a8f)

- OLTP generally use row base4d file format.
- I/O should be reduced so OLAP uses columnar format.

#### Why Columnar format may not be the best?

![image](https://github.com/user-attachments/assets/94d7beb7-be65-4836-9fce-1ec86285d842)

In above case we can get col1 and col2 easily but for col10 we still need to scan the entire file.

To tackle this:

Let's say we have 100 million total rows.

We can store 100,000 records at a time, continuously in one row, then the next 100,000 records in next row and so on in hybrid format.

![image](https://github.com/user-attachments/assets/af359956-aa81-4f62-a692-b1492bc7ae0c)

#### Logical Partitioning in Parquet

![image](https://github.com/user-attachments/assets/d72060bc-6425-4b18-a1e8-3bd2e7b6376d)

Let's day we have 500mb data, each row group by default has 128 mb data, so we will have 4 row groups.
Each row group will have some metadata attached to it.

In our example let's say one row group has 100000 records.
The column is futher stored as a page.

#### Runlength Encoding and Bitpacking

![image](https://github.com/user-attachments/assets/5a0219f3-ea0f-4758-ab80-1f3513a5a79f)

Suppose we have 10 lakh records but there can be say 4 countries.

So parquet actually creates a dictionary of key value pair with key as int starting from 0 to 3 and then in the dictionary encoded data, we can see the keys being used insted of country name.

<img width="1194" height="588" alt="image" src="https://github.com/user-attachments/assets/dc926297-8375-4c85-8575-2816dafda415" />


#### More details on Parquet

The row-wise formats store data as records, one after another. This format works well when accessing entire records frequently. However, it can be inefficient when dealing with analytics, where you often only need specific columns from a large dataset.

<img width="1456" height="732" alt="image" src="https://github.com/user-attachments/assets/dfd90692-bacc-46ef-95db-2cabe9d42f87" />

Imagine a table with 50 columns and millions of rows. If you’re only interested in analyzing 3 of those columns, a row-wise format would still require you to read all 50 columns for each row.

Columnar formats address this issue by storing data in columns instead of rows. This means that when you need specific columns, you can read only the columnsdata you need, significantly reducing the amount of data scanned.

<img width="1456" height="728" alt="image" src="https://github.com/user-attachments/assets/f9195654-310f-4834-acab-644e5c51dfd3" />

However, storing data in a columnar format has some downsides. The record write or update operation requires touching multiple column segments, resulting in numerous I/O operations. This can significantly slow the write performance, especially when dealing with high-throughput writes.

When queries involve multiple columns, the database system must reconstruct the records from separate columns. The cost of this reconstruction increases with the number of columns involved in the query.

The hybrid format combines the best of both worlds. The format groups data into "row groups," each containing a subset of rows (aka horizontal partition). Within each row group, data for each column is called a “column chunk" (aka vertical partition).

<img width="1456" height="637" alt="image" src="https://github.com/user-attachments/assets/f4275a15-7461-4eda-9aff-b5e2d440c105" />

In the row group, these chunks are guaranteed to be stored contiguously on disk.

#### Terminologies

<img width="592" height="628" alt="image" src="https://github.com/user-attachments/assets/1910dccb-e6cf-4b90-8c30-1ec7d5612c66" />

A Parquet file is composed of:

**Row Groups**: Each row group contains a subset of the rows in the dataset. Data is organized into columns within each row group, each stored in a column chunk.

**Column Chunk**: A chunk is the data for a particular column in the row group. Column chunk is further divided into pages.

**Pages:** A page is the smallest data unit in Parquet. There are several types of pages, including data pages (actual data), dictionary pages (dictionary-encoded values), and index pages (used for faster data lookup).

#### Metadata Types in Parquet

**Magic number:** The magic number is a specific sequence of bytes (PAR1) located at the beginning and end of the file. It is used to verify whether it is a valid Parquet file.

**FileMetadata:** Parquet stores FileMetadata in the footer of the file. This metadata provides information like the number of rows, data schema, and row group metadata. Each row group metadata contains information about its column chunks (ColumnMetadata), such as the encoding and compression scheme, the size, the page offset, the min/max value of the column chunk, etc. The application can use information in this metadata to prune unnecessary data.

**PageHeader:** The page header metadata is stored with the page data and includes information such as value, definition, and repetition encoding. Parquet also stores definition and repetition levels to handle nested data. The application uses the header to read and decode the data.

#### How is data written into Parquet?

<img width="1456" height="1030" alt="image" src="https://github.com/user-attachments/assets/5f7d8552-ff1a-4a3b-8648-5a5f8dc1cd2f" />

- The application issues a written request with parameters like the data, the compression and encoding scheme for each column (optional), the file scheme (write to one or multiple files), etc.

- The Parquet Writer first collects information, such as the data schema, the null appearance, the encoding scheme, and all the column types recorded in FileMetadata.

- The Writer writes the magic number at the beginning of the file.

- Then, it calculates the number of row groups based on the row group’s max size (configurable) and the data’s size. This step also determines which subset of data belongs to which row group.

- For each row group, it iterates through the column list to write each column chunk for the row group. This step will use the compression scheme specified by the user (the default is none) to compress the data when writing the chunks.

- The chunk writing process begins by calculating the number of rows per page using the max page size and the chunk size. Next, it will try to calculate the column's min/max statistic. (This calculation is only applied to columns with a measurable type, such as integer or float.)

- Then, the column chunk is written page by page sequentially. Each page has a header that includes the page’s number of rows, the page’s encoding for data, repetition, and definition. The dictionary page is stored with its header before the data page if dictionary encoding is used.

- After writing all the pages for the column chunk, the Parquet Writer constructs the metadata for that chunk, which includes information like the column's min/max, the uncompressed/compressed size, the first data page offset, and the first dictionary page offset.

- The column chunk writing process continues until all columns in the row group are written to disk contiguously. The metadata for each column chunk is recorded in the row group metadata.

- After writing all the row groups, all row groups’ metadata is recorded in the FileMetadata.

- The FileMetadata is written to the footer.

- The process finishes by writing the magic number at the end of the file.

#### How is data read from Parquet?

<img width="1398" height="990" alt="image" src="https://github.com/user-attachments/assets/d5836308-8146-42e4-8efe-5b6bbc83cc8f" />

- The application issues a read request with parameters such as the input file, filters to limit the number of read row groups, the set of desired columns, etc.

- If the application requires verification that it’s reading a valid Parquet file, the reader will check if there is a magic number at the beginning and end of the file by seeking the first and last four bytes.

- It then tries to read the FileMetadata from the footer. It extracts information for later use, such as the file schema and the row group metadata.

- If filters are specified, they will limit the scanned row groups by iterating over every row group and checking the filters against each chunk’s statistics. If it satisfies the filters, this row group is appended to the list, which is later used to read.

- The reader defines the column list to read. If the application specifies a subset of columns it wants to read, the list only contains these columns.

- The next step is reading the row groups. The reader will iterate through the row group list and read each row group.

- The reader will read the column chunks for each row group based on the column list. It used ColumnMetadata to read the chunk.

- When reading the column chunk for the first time, the reader locates the position of the first data page (or dictionary page if dictionary encoding is used) using the first page offset in the column metadata. From this position, the reader reads the pages sequentially until no pages are left.

- To determine whether any data remains, the reader tracks the current number of read rows and compares it to the chunk’s total number of rows. If the two numbers are equal, the reader has read all the chunk data.

- To read and decode each data page, the reader visits the page header to collect information like the value encoding, the definition, and the repetition level encoding.

- After reading all the row groups’ column chunks, the reader moves to read the following row groups.

- The process continues until all the row groups in the row group list are read.

Because the Parquet file can be stored in multiple files, the application can read them simultaneously.

In addition, a single Parquet file is partitioned horizontally (row groups) and vertically (column chunks), which allows the application to read data in parallel at the row group or column level.

#### OLAP Workload Example

<img width="780" height="410" alt="image" src="https://github.com/user-attachments/assets/03629b2a-74be-4803-8114-3439a8ca42e6" />

<img width="1048" height="670" alt="image" src="https://github.com/user-attachments/assets/433d90d9-5364-40ee-945a-281157cf3e6d" />

#### Demo

```parquet-tools inspect <filename>```

![image](https://github.com/user-attachments/assets/be572741-6fd9-470b-ad98-0f0d6c293a38)
![image](https://github.com/user-attachments/assets/e4fff36d-48ed-4ca8-9cbd-310f8b35a103)

Gives some file and brief column level metadata.

```parquet_file.metadata.row_group(0).column_group(0)```
![image](https://github.com/user-attachments/assets/ea81d74c-6fb3-4c80-bbbf-521f6c1a3be2)

Compression is GZIP
![image](https://github.com/user-attachments/assets/7d841a8d-fc8d-4f8c-8a42-da2b436a13fc)

Encoding is explained on top.

#### Bitpacking Advantage

- Bitpacking helps in compressing the bits so in above case we just have 4 unique values and hence we need just 2 bytes.
- Query in seconds for running select on csv,parquet etc..

![image](https://github.com/user-attachments/assets/7700c5a0-90b9-4ad1-b430-25ca7df99903)

#### Summary

![image](https://github.com/user-attachments/assets/e4a1bbe6-629b-4970-94bf-a6493f32146b)

- Here the actual data is stored in the pages and it has metadata like min,max and count.

- Let's say we need to find out people less than 18 years age

![image](https://github.com/user-attachments/assets/eb37e1e1-ddab-42da-872b-0de10dbf12f2)

Here when we divide data into row groups, we dont need to do any IO read operation on Row group 2, it saves lot of time and optimize performance.

The above concept is called **Predicate Pushdown**.

#### Projection Pruning

Projection Pruning means we dont read IO from columns that are not part of the select query or that arent required for any join.