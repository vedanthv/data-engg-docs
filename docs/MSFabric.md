## Microsoft Fabric 

## Section 1 : Introduction and Installation

### 1. Introduction

![image](https://github.com/user-attachments/assets/7c34baaa-fe51-4d01-b47e-34a19eb573e0)

![image](https://github.com/user-attachments/assets/0bf7b0ad-55f1-4744-a6d9-98bdfb9ac455)

### 2. Pre Requisites

![image](https://github.com/user-attachments/assets/7eb5d4bc-accd-44f9-a276-11acfb8a3f5b)

### 3. Project Architecture

![image](https://github.com/user-attachments/assets/10271b70-df84-4690-a1ac-1d0b823aca45)

![image](https://github.com/user-attachments/assets/73e21ba7-23e7-4d80-ba87-617384b8de4f)

![image](https://github.com/user-attachments/assets/39a6f9d6-7842-4401-8f02-486ea80b82ce)

### 4. Installation

- Ensure Hierarchial namespace enabled to create Azure Data Lake Storage Gen2 resource.
- We dont get charged for Synapse Analytics until we create compute.

#### Create Spark Pool

Spark Pool Settings

![image](https://github.com/user-attachments/assets/047a5c38-a11d-45d4-bf17-dd8330253305)

## Section 2 : Understanding Microsoft Fabric

### 5. Evolution of Architecture

![image](https://github.com/user-attachments/assets/155a9882-97a7-4cbd-a37b-720b8b04e2fb)

Metadata caching layer brings ACID properties.

### 6. Delta Lake Structure

![image](https://github.com/user-attachments/assets/5103715a-10a1-483c-a784-b02d0932867d)

![image](https://github.com/user-attachments/assets/c9d5b8eb-e2b9-4d2d-a202-3406834797c4)

![image](https://github.com/user-attachments/assets/259e096d-ebe7-49ba-9547-9a9749b7ad6c)

**What happens under the hood?**

![image](https://github.com/user-attachments/assets/cf9707b4-395e-40cd-b714-17ea79e1bab2)

### 7. Why Fabric?

![image](https://github.com/user-attachments/assets/b226825b-0465-45e6-81f4-18a1ac18b586)

Lot of services need to be created individually.

![image](https://github.com/user-attachments/assets/617423df-80b0-4979-ab03-b15a142df5a9)

![image](https://github.com/user-attachments/assets/91ef44d2-1b7a-4312-96f7-0e9b1a7ecd1e)

### 8. Starting Up Fabric

- Login to fabric with Microsoft entra id account for free trial.
- Go to Settings -> Admin Portal -> enable fabric

### 9. Licensing and Costs

![image](https://github.com/user-attachments/assets/fbadcf29-9e2c-4ec0-8aa7-d47596d1563f)

![image](https://github.com/user-attachments/assets/f936326d-f986-4073-88fc-42bb49f488c5)

![image](https://github.com/user-attachments/assets/d8eb0744-db7f-435a-a934-b9ecf9b41d4a)

Creating Azure Capacity

[Microsoft Official Link](https://learn.microsoft.com/en-gb/fabric/enterprise/buy-subscription)

If you are not able to select subscription follow these steps

- If you can open the subscription but not perform actions:

- Go to Azure Portal > Subscriptions

- Click on the subscription

- Go to Access Control (IAM) > Role Assignments

- Filter by Role = Owner

- You’ll see a list of users, groups, or service principals who are assigned the “Owner” role.

### 10. Fabric Terms

![image](https://github.com/user-attachments/assets/6b106735-7552-40e4-92c6-981799188b78)

Example

![image](https://github.com/user-attachments/assets/ea624065-8cf1-4ae6-a52e-e6a49016b0ac)

### 11. OneLake in Fabric

Data is stored in One data lake based on the workspace names.

There is only one storage point.

![image](https://github.com/user-attachments/assets/7de4af18-ffee-4349-81e5-077ea964aaeb)

We will have only one copy of data and nothing is duplicated.

The files are stored in parquet metadata powered by delta lake.

### 12. One Copy for all computes

All engines store data in One Lake.

![image](https://github.com/user-attachments/assets/8d81d3e9-9b42-4806-9ad6-b137c84579f9)

All data stored in delta parquet format.

## Section 3 : Fabric Lakehouse

### 13. Microsoft Fabric Workspaces

![image](https://github.com/user-attachments/assets/af9bbffc-13bf-468a-b512-1116a40bbc9f)

### 14. Workspace Roles

![image](https://github.com/user-attachments/assets/a9947c7c-7a84-427f-ad55-c3ef9d26544b)

### 15. Creating a Lakehouse

When we create a Lakehouse there are three things:

![image](https://github.com/user-attachments/assets/b728c87a-6d3c-44c1-ae1a-5a463a5ce73c)

Lakehouse - data platform to store the data.

Semantic Model - Dataset to present to powerbi.

SQL Endpoint - we can run queries.

### 16. Lakehouse Explorer

![image](https://github.com/user-attachments/assets/ee727432-a078-47a8-9703-585519e4b696)

Data Uploaded to table

![image](https://github.com/user-attachments/assets/18d37644-fba7-4b13-8464-08ddf8d88496)

Table created from the file

![image](https://github.com/user-attachments/assets/bf739a69-0d03-473a-bab5-a40308ba275f)

Files are stored in parquet with delta log

![image](https://github.com/user-attachments/assets/6a48dcb6-d2ab-4fcc-b095-c8764f92a49e)

Here is delta log info
![image](https://github.com/user-attachments/assets/c9441de4-89cd-407c-a2ad-1f433abf438e)

On clicking properties we can see if its managed or not.

![image](https://github.com/user-attachments/assets/ecb5ea00-99f2-4774-a51a-07e99a0d410a)

### 17. SQL Analytics Endpoint

We can only read data from this enpoint not write / update.

![image](https://github.com/user-attachments/assets/477346d2-6a2c-4349-aee2-508b41531770)

We can create views

![image](https://github.com/user-attachments/assets/a7d64053-b50a-4eb8-8f36-e366462bc167)

### 18. Default Semantic Model View

![image](https://github.com/user-attachments/assets/a3689d2c-eada-4cb7-8944-8dfe5fa1728c)

![image](https://github.com/user-attachments/assets/5e9409fe-741c-43cf-a325-16597edb3782)

In the context of the semantic model in Microsoft Fabric lakehouse, the semantic model itself doesn't directly store raw data. Instead, it provides a logical, structured view of the data stored in the underlying data lake or warehouse.

The semantic model acts as an abstraction layer that organizes and simplifies access to the data, making it easier for reporting and analysis tools to query the data efficiently. The raw data is stored in the data lake or data warehouse, and the semantic model helps to structure and shape this data into meaningful formats suitable for analysis and reporting.

## Section 4 : Data Factory in Fabric

### 19. How to Load data in Lakehouse 

![image](https://github.com/user-attachments/assets/c6ffa031-73fc-41d3-9c90-55af9b85cf3a)

### 20. Fabric vs Azure Data Factory

![image](https://github.com/user-attachments/assets/73beab74-d8a7-4968-a734-5ab28f81b536)

### 21. Data Gateway Types

- Gateway connects two networks

![image](https://github.com/user-attachments/assets/fdcb28e4-76c0-45ac-a248-f3c15d3a2708)

Imagine you have a big box of toys at home, and you want to show them to your friends who live far away. You have two ways to show them: one way is through a special window, and the other way is to use a delivery truck.

**On-Premise Data Gateway (like a special window):**

This is like a window that you open to let your friends see your toys without taking them out of the box. It connects your toys (data) at home to an online game or app that your friends are using. You can think of this as a way to share data that's stored in your house but don't let your friends take it out or change it. It keeps your toys safe inside but lets you show them off.

**VNet Data Gateway (like a delivery truck):**

This method is like using a delivery truck to send some of your toys to your friends' houses. The VNet (Virtual Network) is a big, secure road that connects your house and your friends' houses. When you use this truck, you're moving data across this secure road, allowing your friends to actually play with the toys (data) over at their place, but still keeping it safe and controlled.
So, in simple terms, the on-premise data gateway lets you show your toys to friends securely while they are still at home, and the VNet data gateway lets you share some toys by sending them out safely to your friend's houses.

![image](https://github.com/user-attachments/assets/c42ed06c-7d4a-4d4e-bbf3-603290e4e1cc)

![image](https://github.com/user-attachments/assets/7d38f9d9-f925-4b43-9280-8d582acb5db0)

![image](https://github.com/user-attachments/assets/2873af2a-5ef8-48ef-a7de-ecd16bff993d)

### 22. Connections

![image](https://github.com/user-attachments/assets/35031f0b-a5a4-4c43-80fd-e48b8d1705a3)

Click Gear Icon -> Manage Connections and Gateways

![image](https://github.com/user-attachments/assets/78e1c5f4-cad0-4c81-af0f-75ff4c2f179a)

- Gateway : Equivalent to Integration Runtime in ADF
- Connection : Similar to Linked Service in ADF

### 23. Creating Pipeline

Step 1 : Lookup Activity to query the SQL connecte ddatabase

![image](https://github.com/user-attachments/assets/55a1c0f3-ed62-48b8-aea9-edb3b214f13a)

Step 2 : Foreach activity to go over both tables

![image](https://github.com/user-attachments/assets/36095c7e-d67b-40d7-8d43-5389fcab9604)

Step 3 : For each iteration run copy data activity

![image](https://github.com/user-attachments/assets/53246f88-ec3d-476e-9cca-a34f89c2e5dd)

Destination : Our Onelake data lakehouse

![image](https://github.com/user-attachments/assets/c1bb5fa8-4e6a-4838-be3d-9fdd20962072)

### 24. Dataflow Gen2

![image](https://github.com/user-attachments/assets/75c29c43-44aa-4e96-ae2d-508d1339bd54)

Adding Data Source to Dataflow Gen 2

![image](https://github.com/user-attachments/assets/c3ba3e23-5d04-46d2-b13d-a578b1910943)

Alice here has Blob Storage Contributor role that can be granted in container screen.

![image](https://github.com/user-attachments/assets/8a361494-7f49-4199-86f2-ef467da1ba5e)

Click Combine

![image](https://github.com/user-attachments/assets/8e675945-0ff9-441c-b99d-54e22a159da7)

Click Add Column -> Custom Column

![image](https://github.com/user-attachments/assets/0aba5b70-e335-4cf5-8ddd-91fde9de6c69)

```
if [State] = "CA" then "California" else if 
[State] = "NJ" then "New Jersey" else if
[State] = "FL" then "Florida"
else [State]
```

Click Add Destination -> Lakehouse

![image](https://github.com/user-attachments/assets/20c35d27-bfad-43fe-8b91-ae238d6a03b4)

Next Go to Home -> Save and Run, refresh should automatically start

We should be able to see the data once refresh is completed.

![image](https://github.com/user-attachments/assets/7d0f6ce2-87f1-4e29-b85b-3ce3a1c72007)

## Section 5 : Fabric One Lake

### 25. Shortcuts in Fabric

Shortcuts can be created only at OneLake level.

Let's say finance team wants data from marketing lakehouse.

They can create a shortcut to the marketing lakehouse without copying the data.

The data is refreshed/updated automatically.

![image](https://github.com/user-attachments/assets/40a74d56-44f7-40dc-9789-f24c00a283f7)

No need to copy data while loading from Amazon S3.

### 26. How to create a shortcut?

![image](https://github.com/user-attachments/assets/ba78245f-adc9-44ac-acba-1e560ba6e26a)

![image](https://github.com/user-attachments/assets/1587635a-96c5-4c4b-b651-ab7673725d40)

![image](https://github.com/user-attachments/assets/c05f2eee-c38a-424d-9ceb-20eeb1cb8438)

### 27. Creating Files Shortcut

![image](https://github.com/user-attachments/assets/2da99e53-201c-4205-8bc9-81e89d9a3147)

![image](https://github.com/user-attachments/assets/8b9854d5-139e-4414-bd47-5e054b31749c)

Deleting file at Azure Data Lake Storage

![image](https://github.com/user-attachments/assets/382fd180-449d-4900-b7c4-53288ec10a95)

Data gets deleted here in fabric also.

Deleting data in Fabric

![image](https://github.com/user-attachments/assets/187153da-94a5-445f-a2e1-637c5f0be97d)

Data gets deleted in Azure Blob also.

![image](https://github.com/user-attachments/assets/404e7e6f-2193-41b7-b463-d098d583d0b5)

### 28. Creating Table Shortcut

![image](https://github.com/user-attachments/assets/7e4b97d3-3ad0-4a9d-a936-9556e7230ef9)

We can see that this table is in unmanaged section

![image](https://github.com/user-attachments/assets/d01ea0dc-ac71-4b27-b2f8-7b7a9582e5d7)

![image](https://github.com/user-attachments/assets/fb8e7b20-0322-45f4-aaa7-b7d0dedb3a1e)

In Microsoft Fabric, unidentified tables are entries displayed in the managed section of your data environment that lack associated metadata or table references. Here’s a breakdown of the concept:

Managed vs. Unmanaged: In Fabric, the managed section refers to tables that have both metadata and data managed by the Fabric engine. In contrast, the unmanaged section allows you to upload files in any format, which do not have the same management.

Unidentified Tables: If you create a table that is not in the delta format, it will be saved in the unidentified folder. This often occurs when files, such as CSVs, are included without a defined table structure, leading Fabric to categorize them as unidentified.

Purpose: The main goal of the unidentified prompt is to alert users that these files do not conform to the required structure for the managed section and do not support any tables. Essentially, it indicates that there are files present that need to be reviewed and potentially removed.

If we want files from sub folder we cant create shortcut.

When we create shortcut from files it can be from sub directories also.

Now I dropped a parquet file in adls and there is no unmanaged error.

![image](https://github.com/user-attachments/assets/6d3e2d24-c452-493c-b8b6-7458d7bcf4d8)

### 29. Creating Delta from Parquet

![image](https://github.com/user-attachments/assets/59169588-f362-46d6-8747-f9480166873f)

![image](https://github.com/user-attachments/assets/4441ee78-c523-4868-b976-04c6b367284c)

1. Go to synapse workspace

2. Create new notebook.

```
df = spark.read.format("parquet").load('abfss://containername@storageaccountname.dfs.core.windows.net/UnEmployment.parquet')
```

```
df.write.format('delta').save('abfss://shortcutdelta@msfabriclakehousevedanth.dfs.core.windows.net/')
```

### 30. Creating Shortcut in Fabric

Just execute above code and create a table level shortcut.

![image](https://github.com/user-attachments/assets/c9a202b3-40c2-44f4-ae0f-780c58925f04)

![image](https://github.com/user-attachments/assets/8ba09a68-687f-4cd9-ae9d-85d2dc7c471f)

### 31. Shortcut from a subfolder in Fabric

We cannot create a delta table / shortcut from a sub folder in ADLS Gen2.

![image](https://github.com/user-attachments/assets/1abe0218-6d77-41b8-bc60-dc44942d079c)

### 32. Creating Shortcut from Parquet file

![image](https://github.com/user-attachments/assets/ff3f611e-ff3d-4757-8a10-3064e72b0ae5)

```
df.write.format('parquet').mode('append').save('abfss://shortcutparquet@msfabriclakehousevedanth.dfs.core.windows.net/')
```

We cannot create shortcut from parquet files as well, it lands in unidentified folder.

![image](https://github.com/user-attachments/assets/1e93fa3c-e7c6-4d07-8805-c19c1f429187)

### 33. Summary of Shortcuts

![image](https://github.com/user-attachments/assets/3793b0e3-f30c-4666-8a6a-1c4ce2cd050e)

![image](https://github.com/user-attachments/assets/4bf77b56-c305-476f-b3f2-bf34397880ff)

### 34. Update Scenarios Using Shortcuts : Lakehouse to Datalake

![image](https://github.com/user-attachments/assets/e77d7a15-2485-4a6d-a9bd-e577ea0a59ed)

What effects on table and file when either is updated?

![image](https://github.com/user-attachments/assets/7c3633d9-e9ca-434c-95f4-1003ceea776b)

We cannot update using SQL editor in fabric so let's use notebook.

Code:

```
df = spark.sql("SELECT * FROM demo_lakehouse.Unemployment LIMIT 1000")
display(df)
```

We can see that the session is created in 11s, much faster than synapse

![image](https://github.com/user-attachments/assets/33cf2a32-4f6b-4219-b8bc-09c922d7235c)

```
df_updated = spark.sql("UPDATE demo_lakehouse.Unemployment SET Industry = 'Healthcare Updated' WHERE Industry = 'Healthcare'")
display(df_updated)
```

If we have only reader access then this operation will fail.

This update also reflects on the file in delta lake.

### 35. Storage to Data Lake Shortcut Updates

1st Version

![image](https://github.com/user-attachments/assets/baa995dc-f6f8-482b-b989-4fdfa901e7bb)

Update Code

```
spark.sql('''update vw_unemployment_new set Industry = 'Retail' where Industry = 'Retail Trade' ''')
```

The Industry has changed from Retail Trade to Retail

![image](https://github.com/user-attachments/assets/21111470-00b6-4905-afc4-dbc93492de53)

Update Operation Delta Log

```
{"commitInfo":{"timestamp":1752330893911,"operation":"UPDATE","operationParameters":{"predicate":"[\"(Industry#761 = Retail Trade)\"]"},"readVersion":0,"isolationLevel":"Serializable","isBlindAppend":false,"operationMetrics":{"numRemovedFiles":"1","numRemovedBytes":"39721","numCopiedRows":"1510","numAddedChangeFiles":"0","executionTimeMs":"10094","scanTimeMs":"9455","numAddedFiles":"1","numUpdatedRows":"14","numAddedBytes":"39715","rewriteTimeMs":"635"},"engineInfo":"Apache-Spark/3.4.3.5.3.20250511.1 Delta-Lake/2.4.0.24","txnId":"6ae56a22-9ff9-4b9a-aec1-d7ab21bb57e8"}}
{"remove":{"path":"part-00000-33b67e12-a6d1-40de-86ac-20a6843bdc2a-c000.snappy.parquet","deletionTimestamp":1752330893906,"dataChange":true,"extendedFileMetadata":true,"partitionValues":{},"size":39721,"tags":{}}}
```

### 36. Deleting File Data in Fabric Lake House or ADLS

Deleting any record / file itself from Data Lake deletes it from storage also.

Reverse scenario is also same.

### 37. Deleting Data from Tables in Lake House

![image](https://github.com/user-attachments/assets/a45b3876-c314-4f88-bed9-3007509c08c1)

Reflected in Storage file also, we see 1428 records.

![image](https://github.com/user-attachments/assets/1978e485-c1cc-4bf8-95aa-c7d920a81831)

The reverse is also same scenario, deleting from storage reflects in data lakehouse table also.

### 38. Deleting Shortcut

Deleting the entire shortcut does not delete data in storage.

## Section 7 : Fabric Synapse Data Engineering

### 39. Spark Pools

![image](https://github.com/user-attachments/assets/71ec8d45-f08e-4e57-a17c-a1460577b7f8)

#### Starter Pools in Spark

Spark Starter Pools are machines that are ready and can be spun up anytime.

![image](https://github.com/user-attachments/assets/0cffbf40-6b5d-4d20-98e8-bc3247769492)

Billing time doesnt include the idle time to initialize the spark session.

### 40. Spark Pool Node Size (Starter Pool)

![image](https://github.com/user-attachments/assets/1c150949-30ac-4f5e-bed6-25160188aa4f)

![image](https://github.com/user-attachments/assets/1014fb02-47e0-4951-a265-95416848fe7a)

If Starter Pool is not used for 20 min then session expires

Only the min and max number of nodes can be changed in starter pools, its always going to be medium node.

### 41. Custom Pools

![image](https://github.com/user-attachments/assets/ffc4bb17-7602-4be8-86b2-309e4b6af3ea)

We can adjust the node family and number of nodes but caveat is that it will not give the same instant start time as starter pools, Fabric needs to allocate the resources.

### 42. Standard vs High Concurrency Sessions

It acts like shared cluster in Databricks

![image](https://github.com/user-attachments/assets/c044cf1c-0dd8-4301-99a7-21569879eef6)

### 43. Custom Magic Commands

![image](https://github.com/user-attachments/assets/bbd62f74-8a8e-43f4-bfb9-8740006e60ab)

### 44. MSSparkUtils

![image](https://github.com/user-attachments/assets/87dbaf2c-bff0-4497-aceb-7aa6e5941c2e)

For using Azure Key vault : mssparkutils.credentials.help

<img width="1239" height="397" alt="image" src="https://github.com/user-attachments/assets/4a15e157-0d16-42d0-9a89-2abf3f5bcb54" />

<img width="1289" height="160" alt="image" src="https://github.com/user-attachments/assets/61b6c590-7b97-496b-ac87-fa3c5dc0ae28" />

The Key Vault Secret Officer role will allow creation of secrets and using it in notebook.

### 45. Call Fabric Notebook from Fabric Pipeline

Create New cloud connection

<img width="1843" height="768" alt="image" src="https://github.com/user-attachments/assets/f85c2fdf-c258-42c1-8cf1-890f2da5487d" />

<img width="485" height="351" alt="image" src="https://github.com/user-attachments/assets/d93cbd62-7b3c-4492-a527-e483f0fe2ace" />

We cannot use keyvault at the moment

<img width="486" height="646" alt="image" src="https://github.com/user-attachments/assets/19b920ab-cc0a-4c6f-9251-a1033773267d" />

<img width="1042" height="408" alt="image" src="https://github.com/user-attachments/assets/58b277cd-de84-48dc-af5e-1f91c90d1a06" />

