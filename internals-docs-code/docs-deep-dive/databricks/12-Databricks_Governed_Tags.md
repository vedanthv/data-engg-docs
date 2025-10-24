# Apply Governed Tags to UC Objects

Tags are attributes that include keys and optional values that you can use to organize and categorize securable objects in Unity Catalog. Using tags also simplifies the search and discovery of tables and views using the workspace search functionality.

Securable object tagging is currently supported on catalogs, schemas, tables, table columns, volumes, views, registered models, and model versions.

Governed tags are account-level tags with enforced rules for consistency and control. Using governed tags, you define the allowed keys and values and control which users and groups can assign them to objects. This ensures tags are applied consistently and conform to organizational standards, giving centralized control over classification, compliance, and operations.

System tags are a special type of governed tag that are predefined by Databricks. System tags have a few distinct characteristics:

- System tag definitions (keys and values) are predefined by Databricks.

- Users cannot modify or delete system tag keys or values.

- Users can control who is allowed to assign or unassign system tags through governed tag permission settings.

System tags are designed to support standardized tagging across organizations, particularly for use cases like data classification, ownership, or lifecycle tracking. By using predefined, governed tag definitions, system tags help enforce consistency without requiring users to manually define or manage tag structures.

## Constraint

- Tag keys are case sensitive. For example, Sales and sales are two distinct tags.

- You can assign a maximum of 50 tags to a single securable object.

- The maximum length of a tag key is 255 characters.

- The maximum length of a tag value is 1000 characters.

- The following characters are not allowed in tag keys: ```. , - = / :```

- Trailing and leading spaces are not allowed in tag keys or values.

- Tag search using the workspace search UI is supported only for tables and views.

- Tag search requires exact term matching.

```sql
SET TAG ON CATALOG catalog `cost_center` = `hr`;

UNSET TAG ON CATALOG catalog cost_center;
```

```sql
-- Add the governed tag to ssn column
ALTER TABLE abac.customers.profiles
ALTER COLUMN SSN
SET TAGS ('pii' = 'ssn');
```

