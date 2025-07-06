## Microsoft Fabric 

## Section 1 : Introduction and Installation

### 1. Introduction

![image](https://github.com/user-attachments/assets/7c34baaa-fe51-4d01-b47e-34a19eb573e0)

![image](https://github.com/user-attachments/assets/0bf7b0ad-55f1-4744-a6d9-98bdfb9ac455)

### 2. Pre Requisites

![image](https://github.com/user-attachments/assets/7eb5d4bc-accd-44f9-a276-11acfb8a3f5b)

### 3. Project Architecture

![image](https://github.com/user-attachments/assets/10271b70-df84-4690-a1ac-1d0b823aca45)

![image](https://github.com/user-attachments/assets/73e21ba7-23e7-4d80-ba87-617384b8de4f)

![image](https://github.com/user-attachments/assets/39a6f9d6-7842-4401-8f02-486ea80b82ce)

### 4. Installation

- Ensure Hierarchial namespace enabled to create Azure Data Lake Storage Gen2 resource.
- We dont get charged for Synapse Analytics until we create compute.

#### Create Spark Pool

Spark Pool Settings

![image](https://github.com/user-attachments/assets/047a5c38-a11d-45d4-bf17-dd8330253305)

## Section 2 : Understanding Microsoft Fabric

### 5. Evolution of Architecture

![image](https://github.com/user-attachments/assets/155a9882-97a7-4cbd-a37b-720b8b04e2fb)

Metadata caching layer brings ACID properties.

### 6. Delta Lake Structure

![image](https://github.com/user-attachments/assets/5103715a-10a1-483c-a784-b02d0932867d)

![image](https://github.com/user-attachments/assets/c9d5b8eb-e2b9-4d2d-a202-3406834797c4)

![image](https://github.com/user-attachments/assets/259e096d-ebe7-49ba-9547-9a9749b7ad6c)

**What happens under the hood?**

![image](https://github.com/user-attachments/assets/cf9707b4-395e-40cd-b714-17ea79e1bab2)

### 7. Why Fabric?

![image](https://github.com/user-attachments/assets/b226825b-0465-45e6-81f4-18a1ac18b586)

Lot of services need to be created individually.

![image](https://github.com/user-attachments/assets/617423df-80b0-4979-ab03-b15a142df5a9)

![image](https://github.com/user-attachments/assets/91ef44d2-1b7a-4312-96f7-0e9b1a7ecd1e)

### 8. Starting Up Fabric

- Login to fabric with Microsoft entra id account for free trial.
- Go to Settings -> Admin Portal -> enable fabric

### 9. Licensing and Costs

![image](https://github.com/user-attachments/assets/fbadcf29-9e2c-4ec0-8aa7-d47596d1563f)

![image](https://github.com/user-attachments/assets/f936326d-f986-4073-88fc-42bb49f488c5)

![image](https://github.com/user-attachments/assets/d8eb0744-db7f-435a-a934-b9ecf9b41d4a)

Creating Azure Capacity

[Microsoft Official Link](https://learn.microsoft.com/en-gb/fabric/enterprise/buy-subscription)

If you are not able to select subscription follow these steps

- If you can open the subscription but not perform actions:

- Go to Azure Portal > Subscriptions

- Click on the subscription

- Go to Access Control (IAM) > Role Assignments

- Filter by Role = Owner

- You’ll see a list of users, groups, or service principals who are assigned the “Owner” role.

### 10. Fabric Terms

![image](https://github.com/user-attachments/assets/6b106735-7552-40e4-92c6-981799188b78)

Example

![image](https://github.com/user-attachments/assets/ea624065-8cf1-4ae6-a52e-e6a49016b0ac)

### 11. OneLake in Fabric

Data is stored in One data lake based on the workspace names.

There is only one storage point.

![image](https://github.com/user-attachments/assets/7de4af18-ffee-4349-81e5-077ea964aaeb)

We will have only one copy of data and nothing is duplicated.

The files are stored in parquet metadata powered by delta lake.

### 12. One Copy for all computes

All engines store data in One Lake.

![image](https://github.com/user-attachments/assets/8d81d3e9-9b42-4806-9ad6-b137c84579f9)

All data stored in delta parquet format.

## Section 3 : Fabric Lakehouse

### 13. Microsoft Fabric Workspaces

![image](https://github.com/user-attachments/assets/af9bbffc-13bf-468a-b512-1116a40bbc9f)

### 14. Workspace Roles

![image](https://github.com/user-attachments/assets/a9947c7c-7a84-427f-ad55-c3ef9d26544b)

### 15. Creating a Lakehouse

When we create a Lakehouse there are three things:

![image](https://github.com/user-attachments/assets/b728c87a-6d3c-44c1-ae1a-5a463a5ce73c)

Lakehouse - data platform to store the data.

Semantic Model - Dataset to present to powerbi.

SQL Endpoint - we can run queries.

### 16. Lakehouse Explorer

![image](https://github.com/user-attachments/assets/ee727432-a078-47a8-9703-585519e4b696)

Data Uploaded to table

![image](https://github.com/user-attachments/assets/18d37644-fba7-4b13-8464-08ddf8d88496)

Table created from the file

![image](https://github.com/user-attachments/assets/bf739a69-0d03-473a-bab5-a40308ba275f)

Files are stored in parquet with delta log

![image](https://github.com/user-attachments/assets/6a48dcb6-d2ab-4fcc-b095-c8764f92a49e)

Here is delta log info
![image](https://github.com/user-attachments/assets/c9441de4-89cd-407c-a2ad-1f433abf438e)

On clicking properties we can see if its managed or not.

![image](https://github.com/user-attachments/assets/ecb5ea00-99f2-4774-a51a-07e99a0d410a)

### 17. SQL Analytics Endpoint

We can only read data from this enpoint not write / update.

![image](https://github.com/user-attachments/assets/477346d2-6a2c-4349-aee2-508b41531770)

We can create views

![image](https://github.com/user-attachments/assets/a7d64053-b50a-4eb8-8f36-e366462bc167)

### 18. Default Semantic Model View

![image](https://github.com/user-attachments/assets/a3689d2c-eada-4cb7-8944-8dfe5fa1728c)

![image](https://github.com/user-attachments/assets/5e9409fe-741c-43cf-a325-16597edb3782)

In the context of the semantic model in Microsoft Fabric lakehouse, the semantic model itself doesn't directly store raw data. Instead, it provides a logical, structured view of the data stored in the underlying data lake or warehouse.

The semantic model acts as an abstraction layer that organizes and simplifies access to the data, making it easier for reporting and analysis tools to query the data efficiently. The raw data is stored in the data lake or data warehouse, and the semantic model helps to structure and shape this data into meaningful formats suitable for analysis and reporting.

## Section 4 : Data Factory in Fabric

### 19. How to Load data in Lakehouse 

![image](https://github.com/user-attachments/assets/c6ffa031-73fc-41d3-9c90-55af9b85cf3a)

### 20. Fabric vs Azure Data Factory

![image](https://github.com/user-attachments/assets/73beab74-d8a7-4968-a734-5ab28f81b536)

### 21. Data Gateway Types

- Gateway connects two networks

![image](https://github.com/user-attachments/assets/fdcb28e4-76c0-45ac-a248-f3c15d3a2708)

Imagine you have a big box of toys at home, and you want to show them to your friends who live far away. You have two ways to show them: one way is through a special window, and the other way is to use a delivery truck.

**On-Premise Data Gateway (like a special window):**

This is like a window that you open to let your friends see your toys without taking them out of the box. It connects your toys (data) at home to an online game or app that your friends are using. You can think of this as a way to share data that's stored in your house but don't let your friends take it out or change it. It keeps your toys safe inside but lets you show them off.

**VNet Data Gateway (like a delivery truck):**

This method is like using a delivery truck to send some of your toys to your friends' houses. The VNet (Virtual Network) is a big, secure road that connects your house and your friends' houses. When you use this truck, you're moving data across this secure road, allowing your friends to actually play with the toys (data) over at their place, but still keeping it safe and controlled.
So, in simple terms, the on-premise data gateway lets you show your toys to friends securely while they are still at home, and the VNet data gateway lets you share some toys by sending them out safely to your friend's houses.

![image](https://github.com/user-attachments/assets/c42ed06c-7d4a-4d4e-bbf3-603290e4e1cc)

![image](https://github.com/user-attachments/assets/7d38f9d9-f925-4b43-9280-8d582acb5db0)

![image](https://github.com/user-attachments/assets/2873af2a-5ef8-48ef-a7de-ecd16bff993d)

### 22. Connections

![image](https://github.com/user-attachments/assets/35031f0b-a5a4-4c43-80fd-e48b8d1705a3)

Click Gear Icon -> Manage Connections and Gateways

![image](https://github.com/user-attachments/assets/78e1c5f4-cad0-4c81-af0f-75ff4c2f179a)

- Gateway : Equivalent to Integration Runtime in ADF
- Connection : Similar to Linked Service in ADF

### 23. Creating Pipeline

Step 1 : Lookup Activity to query the SQL connecte ddatabase

![image](https://github.com/user-attachments/assets/55a1c0f3-ed62-48b8-aea9-edb3b214f13a)

Step 2 : Foreach activity to go over both tables

![image](https://github.com/user-attachments/assets/36095c7e-d67b-40d7-8d43-5389fcab9604)

Step 3 : For each iteration run copy data activity

![image](https://github.com/user-attachments/assets/53246f88-ec3d-476e-9cca-a34f89c2e5dd)

Destination : Our Onelake data lakehouse

![image](https://github.com/user-attachments/assets/c1bb5fa8-4e6a-4838-be3d-9fdd20962072)

### 24. Dataflow Gen2

![image](https://github.com/user-attachments/assets/75c29c43-44aa-4e96-ae2d-508d1339bd54)
