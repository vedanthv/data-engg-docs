# Specify a managed storage location in Unity Catalog

A managed storage location specifies a location in cloud object storage for storing data for managed tables and managed volumes.

You can associate a managed storage location with a metastore, catalog, or schema. Managed storage locations at lower levels in the hierarchy override storage locations defined at higher levels when managed tables or managed volumes are created.

New workspaces that are enabled for Unity Catalog automatically are created without a metastore-level managed storage location. 

## What is a managed storage location?

Managed storage locations have the following properties:

- Managed tables and managed volumes store data and metadata files in managed storage locations.
- Managed storage locations cannot overlap with external tables or external volumes.

![alt text](https://snipboard.io/IVnTaY.jpg)

## Rules and Hierarchy

- If the containing schema has a managed location, the data is stored in the schema managed location.
- If the containing schema does not have a managed location but the catalog has a managed location, the data is stored in the catalog managed location.
- If neither the containing schema nor the containing catalog have a managed location, data is stored in the metastore managed location.

## Setting Managed Storage

```sql
CREATE CATALOG <catalog-name>
MANAGED LOCATION 's3://<external-location-bucket-path>/<directory>';
```

```sql
CREATE SCHEMA <catalog>.<schema-name>
MANAGED LOCATION 's3://<external-location-bucket-path>/<directory>';
```