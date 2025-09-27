# Data Engineering and Cloud Platform Knowledge Base

This repository is where I keep track of what I’m learning and experimenting with across data engineering, distributed systems, and cloud platforms. It’s part study notes, part code lab, and part reference guide — essentially a place to capture concepts as I work through them and to revisit later when I need a refresher.

I focus on technologies like Apache Spark, Kafka/Redpanda, Databricks, AWS, and Azure, along with supporting tools and practices that are important for building reliable data systems. You’ll find a mix of summaries, deep dives into tricky concepts, performance tuning notes, and small experiments that test how things work in practice.

The main goal of this repo is to strengthen my own understanding, but I also hope it can be useful to anyone else navigating similar topics. Think of it as a learning log that balances hands-on exploration with professional best practices - something between a personal notebook and a practical guide.

<!-- TOC START -->
# 📑 Data Engineering Knowledge Base


## Azure

2. [Azure Integration Databricks](azure/00-Azure_Integration_Databricks.md)
3. [Azure Portal Subscriptions Resourcegroups](azure/01-Azure_Portal_Subscriptions_ResourceGroups.md)
4. [Azure Cli Scenarios](azure/02-Azure_CLI_Scenarios.md)
5. [Azure Powershell Scenarios](azure/03-Azure_Powershell_Scenarios.md)
6. [Azure Arm Templates](azure/05-Azure_ARM_Templates.md)
7. [Azure Bicep Templates](azure/06-Azure_Bicep_Templates.md)
8. [Overview Of Azure Storage](azure/07-Overview_Of_Azure_Storage.md)
9. [Blob Storage Fundamentals](azure/08-Blob_Storage_Fundamentals.md)
10. [Adls Gen2 Overview](azure/09-ADLS_Gen2_Overview.md)
11. [Azure Rbac Acl](azure/10-Azure_RBAC_ACL.md)
12. [Azure Types Of Storage](azure/11-Azure_Types_Of_Storage.md)
13. [Azure Storage Replication Strategies](azure/12-Azure_Storage_Replication_Strategies.md)
14. [Soft Delete Pitr Azure Storage](azure/13-Soft_Delete_PITR_Azure_Storage.md)
15. [Azure Shared Access Signature](azure/14-Azure_Shared_Access_Signature.md)
16. [Azure Lifetime Management Policies](azure/15-Azure_Lifetime_Management_Policies.md)
17. [Eventgrid Integration Azure](azure/16-EventGrid_Integration_Azure.md)
18. [Azure Encrpytion Standards](azure/17-Azure_Encrpytion_Standards.md)
19. [Azure+ Private Endpoints](azure/18-Azure+_Private_Endpoints.md)
20. [Cross Region Replication Azure](azure/19-Cross_Region_Replication_Azure.md)
21. [Azure Storage Rest Api](azure/20-Azure_Storage_Rest_API.md)
22. [Introduction Azure Data Factory](azure/21-Introduction_Azure_Data_Factory.md)
23. [Azure Data Factory Vs Synapse](azure/22-Azure_Data_Factory_vs_Synapse.md)
24. [Azure Data Factory Architecture](azure/23-Azure_Data_Factory_Architecture.md)

## Data-formats

2. [Data Format Deep Dive Pt1](data-formats/01-Data_Format_Deep_Dive_Pt1.md)
3. [Parquet Format Internals](data-formats/02-Parquet_Format_Internals.md)

## Databricks

2. [Azure Databricks Uc Creation](databricks/01-Azure_Databricks_UC_Creation.md)
3. [Databricks Uc Introduction](databricks/02-Databricks_UC_Introduction.md)
4. [Databricks Managed External Tables Hive](databricks/03-Databricks_Managed_External_Tables_Hive.md)
5. [Uc External Location Storage Credentials](databricks/04-UC_External_Location_Storage_Credentials.md)
6. [Databricks Managed Location Catalog Schema Level](databricks/05-Databricks_Managed_Location_Catalog_Schema_Level.md)
7. [Ctas Deep Clone Shallow Clone Databricks](databricks/06-CTAS_Deep_Clone_Shallow_Clone_Databricks.md)
8. [Rbac Custom Roles Serviceprincipals](databricks/07-RBAC_Custom_Roles_ServicePrincipals.md)
9. [Deletion Vectors Delta Lake](databricks/08-Deletion_Vectors_Delta_lake.md)
10. [Liquid Clustering Delta Lake](databricks/09-Liquid_Clustering_Delta_Lake.md)
11. [Concurrency Liquid Clustering](databricks/10-Concurrency_Liquid_Clustering.md)
12. [Copy Into Databricks](databricks/11-Copy_Into_Databricks.md)
13. [Autoloader Databricks](databricks/12-AutoLoader_Databricks.md)
14. [Intro Databricks Lakeflow Declarative Pipelines](databricks/13-Intro_Databricks_Lakeflow_Declarative_Pipelines.md)
15. [Dlt Batch Vs Streaming Workloads](databricks/14-DLT_Batch_Vs_Streaming_Workloads.md)
16. [Dlt Data Storage Checkpoints](databricks/15-DLT_Data_Storage_Checkpoints.md)
17. [Databricks Secret Scopes](databricks/16-Databricks_Secret_Scopes.md)
18. [Databricks Controlplane Dataplane](databricks/17-Databricks_ControlPlane_DataPlane.md)
19. [Databricks Dlt Code Walkthrough](databricks/18-Databricks_DLT_Code_Walkthrough.md)
20. [Databricks Serverless Compute](databricks/19-Databricks_Serverless_Compute.md)
21. [Databricks Warehouses](databricks/20-Databricks_Warehouses.md)
22. [Databricks Lakehouse Federation](databricks/21-Databricks_Lakehouse_Federation.md)
23. [Databricks Metrics Views](databricks/22-Databricks_Metrics_Views.md)
24. [Databricks Streaming Materialized Views Sql](databricks/23-Databricks_Streaming_Materialized_Views_SQL.md)
25. [Databricks Cli Setup](databricks/24-Databricks_CLI_Setup.md)

## Scenarios


### Spark

2. [Smj Spill To Disk Q1](scenarios/spark/01-SMJ_Spill_To_Disk_Q1.md)
3. [Smj Spill To Disk Q2](scenarios/spark/02-SMJ_Spill_To_Disk_Q2.md)
4. [Smj Output During Spill Q3](scenarios/spark/03-SMJ_Output_During_Spill_Q3.md)
5. [Cross Vs Broadcast Join](scenarios/spark/04-Cross_vs_Broadcast_Join.md)

## Spark

2. [Spark Architecture Yarn](spark/01-Spark_Architecture_YARN.md)
3. [Spark Driver Oom](spark/02-Spark_Driver_OOM.md)
4. [Types Of Memory Spark](spark/03-Types_Of_Memory_Spark.md)
5. [Spark Dynamic Partition Pruning](spark/04-Spark_Dynamic_Partition_Pruning.md)
6. [Spark Salting Technique](spark/05-Spark_Salting_Technique.md)
7. [What Is Spark](spark/06-What_Is_Spark.md)
8. [Why Apache Spark](spark/07-Why_Apache_Spark.md)
9. [Hadoop Vs Spark](spark/08-Hadoop_Vs_Spark.md)
10. [Spark Ecosystem](spark/09-Spark_Ecosystem.md)
11. [Spark Ecosystem](spark/10-Spark_Ecosystem.md)
12. [Spark Architecture](spark/11-Spark_Architecture.md)
13. [Schema In Spark](spark/12-Schema_In_Spark.md)
14. [Handling Corrupt Records Spark](spark/13-Handling_Corrupt_Records_Spark.md)
15. [Spark Transformations Actions](spark/14-Spark_Transformations_Actions.md)
16. [Spark Dag Lazy Eval](spark/15-Spark_DAG_Lazy_Eval.md)
17. [Spark Json Data](spark/16-Spark_JSON_Data.md)
18. [Spark Sql Engine](spark/17-Spark_SQL_Engine.md)
19. [Spark Rdd](spark/18-Spark_RDD.md)
20. [Spark Writing Data Disk](spark/19-Spark_Writing_Data_Disk.md)
21. [Spark Partitioning Bucketing](spark/20-Spark_Partitioning_Bucketing.md)
22. [Spark Session Vs Context](spark/21-Spark_Session_vs_Context.md)
23. [Spark Job Stage Task](spark/22-Spark_Job_Stage_Task.md)
24. [Spark Transformations](spark/23-Spark_Transformations.md)
25. [Spark Union Vs Unionall](spark/24-Spark_Union_vs_UnionAll.md)
26. [Spark Repartition Vs Coalesce](spark/25-Spark_Repartition_vs_Coalesce.md)
27. [Spark Case When](spark/26-Spark_Case_When.md)
28. [Spark Unique Sorted Records](spark/27-Spark_Unique_Sorted_Records.md)
29. [Spark Agg Functions](spark/28-Spark_Agg_Functions.md)
30. [Spark Group By](spark/30-Spark_Group_By.md)
31. [Spark Joins Intro](spark/31-Spark_Joins_Intro.md)
32. [Spark Join Strategies](spark/32-Spark_Join_Strategies.md)
33. [Spark Window Functions](spark/33-Spark_Window_Functions.md)
34. [Spark Memory Management](spark/34-Spark_Memory_Management.md)
35. [Spark Executor Oom](spark/35-Spark_Executor_OOM.md)
36. [Spark Submit Command](spark/36-Spark_Submit_Command.md)
37. [Spark Deployment Modes](spark/37-Spark_Deployment_Modes.md)
38. [Spark Adaptive Query Execution](spark/38-Spark_Adaptive_Query_Execution.md)
39. [Spark Dynamic Resource Allocation](spark/39-Spark_Dynamic_Resource_Allocation.md)
40. [Spark Dynamic Partition Pruning](spark/40-Spark_Dynamic_Partition_Pruning.md)

## Streaming


### Architecture

2. [Use Cases Streaming](streaming/architecture/01-Use_Cases_Streaming.md)
3. [Redpanda Vs Kafka Arch Differences](streaming/architecture/02-Redpanda_vs_Kafka_Arch_Differences.md)
4. [Redpanda Architure In Depth Pt1](streaming/architecture/03-Redpanda_Architure_In_Depth_Pt1.md)

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
<!-- TOC END -->


