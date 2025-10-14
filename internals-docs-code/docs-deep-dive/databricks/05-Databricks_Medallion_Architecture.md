## Databricks Medallion Architecture

The medallion architecture describes a series of data layers that denote the quality of data stored in the lakehouse. Databricks recommends taking a multi-layered approach to building a single source of truth for enterprise data products.

This architecture guarantees atomicity, consistency, isolation, and durability as data passes through multiple layers of validations and transformations before being stored in a layout optimized for efficient analytics. The terms bronze (raw), silver (validated), and gold (enriched) describe the quality of the data in each of these layers.

### Multi Hop Design Pattern of Medallion Architecture

A medallion architecture is a data design pattern used to organize data logically. Its goal is to incrementally and progressively improve the structure and quality of data as it flows through each layer of the architecture (from Bronze ⇒ Silver ⇒ Gold layer tables). Medallion architectures are sometimes also referred to as multi-hop architectures.

By progressing data through these layers, organizations can incrementally improve data quality and reliability, making it more suitable for business intelligence and machine learning applications.

![alt text](https://snipboard.io/YKepZh.jpg)

Example Medallion Architecture

![alt text](https://snipboard.io/URFJqw.jpg)

### Silver Layer Good Practices

- Should always include at least one validated, non-aggregated representation of each record. If aggregate representations drive many downstream workloads, those representations might be in the silver layer, but typically they are in the gold layer.

- Is where you perform data cleansing, deduplication, and normalization.

- Enhances data quality by correcting errors and inconsistencies.

- Structures data into a more consumable format for downstream processing.

### Enforcing Data Quality at Silver Layer

- Schema enforcement
- Handling of null and missing values
- Data deduplication
- Resolution of out-of-order and late-arriving data issues
- Data quality checks and enforcement
- Schema evolution
- Type casting
- Joins

