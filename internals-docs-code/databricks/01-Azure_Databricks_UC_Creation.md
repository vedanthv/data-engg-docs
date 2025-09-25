## How to configure and create Unity Catalog in Azure

We need to setup Storage Account under the same RG where Dsatabricks Workspace is deployed.

Also we need to create a UC Databricks Connector to connect to the resource group.

Then give Storage Data Contributor access to the UC Databrticks Connector Managed Identity.

Go to Databricks [Login Page](https://accounts.azuredatabricks.net/login) and select the account that is the admin.

Go to catalog and create a new metastore. 
<img width="1919" height="473" alt="image" src="https://github.com/user-attachments/assets/bc524827-87df-4c19-8b39-a37d462afd7a" />

Fill in the details

<img width="1171" height="666" alt="image" src="https://github.com/user-attachments/assets/acd4a196-7aec-40f0-8d87-a105967cd629" />

<img width="1916" height="660" alt="image" src="https://github.com/user-attachments/assets/727c3df7-614d-4588-9734-df12a0aa0ef1" />

Imp : Login from your admin account

We can now see more options like Add Catalog, Add Credentials, Create Volume after UC is enabled.

<img width="1918" height="522" alt="image" src="https://github.com/user-attachments/assets/1f93d9f8-adf0-4490-960a-7d682b86e868" />
