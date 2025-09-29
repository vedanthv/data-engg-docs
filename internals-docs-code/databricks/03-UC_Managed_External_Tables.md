## Managed vs External Tables in UC

**Managed tables** are fully managed by Unity Catalog, which means that Unity Catalog manages both the governance and the underlying data files for each managed table. Managed tables are stored in a Unity Catalog-managed location in your cloud storage. Managed tables always use the Delta Lake format. You can store managed tables at the metastore, catalog, or schema levels.

**External tables** are tables whose access from Databricks is managed by Unity Catalog, but whose data lifecycle and file layout are managed using your cloud provider and other data platforms. Typically you use external tables to register large amounts of your existing data in Databricks, or if you also require write access to the data using tools outside of Databricks. External tables are supported in multiple data formats. Once an external table is registered in a Unity Catalog metastore, you can manage and audit Databricks access to it---and work with it---just like you can with managed tables.

**Managed volumes** are fully managed by Unity Catalog, which means that Unity Catalog manages access to the volume's storage location in your cloud provider account. When you create a managed volume, it is automatically stored in the managed storage location assigned to the containing schema.

**External volumes** represent existing data in storage locations that are managed outside of Databricks, but registered in Unity Catalog to control and audit access from within Databricks. When you create an external volume in Databricks, you specify its location, which must be on a path that is defined in a Unity Catalog external location.

## Cloud Storage and Data Isolation

**Managed storage**: default locations for managed tables and managed volumes (unstructured, non-tabular data) that you create in Databricks. These managed storage locations can be defined at the metastore, catalog, or schema level. You create managed storage locations in your cloud provider, but their lifecycle is fully managed by Unity Catalog.

Storage locations where external tables and volumes are stored. These are tables and volumes whose access from Databricks is managed by Unity Catalog, but whose data lifecycle and file layout are managed using your cloud provider and other data platforms. Typically you use external tables or volumes to register large amounts of your existing data in Databricks, or if you also require write access to the data using tools outside of Databricks.

