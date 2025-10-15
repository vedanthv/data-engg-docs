## Reference Architectures Using Databricks and AWS

### Built-in ingestion from SaaS apps and databases with Lakeflow Connect

![alt text](https://snipboard.io/DPcxKn.jpg)

Databricks Lakeflow Connect offers built-in connectors for ingestion from enterprise applications and databases. The resulting ingestion pipeline is governed by Unity Catalog and is powered by serverless compute and Lakeflow Declarative Pipelines.

Lakeflow Connect leverages efficient incremental reads and writes to make data ingestion faster, scalable, and more cost-efficient, while your data remains fresh for downstream consumption.

### Batch ingestion and ETL

Ingestion tools use source-specific adapters to read data from the source and then either store it in the cloud storage from where Auto Loader can read it, or call Databricks directly (for example, with partner ingestion tools integrated into the Databricks lakehouse). 

To load the data, the Databricks ETL and processing engine runs the queries via Lakeflow Declarative Pipelines. Orchestrate single or multitask jobs using Lakeflow Jobs and govern them using Unity Catalog (access control, audit, lineage, and so on). 

To provide access to specific golden tables for low-latency operational systems, export the tables to an operational database such as an RDBMS or key-value store at the end of the ETL pipeline.

![alt text](https://snipboard.io/d7I50M.jpg)

### Stream Processing and CDC

![alt text](https://snipboard.io/9MX0tv.jpg)

The Databricks ETL engine Spark Structured Streaming to read from event queues such as Apache Kafka or AWS Kinesis. The downstream steps follow the approach of the Batch use case above.

Real-time change data capture (CDC) typically uses an event queue to store the extracted events. From there, the use case follows the streaming use case.

If CDC is done in batch where the extracted records are stored in cloud storage first, then Databricks Autoloader can read them and the use case follows Batch ETL.

### Machine Learning and AI : Traditional

![alt text](https://snipboard.io/uPmSGZ.jpg)

For machine learning, the Databricks Data Intelligence Platform provides Mosaic AI, which comes with state-of-the-art machine and deep learning libraries. It provides capabilities such as Feature Store and Model Registry (both integrated into Unity Catalog), low-code features with AutoML, and MLflow integration into the data science lifecycle.

All data science-related assets (tables, features, and models) are governed by Unity Catalog and data scientists can use Lakeflow Jobs to orchestrate their jobs.

For deploying models in a scalable and enterprise-grade way, use the MLOps capabilities to publish the models in model serving.

