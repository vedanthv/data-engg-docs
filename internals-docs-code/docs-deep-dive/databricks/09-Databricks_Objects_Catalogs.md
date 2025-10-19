## Catalogs in Databricks

A catalog is the primary unit of data organization in the Databricks Unity Catalog data governance model. This article gives an overview of catalogs in Unity Catalog and how best to use them.

Catalogs are the first layer in Unity Catalog's three-level namespace (catalog.schema.table-etc). They contain schemas, which in turn can contain tables, views, volumes, models, and functions. Catalogs are registered in a Unity Catalog metastore in your Databricks account

![alt text](https://snipboard.io/nmHcoU.jpg)

### How Should I organize my data in catalogs?

When you design your data governance model, you should give careful thought to the catalogs that you create. As the highest level in your organization's data governance model, each catalog should represent a logical unit of data isolation and a logical category of data access, allowing an efficient hierarchy of grants to flow down to schemas and the data objects that they contain. Catalogs therefore often mirror organizational units or software development lifecycle scopes. You might choose, for example, to have a catalog for production data and a catalog for development data, or a catalog for non-customer data and one for sensitive customer data.

### Data Isolation in Catalogs

Each catalog typically has its own managed storage location to store managed tables and volumes, providing physical data isolation at the catalog level. You can also choose to store data at the metastore level, providing a default storage location for catalogs that don't have a managed storage location of their own. You can add storage at the schema level for more granular data isolation.

Because your Databricks account has one metastore per region, catalogs are inherently isolated by region.

### Catalog Lvel Privileges

Because grants on any Unity Catalog object are inherited by children of that object, owning a catalog or having broad privileges on a catalog is very powerful. For example, catalog owners have all privileges on the catalog and the objects in the catalog, and they can grant access to any object in the catalog. Users with SELECT on a catalog can read any table in the catalog. Users with CREATE TABLE on a catalog can create a table in any schema in the catalog.

To enforce the principle of least privilege, where users have the minimum access they need to perform their required tasks, typically you grant access only to the specific objects or level in the hierarchy that the user requires. But catalog-level privileges let the catalog owner manage what lower-level object owners can grant. Even if a user is granted access to a low-level data object like a table, for example, that user cannot access that table unless they also have the USE CATALOG privilege on the catalog that contains the table.

### Catalog Types

**Standard catalog:** the typical catalog, used as the primary unit to organize your data objects in Unity Catalog. This is the catalog type that is discussed in this article.

**Foreign catalog:** a Unity Catalog object that is used only in Lakehouse Federation scenarios. A foreign catalog mirrors a database in an external data system, enabling you to perform read-only queries on that data system in your Databricks workspace.

```hive_metastore``` catalog: This is the repository of all data managed by the legacy Hive metastore in Databricks workspaces. When an existing non-Unity Catalog workspace is converted to Unity Catalog, all objects that are registered in the legacy Hive metastore are surfaced in Unity Catalog in the hive_metastore catalog. 

```Workspace catalog```: In all new workspaces, this catalog is created for you by default. Typically, it shares its name with your workspace name. If this catalog exists, all users in your workspace (and only your workspace) have access to it by default, which makes it a convenient place for users to try out the process of creating and accessing data objects in Unity Catalog.

### Workspace Catalog Binding

If you use workspaces to isolate user data access, you might want to use workspace-catalog bindings. Workspace-catalog bindings enable you to limit catalog access by workspace boundaries. For example, you can ensure that workspace admins and users can only access production data in prod_catalog from a production workspace environment, prod_workspace. Catalogs are shared with all workspaces attached to the current metastore unless you specify a binding.

### Creating A Catalog - Requirements

To create a catalog, regardless of catalog type:

- You must be a Databricks metastore admin or have the ```CREATE CATALOG``` privilege on the metastore.

- The compute resource that you use to run a notebook to create a catalog must be on Databricks Runtime 11.3 or above and must use a Unity Catalog-compliant access mode. See Access modes. SQL warehouses always support Unity Catalog.

To create a **shared catalog**:

- The Delta Sharing share must already exist in your workspace.

- You must be a metastore admin, have the ```USE PROVIDER``` privilege on the metastore, or own the provider object that includes the share.

To create a **standard catalog**:

- If you specify a managed storage location for the catalog, you must have the CREATE MANAGED STORAGE privilege on the target external location.

- If no metastore-level managed storage exists, then you must specify a managed storage location for the catalog.
  
To create a **foreign catalog**:

You must be either the owner of the connection that you use to create the foreign catalog or have the CREATE FOREIGN CATALOG privilege on the connection.

You must use compute on Databricks Runtime 13.1 or above. SQL warehouses must be Pro or Serverless.

By default, the catalog is shared with all workspaces attached to the current metastore. If the catalog will contain data that should be restricted to specific workspaces, clear the All workspace have access option and use the Assign to workspaces button to add those workspaces. The current workspace must be included.

After you assign a workspace, you can optionally change its default Read & Write access level to Read Only: select the workspace from the list and click the Manage Access Level button.

### Managing the Default Catalog

A default catalog is configured for each workspace that is enabled for Unity Catalog. The default catalog lets you perform data operations without specifying a catalog. If you omit the top-level catalog name when you perform data operations, the default catalog is assumed.

A workspace admin can view or switch the default catalog using the Admin Settings UI. You can also set the default catalog for a cluster using a Spark config.

The workspace default catalog setting applies only when using compute that meets the compute requirements for Unity Catalog. Specifically, this means that you're using either a SQL warehouse, or a cluster configured with standard or dedicated access mode. Compute resources that aren't compatible with Unity Catalog use hive_metastore as the default catalog.

Commands that do not specify the catalog (for example GRANT CREATE TABLE ON SCHEMA myschema TO mygroup) are evaluated for the catalog in the following order:

- Is the catalog set for the session using a ```USE CATALOG``` statement or a JDBC setting?
- Is the Spark configuration ```spark.databricks.sql.initial.catalog.namespace``` set on the cluster?
- Is there a workspace default catalog set for the cluster?

The pipeline configuration for Lakeflow Declarative Pipelines sets a default catalog that overrides workspace default.

### Default Catalog when UC is enabled

The default catalog that was initially configured for your workspace depends on how your workspace was enabled for Unity Catalog:

- For some workspaces that were enabled for Unity Catalog automatically, the workspace catalog was set as the default catalog. 

- For all other workspaces, the hive_metastore catalog was set as the default catalog.

When you are migrating from the Hive metastore to Unity Catalog, you can set the default catalog to hive_metastore to avoid impacting existing code that references the Hive metastore.

