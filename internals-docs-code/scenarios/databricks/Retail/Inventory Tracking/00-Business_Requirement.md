## Retail SKU Tracking

Retailer X needs a reliable, near-real-time SKU Tracking capability to monitor inventory movement across stores, warehouses and online channels. The objective is to produce a single source of truth for SKU on-hand and movement, detect stockouts and low-stock conditions early, enable fast root-cause analysis (sales vs shipments vs returns), improve availability, reduce lost sales, and optimize replenishment — all while ensuring governed access to inventory data for operations, merchandising, and finance.

### Business Objectives

**Accurate on-hand inventory (per SKU × location)**

Maintain a canonical, up-to-date view of on-hand inventory for every SKU at store and warehouse locations, with at least “near-real-time” freshness (target: ≤ 5–15 minutes for critical locations).

**Detect and act on stockouts / low stock**

Automatically detect stockouts and send prioritized alerts to store ops and replenishment teams to reduce out-of-stock lost sales by X% (target reduction: 10–25% in year 1).

**Understand inventory drivers (root cause)**

Attribute inventory changes to transactions (sales), receipts, transfers, and returns so business users can distinguish demand vs supply issues.

**Improve replenishment & planning**

Provide accurate inputs to replenishment and planning systems (EOQ, reorder points, vendor orders), improving forecast accuracy and lowering safety stock.

**Provide governed data for analytics and ML**

Deliver curated Gold tables for BI dashboards, machine learning models (demand forecasting, anomaly detection), and downstream systems — governed by Unity Catalog and RBAC.

### Stakeholders

Head of Merchandising / Inventory Planning — business owner; defines KPI targets and thresholds.

Store Operations / Regional Ops Managers — consumers of per-store alerts and dashboards; act on low-stock alerts.

Supply Chain / Warehouse Managers — monitor receipts, throughput, and exceptions.

### Business KPIs

**Out-of-stock (OOS) reduction:** decrease OOS incidents for tracked SKUs by ≥ 10% within 6 months.

**Sales retention:** reduce lost sales due to stockouts by target percentage (business to define baseline).

**Inventory turns / DOI improvement:** reduce excess safety stock; improve turns by X% in 12 months.

### Data Requirements and Sources

1. POS Events - transactional sales (transaction_id, ts, sku, qty, price, store_id, payment_type). Source: POS system / middleware.
2. WMS Snapshots - periodic on-hand snapshots per warehouse (snapshot_ts, sku, on_hand, warehouse_id).
3. Shipment Receipts - inbound shipments and transfers (shipment_id, ts, sku, qty, location).
4. Returns Tracking - return events (return_id, ts, sku, qty, location, reason).
5. Product Master - SKU attributes (sku, title, category, cost, price, dimensions, active_flag).
6. Store / Location Master - location metadata (store_id, type, region, manager).

### Expected Business Impact

**Reduced lost sales:** by preventing stockouts with faster detection & replenishment. If stockouts currently cause 2% lost sales on $100M revenue, reducing OOS by 20% saves $400k/year (example).

**Lower carrying costs: ** improved DOI and demand insights reduce excess safety stock — savings vary by inventory value and turnover improvements.

**Operational efficiency:** fewer manual investigations; store managers get precise alerts and recommended actions.

**Faster analytics:** unified datasets reduce time to insight for merchandising and supply chain teams.

