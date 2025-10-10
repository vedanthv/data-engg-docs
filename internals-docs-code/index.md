# Data Engineering and Cloud Platform Knowledge Base

This repository is where I keep track of what I’m learning and experimenting with across data engineering, distributed systems, and cloud platforms. It’s part study notes, part code lab, and part reference guide — essentially a place to capture concepts as I work through them and to revisit later when I need a refresher.

I focus on technologies like Apache Spark, Kafka/Redpanda, Databricks, AWS, and Azure, along with supporting tools and practices that are important for building reliable data systems. You’ll find a mix of summaries, deep dives into tricky concepts, performance tuning notes, and small experiments that test how things work in practice.

The main goal of this repo is to strengthen my own understanding, but I also hope it can be useful to anyone else navigating similar topics. Think of it as a learning log that balances hands-on exploration with professional best practices - something between a personal notebook and a practical guide.

<!-- TOC START -->
# 📑 Data Engineering Knowledge Base


## Azure

1. [Azure Integration Databricks](azure/00-Azure_Integration_Databricks.md)
2. [Azure Portal Subscriptions Resourcegroups](azure/01-Azure_Portal_Subscriptions_ResourceGroups.md)
3. [Azure Cli Scenarios](azure/02-Azure_CLI_Scenarios.md)
4. [Azure Powershell Scenarios](azure/03-Azure_Powershell_Scenarios.md)
5. [Azure Arm Templates](azure/05-Azure_ARM_Templates.md)
6. [Azure Bicep Templates](azure/06-Azure_Bicep_Templates.md)
7. [Overview Of Azure Storage](azure/07-Overview_Of_Azure_Storage.md)
8. [Blob Storage Fundamentals](azure/08-Blob_Storage_Fundamentals.md)
9. [Adls Gen2 Overview](azure/09-ADLS_Gen2_Overview.md)
10. [Azure Rbac Acl](azure/10-Azure_RBAC_ACL.md)
11. [Azure Types Of Storage](azure/11-Azure_Types_Of_Storage.md)
12. [Azure Storage Replication Strategies](azure/12-Azure_Storage_Replication_Strategies.md)
13. [Soft Delete Pitr Azure Storage](azure/13-Soft_Delete_PITR_Azure_Storage.md)
14. [Azure Shared Access Signature](azure/14-Azure_Shared_Access_Signature.md)
15. [Azure Lifetime Management Policies](azure/15-Azure_Lifetime_Management_Policies.md)
16. [Eventgrid Integration Azure](azure/16-EventGrid_Integration_Azure.md)
17. [Azure Encrpytion Standards](azure/17-Azure_Encrpytion_Standards.md)
18. [Azure+ Private Endpoints](azure/18-Azure+_Private_Endpoints.md)
19. [Cross Region Replication Azure](azure/19-Cross_Region_Replication_Azure.md)
20. [Azure Storage Rest Api](azure/20-Azure_Storage_Rest_API.md)
21. [Introduction Azure Data Factory](azure/21-Introduction_Azure_Data_Factory.md)
22. [Azure Data Factory Vs Synapse](azure/22-Azure_Data_Factory_vs_Synapse.md)
23. [Azure Data Factory Architecture](azure/23-Azure_Data_Factory_Architecture.md)
24. [Adf Triggers Intro](azure/24-ADF_Triggers_Intro.md)
25. [Index](azure/index.md)

## Data-formats

1. [Data Format Deep Dive Pt1](data-formats/01-Data_Format_Deep_Dive_Pt1.md)
2. [Parquet Format Internals](data-formats/02-Parquet_Format_Internals.md)

## Databricks

1. [Azure Databricks Uc Creation](databricks/01-Azure_Databricks_UC_Creation.md)
2. [Databricks Uc Introduction](databricks/02-Databricks_UC_Introduction.md)
3. [Databricks Managed External Tables Hive](databricks/03-Databricks_Managed_External_Tables_Hive.md)
4. [Uc Managed External Tables](databricks/03-UC_Managed_External_Tables.md)
5. [Uc External Location Storage Credentials](databricks/04-UC_External_Location_Storage_Credentials.md)
6. [Databricks Managed Location Catalog Schema Level](databricks/05-Databricks_Managed_Location_Catalog_Schema_Level.md)
7. [Ctas Deep Clone Shallow Clone Databricks](databricks/06-CTAS_Deep_Clone_Shallow_Clone_Databricks.md)
8. [Rbac Custom Roles Serviceprincipals](databricks/07-RBAC_Custom_Roles_ServicePrincipals.md)
9. [Deletion Vectors Delta Lake](databricks/08-Deletion_Vectors_Delta_lake.md)
10. [Liquid Clustering Delta Lake](databricks/09-Liquid_Clustering_Delta_Lake.md)
11. [Concurrency Liquid Clustering](databricks/10-Concurrency_Liquid_Clustering.md)
12. [Copy Into Databricks](databricks/11-Copy_Into_Databricks.md)
13. [Autoloader Databricks](databricks/12-AutoLoader_Databricks.md)
14. [12.1 Autoloader Databricks Schema Inference](databricks/12.1-AutoLoader_Databricks_Schema_Inference.md)
15. [Intro Databricks Lakeflow Declarative Pipelines](databricks/13-Intro_Databricks_Lakeflow_Declarative_Pipelines.md)
16. [Dlt Batch Vs Streaming Workloads](databricks/14-DLT_Batch_Vs_Streaming_Workloads.md)
17. [Dlt Data Storage Checkpoints](databricks/15-DLT_Data_Storage_Checkpoints.md)
18. [Databricks Secret Scopes](databricks/16-Databricks_Secret_Scopes.md)
19. [Databricks Controlplane Dataplane](databricks/17-Databricks_ControlPlane_DataPlane.md)
20. [Databricks Dlt Code Walkthrough](databricks/18-Databricks_DLT_Code_Walkthrough.md)
21. [Databricks Serverless Compute](databricks/19-Databricks_Serverless_Compute.md)
22. [Databricks Warehouses](databricks/20-Databricks_Warehouses.md)
23. [Databricks Lakehouse Federation](databricks/21-Databricks_Lakehouse_Federation.md)
24. [Databricks Metrics Views](databricks/22-Databricks_Metrics_Views.md)
25. [Databricks Streaming Materialized Views Sql](databricks/23-Databricks_Streaming_Materialized_Views_SQL.md)
26. [Databricks Cli Setup](databricks/24-Databricks_CLI_Setup.md)
27. [Index](databricks/index.md)

## Scenarios

1. [Index](scenarios/index.md)

### Databricks

1. [Retail Sku Inventory Tracking](scenarios/databricks/00-Retail_SKU_Inventory_Tracking.md)
2. [Index](scenarios/databricks/index.md)

### Spark

1. [Smj Spill To Disk Q1](scenarios/spark/01-SMJ_Spill_To_Disk_Q1.md)
2. [Smj Spill To Disk Q2](scenarios/spark/02-SMJ_Spill_To_Disk_Q2.md)
3. [Smj Output During Spill Q3](scenarios/spark/03-SMJ_Output_During_Spill_Q3.md)
4. [Cross Vs Broadcast Join](scenarios/spark/04-Cross_vs_Broadcast_Join.md)
5. [Index](scenarios/spark/index.md)

## Spark

1. [Spark Architecture Yarn](spark/01-Spark_Architecture_YARN.md)
2. [Spark Driver Oom](spark/02-Spark_Driver_OOM.md)
3. [Types Of Memory Spark](spark/03-Types_Of_Memory_Spark.md)
4. [Spark Dynamic Partition Pruning](spark/04-Spark_Dynamic_Partition_Pruning.md)
5. [Spark Salting Technique](spark/05-Spark_Salting_Technique.md)
6. [What Is Spark](spark/06-What_Is_Spark.md)
7. [Why Apache Spark](spark/07-Why_Apache_Spark.md)
8. [Hadoop Vs Spark](spark/08-Hadoop_Vs_Spark.md)
9. [Spark Ecosystem](spark/09-Spark_Ecosystem.md)
10. [Spark Ecosystem](spark/10-Spark_Ecosystem.md)
11. [Spark Architecture](spark/11-Spark_Architecture.md)
12. [Schema In Spark](spark/12-Schema_In_Spark.md)
13. [Handling Corrupt Records Spark](spark/13-Handling_Corrupt_Records_Spark.md)
14. [Spark Transformations Actions](spark/14-Spark_Transformations_Actions.md)
15. [Spark Dag Lazy Eval](spark/15-Spark_DAG_Lazy_Eval.md)
16. [Spark Json Data](spark/16-Spark_JSON_Data.md)
17. [Spark Sql Engine](spark/17-Spark_SQL_Engine.md)
18. [Spark Rdd](spark/18-Spark_RDD.md)
19. [Spark Writing Data Disk](spark/19-Spark_Writing_Data_Disk.md)
20. [Spark Partitioning Bucketing](spark/20-Spark_Partitioning_Bucketing.md)
21. [Spark Session Vs Context](spark/21-Spark_Session_vs_Context.md)
22. [Spark Job Stage Task](spark/22-Spark_Job_Stage_Task.md)
23. [Spark Transformations](spark/23-Spark_Transformations.md)
24. [Spark Union Vs Unionall](spark/24-Spark_Union_vs_UnionAll.md)
25. [Spark Repartition Vs Coalesce](spark/25-Spark_Repartition_vs_Coalesce.md)
26. [Spark Case When](spark/26-Spark_Case_When.md)
27. [Spark Unique Sorted Records](spark/27-Spark_Unique_Sorted_Records.md)
28. [Spark Agg Functions](spark/28-Spark_Agg_Functions.md)
29. [Spark Group By](spark/30-Spark_Group_By.md)
30. [Spark Joins Intro](spark/31-Spark_Joins_Intro.md)
31. [Spark Join Strategies](spark/32-Spark_Join_Strategies.md)
32. [Spark Window Functions](spark/33-Spark_Window_Functions.md)
33. [Spark Memory Management](spark/34-Spark_Memory_Management.md)
34. [Spark Executor Oom](spark/35-Spark_Executor_OOM.md)
35. [Spark Submit Command](spark/36-Spark_Submit_Command.md)
36. [Spark Deployment Modes](spark/37-Spark_Deployment_Modes.md)
37. [Spark Adaptive Query Execution](spark/38-Spark_Adaptive_Query_Execution.md)
38. [Spark Dynamic Resource Allocation](spark/39-Spark_Dynamic_Resource_Allocation.md)
39. [Spark Dynamic Partition Pruning](spark/40-Spark_Dynamic_Partition_Pruning.md)
40. [Index](spark/index.md)

## Streaming

1. [Index](streaming/index.md)

### Architecture

2. [Use Cases Streaming](streaming/architecture/01-Use_Cases_Streaming.md)
3. [Redpanda Vs Kafka Arch Differences](streaming/architecture/02-Redpanda_vs_Kafka_Arch_Differences.md)
4. [Redpanda Architure In Depth Pt1](streaming/architecture/03-Redpanda_Architure_In_Depth_Pt1.md)
5. [Index](streaming/architecture/index.md)

### Kafka

2. [Kafka Kraft Setup](streaming/kafka/01-Kafka_KRaft_Setup.md)
3. [Kafka Broker Properties](streaming/kafka/02-Kafka_Broker_Properties.md)
4. [Topic Default Properties](streaming/kafka/03-Topic_Default_Properties.md)
5. [Kafka Hardware Considerations](streaming/kafka/04-Kafka_Hardware_Considerations.md)
6. [Kafka Configuring Clusters Broker Consideration](streaming/kafka/05-Kafka_Configuring_Clusters_Broker_Consideration.md)
7. [Kafka Broker Os Tuning](streaming/kafka/06-Kafka_Broker_OS_Tuning.md)
8. [Kafka Os Tuning Dirty Page Handling](streaming/kafka/07-Kafka_OS_Tuning_Dirty_Page_Handling.md)
9. [Kafka File Descriptors Overcommit Memory](streaming/kafka/08-Kafka_File_Descriptors_Overcommit_Memory.md)
10. [Kafka Production Concerns](streaming/kafka/09-Kafka_Production_Concerns.md)
11. [Kafka Message Types](streaming/kafka/10-Kafka_Message_Types.md)
12. [Kafka Configuring Producers Pt1](streaming/kafka/11-Kafka_Configuring_Producers_Pt1.md)
13. [Kafka Configuring Producers Pt2](streaming/kafka/12-Kafka_Configuring_Producers_Pt2.md)
14. [Kafka Serializers Avro Pt1](streaming/kafka/13-Kafka_Serializers_Avro_Pt1.md)
15. [Kafka Serializers Avro Pt2](streaming/kafka/14-Kafka_Serializers_Avro_Pt2.md)
16. [Kafka Partitions](streaming/kafka/15-Kafka_Partitions.md)
17. [Kafka Headers](streaming/kafka/16-Kafka_Headers.md)
18. [Kafka Interceptors](streaming/kafka/17-Kafka_Interceptors.md)
19. [Kafka Quotas And Throttling](streaming/kafka/18-Kafka_Quotas_And_Throttling.md)
20. [Kafka Consumer Eager And Cooperative Rebalance](streaming/kafka/19-Kafka_Consumer_Eager_And_Cooperative_Rebalance.md)
21. [Kafka Consumer Static Partitioning](streaming/kafka/20-Kafka_Consumer_Static_Partitioning.md)
22. [Kafka Poll Loop](streaming/kafka/21-Kafka_Poll_Loop.md)
23. [Index](streaming/kafka/index.md)
<!-- TOC END -->


