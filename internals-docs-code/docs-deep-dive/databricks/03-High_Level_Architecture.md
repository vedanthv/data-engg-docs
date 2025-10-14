## High Level Architecture

A Databricks account is the top-level construct that you use to manage Databricks across your organization. At the account level, you manage:

- Identity and access: Users, groups, service principals, SCIM provisioning, and SSO configuration.
Workspace management: Create, update, and delete workspaces across multiple regions.

- Unity Catalog metastore management: Create and attach metastore to workspaces.

- Usage management: Billing, compliance, and policies.

An account can contain multiple workspaces and Unity Catalog metastores.

Workspaces are the collaboration environment where users run compute workloads such as ingestion, interactive exploration, scheduled jobs, and ML training.

Unity Catalog metastores are the central governance system for data assets such as tables and ML models. You organize data in a metastore under a three-level namespace:

<catalog-name>.<schema-name>.<object-name>

Metastores are attached to workspaces. You can link a single metastore to multiple Databricks workspaces in the same region, giving each workspace the same data view. Data access controls can be managed across all linked workspaces.

![alt text](https://snipboard.io/0DjZmx.jpg)

## Workspace Architecture

Databricks operates out of a control plane and a compute plane.

The control plane includes the backend services that Databricks manages in your Databricks account. The web application is in the control plane.

The compute plane is where your data is processed. There are two types of compute planes depending on the compute that you are using.

- For serverless compute, the serverless compute resources run in a serverless compute plane in your Databricks account.

- For classic Databricks compute, the compute resources are in your AWS account in what is called the classic compute plane. This refers to the network in your AWS account and its resources.

Each Databricks workspace has an associated storage bucket known as the workspace storage bucket. The workspace storage bucket is in your cloud account.

![alt text](https://snipboard.io/DeSp3G.jpg)

### Serverless Compute

In the serverless compute plane, Databricks compute resources run in a compute layer within your Databricks account. Databricks creates a serverless compute plane in the same cloud region as your workspace's classic compute plane. You select this region when creating a workspace.

To protect customer data within the serverless compute plane, serverless compute runs within a network boundary for the workspace, with various layers of security to isolate different Databricks customer workspaces and additional network controls between clusters of the same customer.

In the classic compute plane, Databricks compute resources run in your cloud account. New compute resources are created within each workspace's virtual network in the customer's cloud account.

A classic compute plane has natural isolation because it runs in each customer's own cloud account. 

## Workspace Storage

### Serverless Workspaces

Serverless workspaces use default storage, which is a fully managed storage location for your workspace's system data and Unity Catalog catalogs. Serverless workspaces also support the ability to connect to your cloud storage locations. 

### Traditional Workspaces

Workspace system data: Workspace system data is generated as you use various Databricks features such as creating notebooks. This bucket includes notebook revisions, job run details, command results, and Spark logs
Unity Catalog workspace catalog: If your workspace was enabled for Unity Catalog automatically, the workspace storage bucket contains the default workspace catalog. All users in your workspace can create assets in the default schema in this catalog.

