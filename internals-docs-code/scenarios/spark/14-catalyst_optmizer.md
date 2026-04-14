## Catalyst Optimizer Spark In Depth

<img src = 'https://snipboard.io/psJALv.jpg'>

Example:

Here’s the same **end-to-end real example**, mapped cleanly to each Catalyst phase, without any extra styling.

---

# Example Scenario

Tables:

* `orders(customer_id, amount, order_date)`
* `customers(customer_id, country, status)`

Query:

```sql
SELECT c.customer_id, SUM(o.amount) AS total_revenue
FROM orders o
JOIN customers c
  ON o.customer_id = c.customer_id
WHERE c.country = 'India'
  AND c.status = 'active'
  AND o.order_date >= '2025-01-01'
GROUP BY c.customer_id
```

---

# 1. Parsing → Unresolved Logical Plan

Spark converts SQL into an internal tree (AST → logical plan).

```text
'Project [customer_id, sum(amount)]
+- 'Filter (country = 'India' AND status = 'active' AND order_date >= ...)
   +- 'Join (o.customer_id = c.customer_id)
      :- 'UnresolvedRelation orders
      +- 'UnresolvedRelation customers
```

Key points:

* Table names and columns are not validated yet
* Everything is symbolic (strings)

---

# 2. Analysis → Resolved Logical Plan

Spark validates against the catalog (Hive metastore / Unity Catalog).

```text
Project [c.customer_id, sum(o.amount)]
+- Filter (c.country = 'India' AND c.status = 'active' AND o.order_date >= ...)
   +- Join Inner, (o.customer_id = c.customer_id)
      :- Relation orders(customer_id, amount, order_date)
      +- Relation customers(customer_id, country, status)
```

Key changes:

* Tables resolved to actual metadata
* Columns are fully qualified
* Type checking is done

---

# 3. Logical Optimization → Optimized Logical Plan

Catalyst applies rule-based optimizations.

## a) Predicate Pushdown

Filters are pushed closer to data sources:

```text
orders → filter(order_date >= '2025-01-01')
customers → filter(country = 'India' AND status = 'active')
```

## b) Projection Pruning

Only required columns are kept:

```text
orders → [customer_id, amount, order_date]
customers → [customer_id, country, status]
```

## Optimized Plan

```text
Project [customer_id, sum(amount)]
+- Aggregate [customer_id]
   +- Join Inner
      :- Filter (order_date >= ...)
         +- orders [customer_id, amount]
      +- Filter (country = 'India' AND status = 'active')
         +- customers [customer_id]
```

Key impact:

* Less data read from disk
* Smaller join input
* Reduced memory and shuffle

---

# 4. Physical Planning → Best Physical Plan

Spark generates multiple strategies and selects one using cost-based optimization.

Possible strategies:

* Broadcast Hash Join
* Sort Merge Join
* Shuffle Hash Join

Assumption:

* `customers` is small

Chosen plan:

```text
HashAggregate
+- BroadcastHashJoin (build = customers)
   :- Filter orders
   +- BroadcastExchange
      +- Filter customers
```

Key decisions:

* Broadcast `customers` to all executors
* Avoid shuffle on the smaller side
* Perform join locally

---

# 5. Code Generation → JVM Bytecode

Spark generates Java bytecode using WholeStageCodeGen.

Instead of executing operators one-by-one:

```text
scan → filter → join → aggregate
```

Spark fuses them into a single compiled function:

```java
while (input.hasNext()) {
    if (order_date >= ...) {
        if (customer_map.contains(customer_id)) {
            total += amount;
        }
    }
}
```

Key points:

* Runs entirely in JVM
* No Python involved
* Minimizes function call overhead
* Uses tight loops and CPU-efficient execution

---

# 6. Execution → Distributed Execution

Execution happens across the cluster.

Flow:

1. Read partitions of `orders`
2. Apply filter (`order_date`)
3. Broadcast `customers` to all executors
4. Perform join locally in each executor
5. Aggregate per partition
6. Shuffle (if needed for final aggregation)
7. Return result

Output:

```text
customer_id | total_revenue
------------|--------------
101         | 50000
102         | 72000
```

---

# What Actually Improved Performance

1. Predicate pushdown
   Reduced data scanned from storage

2. Projection pruning
   Reduced unnecessary columns

3. Broadcast join
   Eliminated large shuffle

4. Whole-stage code generation
   Converted plan into optimized JVM bytecode

---

# Important Insight

* Spark SQL / DataFrame API stays inside JVM through this entire pipeline
* Python UDFs break this pipeline and introduce Python worker overhead
* That’s why built-in functions are significantly faster