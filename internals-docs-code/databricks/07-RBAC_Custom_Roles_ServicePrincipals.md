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


### 🔹 Azure AD Interview Questions (for Data Engineers)

Q1. What is Azure Active Directory (Azure AD)?

Answer:
Azure AD is Microsoft’s cloud-based identity and access management service. It authenticates users, applications, and services, and authorizes them to access Azure resources. Unlike on-prem AD, Azure AD is designed for cloud-first apps, RBAC, and SSO.

Q2. What is the difference between Azure AD Users, Groups, Service Principals, and Managed Identities?

Answer:

Users → Human identities (employees, admins).

Groups → Collection of users/SPs for easier role assignment.

Service Principal (SP) → Non-human identity for applications to access resources.

Managed Identity → A special type of SP managed automatically by Azure, used by Azure services (like Databricks, ADF) to access resources without credentials.

Q3. What’s the difference between Service Principal and Managed Identity?

Answer:

Service Principal → You create it manually, assign roles, and manage secrets/certs.

Managed Identity → Azure creates/rotates credentials automatically, no secrets to manage.
Example: Databricks UC Connector → Managed Identity (no secrets). A legacy pipeline using Python SDK → Service Principal (with client secret).

Q4. How does RBAC work in Azure?

Answer:

RBAC (Role-Based Access Control) grants permissions at scope levels: Subscription → Resource Group → Resource.

Roles are assigned to principals (user, group, SP, or MI).

Built-in roles include: Owner, Contributor, Reader, Storage Blob Data Reader/Contributor.
Example: Assign Storage Blob Data Contributor to a Databricks SP so it can read/write to ADLS.

Q5. How is Azure AD different from On-prem Active Directory?

Answer:

AD (On-prem) → Kerberos/NTLM, domain-joined machines, Windows environments.

Azure AD → OAuth2, SAML, OpenID Connect, cloud-first, SSO, SaaS app integration.

Azure AD cannot join servers to a domain but can integrate with ADDS (hybrid).

Q6. What is Conditional Access in Azure AD?

Answer:
It enforces policies like MFA, location restrictions, or device compliance before granting access.
Example: Require MFA for accessing Databricks workspace from outside corporate network.

Q7. What is a Custom Role in Azure AD?

Answer:

Built-in roles may not cover all needs.

Custom roles let you define granular actions (e.g., “read blobs, but not delete”).
Example: A custom role for analysts → can read raw/curated ADLS folders but not write/delete.

Q8. What are the authentication protocols supported by Azure AD?

Answer:

OAuth 2.0 → App-to-app access (SPs, APIs)

OpenID Connect (OIDC) → User authentication + SSO

SAML 2.0 → Enterprise SSO with third-party apps

SCIM → User/group provisioning

Example: Databricks notebooks → ADLS (OAuth 2.0 via SP/MI).

Q9. Explain a real-world flow of Databricks accessing ADLS with Unity Catalog and Azure AD.

Answer:

User runs a query in Databricks notebook.

Unity Catalog enforces permissions (does user have SELECT?).

Databricks uses storage credential (SP or Managed Identity) registered in UC.

Azure AD authenticates the SP/MI.

ADLS authorizes via RBAC role (Storage Blob Data Contributor).

Data is read/written securely, no secrets exposed.

Q10. What is the difference between Directory Roles vs Azure RBAC Roles?

Answer:

Directory Roles → Control Azure AD objects (users, groups, SPs). Example: Global Admin, User Administrator.

RBAC Roles → Control access to Azure resources (storage, VMs, databases). Example: Storage Blob Data Contributor.

Q11. How would you give different levels of access to Finance vs Data Science teams on the same ADLS account?

Answer:

Create two groups in Azure AD → finance-users, ds-users.

Assign RBAC roles:

Finance → Read access only (custom role or Blob Data Reader).

DS → Read/Write on curated container (Blob Data Contributor).

In Unity Catalog, assign table permissions → Finance: SELECT, DS: SELECT/INSERT/UPDATE.

Q12. What are some common security best practices with Azure AD in Data Engineering?

Answer:

Use Managed Identities instead of secrets.

Use Groups for access, not direct user assignments.

Use Conditional Access (MFA, network restrictions).

Follow least privilege principle with custom roles.

Enable logging (Azure AD logs, storage logs, Databricks audit logs) for compliance.

### OpenID Connect (OIDC)

OpenID Connect is an identity layer built on top of OAuth 2.0.

OAuth 2.0 → Handles authorization (what an app can do on your behalf).

OIDC → Adds authentication (who you are, your identity).

**How it works (simple flow):**

A user tries to log in to an app (e.g., Databricks).
The app redirects them to Azure AD (the identity provider) using OIDC.
Azure AD authenticates the user (password, MFA, etc.).

**Azure AD returns tokens:**

ID Token (JWT) → contains identity info (username, email, groups).
Access Token → lets the app call APIs on user’s behalf.
The app trusts the ID token and logs the user in.

**Example in Azure AD + Databricks**

You open Databricks workspace in browser.
Databricks uses OIDC with Azure AD to authenticate you.
Azure AD issues an ID token with your email + groups.
Databricks checks your group → grants access based on Unity Catalog permissions.

**Why OIDC is important?**

It enables SSO (Single Sign-On) across cloud apps.
Works with MFA and Conditional Access.
Uses JWT tokens that are stateless and easy to validate.

**✅ Summary for interview:**
OpenID Connect is an authentication protocol built on OAuth 2.0. It issues ID tokens (JWTs) that allow apps to verify a user’s identity and support SSO. In Azure AD, OIDC is used when logging into cloud apps like Databricks, Power BI, or ADF.

**Imagine this:**

You want to enter a party 🎉.
The party organizer is the app (like Databricks).
At the door, they don’t know you… so they send you to the government office (Azure AD).

**What happens:**

You go to the government office (Azure AD).
You show your ID card, fingerprint, maybe even OTP → they confirm you are really you ✅.
They give you a badge (the ID token).
You take that badge back to the party 🎉.

The party organizer looks at the badge → “Okay, you are Vedanth, you’re allowed in.”

If you want to get food 🍕 or drinks 🥤 inside, the badge can also have permissions (access token) telling the staff what you’re allowed to do.

**Difference:**

- OAuth 2.0 → Badge only says what you can do inside the party.
- OIDC → Badge also says who you are.
