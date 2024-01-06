# Azure Databricks

At the core of Azure Databricks is the open source distributed compute processing engine called Apache Spark, which is widely used in the industry for developing big data projects. 

Databricks is a company created by the founders of Apache Spark, to make it easier to work with Spark by providing the necessary management layers. 

Microsoft makes, the Databricks service available on its Azure Cloud platform as a first party service. These three offerings together makes Azure Databricks.

This is the notes for the course [Azure Databricks Spark Core For DE](https://www.udemy.com/course/azure-databricks-spark-core-for-data-engineers/) on Udemy by Ramesh Retnasamy.

## Structure of the Course

![image](https://github.com/vedanthv/data-engg/assets/44313631/54d01f29-67c8-42fd-b960-c06cfee5b1bb)

## High Level Overview Of Azure Databricks

![image](https://github.com/vedanthv/data-engg/assets/44313631/bbf82420-852c-4392-b987-374653c96c08)

## Apache Spark Fundamentals

![image](https://github.com/vedanthv/data-engg/assets/44313631/a1615348-c8da-4e3e-8896-a8e4054f37b7)

## Apache Spark Architecture

![image](https://github.com/vedanthv/data-engg/assets/44313631/95991341-e293-468a-b9f7-4d13fc73381d)

- Catalyst Optimizer converts the code into a high level optimization plan and Tungsten helps with memory management.

## Azure Databricks for Spark

![image](https://github.com/vedanthv/data-engg/assets/44313631/c0941bb9-ddcd-47ca-baf6-9f483bb4ab99)

## Azure Databricks Architecture

Databricks Architecture is basically split into two parts, one called the Control Plane and another one called the Data Plane.

Control plane is located in Databricks own subscription.

This contains the Databricks UX and also the Cluster Manager.

It's also home to the Databricks File System (DBFS) and also metadata about Clusters, Files mounted, etc. Data Plane is located in the customer subscription.

When you create a Databricks service in Azure, there are four resources created in your subscription, a Virtual Network and Network Security Group for the Virtual Network.
Azure Blob Storage for the default storage and also a Databricks Workspace.

When a user requests for a cluster, Databricks Cluster Manager will create the required virtual machines in our subscription via the Azure Resource Manager.

So none of the customer data leaves a subscription.

Temporary outputs such as running a display command or data for manage tables, are stored in the Azure Blob Storage, and the processing also happens within the 
VNet in our subscription. The Azure Blob Storage we have shown here is the default storage or otherwise called the DBFS a route, and it's not recommended as a 
permanent data storage.

![image](https://github.com/vedanthv/data-engg/assets/44313631/c0312226-dada-4d5a-ba5f-9f58fe3b2e79)

## Clusters in Databricks

![image](https://github.com/vedanthv/data-engg/assets/44313631/a1d183e6-ff83-4517-9d75-2a4d5875de39)

![image](https://github.com/vedanthv/data-engg/assets/44313631/33deceff-52bb-4a3e-ade5-c3e99364d3d1)

## Cluster Configuration

**# of Nodes**

Single Node - only one VM 
Multi Node - Has Main Node and Worker Nodes

![image](https://github.com/vedanthv/data-engg/assets/44313631/5df93968-cb32-4067-ad62-ccaa674c85d5)

**Access Modes**
![image](https://github.com/vedanthv/data-engg/assets/44313631/764b0c93-3b69-48f2-90c8-075c8e1107b6)

**Databricks Runtime Configuration**
![image](https://github.com/vedanthv/data-engg/assets/44313631/1dce7f80-3f2a-4df4-b73b-cdea00ea6568)

**Auto Termination**
![image](https://github.com/vedanthv/data-engg/assets/44313631/afd1ae00-f00c-4554-941b-7d8d31ec044a)

**Auto Scaling**
![image](https://github.com/vedanthv/data-engg/assets/44313631/8e9bfd4e-6157-477f-9050-9940a0adadb3)

**Cluster Policies**

- Can be set by the administrators to limit the use of clusters that extend beyond a certain budget or memory constraint.
- Simplifies the UI

## Azure Databricks Pricing Calculation

![image](https://github.com/vedanthv/data-engg/assets/44313631/194ba704-5333-4235-a861-f7e8c7e11df6)

## Accessing Azure Data Lake Storage

- Access Keys
- Azure Active Directory
- Service Principal
- Cluster Scoped Auth
- Session Scoped Auth

**Access Keys**
![image](https://github.com/vedanthv/data-engg/assets/44313631/678d6b93-a60e-405d-8217-7852ffa84f46)

**Shared Access Signature**

![image](https://github.com/vedanthv/data-engg/assets/44313631/5f9ca380-1627-4c64-b106-80ed5e0b683e)

![image](https://github.com/vedanthv/data-engg/assets/44313631/744b294f-f01f-4f3c-aeaa-829ef8679bab)

**Service Principal**

![image](https://github.com/vedanthv/data-engg/assets/44313631/be9db54e-ea32-4959-a02b-7c41a3bb0811)

**Steps**

![image](https://github.com/vedanthv/data-engg/assets/44313631/90f3b5fc-6cee-42a7-bdfa-6a5f26ec6307)

**Cluster Scoped Authentication**

**Session Scoped Vs Cluster Scoped Authentication**

![image](https://github.com/vedanthv/data-engg/assets/44313631/1cd5a112-9b6b-4444-b78a-94955e467b08)

![image](https://github.com/vedanthv/data-engg/assets/44313631/596b97b0-5cae-4a97-8762-eb9813ac29b6)

We need to add the same credentials as in Access Keys but in the Spark Config text area of the cluster itself.

Now when we remove the config from the notebook with Access Keys we can still access the notebooks.

**AAD Credential Passthrough**

![image](https://github.com/vedanthv/data-engg/assets/44313631/ce6d7777-9bd3-43b9-9976-4c00badefb12)

Now even if we are the owner of the storage account, we can't access the data without creating a role that gives the **Storage Blob Contributor Access**

Again we don't need to mention any credentials in the notebook.

## Managing the Secrets Using Secret Scope

### Creating a Secret Scope

- Go to the Databricks Home Page

- Add 'secrets/createScope' to the end of the URL.

- Add secret scope name and then select all users.

- Add the Vault URL and Resource Id that can be got from the Key Vault on Azure (Home/key-vault/properties)

![image](https://github.com/vedanthv/data-engg/assets/44313631/2adb5d54-0a96-4ac1-b723-52f179a57874)

![image](https://github.com/vedanthv/data-engg/assets/44313631/dbe934a9-98c7-41bc-ad2a-1909e4dddf1f)

**Databricks Secrets Utility**

To list the name of the secret scope : ```dbutils.secrets.list(scope = formula1-scope)```

To check if a key is a secret scope use : ```dbutils.secrets.get(scope = 'formula1-scope',key = 'fomula1-dl-account-key')```

### Adding the Secret Scope to the Cluster

To add the access key to the cluster add the following to the spark config ```fs.azure.account.key.formula1dl.dfs.core.windows.net{{secrets/formula1-scope/formula1dl-account-key}}```

Any notebook that has access to the cluser will have access to the ADLS Storage.

## DBFS Root

- The deployment created a default Azure Blob Storage and mounted that to DBFS. So we could run DBFS or Databricks File System utilities to interact with the Azure Blob Storage from the Databricks workspace.
  
- DBFS or Databricks File System here, is a distributed file system mounted on the Databricks workspace.
  
- This can be accessed from any of the Databricks Clusters created in this workspace.

- It's just an abstraction layer on top of the Azure Object Storage.

- The key takeaway here is that, DBFS is simply a file system that provides distributed access to the data stored in Azure storage.

- It's not a storage solution in itself. The storage here is the Azure Blob Storage, and this is the default storage that's created when the Databricks workspace was deployed.
  
- This DBFS mount on the default Azure Blob Storage is called DBFS Root. As we said, DBFS Root is backed by Azure Blob Storage in the databricks created Resource Group.
  
- You can access one of the special folders within DBFS Root called File Store via the Web User Interface.

- You can use this as a temporary storage, for example, to store any images to be used in notebooks or some data to play with quickly.
  
- Databricks also stores query results from commands such as display in DBFS Root. Similar to Hive, Databricks also allows us to create both managed and external tables.
  
- If you create a managed table without specifying the location for the database, that data will also be stored in DBFS Root, i.e. the default location for managed tables is DBFS Root. But you can change that during the database creation.
  
- Even though DBFS Root is the default storage for Databricks, it's not the recommended location to store customer data.

- When you drop the Databricks workspace, this storage also gets dropped, which is not what you would want for the customer data.

- Instead, we can use an external Data Lake, fully controlled by the customer and we can mount that to the workspace.

**Implementation**

The DBFS Console is hidden. First go to the top right 'az_admin@gmail.com' and click it.

Then Click on Admin Console >> Workplace Settings >> Search For DBFS >> Enable DBFS Browser >> Refresh the Browser

Now Go to the Data tab and Click Browse DBFS >> Click FileStore.

The files that are in the FileStore can be used by all the users of the workspace.

### Databricks Mounts

- We said that we shouldn't be using DBFS Root for keeping customer data.
- Now the question becomes if we can't use DBFS Root as the storage for customer data, where do we store that?
- Customers can create separate Azure Blob Storage or Azure Data Lake storage accounts in their subscription and keep the data in them.
- In this Architecture, when you delete the Databricks workspace, the customer data still stays without being untouched.
- In order to access the storage, we can use the ABFS protocol like we did before in the previous section of the course.
- But as you saw previously, this approach is tedious for two reasons.
- Firstly, we need to deal with those along ABFS URLs rather than the file system semantics to access the files.
- Secondly, every time we'll have to use the credentials to authenticate to the storage accounts before accessing the data from them.
- To make this experience better, Databricks allows us to mount these storage accounts to DBFS. We specify the credential when the storage is mounted.
- Once it's mounted, everyone who has access to the workspace can access the data without providing the credentials.
- Also, they will be able to use the file system semantics rather than the long URLs. In summary, Databricks mounts offer some important benefits to the storage solution in Databricks.
- Once the Azure object storage solution, such as Azure Data Lake or the Blob storage has been mounted onto the Databricks workspace, you can access the mount points without specifying the credentials.
- This allows for accessing the Azure storage from Databricks using file semantics rather than the long storage URLs. You can treat a mount point as the same as mapping another drive to your computer.
- DBFS is just an abstraction layer and it still stores the files to the Azure storage, so you get all the benefits such as different performance tiers, replication, massive storage etc., as you would generally get from Azure storage.
- This was the recommended solution from Databricks to access Azure Data Lake until the introduction of Unity Catalog, which became generally available around end of 2022.
- Databricks now recommends using the Unity Catalog for better security, but most projects I see today are still using Databricks Mounts to access the data. So please be familiar with this approach and you will come across it in your projects.
- In case you are wondering how to access data using Unity Catalog, Once a workspace has been configured with Unity Catalog, you can simply use the ABFS protocol to access the Data Lake like we have been doing so far.

![image](https://github.com/vedanthv/data-engg/assets/44313631/18c291e8-2116-41bc-9721-1d2d3f93f526)

![image](https://github.com/vedanthv/data-engg/assets/44313631/1320ecd4-c74f-4d8e-9aa2-8059ee53c2c2)

![image](https://github.com/vedanthv/data-engg/assets/44313631/34076c8c-2677-4d95-bd86-de0b4a7cf855)

Mounting Azure Data Lake Storage Gen2 : [Code](https://github.com/vedanthv/data-engg/blob/main/databricks/8.mount_adls_containers_for_project%20(1).py)

**Partition By allows us to create different data folders for various date years**

**When we have a nested JSON data, the nested keys and values must be defined in a separate schema**

If there are multiple lines in a JSON file then we can set option as ```.option("multiLine",True)```
