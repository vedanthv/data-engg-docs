# Volumes in Databricks

Volumes are Unity Catalog objects that enable governance over non-tabular datasets. Volumes represent a logical volume of storage in a cloud object storage location. Volumes provide capabilities for accessing, storing, governing, and organizing files.

While tables govern tabular data, volumes govern non-tabular data of any format, including structured, semi-structured, or unstructured.

Databricks recommends using volumes to govern access to all non-tabular data. Volumes are available in two types:

- Managed volumes: For simple Databricks-managed storage.

- External volumes: For adding governance to existing cloud object storage locations.
  
## Uses cases for volumes

Use cases for volumes include:

- Register landing areas for raw data produced by external systems to support its processing in the early stages of ETL pipelines and other data engineering activities.

- Register staging locations for ingestion. For example, using Auto Loader, COPY INTO, or CTAS (CREATE TABLE AS) statements.

- Provide file storage locations for data scientists, data analysts, and machine learning engineers to use as parts of their exploratory data analysis and other data science tasks.

- Give Databricks users access to arbitrary files produced and deposited in cloud storage by other systems. For example, large collections of unstructured data (such as image, audio, video, and PDF files) captured by surveillance systems or IoT devices, or library files (JARs and Python wheel files) exported from local dependency management systems or CI/CD pipelines.

- Store operational data, such as logging or checkpointing files.

## Managed Vs External Volumes

![alt text](https://snipboard.io/CuRcF3.jpg)

## Why use managed volumes?

- Managed volumes have the following benefits:

- Default choice for Databricks workloads.

- No need to manage cloud credentials or storage paths manually.

- Simplest option for creating governed storage locations quickly.

## Why use use external volumes?

E- xternal volumes allow you to add Unity Catalog data governance to existing cloud object storage directories. Some use cases for external volumes include the following:

- Adding governance where data already resides, without requiring data copy.
- Governing files produced by other systems that must be ingested or accessed by Databricks.
- Governing data produced by Databricks that must be accessed directly from cloud object storage by other systems.
- Databricks recommends using external volumes to store non-tabular data files that are read or written by external systems in addition to Databricks. 
- Unity Catalog doesn't govern reads and writes performed directly against cloud object storage from external systems, so you must configure additional policies and credentials in your cloud account so that data governance policies are respected outside Databricks.

## Path for Accessing Volumes

```/Volumes/<catalog>/<schema>/<volume>/<path>/<file-name>```

**You can't register files in volumes as tables in Unity Catalog. Volumes are intended for path-based data access only. Use tables when you want to work with tabular data in Unity Catalog.**

# Tables in Databricks

![alt text](https://snipboard.io/RD8AJU.jpg)