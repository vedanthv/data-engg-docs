# Connect to cloud object storage using Unity Catalog

## How Does UC use cloud storage?

Databricks recommends using Unity Catalog to manage access to all data that you have stored in cloud object storage. Unity Catalog provides a suite of tools to configure secure connections to cloud object storage. These connections provide access to complete the following actions:

- Ingest raw data into a lakehouse.
- Create and read managed tables and managed volumes of unstructured data in Unity Catalog-managed cloud storage.
- Register or create external tables containing tabular data and external volumes containing unstructured data in cloud storage that is managed using your cloud provider.
- Read and write unstructured data (Unity Catalog volumes).

There are two primary ways in which databricks allows us to use cloud storage:

- Default (or “managed”) storage locations for managed tables and managed volumes (unstructured, non-tabular data) that you create in Databricks. These managed storage locations can be defined at the metastore, catalog, or schema level. You create managed storage locations in your cloud provider, but their lifecycle is fully managed by Unity Catalog.

- Storage locations where external tables and volumes are stored. These are tables and volumes whose access from Databricks is managed by Unity Catalog, but whose data lifecycle and file layout are managed using your cloud provider and other data platforms. Typically you use external tables to register large amounts of your existing data in Databricks, or if you also require write access to the data using tools outside of Databricks.

There are three major options supported by UC:

- AWS/Azure S3 or Blob buckets
- Cloudflare R2 Buckets
- Legacy dbfs root

## Governing Access to Cloud Storage

To manage access to the underlying cloud storage that holds tables and volumes, Unity Catalog uses a securable object called an external location, which defines a path to a cloud storage location and the credentials required to access that location. 

Those credentials are, in turn, defined in a Unity Catalog securable object called a storage credential. By **granting and revoking access to external location securables in Unity Catalog, you control access to the data in the cloud storage location**. By **granting and revoking access to storage credential securables in Unity Catalog, you control the ability to create external location objects**.

## Overview of Storage Credentials

A storage credential represents an authentication and authorization mechanism for accessing data stored on your cloud tenant. For example, a storage credential is associated with an IAM role for S3 buckets, or with an R2 API token for Cloudflare R2 buckets.

Privileges granted in Unity Catalog control which users and groups can use the credential to define external locations. Permission to create and use storage credentials should be granted only to users who need to create external location objects.

## Overview of External Locations

An external location combines a cloud storage path with a storage credential that authorizes access to the specified path. Multiple external locations can use the same storage credential. External locations can reference storage paths in any of the supported cloud storage options.

![alt text](https://docs.databricks.com/aws/en/assets/images/external-locations-overview-b859ea8737cef28752918431fd816730.png)

- Each external location references a storage credential and a cloud storage location.
- Multiple external locations can reference the same storage credential. Storage credential 1 grants access to everything under the path bucket/tables/*, so both External location A and External location B reference it.

External locations are used in Unity Catalog both for external data assets, like external tables and external volumes, and for managed data assets, like managed tables and managed volumes.

## Using External Locations when creating external tables and volumes

External tables and external volumes registered in Unity Catalog are essentially pointers to data in cloud storage that you manage outside of Databricks. When you create an external table or external volume in Unity Catalog, you must reference a cloud storage path that is included in an external location object that you have been granted adequate privileges on.

## Using External Location when creating managed tables and volumes

Managed tables and managed volumes are fully managed by Unity Catalog. They are stored by default in a managed storage location, which can be defined at the metastore, catalog, or schema level. When you assign a managed storage location to a metastore, catalog, or schema, you must reference an external location object, and you must have adequate privileges to use it.

### ⚠️ Important

If you update external table metadata using a non-Databricks client or using path-based access from within Databricks, that metadata does not automatically sync state with Unity Catalog. Databricks recommends against such metadata updates, but if you do perform one, you must run MSCK REPAIR TABLE <table-name> SYNC METADATA to bring the schema in Unity Catalog up to date.