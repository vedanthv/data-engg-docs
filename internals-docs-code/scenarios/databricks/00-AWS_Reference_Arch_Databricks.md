## Reference Databricks Architecture on AWS

![alt text](https://snipboard.io/ypWTYM.jpg)

The AWS reference architecture shows the following AWS-specific services for ingesting, storage, serving, and analysis:

- Amazon Redshift as a source for Lakehouse Federation
- Amazon AppFlow and AWS Glue for batch ingest
- AWS IoT Core, Amazon Kinesis, and AWS DMS for streaming ingest
- Amazon S3 as the object storage for data and AI assets
- Amazon RDS and Amazon DynamoDB as operational databases
- Amazon QuickSight as BI tool
- Amazon Bedrock is used by Model Serving to call external LLMs from leading AI startups and Amazon

## Organization of Reference Architecture

The reference architecture is structured along the swim lanes **Source, Ingest, Transform, Query/Process, Serve, Analysis, and Storage:**

### Source

There are three ways to integrate external data into the Data Intelligence Platform:

- **ETL:** The platform enables integration with systems that provide semi-structured and unstructured data (such as sensors, IoT devices, media, files, and logs), as well as structured data from relational databases or business applications.
  
- **Lakehouse Federation:** SQL sources, such as relational databases, can be integrated into the lakehouse and Unity Catalog without ETL. In this case, the source system data is governed by Unity Catalog, and queries are pushed down to the source system.

- **Catalog Federation:** External Hive Metastore catalogs or AWS Glue can also be integrated into Unity Catalog through catalog federation, allowing Unity Catalog to control the tables stored in Hive Metastore or AWS Glue.

### Ingest

Ingest data into the lakehouse via batch or streaming:

- **Databricks Lakeflow Connect** offers built-in connectors for ingestion from enterprise applications and databases. The resulting ingestion pipeline is governed by Unity Catalog and is powered by serverless compute and Lakeflow Declarative Pipelines.

- Files delivered to cloud storage can be loaded directly using the Databricks **Auto Loader**.

- For batch ingestion of data from enterprise applications into Delta Lake, the Databricks lakehouse relies on partner ingest tools with specific adapters for these systems of record.

- Streaming events can be ingested directly from event streaming systems such as Kafka using **Databricks Structured Streaming**. Streaming sources can be sensors, IoT, or change data capture processes.

### Storage

Data is typically stored in the cloud storage system where the ETL pipelines use the medallion architecture to store data in a curated way as Delta files/tables or Apache Iceberg tables.

### Transform and Query / process

- The Databricks lakehouse uses its engines **Apache Spark and Photon** for all transformations and queries.

- **Lakeflow Declarative Pipelines** is a declarative framework for simplifying and optimizing reliable, maintainable, and testable data processing pipelines.

Powered by Apache Spark and Photon, the **Databricks Data Intelligence Platform** supports both types of workloads: SQL queries via SQL warehouses, and SQL, Python and Scala workloads via workspace clusters.

For data science (ML Modeling and Gen AI), the **Databricks AI and Machine Learning platform** provides specialized ML runtimes for AutoML and for coding ML jobs. All data science and MLOps workflows are best supported by MLflow.

### Serving

For data warehousing (DWH) and BI use cases, the Databricks lakehouse provides Databricks SQL, the data warehouse powered by SQL warehouses, and serverless SQL warehouses.

For machine learning, Mosaic AI Model Serving is a scalable, real-time, enterprise-grade model serving capability hosted in the Databricks control plane. Mosaic AI Gateway is Databricks solution for governing and monitoring access to supported generative AI models and their associated model serving endpoints.

### Operational databases:

Lakebase is an online transaction processing (OLTP) database based on Postgres and fully integrated with the Databricks Data Intelligence Platform. It allows you to create OLTP databases on Databricks, and integrate OLTP workloads with your Lakehouse.
External systems, such as operational databases, can be used to store and deliver final data products to user applications.

### Collaboration:

Business partners get secure access to the data they need through Delta Sharing.

Based on Delta Sharing, the Databricks Marketplace is an open forum for exchanging data products.

Clean Rooms are secure and privacy-protecting environments where multiple users can work together on sensitive enterprise data without direct access to each other's data.

### Analysis

The final business applications are in this swim lane. Examples include custom clients such as AI applications connected to Mosaic AI Model Serving for real-time inference or applications that access data pushed from the lakehouse to an operational database.

For BI use cases, analysts typically use BI tools to access the data warehouse. SQL developers can additionally use the Databricks SQL Editor (not shown in the diagram) for queries and dashboarding.

The Data Intelligence Platform also offers dashboards to build data visualizations and share insights.

### Integrate

The Databricks platform integrates with standard identity providers for user management and single sign on (SSO).
External AI services like OpenAI, LangChain or HuggingFace can be used directly from within the Databricks Intelligence Platform.

External orchestrators can either use the comprehensive REST API or dedicated connectors to external orchestration tools like Apache Airflow.

Unity Catalog is used for all data & AI governance in the Databricks Intelligence Platform and can integrate other databases into its governance through Lakehouse Federation.

Additionally, Unity Catalog can be integrated into other enterprise catalogs. Contact the enterprise catalog vendor for details.