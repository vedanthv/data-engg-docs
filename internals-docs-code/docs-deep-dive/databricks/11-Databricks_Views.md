# Views in Databricks

A view is a read-only object that is the result of a query over one or more tables and views in a Unity Catalog metastore. You can create a view from tables and from other views in multiple schemas and catalogs.

A view stores the text of a query typically against one or more data sources or tables in the metastore. In Databricks, a view is equivalent to a Spark DataFrame persisted as an object in a schema. Unlike DataFrames, you can query views from anywhere in Databricks, assuming that you have permission to do so. Creating a view does not process or write any data. Only the query text is registered to the metastore in the associated schema.

## Metric Views

Metric views in Unity Catalog define reusable business metrics that are centrally maintained and accessible to all users in your workspace. A metric view abstracts the logic behind commonly used KPIs—such as revenue, customer count, or conversion rate—so they can be consistently queried across dashboards, notebooks, and reports. Each metric view specifies a set of measures and dimensions based on a source table, view, or SQL query. Metric views are defined in YAML and queried using SQL.

Using metric views helps reduce inconsistencies in metric definitions that might otherwise be duplicated across multiple tools and workflows. 

## Materialized Views

Materialized views incrementally calculate and update the results returned by the defining query. Materialized views on Databricks are a special kind of Delta table. Whereas all other views on Databricks calculate results by evaluating the logic that defined the view when it is queried, materialized views process results and store them in an underlying table when updates are processed using either a refresh schedule or running a pipeline update.

You can register materialized views in Unity Catalog using Databricks SQL or define them as part of Lakeflow Declarative Pipelines.

## Temporary Views

- A temporary view has limited scope and persistence and is not registered to a schema or catalog. The lifetime of a temporary view differs based on the environment you're using:

- In notebooks and jobs, temporary views are scoped to the notebook or script level. They cannot be referenced outside of the notebook in which they are declared, and no longer exist when the notebook detaches from the cluster.

- In Databricks SQL, temporary views are scoped to the query level. Multiple statements within the same query can use the temp view, but it cannot be referenced in other queries, even within the same dashboard.

## Dynamic Views

Give access to custom functions that help in column masking and row/column level access.

## Dropping a View

```sql

DROP VIEW IF EXISTS catalog_name.schema_name.view_name;

```

## Creating a Dynamic View

In Unity Catalog, you can use dynamic views to configure fine-grained access control, including:

- Security at the level of columns or rows.

- Data masking.

- Unity Catalog introduces the following functions, which allow you to dynamically limit which users can access a row, column, or record in a view:

```current_user()```: Returns the current user's email address.

```is_account_group_member()```: Returns TRUE if the current user is a member of a specific account-level group. Recommended for use in dynamic views against Unity Catalog data.

### Requirements for Dynamic Views

To create or read dynamic views, requirements are the same as those for standard views, except for compute requirements. You must use one of the following compute resources:

- A SQL warehouse.
  
- Compute with standard access mode (formerly shared access mode).
  
- Compute with dedicated access mode (formerly single user access mode) on Databricks Runtime 15.4 LTS or above.
  
- You cannot read dynamic views using dedicated compute on Databricks Runtime 15.3 or below.

To take advantage of the data filtering provided in Databricks Runtime 15.4 LTS and above, you must also verify that your workspace is enabled for serverless compute, because the data filtering functionality that supports dynamic views runs on serverless compute.

### Column Level Permissions

With a dynamic view, you can limit the columns a specific user or group can access. In the following example, only members of the auditors group can access email addresses from the sales_raw table. During query analysis, Apache Spark replaces the CASE statement with either the literal string REDACTED or the actual contents of the email address column. Other columns are returned as normal. This strategy has no negative impact on the query performance.

```sql
-- Alias the field 'email' to itself (as 'email') to prevent the
-- permission logic from showing up directly in the column name results.
CREATE VIEW sales_redacted AS
SELECT
  user_id,
  CASE WHEN
    is_account_group_member('auditors') THEN email
    ELSE 'REDACTED'
  END AS email,
  country,
  product,
  total
FROM sales_raw
```

### Row Level Permissions

```sql
CREATE VIEW sales_redacted AS
SELECT
  user_id,
  country,
  product,
  total
FROM sales_raw
WHERE
  CASE
    WHEN is_account_group_member('managers') THEN TRUE
    ELSE total <= 1000000
  END;
```

### Data Masking

```sql
-- The regexp_extract function takes an email address such as
-- user.x.lastname@example.com and extracts 'example', allowing
-- analysts to query the domain name.

CREATE VIEW sales_redacted AS
SELECT
  user_id,
  region,
  CASE
    WHEN is_account_group_member('auditors') THEN email
    ELSE regexp_extract(email, '^.*@(.*)$', 1)
  END
  FROM sales_raw
```

You have this expression:

```sql
regexp_extract(email, '^.*@(.*)$', 1)
```

and your input email is:

```
user.x.lastname@example.com
```

---

### 🧩 Step 1: Function purpose

`regexp_extract(column, pattern, groupIndex)`

* **column** → the string column to extract from (`email`)
* **pattern** → the regular expression pattern (`'^.*@(.*)$'`)
* **groupIndex** → which *capturing group* to return (in this case `1`)

---

### 🧠 Step 2: Understanding the regex pattern

#### Pattern: `^.*@(.*)$`

| Regex Part | Meaning                                        | What it matches in your email      |
| ---------- | ---------------------------------------------- | ---------------------------------- |
| `^`        | Start of string                                | Anchors the regex to the beginning |
| `.*`       | Any characters (0 or more)                     | Matches `user.x.lastname`          |
| `@`        | Literal `@` symbol                             | Matches the `@` in your email      |
| `(.*)`     | **Capture group 1** → any characters after `@` | Matches `example.com`              |
| `$`        | End of string                                  | Ensures it goes till the end       |

---

### ⚙️ Step 3: What `regexp_extract` does

`regexp_extract` **extracts the content of capturing group 1**, i.e. whatever is inside `( ... )`.

So, for your input:

```
user.x.lastname@example.com
```

* Everything before `@` → `user.x.lastname`
* Everything after `@` → `example.com` ← **captured group**

---

### ✅ Final Output

The result of:

```sql
regexp_extract(email, '^.*@(.*)$', 1)
```

is:

```
example.com
```

---

### 🧠 Optional — What if you used group 0?

If you wrote:

```sql
regexp_extract(email, '^.*@(.*)$', 0)
```

That would return the **entire matched string**, i.e. the full email:

```
user.x.lastname@example.com
```

---

