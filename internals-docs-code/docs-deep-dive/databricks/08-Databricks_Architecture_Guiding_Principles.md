## Databricks Guiding Priciples for Lakehouse

### Curate Data and Offer Trusted Products

![alt text](https://snipboard.io/NyD1a0.jpg)

Curating data by establishing a layered (or multi-hop) architecture is a critical best practice for the lakehouse, as it allows data teams to structure the data according to quality levels and define roles and responsibilities per layer. A common layering approach is:

- Ingest layer: Source data gets ingested into the lakehouse into the first layer and should be persisted there. When all downstream data is created from the ingest layer, rebuilding the subsequent layers from this layer is possible, if needed.
  
- Curated layer: The purpose of the second layer is to hold cleansed, refined, filtered and aggregated data. The goal of this layer is to provide a sound, reliable foundation for analyses and reports across all roles and functions.
  
- Final layer: The third layer is created around business or project needs; it provides a different view as data products to other business units or projects, preparing data around security needs (for example, anonymized data), or optimizing for performance (with pre-aggregated views). 

The data products in this layer are seen as the truth for the business.

Pipelines across all layers need to ensure that data quality constraints are met, meaning that data is accurate, complete, accessible, and consistent at all times, even during concurrent reads and writes. 

The validation of new data happens at the time of data entry into the curated layer, and the following ETL steps work to improve the quality of this data. 

Data quality must improve as data progresses through the layers and, as such, the trust in the data subsequently increases from a business point of view.

### Democratizing Data Value through Self Service

The best data lake cannot provide sufficient value, if users cannot access the platform or data for their BI and ML/AI tasks easily. Lower the barriers to accessing data and platforms for all business units. Consider lean data management processes and provide self-service access for the platform and the underlying data.

![alt text](https://snipboard.io/Nu275c.jpg)

Businesses that have successfully moved to a data-driven culture will thrive. This means every business unit derives its decisions from analytical models or from analyzing its own or centrally provided data. For consumers, data has to be easily discoverable and securely accessible.

A good concept for data producers is “data as a product”: The data is offered and maintained by one business unit or business partner like a product and consumed by other parties with proper permission control. Instead of relying on a central team and potentially slow request processes, these data products must be created, offered, discovered, and consumed in a self-service experience.

However, it's not just the data that matters. The democratization of data requires the right tools to enable everyone to produce or consume and understand the data. For this, you need the data lakehouse to be a modern data and AI platform that provides the infrastructure and tooling for building data products without duplicating the effort of setting up another tool stack.

### Adopt an Organization Wide Data and AI Governance Strategy

![alt text](https://snipboard.io/0RjwK6.jpg)

Data governance is a broad topic. The lakehouse covers the following dimensions:

- Data quality

The most important prerequisite for correct and meaningful reports, analysis results, and models is high-quality data. Quality assurance (QA) needs to exist around all pipeline steps. Examples of how to implement this include having data contracts, meeting SLAs, keeping schemas stable, and evolving them in a controlled way.

- Data catalog

Another important aspect is data discovery: Users of all business areas, especially in a self-service model, must be able to discover relevant data easily. Therefore, a lakehouse needs a data catalog that covers all business-relevant data. The primary goals of a data catalog are as follows:

  - Ensure the same business concept is uniformly called and declared across the business. You might think of it as a semantic model in the curated and the final layer.
  
  - Track the data lineage precisely so that users can explain how these data arrived at their current shape and form.
  
  - Maintain high-quality metadata, which is as important as the data itself for proper use of the data.

- Access Control
  
As the value creation from the data in the lakehouse happens across all business areas, the lakehouse must be built with security as a first-class citizen. Companies might have a more open data access policy or strictly follow the principle of least privileges. 

Independent of that, data access controls must be in place in every layer. It is important to implement fine-grade permission schemes from the very beginning (column- and row-level access control, role-based or attribute-based access control). 

Companies can start with less strict rules. But as the lakehouse platform grows, all mechanisms and processes for a more sophisticated security regime should already be in place. Additionally, all access to the data in the lakehouse must be governed by audit logs from the get-go.

### Build to Scale and Optimize for Costs and Performance

Standard ETL processes, business reports, and dashboards often have a predictable resource need from a memory and computation perspective. However, new projects, seasonal tasks, or modern approaches like model training (churn, forecast, maintenance) generate peaks of resource need. 

To enable a business to perform all these workloads, a scalable platform for memory and computation is necessary. New resources must be added easily on demand, and only the actual consumption should generate costs. As soon as the peak is over, resources can be freed up again and costs reduced accordingly. Often, this is referred to as horizontal scaling (fewer or more nodes) and vertical scaling (larger or smaller nodes).

Scaling also enables businesses to improve the performance of queries by selecting nodes with more resources or clusters with more nodes. But instead of permanently providing large machines and clusters they can be provisioned on demand only for the time needed to optimize the overall performance to cost ratio. 

Another aspect of optimization is storage versus compute resources. Since there is no clear relation between the volume of the data and workloads using this data (for example, only using parts of the data or doing intensive calculations on small data), it is a good practice to settle on an infrastructure platform that decouples storage and compute resources.

