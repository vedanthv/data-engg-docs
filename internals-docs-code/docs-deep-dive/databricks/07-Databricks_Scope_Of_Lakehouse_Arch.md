## Databricks : Scope of Lakehouse Architecture

### User Personas

**Data engineers** provide data scientists and business analysts with accurate and reproducible data for timely decision-making and real-time insights. They implement highly consistent and reliable ETL processes to increase user confidence and trust in data. They ensure that data is well integrated with the various pillars of the business and typically follow software engineering best practices.

**Data scientists** blend analytical expertise and business understanding to transform data into strategic insights and predictive models. They are adept at translating business challenges into data-driven solutions, be that through retrospective analytical insights or forward-looking predictive modeling. Leveraging data modeling and machine learning techniques, they design, develop, and deploy models that unveil patterns, trends, and forecasts from data. They act as a bridge, converting complex data narratives into comprehensible stories, ensuring business stakeholders not only understand but can also act upon the data-driven recommendations, in turn driving a data-centric approach to problem-solving within an organization.

**ML engineers** (machine learning engineers) lead the practical application of data science in products and solutions by building, deploying, and maintaining machine learning models. Their primary focus pivots towards the engineering aspect of model development and deployment. ML Engineers ensure the robustness, reliability, and scalability of machine learning systems in live environments, addressing challenges related to data quality, infrastructure, and performance. By integrating AI and ML models into operational business processes and user-facing products, they facilitate the utilization of data science in solving business challenges, ensuring models don't just stay in research but drive tangible business value.

**Business analysts and business users**: Business analysts provide stakeholders and business teams with actionable data. They often interpret data and create reports or other documentation for management using standard BI tools. They are typically the first point of contact for non-technical business users and operations colleagues for quick analysis questions. 

Dashboards and business apps delivered on the Databricks platform can be used directly by business users.
Apps Developer create secure data and AI applications on the data platform and share those apps with business users.
Business partners are important stakeholders in an increasingly networked business world. They are defined as a company or individuals with whom a business has a formal relationship to achieve a common goal, and can include vendors, suppliers, distributors, and other third-party partners. Data sharing is an important aspect of business partnerships, as it enables the transfer and exchange of data to enhance collaboration and data-driven decision-making.

### Domains of Platform Framework

**Storage:** In the cloud, data is mainly stored in scalable, efficient, and resilient object storage on cloud providers.

**Governance:** Capabilities around data governance, such as access control, auditing, metadata management, lineage tracking, and monitoring for all data and AI assets.

**AI engine:** The AI engine provides generative AI capabilities for the whole platform.

**Ingest and transform:** The capabilities for ETL workloads.

**Advanced analytics, ML, and AI:** All capabilities around machine learning, AI, Generative AI, and also streaming analytics.

**Data warehouse:** The domain supporting DWH and BI use cases.

**Operational Database:** Capabilities and services around operational databases like OLTP databases (online transaction processing), key-value stores, etc.

**Automation:** Workflow management for data processing, machine learning, analytics pipelines, including CI/CD and MLOps support.

**ETL and Data science tools:** The front-end tools that data engineers, data scientists and ML engineers primarily use for work.

**BI tools:** The front-end tools that BI analysts primarily use for work.

Data and AI apps Tools that build and host applications that use the data managed by the underlying platform and leverage its analytics and AI capabilities in a secure and governance-compliant manner.

**Collaboration:** Capabilities for data sharing between two or more parties.

![alt text](https://snipboard.io/dsvbOp.jpg)

### Data Workloads in Databricks

#### Ingest and Transform

**Databricks Lakeflow Connect** offers built-in connectors for ingestion from enterprise applications and databases. The resulting ingestion pipeline is governed by Unity Catalog and is powered by serverless compute and Lakeflow Declarative Pipelines.

**Auto Loader** incrementally and automatically processes files landing in cloud storage in scheduled or continuous jobs - without the need to manage state information. Once ingested, raw data needs to be transformed so it's ready for BI and ML/AI. Databricks provides powerful ETL capabilities for data engineers, data scientists, and analysts.

**Lakeflow Declarative Pipelines** allows writing ETL jobs in a declarative way, simplifying the entire implementation process. Data quality can be improved by defining data expectations.

#### Data Warehouse

The Databricks Data Intelligence Platform also has a complete data warehouse solution with Databricks SQL, centrally governed by **Unity Catalog** with fine-grained access control.

**AI functions** are built-in SQL functions that allow you to apply AI on your data directly from SQL. Integrating AI into analysis jobs provides access to information previously inaccessible to analysts, and empowers them to make more informed decisions, manage risks, and sustain a competitive advantage through data-driven innovation and efficiency.

#### Operational Database

**Lakebase** is an online transaction processing (OLTP) database based on Postgres and fully integrated with the Databricks Data Intelligence Platform. It allows you to create an OLTP database on Databricks, and integrate OLTP workloads with your Lakehouse. 

Lakebase allows to sync data between OLTP and online analytical processing (OLAP) workloads, and is well integrated with Feature management, SQL warehouses, and Databricks Apps.

### Outline of Databricks Feature Areas

#### Cloud Storage

All data for the lakehouse is stored in the cloud provider's object storage. Databricks supports three cloud providers: AWS, Azure, and GCP. Files in various structured and semi-structured formats (for example, Parquet, CSV, JSON, and Avro), as well as unstructured formats (such as images and documents), are ingested and transformed using either batch or streaming processes.

**Delta Lake** is the recommended data format for the lakehouse (file transactions, reliability, consistency, updates, and so on). It's also possible to **read Delta tables using Apache Iceberg clients**.

No proprietary data formats are used in the Databricks Data Intelligence Platform: Delta Lake and Iceberg are open source to avoid vendor lock-in.

#### Data and AI Governance

On top of the storage layer, Unity Catalog offers a wide range of data and AI governance capabilities, including metadata management in the **metastore, access control, auditing, data discovery, and data lineage**.

Lakehouse monitoring provides out-of-the-box quality metrics for data and AI assets, and auto-generated dashboards to visualize these metrics.

External SQL sources can be integrated into the lakehouse and Unity Catalog through **lakehouse federation**.

#### Orchestration

**Lakeflow Jobs** enable you to run diverse workloads for the full data and AI lifecycle on any cloud. They allow you to orchestrate jobs as well as Lakeflow Declarative Pipelines for SQL, Spark, notebooks, DBT, ML models, and more.

#### Collaboration

**Delta Sharing** is an open protocol developed by Databricks for secure data sharing with other organizations regardless of the computing platforms they use.

**Databricks Marketplace** is an open forum for exchanging data products. It takes advantage of Delta Sharing to give data providers the tools to  share data products securely and data consumers the power to explore and expand their access to the data and data services they need.

**Clean Rooms use Delta Sharing** and serverless compute to provide a secure and privacy-protecting environment where multiple parties can work together on sensitive enterprise data without direct access to each other's data.