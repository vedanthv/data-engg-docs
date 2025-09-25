# Data Engineering and Cloud Platform Knowledge Base

This repository is where I keep track of what I’m learning and experimenting with across data engineering, distributed systems, and cloud platforms. It’s part study notes, part code lab, and part reference guide — essentially a place to capture concepts as I work through them and to revisit later when I need a refresher.

I focus on technologies like Apache Spark, Kafka/Redpanda, Databricks, AWS, and Azure, along with supporting tools and practices that are important for building reliable data systems. You’ll find a mix of summaries, deep dives into tricky concepts, performance tuning notes, and small experiments that test how things work in practice.

The main goal of this repo is to strengthen my own understanding, but I also hope it can be useful to anyone else navigating similar topics. Think of it as a learning log that balances hands-on exploration with professional best practices - something between a personal notebook and a practical guide.

<!-- TOC START -->
# 📑 Table of Contents

## Outline of Sections 
- Azure
- Data-formats
- Databricks
- Scenarios
- Spark
- Streaming

## Activities-pipelines

1. [Simplecopydata](notebooks/adf/activities-pipelines/00-simpleCopyData.json)
2. [Eventtriggerschedule](notebooks/adf/activities-pipelines/01-eventTriggerSchedule.json)
3. [Filteractivityarray](notebooks/adf/activities-pipelines/02-filterActivityArray.json)
4. [Foreach](notebooks/adf/activities-pipelines/03-forEach.json)
5. [Masterchilddependency](notebooks/adf/activities-pipelines/04-masterChildDependency.json)
6. [Metadataactivity](notebooks/adf/activities-pipelines/05-metaDataActivity.json)
7. [Parameterizedpipeline](notebooks/adf/activities-pipelines/06-parameterizedPipeline.json)
8. [Set Append Activity](notebooks/adf/activities-pipelines/07-set-append-activity.json)
9. [Switchactivity](notebooks/adf/activities-pipelines/08-switchActivity.json)
10. [Systemvariables](notebooks/adf/activities-pipelines/09-systemVariables.json)
11. [Untilactivity](notebooks/adf/activities-pipelines/10-untilActivity.json)

## Adf


## Architecture

1. [Use Cases Streaming](streaming/architecture/01-Use_Cases_Streaming.md)
2. [Redpanda Vs Kafka Arch Differences](streaming/architecture/02-Redpanda_vs_Kafka_Arch_Differences.md)
3. [Redpanda Architure In Depth Pt1](streaming/architecture/03-Redpanda_Architure_In_Depth_Pt1.md)

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

## Data

1. [Emp](notebooks/spark/data/emp.csv)
2. [Emp New](notebooks/spark/data/emp_new.csv)
3. [Order Multiline](notebooks/spark/data/order_multiline.json)
4. [Order Singleline](notebooks/spark/data/order_singleline.json)

## Data-formats

1. [Data Format Deep Dive Pt1](data-formats/01-Data_Format_Deep_Dive_Pt1.md)

## Databricks

1. [Azure Databricks Uc Creation](databricks/01-Azure_Databricks_UC_Creation.md)
2. [Databricks Uc Introduction](databricks/02-Databricks_UC_Introduction.md)
3. [Databricks Managed External Tables Hive](databricks/03-Databricks_Managed_External_Tables_Hive.md)
4. [Uc External Location Storage Credentials](databricks/04-UC_External_Location_Storage_Credentials.md)
5. [Databricks Managed Location Catalog Schema Level](databricks/05-Databricks_Managed_Location_Catalog_Schema_Level.md)
6. [Ctas Deep Clone Shallow Clone Databricks](databricks/06-CTAS_Deep_Clone_Shallow_Clone_Databricks.md)
7. [Rbac Custom Roles Serviceprincipals](databricks/07-RBAC_Custom_Roles_ServicePrincipals.md)
8. [Deletion Vectors Delta Lake](databricks/08-Deletion_Vectors_Delta_lake.md)
9. [Liquid Clustering Delta Lake](databricks/09-Liquid_Clustering_Delta_Lake.md)
10. [Concurrency Liquid Clustering](databricks/10-Concurrency_Liquid_Clustering.md)
11. [Copy Into Databricks](databricks/11-Copy_Into_Databricks.md)
12. [Autoloader Databricks](databricks/12-AutoLoader_Databricks.md)
13. [Intro Databricks Lakeflow Declarative Pipelines](databricks/13-Intro_Databricks_Lakeflow_Declarative_Pipelines.md)
14. [Dlt Batch Vs Streaming Workloads](databricks/14-DLT_Batch_Vs_Streaming_Workloads.md)
15. [Dlt Data Storage Checkpoints](databricks/15-DLT_Data_Storage_Checkpoints.md)
16. [Databricks Secret Scopes](databricks/16-Databricks_Secret_Scopes.md)
17. [Databricks Controlplane Dataplane](databricks/17-Databricks_ControlPlane_DataPlane.md)
18. [Databricks Dlt Code Walkthrough](databricks/18-Databricks_DLT_Code_Walkthrough.md)
19. [Databricks Serverless Compute](databricks/19-Databricks_Serverless_Compute.md)
20. [Databricks Warehouses](databricks/20-Databricks_Warehouses.md)
21. [Databricks Lakehouse Federation](databricks/21-Databricks_Lakehouse_Federation.md)
22. [Databricks Metrics Views](databricks/22-Databricks_Metrics_Views.md)
23. [Databricks Streaming Materialized Views Sql](databricks/23-Databricks_Streaming_Materialized_Views_SQL.md)
24. [Databricks Cli Setup](databricks/24-Databricks_CLI_Setup.md)

## Databricks

1. [Auto Loader Normal Schema Evolution](notebooks/databricks/Auto Loader  Normal Schema Evolution.ipynb)
2. [Auto Loader Rescue Mode](notebooks/databricks/Auto Loader rescue mode.ipynb)
3. [Column Level Masking](notebooks/databricks/Column Level Masking.ipynb)
4. [Delta Live Tables](notebooks/databricks/Delta Live Tables.ipynb)
5. [Row Level Filters](notebooks/databricks/Row Level Filters.dbc)
6. [User Defined Functions](notebooks/databricks/User Defined Functions.ipynb)
7. [Working With Json](notebooks/databricks/Working with JSON.ipynb)

## Kafka

1. [.env](notebooks/kafka/.env)
2. [Dockerfile](notebooks/kafka/Dockerfile)
3. [Readme](notebooks/kafka/README.md)
4. [Docker Compose](notebooks/kafka/docker-compose.yml)
5. [Requirements](notebooks/kafka/requirements.txt)

## Kafka

1. [Kafka Kraft Setup](streaming/kafka/01-Kafka_KRaft_Setup.md)
2. [Kafka Broker Properties](streaming/kafka/02-Kafka_Broker_Properties.md)
3. [Topic Default Properties](streaming/kafka/03-Topic_Default_Properties.md)
4. [Kafka Hardware Considerations](streaming/kafka/04-Kafka_Hardware_Considerations.md)
5. [Kafka Configuring Clusters Broker Consideration](streaming/kafka/05-Kafka_Configuring_Clusters_Broker_Consideration.md)
6. [Kafka Broker Os Tuning](streaming/kafka/06-Kafka_Broker_OS_Tuning.md)
7. [Kafka Os Tuning Dirty Page Handling](streaming/kafka/07-Kafka_OS_Tuning_Dirty_Page_Handling.md)
8. [Kafka File Descriptors Overcommit Memory](streaming/kafka/08-Kafka_File_Descriptors_Overcommit_Memory.md)
9. [Kafka Production Concerns](streaming/kafka/09-Kafka_Production_Concerns.md)

## Scenario-based-pipelines

1. [Webhookemailsimple](notebooks/adf/scenario-based-pipelines/00-webhookEmailSimple.json)
2. [Sqlserverlookupactivity](notebooks/adf/scenario-based-pipelines/01-sqlServerLookupActivity.json)
3. [Storedprocedurelookupactivity](notebooks/adf/scenario-based-pipelines/02-storedProcedureLookupActivity.json)
4. [Readme](notebooks/adf/scenario-based-pipelines/README.md)

## Scenarios


## Spark

1. [00 Installing Spark](notebooks/spark/00_Installing_Spark.ipynb)
2. [02 Transformationsptii](notebooks/spark/02_TransformationsPtII.ipynb)
3. [03 Transformationsptiii](notebooks/spark/03_TransformationsPtIII.ipynb)
4. [04 Strings Dates](notebooks/spark/04_Strings_Dates.ipynb)
5. [05 Union Unionall Aggregations](notebooks/spark/05_Union_UnionAll_Aggregations.ipynb)
6. [06 Window Functions](notebooks/spark/06_Window_Functions.ipynb)
7. [07 Repartitioning Coalesce Joins](notebooks/spark/07_Repartitioning_Coalesce_Joins.ipynb)
8. [08 Readformats Handlingerronousrecords](notebooks/spark/08_ReadFormats_HandlingErronousRecords.ipynb)
9. [09 Complexfileformats](notebooks/spark/09_ComplexFileFormats.ipynb)
10. [10 Working With Json Data](notebooks/spark/10_Working_With_Json_Data.ipynb)
11. [11 Writing Data Spark](notebooks/spark/11_Writing_Data_Spark.ipynb)
12. [12 Spark Udfs](notebooks/spark/12_Spark_UDFs.ipynb)
13. [13 Spark Dag Ui](notebooks/spark/13_Spark_DAG_UI.ipynb)
14. [14 Optimizingshuffles](notebooks/spark/14_OptimizingShuffles.ipynb)
15. [16 Cache Persist Techniques](notebooks/spark/16_Cache_Persist_Techniques.ipynb)
16. [21 Broadcastvariables Accumulators](notebooks/spark/21_BroadCastVariables_Accumulators.ipynb)
17. [22 Join Optimizations](notebooks/spark/22_Join_Optimizations.ipynb)
18. [22 Join Optimizations Pt2](notebooks/spark/22_Join_Optimizations_Pt2.ipynb)
19. [23 Dynamic Static Resource Allocation](notebooks/spark/23_Dynamic_Static_Resource_Allocation.ipynb)
20. [24 Skewness And Salting](notebooks/spark/24_Skewness_And_Salting.ipynb)
21. [Notes](notebooks/spark/notes.md)

## Spark

1. [Smj Spill To Disk Q1](scenarios/spark/01-SMJ_Spill_To_Disk_Q1.md)
2. [Smj Spill To Disk Q2](scenarios/spark/02-SMJ_Spill_To_Disk_Q2.md)
3. [Smj Output During Spill Q3](scenarios/spark/03-SMJ_Output_During_Spill_Q3.md)
4. [Cross Vs Broadcast Join](scenarios/spark/04-Cross_vs_Broadcast_Join.md)

## Spark

1. [Spark Architecture Yarn](spark/01-Spark_Architecture_YARN.md)
2. [Spark Driver Oom](spark/02-Spark_Driver_OOM.md)
3. [Types Of Memory Spark](spark/03-Types_Of_Memory_Spark.md)
4. [Spark Dynamic Partition Pruning](spark/04-Spark_Dynamic_Partition_Pruning.md)
5. [Spark Salting Technique](spark/05-Spark_Salting_Technique.md)

## Src

1. [Admin](notebooks/kafka/src/admin.py)
2. [Avro Consumer](notebooks/kafka/src/avro_consumer.py)
3. [Avro Producer](notebooks/kafka/src/avro_producer.py)
4. [Consumer](notebooks/kafka/src/consumer.py)
5. [Json Producer](notebooks/kafka/src/json_producer.py)
6. [Producer](notebooks/kafka/src/producer.py)
7. [Register Avro Schema](notebooks/kafka/src/register_avro_schema.py)
8. [Schema](notebooks/kafka/src/schema.avro)
9. [Utils](notebooks/kafka/src/utils.py)

## Streaming

<!-- TOC END -->


