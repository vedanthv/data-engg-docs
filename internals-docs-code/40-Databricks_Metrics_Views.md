# Metrics Views in Databricks

<img width="1184" height="688" alt="image" src="https://github.com/user-attachments/assets/8c38c42f-9765-4b3b-b35a-b5265114c5e2" />

<img width="1830" height="817" alt="image" src="https://github.com/user-attachments/assets/68e993d4-67c6-4372-a346-849b84375ec5" />

## Example Use Case

<img width="1172" height="686" alt="image" src="https://github.com/user-attachments/assets/df78a856-1b45-4787-a50b-a6dedc61440c" />

## How to Create Metrics Views in Databricks?

Measures are quantitative values like sales, revenue etc.

Dimensions are used to support measures like year, month etc. Eg: sales per year, revenue per month

Any joins in metric views are left outer joins.

Metric views are defined in yaml format

Eg:

```yaml
version: 0.1

source: dev.bronze.orders_raw

dimensions:
  - name: Order Key
    expr: o_orderkey

  - name: Customer Key
    expr: o_custkey

  - name: Order Status
    expr: o_orderstatus

  - name: Order Status Readable
    expr: >
      case 
        when o_orderstatus = 'O' then 'Open'
        when o_orderstatus = 'F' then 'Fulfilling'
        when o_orderstatus = 'P' then 'Processing'
      end

  - name: Order Date
    expr: o_orderdate

  - name: Order Year
    expr: DATE_TRUNC('year',o_orderdate)

  - name: Order Priority
    expr: o_orderpriority

  - name: Clerk
    expr: o_clerk

  - name: Ship Priority
    expr: o_shippriority

measures:
  - name: Total Price
    expr: SUM(o_totalprice)

  - name: Average Total Price
    expr: AVG(o_totalprice)

  - name: Count of Orders
    expr: COUNT(DISTINCT(o_orderkey))
```

<img width="1163" height="786" alt="image" src="https://github.com/user-attachments/assets/0d4f3361-edc8-4a65-b94a-3b76f55968b4" />

<img width="1139" height="650" alt="image" src="https://github.com/user-attachments/assets/25b4616b-1efb-4624-aeb9-79bc9851f076" />

Querying the metric view

<img width="1117" height="416" alt="image" src="https://github.com/user-attachments/assets/ed995338-1a46-414d-b470-a7faf07281c7" />

### Window Functions

```yaml
measures:
  - name: Total Price
    expr: SUM(o_totalprice)

  - name: Average Total Price
    expr: AVG(o_totalprice)

  - name: Count of Orders
    expr: COUNT(DISTINCT(o_orderkey))

  - name: Total Orders Current Year
    expr: COUNT(DISTINCT o_orderkey)
    window:
      - order: Order Year
        range: current
        semiadditive: last

  - name: Total Orders Last Year
    expr: COUNT(DISTINCT o_orderkey)
    window:
      - order: Order Year
        range: trailing 1 year
        semiadditive: last
```

### Final Metric Views with Joins

```yaml
version: 0.1

source: dev.bronze.orders_raw

joins:
  - name: cust_dim
    source: dev.bronze.customer_raw
    on: cust_dim.c_custkey = source.o_custkey

dimensions:
  - name: Order Key
    expr: o_orderkey

  - name: Customer Key
    expr: o_custkey

  - name: Order Status
    expr: o_orderstatus

  - name: Order Status Readable
    expr: >
      case 
        when o_orderstatus = 'O' then 'Open'
        when o_orderstatus = 'F' then 'Fulfilling'
        when o_orderstatus = 'P' then 'Processing'
      end

  - name: Customer Market Segment
    expr: cust_dim.c_mktsegment

  - name: Order Date
    expr: o_orderdate

  - name: Order Year
    expr: DATE_TRUNC('year',o_orderdate)

  - name: Order Priority
    expr: o_orderpriority

  - name: Clerk
    expr: o_clerk

  - name: Ship Priority
    expr: o_shippriority

measures:
  - name: Total Price
    expr: SUM(o_totalprice)

  - name: Average Total Price
    expr: AVG(o_totalprice)

  - name: Count of Orders
    expr: COUNT(DISTINCT(o_orderkey))

  - name: Total Orders Current Year
    expr: COUNT(DISTINCT o_orderkey)
    window:
      - order: Order Year
        range: current
        semiadditive: last

  - name: Total Orders Last Year
    expr: COUNT(DISTINCT o_orderkey)
    window:
      - order: Order Year
        range: trailing 1 year
        semiadditive: last

  - name: Year on Year Growth
    expr: MEASURE(`Total Orders Current Year`)-MEASURE(`Total Orders Last Year`)
```

### Clear Example of Metric View vs Standard View

---

## 1. Standard View Approach

If you only had **standard views**, you’d need **separate SQL queries** (or separate views) for each grouping level.

### (a) Group by **State**

```sql
SELECT
    state,
    SUM(revenue) / COUNT(DISTINCT customer_id) AS revenue_per_customer
FROM orders
GROUP BY state;
```

### (b) Group by **Region**

```sql
SELECT
    region,
    SUM(revenue) / COUNT(DISTINCT customer_id) AS revenue_per_customer
FROM orders
GROUP BY region;
```

### (c) Group by **Country**

```sql
SELECT
    country,
    SUM(revenue) / COUNT(DISTINCT customer_id) AS revenue_per_customer
FROM orders
GROUP BY country;
```

👉 Notice: you either write **multiple queries/views**, or you compute all combinations in one big query with `GROUP BY CUBE(country, region, state)` (which can be heavy).

---

## 2. Metric View Approach

With a **metric view**, you define the **metric once**:

```sql
CREATE OR REPLACE METRIC VIEW revenue_metrics
AS SELECT
    country,
    region,
    state,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT customer_id) AS distinct_customers
FROM orders
GROUP BY country, region, state;
```

* **Metric defined:**

  ```sql
  revenue_per_customer = total_revenue / distinct_customers
  ```

Now, when analysts query this metric view, they don’t need to rewrite SQL for each grouping.
The query engine rewrites it under the hood.

---

### Example Queries on Metric View

#### (a) Group by **State**

```sql
SELECT
    state,
    total_revenue / distinct_customers AS revenue_per_customer
FROM revenue_metrics;
```

#### (b) Group by **Region**

```sql
SELECT
    region,
    SUM(total_revenue) / SUM(distinct_customers) AS revenue_per_customer
FROM revenue_metrics
GROUP BY region;
```

#### (c) Group by **Country**

```sql
SELECT
    country,
    SUM(total_revenue) / SUM(distinct_customers) AS revenue_per_customer
FROM revenue_metrics
GROUP BY country;
```

👉 Difference: You don’t redefine the metric — you just group by a different **dimension** (state, region, country).
Databricks rewrites the query correctly to maintain **metric consistency** (so that KPIs mean the same thing everywhere).

---

✅ **In short:**

* **Standard views** = you must predefine each grouping (state/region/country).
* **Metric views** = define the metric once (`revenue_per_customer`) and reuse across any dimension.
