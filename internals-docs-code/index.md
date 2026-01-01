# Data Engineering and Cloud Platform Knowledge Base

This repository is where I keep track of what I’m learning and experimenting with across data engineering, distributed systems, and cloud platforms. It’s part study notes, part code lab, and part reference guide — essentially a place to capture concepts as I work through them and to revisit later when I need a refresher.

I focus on technologies like Apache Spark, Kafka/Redpanda, Databricks, AWS, and Azure, along with supporting tools and practices that are important for building reliable data systems. You’ll find a mix of summaries, deep dives into tricky concepts, performance tuning notes, and small experiments that test how things work in practice.

The main goal of this repo is to strengthen my own understanding, but I also hope it can be useful to anyone else navigating similar topics. Think of it as a learning log that balances hands-on exploration with professional best practices - something between a personal notebook and a practical guide.

<!-- TOC START -->
# 📑 Data Engineering Knowledge Base


## Airflow

1. [What Is Airflow](airflow/00-What_Is_Airflow.md)
2. [Airflow Vs Databricks Jobs](airflow/01-Airflow_vs_Databricks_Jobs.md)
3. [Building Blocks Airflow](airflow/02-Building_Blocks_Airflow.md)
4. [Airflow Arch Metadata Db](airflow/03-Airflow_Arch_Metadata_DB.md)
5. [Lifecycle Of Dag Run](airflow/04-Lifecycle_Of_DAG_Run.md)
6. [Airflow Scheduler Deepdive](airflow/05-Airflow_Scheduler_DeepDive.md)
7. [Index](airflow/index.md)

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
25. [Adf Parameters](azure/25-ADF_Parameters.md)
26. [Index](azure/index.md)

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

## Docs-deep-dive


### Databricks

1. [What Is Lakehouse](docs-deep-dive/databricks/00-What_Is_Lakehouse.md)
2. [Lakehouse Vs Delta Lake Vs Warehouse](docs-deep-dive/databricks/01-Lakehouse_vs_Delta_Lake_vs_Warehouse.md)
3. [All Delta Things Databricks](docs-deep-dive/databricks/02-All_Delta_Things_Databricks.md)
4. [High Level Architecture](docs-deep-dive/databricks/03-High_Level_Architecture.md)
5. [Databricks Acid Guarantees](docs-deep-dive/databricks/04-Databricks_ACID_Guarantees.md)
6. [Databricks Medallion Architecture](docs-deep-dive/databricks/05-Databricks_Medallion_Architecture.md)
7. [Databricks Single Source Of Truth Arch](docs-deep-dive/databricks/06-Databricks_Single_Source_Of_Truth_Arch.md)
8. [Databricks Scope Of Lakehouse Arch](docs-deep-dive/databricks/07-Databricks_Scope_Of_Lakehouse_Arch.md)
9. [Databricks Architecture Guiding Principles](docs-deep-dive/databricks/08-Databricks_Architecture_Guiding_Principles.md)
10. [Databricks Objects Catalogs](docs-deep-dive/databricks/09-Databricks_Objects_Catalogs.md)
11. [Databricks Objects Volumes Tables](docs-deep-dive/databricks/10-Databricks_Objects_Volumes_Tables.md)
12. [Databricks Views](docs-deep-dive/databricks/11-Databricks_Views.md)
13. [Databricks Governed Tags](docs-deep-dive/databricks/12-Databricks_Governed_Tags.md)
14. [Databricks Connecting To Cloud Object Storage Intro](docs-deep-dive/databricks/13-Databricks_Connecting_To_Cloud_Object_Storage_Intro.md)
15. [Databricks Managed Storage Location Hierarchy](docs-deep-dive/databricks/14-Databricks_Managed_Storage_Location_Hierarchy.md)
16. [Databricks Service Credentials](docs-deep-dive/databricks/15-Databricks_Service_Credentials.md)
17. [Databricks Connecting To Managed Ingestion Sources Intro](docs-deep-dive/databricks/16-Databricks_Connecting_To_Managed_Ingestion_Sources_Intro.md)
18. [Databricks Query Federation](docs-deep-dive/databricks/17-Databricks_Query_Federation.md)
19. [Image](docs-deep-dive/databricks/image.png)

## Scenarios

1. [Index](scenarios/index.md)

### Adf

1. [Architectures](scenarios/adf/architectures.md)

### Databricks

1. [Aws Reference Arch Databricks](scenarios/databricks/00-AWS_Reference_Arch_Databricks.md)
2. [Reference Architectures Pt1](scenarios/databricks/01-Reference_Architectures_Pt1.md)
3. [Index](scenarios/databricks/index.md)

### Kafka

1. [Why Closed Segments Files Open](scenarios/kafka/00-Why_Closed_Segments_Files_Open.md)
2. [How Does Producer Guarantee Exactly Once](scenarios/kafka/01-How_Does_Producer_Guarantee_Exactly_Once.md)
3. [Does Seq No Remain Same After Producer Goes Down](scenarios/kafka/02-Does_Seq_No_Remain_Same_After_Producer_Goes_Down.md)
4. [What Happens When Reelection Happens](scenarios/kafka/03-What_Happens_When_ReElection_Happens.md)
5. [Give Walkthrough Of Leader Epoch Log Truncation](scenarios/kafka/04-Give_Walkthrough_Of_Leader_Epoch_Log_Truncation.md)
6. [Explain Diff Dirtyratio Dirtybackgroundratio](scenarios/kafka/05-Explain_Diff_dirtyRatio_dirtyBackgroundRatio.md)
7. [Are Kafka Consumers Thread Safe](scenarios/kafka/06-Are_Kafka_Consumers_Thread_Safe.md)
8. [Is Retention Ms Defined Partition Level](scenarios/kafka/07-Is_Retention_ms_Defined_Partition_Level.md)
9. [Difference Btwn Sticky Cooperative Sticky Assignor](scenarios/kafka/08-Difference_Btwn_Sticky_Cooperative_Sticky_Assignor.md)
10. [How Does Kafka Ensure Partial Idempotence](scenarios/kafka/09-How_Does_Kafka_Ensure_Partial_Idempotence.md)
11. [How Does Kafka Know Which Messages Are Processed Not Just Read](scenarios/kafka/10-How_Does_Kafka_Know_Which_Messages_Are_Processed_Not_Just_Read.md)
12. [Index](scenarios/kafka/index.md)

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
40. [Spark Executor Tuning](spark/41-Spark_Executor_Tuning.md)
41. [Index](spark/index.md)

## Streaming

1. [Index](streaming/index.md)

### Architecture

2. [Use Cases Streaming](streaming/architecture/01-Use_Cases_Streaming.md)
3. [Redpanda Vs Kafka Arch Differences](streaming/architecture/02-Redpanda_vs_Kafka_Arch_Differences.md)
4. [Redpanda Architure In Depth Pt1](streaming/architecture/03-Redpanda_Architure_In_Depth_Pt1.md)
5. [Index](streaming/architecture/index.md)

### Flink

1. [Introduction To Flink](streaming/flink/00-Introduction_To_Flink.md)
2. [Jobmanager In Flink](streaming/flink/01-JobManager_In_Flink.md)
3. [Taskmanager In Flink](streaming/flink/02-TaskManager_In_Flink.md)
4. [Slots Vs Cores Flink Tm](streaming/flink/03-Slots_vs_Cores_Flink_TM.md)
5. [Operating Chaining Flink](streaming/flink/04-Operating_Chaining_Flink.md)
6. [Stateful Streaming Flink Pt1](streaming/flink/05-Stateful_Streaming_Flink_Pt1.md)
7. [Processing Vs Event Time Flink](streaming/flink/06-Processing_vs_Event_Time_Flink.md)
8. [Checkpoints Savepoints Flink](streaming/flink/07-Checkpoints_Savepoints_Flink.md)
9. [Stateful Upgrades Flink](streaming/flink/08-Stateful_Upgrades_Flink.md)

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
23. [Kafka Configuring Consumers Pt1](streaming/kafka/22-Kafka_Configuring_Consumers_Pt1.md)
24. [Kafka Configuring Consumers Pt2](streaming/kafka/23-Kafka_Configuring_Consumers_Pt2.md)
25. [Kafka Partition Assignment Strategies](streaming/kafka/24-Kafka_Partition_Assignment_Strategies.md)
26. [Kafka Commits Offsets Intro](streaming/kafka/25-Kafka_Commits_Offsets_Intro.md)
27. [Kafka Types Of Commits](streaming/kafka/26-Kafka_Types_Of_Commits.md)
28. [Kafka Rebalance Listeners](streaming/kafka/27-Kafka_Rebalance_Listeners.md)
29. [Kafka Consuming Records With Spec Offset](streaming/kafka/28-Kafka_Consuming_Records_With_Spec_Offset.md)
30. [Kafka Exiting Consumer Poll Loop](streaming/kafka/29-Kafka_Exiting_Consumer_Poll_Loop.md)
31. [Kafka Deserialisers](streaming/kafka/30-Kafka_Deserialisers.md)
32. [Kafka Standalone Consumers](streaming/kafka/31-Kafka_Standalone_Consumers.md)
33. [Kafka Internals Zookeeper](streaming/kafka/32-Kafka_Internals_Zookeeper.md)
34. [Kafka Raft Consensus Protocol](streaming/kafka/33-Kafka_Raft_Consensus_Protocol.md)
35. [Kafka Controller Quorum](streaming/kafka/34-Kafka_Controller_Quorum.md)
36. [Kafka Replication Concepts](streaming/kafka/35-Kafka_Replication_Concepts.md)
37. [Kafka Insync Outofsync Replicas](streaming/kafka/36-Kafka_InSync_OutOfSync_Replicas.md)
38. [Kafka Request Processing Pt1](streaming/kafka/37-Kafka_Request_Processing_Pt1.md)
39. [Kafka Request Processing Pt2 Produce Requests](streaming/kafka/38-Kafka_Request_Processing_Pt2_Produce_Requests.md)
40. [Kafka Fetch Requests Pt1](streaming/kafka/39-Kafka_Fetch_Requests_Pt1.md)
41. [Kafka Fetch Requests Pt2](streaming/kafka/40-Kafka_Fetch_Requests_Pt2.md)
42. [Kafka Physical Storage Introduction](streaming/kafka/41-Kafka_Physical_Storage_Introduction.md)
43. [Kafka Tiered Storage](streaming/kafka/42-Kafka_Tiered_Storage.md)
44. [Kafka Partition Allocation](streaming/kafka/43-Kafka_Partition_Allocation.md)
45. [Kafka File Formats Intro](streaming/kafka/44-Kafka_File_Formats_Intro.md)
46. [Kafka Message Batch Headers](streaming/kafka/45-Kafka_Message_Batch_Headers.md)
47. [Kafka Indexes](streaming/kafka/46-Kafka_Indexes.md)
48. [Kafka Compaction](streaming/kafka/47-Kafka_Compaction.md)
49. [Kafka Tombstoning Records](streaming/kafka/48-Kafka_Tombstoning_Records.md)
50. [Kafka Reliability Guarantees](streaming/kafka/49-Kafka_Reliability_Guarantees.md)
51. [Kafka Replication Procedures](streaming/kafka/50-Kafka_Replication_Procedures.md)
52. [Kafka Broker Config Replication Factor](streaming/kafka/51-Kafka_Broker_Config_Replication_Factor.md)
53. [Kafka Broker Configuration Unclean Leader Election](streaming/kafka/52-Kafka_Broker_Configuration_Unclean_Leader_Election.md)
54. [Kafka Log Truncation On Out Of Sync Leader](streaming/kafka/53-Kafka_Log_Truncation_On_Out_Of_Sync_Leader.md)
55. [Kafka Keeping Replicas In Sync](streaming/kafka/54-Kafka_Keeping_Replicas_In_Sync.md)
56. [Kafka Using Producers Reliable System Scenarios](streaming/kafka/55-Kafka_Using_Producers_Reliable_System_Scenarios.md)
57. [Kafka Producer Retries Additional Error Handling](streaming/kafka/56-Kafka_Producer_Retries_Additional_Error_Handling.md)
58. [Kafka Using Consumers In Reliable System Intro](streaming/kafka/57-Kafka_Using_Consumers_In_Reliable_System_Intro.md)
59. [Kafka Important Consumer Properties Intro](streaming/kafka/58-Kafka_Important_Consumer_Properties_Intro.md)
60. [Kafka Consumer Properties Pt2](streaming/kafka/59-Kafka_Consumer_Properties_Pt2.md)
61. [Kafka Explicitly Commiting Offsets Pt1](streaming/kafka/60-Kafka_Explicitly_Commiting_Offsets_Pt1.md)
62. [Kafka Explicitly Commiting Offsets Pt2](streaming/kafka/61-Kafka_Explicitly_Commiting_Offsets_Pt2.md)
63. [Kafka Validating Configuration](streaming/kafka/62-Kafka_Validating_Configuration.md)
64. [Kafka Monitoring In Production](streaming/kafka/63-Kafka_Monitoring_In_Production.md)
65. [Index](streaming/kafka/index.md)
<!-- TOC END -->


