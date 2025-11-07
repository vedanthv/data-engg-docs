# Databricks Query Federation

![alt text](https://snipboard.io/qCy4ne.jpg)

## Why Use Query Federation?

The lakehouse emphasizes central storage of data to reduce data redundancy and isolation. Your organization might have numerous data systems in production, and you might want to query data in connected systems for a number of reasons:

- On-demand reporting.
- Proof-of-concept work.
- The exploratory phase of new ETL pipelines or reports.
- Supporting workloads during incremental migration.
- In each of these scenarios, query federation gets you to insights faster, because you can query the data in place and avoid complex and time-consuming ETL processing.

Query federation is meant for use cases when:

- You don't want to ingest data into Databricks.
- You want your queries to take advantage of compute in the external database system.
- You want the advantages of Unity Catalog interfaces and data governance, including fine-grained access control, data lineage, and search.

## Query Federation vs Lakeflow Connect

Query federation allows you to query external data sources without moving your data. Databricks recommends ingestion using managed connectors because they scale to accommodate high data volumes, low-latency querying, and third-party API limits. However, you might want to query your data without moving it. 

When you have a choice between managed ingestion connectors and query federation, choose query federation for ad hoc reporting or proof-of-concept work on your ETL pipelines.

