### Role Based Access Control | Custom Role Definitions | Service Principals

**1️⃣ Azure RBAC Roles (Role-Based Access Control)**

**Purpose:**
RBAC in Azure controls who can do what on which resource.

**Key Concepts:**

Scope: Defines where the role applies (Subscription → Resource Group → Resource).

Role: Defines what actions can be performed.

Principal: The identity (user, group, or application) assigned the role.

<img width="901" height="350" alt="image" src="https://github.com/user-attachments/assets/1cfbf694-41cf-4218-85a9-2d00f4f3eac9" />

2️⃣ Custom Roles

Purpose:
When built-in roles are too broad or restrictive, you can create custom roles with exactly the permissions you need.

**How it works:**

- Define a JSON file with allowed actions (Microsoft.Storage/storageAccounts/blobServices/containers/read, etc.)

- Assign it to users/groups/service principals.

Example JSON for a custom role (ADLS read-only access):

```json
{
  "Name": "ADLS ReadOnly",
  "IsCustom": true,
  "Description": "Read-only access to ADLS Gen2 containers",
  "Actions": [
    "Microsoft.Storage/storageAccounts/blobServices/containers/read",
    "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read"
  ],
  "NotActions": [],
  "AssignableScopes": ["/subscriptions/<subscription-id>"]
}

```
When to use:

You want a minimal-privilege principle, e.g., a BI service can only read blobs, not delete them.

**3️⃣ Service Principals**

**Purpose:**
A service principal is like a “user identity” for applications, scripts, or automated services.

**Why needed:**

- Azure RBAC requires an identity for access.
- You don’t want to use your personal account for automated tasks.

Example: Databricks accessing ADLS via a service principal.

**Types of Service Principals Authentication:**

- Client Secret: Password-like string.
- Certificate: Secure certificate authentication.
- Managed Identity (Recommended for Databricks UC Connector): Azure handles the credentials for you.

**How it works in practice (Databricks + ADLS)**

- Create a service principal in Azure AD.
- Assign RBAC (e.g., Storage Blob Data Contributor) on the storage account/container.
- Use this SP to create a Databricks Storage Credential (or UC connector).
- Unity Catalog or your clusters use the SP to access storage without exposing your personal account.
