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

## Technical Requirements

### Data and Operations Success Criteria

**Inventory freshness:** 90% of critical SKUs (top N) show ≤ 15 minute data lag.

**Data completeness:** 99.9% of inbound events are ingested and processed (measured by files/events count).

**Pipeline reliability:** 99% job success rate (no more than N failures per month).

**Alert latency:** time from detection to alert < 5 minutes for critical alerts.

### Data Quality and Governance Requirements

**Completeness:** expected counts from sources vs actual ingested counts; automated alerts on anomalies.

**Accuracy:** checksum reconciliation (e.g., daily compare WMS snapshot on_hand vs computed on_hand from transactions + receipts).

**Timeliness:** freshness SLA monitoring for critical sources.

**Traceability:** retain raw Bronze data for audit and lineage; link ledger entries back to raw events (event_id, source_file, ingestion_ts).

**Access controls:** Unity Catalog object permissions, row/column masking for PII in product/supplier fields.

**Retention & archival:** raw Bronze kept for 90–365 days (depends on regulatory/commercial requirements), Silver/Gold per business need.

### Functional Requrirements

**Ingest:** continuous ingestion of events (Auto Loader/streaming), plus periodic WMS snapshots.

**Normalize & dedupe:** normalize fields and dedupe on event_id + source; dedupe logic must be idempotent.

**Inventory ledger:** produce append-only ledger of delta_qty per event, preserving full audit trail.

**Stateful upserts:** apply ledger deltas to a canonical inventory_current(sku, location, on_hand) via idempotent MERGE (SCD1).

**Metrics:** compute daily/hourly SKU metrics (sales, receipts, returns, net_change, DOI).

**Alerts:** rule-based alerts (thresholds, stockouts), prioritized and routed to Ops (email/Slack/Teams).

**APIs / exports:** provide data access via Databricks SQL views, Delta Sharing (optional), or push to downstream systems.

**Monitoring:** pipeline health dashboards, SLA alerts, DLT expectations (if used).

### Non Functional Requirements

**Scalability:** handle peak event rates (estimate: transactions per minute for peak days). Design will scale horizontally (Auto Loader + job clusters).

**Availability:** target uptime for pipelines (e.g., 99% during business hours).

**Security:** data at rest encryption (ADLS), secrets in Key Vault; least-privilege access via Unity Catalog.

**Performance:** query latency targets for Gold aggregated queries (e.g., < 2 seconds for top queries on DBSQL).

**Costs:** ability to control compute costs via compute policies and job cluster sizing.