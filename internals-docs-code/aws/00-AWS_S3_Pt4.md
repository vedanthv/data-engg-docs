# AWS : Policies and Permissions in AWS for S3

---

# 1. Types of Permissions in S3

S3 permissions are controlled by **four main mechanisms**:

| Permission Type     | Where Applied  | Purpose                           |
| ------------------- | -------------- | --------------------------------- |
| IAM Policies        | User / Role    | Control what an identity can do   |
| Bucket Policies     | Bucket         | Control who can access the bucket |
| ACLs                | Object/Bucket  | Legacy permission system          |
| Block Public Access | Account/Bucket | Prevent public exposure           |

---

# 2. IAM Policies for S3

IAM policies are attached to **users, roles, or groups** using AWS Identity and Access Management.

They control **what actions an identity can perform on S3**.

Example policy allowing read access:

```json
{
 "Effect": "Allow",
 "Action": [
   "s3:GetObject"
 ],
 "Resource": "arn:aws:s3:::my-data-bucket/*"
}
```

Meaning:

* Allow reading objects
* In `my-data-bucket`

---

# 3. S3 Bucket Policies

Bucket policies are **resource-based policies attached directly to a bucket**.

They control **who can access the bucket**.

Example:

```json
{
 "Version":"2012-10-17",
 "Statement":[
   {
     "Effect":"Allow",
     "Principal":"*",
     "Action":"s3:GetObject",
     "Resource":"arn:aws:s3:::my-bucket/*"
   }
 ]
}
```

Meaning:

* Anyone can read objects in the bucket.

This is commonly used for:

* Public websites
* Cross-account access
* Service integrations

---

# 4. Access Control Lists (ACLs)

ACLs are an **older permission mechanism** in S3.

They grant permissions at:

* bucket level
* object level

Example permissions:

| Permission | Meaning        |
| ---------- | -------------- |
| READ       | Read objects   |
| WRITE      | Upload objects |
| READ_ACP   | Read ACL       |
| WRITE_ACP  | Modify ACL     |

However, AWS recommends **disabling ACLs** and using policies instead.

---

# 5. Block Public Access

AWS provides **Block Public Access settings** to prevent accidental exposure.

You can block:

* Public bucket policies
* Public ACLs

This is extremely important because many **data leaks happen due to public S3 buckets**.

---

# 6. Common S3 Permissions (Actions)

Some frequently used S3 API actions:

| Action               | Purpose              |
| -------------------- | -------------------- |
| s3:ListBucket        | List bucket contents |
| s3:GetObject         | Read object          |
| s3:PutObject         | Upload object        |
| s3:DeleteObject      | Delete object        |
| s3:GetBucketLocation | Get region info      |

Example policy allowing uploads:

```json
{
 "Effect":"Allow",
 "Action":"s3:PutObject",
 "Resource":"arn:aws:s3:::data-bucket/*"
}
```

---

# 7. Cross-Account Access Example

A common data engineering scenario:

Account A → produces data
Account B → consumes data

Bucket policy in Account A:

```json
{
 "Effect":"Allow",
 "Principal":{
   "AWS":"arn:aws:iam::123456789012:root"
 },
 "Action":"s3:GetObject",
 "Resource":"arn:aws:s3:::data-bucket/*"
}
```

This allows **another AWS account to read objects**.

---

# 8. Example Data Pipeline Permissions

For a pipeline:

```
Kinesis → Lambda → S3
```

Lambda role must allow:

```
s3:PutObject
s3:AbortMultipartUpload
```

So the role policy would include:

```json
{
 "Effect":"Allow",
 "Action":[
   "s3:PutObject"
 ],
 "Resource":"arn:aws:s3:::streaming-data-bucket/*"
}
```

This is similar to pipelines using:

* Amazon Kinesis
* AWS Lambda
* Amazon Athena

---

# 9. How AWS Evaluates S3 Permissions

When a request is made to S3:

```
IAM Policy
      +
Bucket Policy
      +
ACL
      +
Block Public Access
```

AWS checks:

1. Explicit **Deny**
2. Explicit **Allow**
3. Otherwise **Implicit Deny**

---



# 10. Very Common Interview Scenario

**Question**

A user has IAM permission to access S3 but still gets **AccessDenied**. Why?

Possible reasons:

* Bucket policy denies access
* Block public access enabled
* Object owned by another account
* Missing `s3:ListBucket`
* Explicit deny in policy

---

✅ **Simple Summary**

| Mechanism           | Level         |
| ------------------- | ------------- |
| IAM Policy          | Identity      |
| Bucket Policy       | Bucket        |
| ACL                 | Object/Bucket |
| Block Public Access | Safety layer  |

When a request is made to Amazon S3, AWS evaluates **multiple policy layers together** before deciding whether the request should be **allowed or denied**.

The main policies involved are:

* AWS Identity and Access Management **IAM policies**
* **S3 bucket policies**
* **ACLs**
* **Block Public Access settings**
* **Service Control Policies (SCPs)** if using AWS Organizations

---

# 1. Order AWS Uses to Evaluate S3 Permissions

AWS evaluates permissions using this logic:

```
1️⃣ Explicit Deny anywhere → ACCESS DENIED

2️⃣ If at least one policy allows → ACCESS ALLOWED

3️⃣ If no explicit allow → IMPLICIT DENY
```

Think of it like:

```
Deny > Allow > Default Deny
```

Explicit deny **always wins**, even if other policies allow access.

---

# 2. Example Scenario 1 (IAM Allows but Bucket Denies)

### Setup

IAM policy for a user:

```json
{
 "Effect": "Allow",
 "Action": "s3:GetObject",
 "Resource": "arn:aws:s3:::data-bucket/*"
}
```

Bucket policy:

```json
{
 "Effect": "Deny",
 "Principal": "*",
 "Action": "s3:GetObject",
 "Resource": "arn:aws:s3:::data-bucket/*"
}
```

---

### Request

User tries:

```
GET s3://data-bucket/file1.csv
```

---

### Evaluation

| Policy        | Result        |
| ------------- | ------------- |
| IAM policy    | Allow         |
| Bucket policy | Explicit Deny |

Final result:

```
ACCESS DENIED
```

Because **explicit deny overrides allow**.

---

# 3. Example Scenario 2 (Bucket Allows Cross Account)

### Setup

Account A owns the bucket.

Bucket policy:

```json
{
 "Effect":"Allow",
 "Principal":{
   "AWS":"arn:aws:iam::222222222222:root"
 },
 "Action":"s3:GetObject",
 "Resource":"arn:aws:s3:::analytics-bucket/*"
}
```

---

### Request

A user from Account B tries to read:

```
s3://analytics-bucket/report.parquet
```

---

### Evaluation

| Policy                  | Result |
| ----------------------- | ------ |
| Bucket policy           | Allow  |
| IAM policy in Account B | Allow  |

Final result:

```
ACCESS GRANTED
```

Both sides allow access.

---

# 4. Example Scenario 3 (Missing Permission)

IAM policy:

```json
{
 "Effect": "Allow",
 "Action": "s3:GetObject",
 "Resource": "arn:aws:s3:::logs-bucket/*"
}
```

User tries:

```
aws s3 ls s3://logs-bucket
```

---

### Evaluation

| Required Permission | Status  |
| ------------------- | ------- |
| s3:ListBucket       | Missing |

Result:

```
ACCESS DENIED
```

Because listing a bucket requires:

```
s3:ListBucket
```

on:

```
arn:aws:s3:::logs-bucket
```

---

# 5. Example Scenario 4 (Block Public Access)

Bucket policy allows public read:

```json
{
 "Effect":"Allow",
 "Principal":"*",
 "Action":"s3:GetObject",
 "Resource":"arn:aws:s3:::public-images/*"
}
```

But **Block Public Access is enabled**.

---

### Evaluation

| Layer               | Result |
| ------------------- | ------ |
| Bucket policy       | Allow  |
| Block Public Access | Deny   |

Final result:

```
ACCESS DENIED
```

Block Public Access overrides public policies.

---

# 6. Real Data Engineering Example

Pipeline:

```
Kinesis → Lambda → S3
```

Services involved:

* Amazon Kinesis
* AWS Lambda
* Amazon S3

---

### Lambda Role Policy

```json
{
 "Effect":"Allow",
 "Action":[
   "s3:PutObject"
 ],
 "Resource":"arn:aws:s3:::stream-data/*"
}
```

If the bucket policy contains:

```json
{
 "Effect":"Deny",
 "Principal":"*",
 "Action":"s3:PutObject",
 "Resource":"arn:aws:s3:::stream-data/*"
}
```

Result:

```
Lambda fails with AccessDenied
```

Even though IAM allowed it.

---

# 7. Full Evaluation Flow (Interview Answer)

When S3 receives a request:

```
1️⃣ Check Service Control Policies
2️⃣ Check IAM policies
3️⃣ Check bucket policies
4️⃣ Check ACLs
5️⃣ Check Block Public Access
6️⃣ Evaluate explicit deny vs allow
```