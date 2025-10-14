## What is Databricks Lakehouse?

A data lakehouse is a data management system that combines the benefits of data lakes and data warehouses. This article describes the lakehouse architectural pattern and what you can do with it on Databricks.

![alt text](https://snipboard.io/p5h9Ny.jpg)

Data lakehouses often use a data design pattern that incrementally improves, enriches, and refines data as it moves through layers of staging and transformation. Each layer of the lakehouse can include one or more layers. This pattern is frequently referred to as a medallion architecture.

Databricks is built on Apache Spark. Apache Spark enables a massively scalable engine that runs on compute resources decoupled from storage.

The Databricks lakehouse uses two additional key technologies:

Delta Lake: an optimized storage layer that supports ACID transactions and schema enforcement.
Unity Catalog: a unified, fine-grained governance solution for data and AI.

**A schema-on-write approach, combined with Delta schema evolution capabilities, means that you can make changes to this layer without necessarily having to rewrite the downstream logic that serves data to your end users.**

### Capabilities of Lakehouse

**Real-time data processing:** Process streaming data in real-time for immediate analysis and action.

**Data integration:** Unify your data in a single system to enable collaboration and establish a single source of truth for your organization.

**Schema evolution:** Modify data schema over time to adapt to changing business needs without disrupting existing data pipelines.

**Data transformations:** Using Apache Spark and Delta Lake brings speed, scalability, and reliability to your data.

**Data analysis and reporting:** Run complex analytical queries with an engine optimized for data warehousing workloads.

**Machine learning and AI:** Apply advanced analytics techniques to all of your data. Use ML to enrich your data and support other workloads.

**Data versioning and lineage:** Maintain version history for datasets and track lineage to ensure data provenance and traceability.

**Data governance:** Use a single, unified system to control access to your data and perform audits.

**Data sharing:** Facilitate collaboration by allowing the sharing of curated data sets, reports, and insights across teams.

**Operational analytics:** Monitor data quality metrics, model quality metrics, and drift by applying machine learning to lakehouse monitoring data.