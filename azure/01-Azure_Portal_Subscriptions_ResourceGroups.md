## Azure Portal, Subscriptions and Resource Groups

### Resource Groups

In the process of working with Azure, you quickly encounter many different resources connected to it, for example, virtual machines, storage accounts, and databases. When you have such a large number of resources in Azure, it becomes challenging to track the various ones in use or simply keep track of them in general. That is where Resource Group in Azure comes in.

A Resource Group in Azure is a method of categorizing or bringing related resources under a similar group in the Azure platform. Similar to how a folder is used to store all the relevant documents required to complete a certain task or work on an application. This allows resources to be easily managed, monitored, and protected due to their central location as well as being easier to group.

The resource group can be all the resources for the solution or only discrete resources that you want to create as a group. The resource group in Azure scope is also used throughout the Azure portal to build views that contain cross-resource information. For example:

**Metrics Blade**

<img width="1897" height="742" alt="image" src="https://github.com/user-attachments/assets/530c6897-43c1-4f91-bcb2-0990a9212c4e" />

**Deployments Blade**

<img width="1914" height="765" alt="image" src="https://github.com/user-attachments/assets/fcd97a77-36d9-469f-a5ef-56bd338a62a9" />

**Policy and Compliance Blade**

<img width="1918" height="669" alt="image" src="https://github.com/user-attachments/assets/3b5e311d-dfc0-4359-b5f0-bd341d6ef56f" />

**Diagnostics Blade to send resource group activity to one data storage**

<img width="1919" height="807" alt="image" src="https://github.com/user-attachments/assets/4712defa-74a4-4152-9416-c978363fa5af" />

#### Advantages

**Logical Grouping**: Resources in the Azure resource group can be related as they are based on a common parameter like requirements for a particular application or service. By arranging resources in such a manner, there is easy organization and management of resources to help achieve set objectives.

**Deployment Management**: You can deploy and manage resources all at once in a resource group in Azure if needed. This is especially helpful when applying large solutions in organizations with numerous dependencies between resources.

**Access Control**: Azure Resource groups enable you to implement Role-Based Access Control that is RBAC. This entails that you get to decide who is allowed to update, or even use, certain resources that are enclosed in a given group.

**Resource Lifecycle Management**: Resource groups in Azure can also be applied to control the resources’ life cycle. All resources within the Azure resource groups can be deployed, updated or deleted in a single attempt as a group.

**Cost Management**: When such resources are disaggregated you can easily manage your costs since they are frequently related. Azure also has features that allow displaying consumption and costs for every created resource group if it is a concern for the user.

🔹 Azure Hierarchy: Resources → Resource Groups → Subscriptions

#### 1. **Azure Resources**

* **Definition**: The actual services you create/use in Azure.
* **Examples**:

  * A **Storage Account** (ADLS Gen2)
  * A **SQL Database**
  * A **Virtual Machine (VM)**
  * A **Synapse Workspace**
* **Key point**: These are the *building blocks*. Everything you deploy in Azure is a **resource**.

#### 2. **Resource Groups (RG)**

* **Definition**: A logical **container** that holds related Azure resources.
* **Purpose**:

  * Organize resources (by project, department, environment).
  * Apply **RBAC (access control)** at the group level.
  * Apply **tags** for cost management.
  * Manage lifecycle (delete the RG → all resources inside are deleted).
* **Example**:

  * RG: `RetailAnalytics-Dev-RG`

    * Resources inside:

      * `RetailADLS` (Storage Account)
      * `RetailSQLDB` (Azure SQL DB)
      * `RetailADF` (Data Factory)

#### 3. **Subscriptions**

* **Definition**: The **billing boundary** in Azure. It defines how you pay and how access is controlled.
* **Purpose**:

  * Groups **resource groups + resources** under one billing account.
  * Has **spending limits, quotas, and policies**.
  * Tied to an **Azure Active Directory tenant**.
* **Examples**:

  * `Pay-As-You-Go Subscription`
  * `Free Trial Subscription`
  * `Enterprise Agreement Subscription` (corporate)

🔹 Hierarchy Diagram

```
Subscription (Billing boundary, access policies)
│
├── Resource Group 1 (Logical container)
│   ├── Resource: Azure Data Lake Storage
│   ├── Resource: Azure SQL Database
│   └── Resource: Azure Data Factory
│
└── Resource Group 2
    ├── Resource: Event Hub
    ├── Resource: Synapse Analytics
    └── Resource: Key Vault
```

🔹 Real-Life Analogy

* **Subscription** = A **house lease contract** (defines who pays the bills, how much you can use).
* **Resource Group** = A **room in the house** (you organize furniture/resources here).
* **Resource** = A **piece of furniture** (bed, desk, chair → SQL DB, Storage, ADF).

🔹 Interview Cheat Sheet

**Q1. What is the difference between a Resource and a Resource Group?**

* A resource is the actual service (e.g., Storage, SQL DB).
* A resource group is a logical container for related resources.

**Q2. Can a resource exist in multiple resource groups?**

* ❌ No, a resource belongs to only **one resource group**.
* But you can move it to another RG (with limitations).

**Q3. What is the difference between a Subscription and a Resource Group?**

* Subscription = billing & access boundary.
* Resource Group = logical container inside a subscription for resources.

**Q4. Can a resource group span multiple subscriptions?**

* ❌ No, a resource group belongs to **exactly one subscription**.

**Q5. Why do we need multiple subscriptions?**

* To separate **environments** (Dev/Test/Prod), billing accounts, or departments.

---

✅ Quick memory hook:
**Resource → The “what” (service).**
**Resource Group → The “where” (container).**
**Subscription → The “who pays” (billing).**

---
