## Databricks Unity Catalog Introduction

<img width="845" height="515" alt="image" src="https://github.com/user-attachments/assets/ddbab59d-b3f3-49bf-b72c-d277d5ca84d2" />

<img width="818" height="465" alt="image" src="https://github.com/user-attachments/assets/bc375d92-7ffe-45c8-967e-0df24a5a25bd" />

<img width="826" height="526" alt="image" src="https://github.com/user-attachments/assets/3b71c83d-dfd3-476a-a366-1f90f6d993de" />

⚠️ Metadata in Metastore is stored on control plane and actual data is on data plane.

<img width="884" height="546" alt="image" src="https://github.com/user-attachments/assets/2ac5bf99-51a6-4a9f-abb3-56c3e035e7fd" />

Catalog is called data securable object because without having access to ```USE CATALOG``` we cannot query any data objects.

### Securable Data Objects that we can use to manage external data sources

In addition to the database objects and AI assets that are contained in schemas, Unity Catalog also uses the following securable objects to manage access to cloud storage and other external data sources and services:

Storage credentials, which encapsulate a long-term cloud credential that provides access to cloud storage.

External locations, which reference both a cloud storage path and the storage credential required to access it. External locations can be used to create external tables or to assign a managed storage location for managed tables and volumes. 

Connections, which represent credentials that give read-only access to an external database in a database system like MySQL using Lakehouse Federation. 

Service credentials, which encapsulate a long-term cloud credential that provides access to an external service. See Create service credentials.

### Admin Roles

Account admins: can create metastores, link workspaces to metastores, add users, and assign privileges on metastores.

Workspace admins: can add users to a workspace, and manage many workspace-specific objects like jobs and notebooks. Depending on the workspace, workspace admins can also have many privileges on the metastore that is attached to the workspace.

Metastore admins: This optional role is required if you want to manage table and volume storage at the metastore level. It is also convenient if you want to manage data centrally across multiple workspaces in a region.

