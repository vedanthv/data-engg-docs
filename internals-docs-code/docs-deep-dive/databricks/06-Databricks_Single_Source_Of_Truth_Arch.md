## Single Source of Truth Architecture in Databricks

Delta Lake transactions use log files stored alongside data files to provide ACID guarantees at a table level. Because the data and log files backing Delta Lake tables live together in cloud object storage, reading and writing data can occur simultaneously without risk of many queries resulting in performance degradation or deadlock for business-critical workloads. 

This means that users and applications throughout the enterprise environment can connect to the same single copy of the data to drive diverse workloads, with all viewers guaranteed to receive the most current version of the data at the time their query executes.

### Views in Databricks

In Databricks, **views** are saved queries that reference data stored in tables within the lakehouse. They do not store data themselves; instead, they define how to access and present data from existing tables.

When you create a **table**, the query that produces it runs once at write time, and the results are stored physically.
When you create a **view**, the defining query does not store results. Instead, the query is executed **every time** someone reads from the view.

Because of this behavior:

* Views always show **up-to-date data**, reflecting the latest state of the underlying tables.
* Compute resources are used **only when someone queries the view**, not when it is created or updated.

Databricks allows you to use **Unity Catalog** to manage and secure views just like tables. This means:

* You can control access to views through Unity Catalog permissions.
* You can share views across teams and departments.
* Teams can reuse shared views to ensure consistent logic and metrics for business reporting and analytics.

In summary, views in Databricks are a way to define reusable, secure, and always-current queries without physically storing new data.

