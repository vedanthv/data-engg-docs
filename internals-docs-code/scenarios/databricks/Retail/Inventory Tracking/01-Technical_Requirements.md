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