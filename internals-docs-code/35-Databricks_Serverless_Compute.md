## Databricks Serverless Compute

### Architecture

<img width="1711" height="904" alt="image" src="https://github.com/user-attachments/assets/1e1d3b90-e81e-4497-9e31-4b78c4d6a354" />

Unlike Classic Architecture, the compute is not on the data plane, its on the compute plane managed by Databricks.

Databricks spins up clusters in the same region as the workspace to reduce latency.

The VM's used for one customer is not reused again.

We need to enable serverless compute in account console to create serverless cluster.
