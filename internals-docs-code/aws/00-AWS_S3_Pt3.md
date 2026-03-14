## Amazon S3 Lifecycle Policies

**Lifecycle policies** in Amazon S3 automatically **transition or delete objects over time** to reduce storage cost and manage data retention.

Instead of manually moving files between storage classes, you define **rules** and S3 automatically performs the action.

---

### 1. Why Lifecycle Policies Are Used

Common reasons:

**Cost optimization**

* Move old data to cheaper storage classes.

**Data retention**

* Automatically delete data after compliance period.

**Data lake optimization**

* Keep recent data hot and archive old data.

Example data engineering pipeline (similar to your streaming setups):

```
Kinesis → Lambda → S3 (Standard)
             ↓
        Lifecycle Policy
             ↓
  30 days → S3 Standard-IA
  90 days → S3 Glacier
  1 year → Delete
```

---

### 2. Types of Lifecycle Actions

Lifecycle rules support **two main actions**.

#### Transition

Move objects to a cheaper storage class.

Examples:

| After    | Move To                       |
| -------- | ----------------------------- |
| 30 days  | S3 Standard-IA                |
| 60 days  | S3 Glacier Instant Retrieval  |
| 90 days  | S3 Glacier Flexible Retrieval |
| 180 days | S3 Glacier Deep Archive       |

Common storage classes used in transitions:

* Amazon S3 Standard
* Amazon S3 Standard-IA
* Amazon S3 Glacier Instant Retrieval
* Amazon S3 Glacier Flexible Retrieval
* Amazon S3 Glacier Deep Archive

---

### Expiration

Automatically **delete objects** after a specified time.

Example:

```
Delete logs after 365 days
```

Used for:

* temporary logs
* staging data
* streaming buffers

---

## 3. Lifecycle Rule Components

A lifecycle rule has four main parts.

### 1. Rule Scope

Which objects the rule applies to.

Examples:

* Entire bucket
* Prefix
* Tags

Example prefix:

```
logs/
analytics/
raw-data/
```

---

### 2. Transition Rules

Example:

```
After 30 days → Standard-IA
After 90 days → Glacier
```

---

### 3. Expiration Rules

Example:

```
Delete objects after 365 days
```

---

### 4. Noncurrent Version Actions

For **versioned buckets**.

You can:

* Transition old versions
* Delete old versions

Example:

```
Delete previous versions after 30 days
```

---

## 4. Real Data Engineering Example

Imagine a **data lake**.

```
s3://data-lake/
      ├── raw/
      ├── processed/
      └── logs/
```

Lifecycle policy:

| Folder     | Rule                              |
| ---------- | --------------------------------- |
| raw/       | Move to Standard-IA after 30 days |
| processed/ | Move to Glacier after 90 days     |
| logs/      | Delete after 180 days             |

This reduces **S3 storage cost dramatically**.

---

## 5. Example Lifecycle Policy (JSON)

Example rule:

```json
{
  "Rules": [
    {
      "ID": "MoveToIAAndGlacier",
      "Filter": {
        "Prefix": "logs/"
      },
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

---

## 6. Lifecycle Policies with Versioning

If **bucket versioning is enabled**, you can manage:

| Action                 | Example                           |
| ---------------------- | --------------------------------- |
| Noncurrent transitions | Move old versions to Glacier      |
| Noncurrent expiration  | Delete old versions after 30 days |
| Expired delete markers | Clean up delete markers           |

---

## 7. Important Lifecycle Policy Rules (Interview Point)

Minimum storage duration:

| Storage Class    | Minimum  |
| ---------------- | -------- |
| Standard-IA      | 30 days  |
| One Zone-IA      | 30 days  |
| Glacier Instant  | 90 days  |
| Glacier Flexible | 90 days  |
| Deep Archive     | 180 days |

Deleting earlier still charges for full duration.

---

## 8. Example AWS Console Steps

1. Open **S3**
2. Select bucket
3. Go to **Management tab**
4. Click **Lifecycle rules**
5. Create rule
6. Choose:

   * prefix or tags
   * transition storage class
   * expiration

---

## 9. Real Interview Scenario

**Question:**

Your S3 bucket receives **1 TB of logs per day** but analysts only query the last **7 days**. How do you reduce cost?

**Answer:**

Lifecycle rule:

```
7 days → Standard-IA
30 days → Glacier
180 days → Delete
```

---

💡 **Advanced Tip (used in large data lakes)**

Companies combine:

* Amazon S3 lifecycle policies
* AWS Glue catalogs
* Amazon Athena queries

so that **recent data is fast to query and older data is archived cheaply**.

In versioned buckets of Amazon S3, an **Expired Delete Marker (EDM)** is a **delete marker that no longer has any object versions associated with it**.

To understand it clearly, you need to know **two concepts**: **versioning** and **delete markers**.

---

## 1. What is a Delete Marker?

When **versioning is enabled**, deleting an object **does NOT remove the object immediately**.

Instead, S3:

1. Keeps the old versions
2. Adds a **delete marker** as the latest version

Example:

```
Object: data.csv

Version 1 → original file
Version 2 → updated file
Version 3 → DELETE MARKER
```

Now when someone requests:

```
GET data.csv
```

S3 returns **404 Not Found** because the delete marker is the latest version.

But the old versions **still exist**.

---

## 2. What is an Expired Delete Marker?

A delete marker becomes **expired** when:

* It is the **only version left** for that object.

Example:

Before lifecycle cleanup:

```
data.csv
 ├── Version 1 (object)
 ├── Version 2 (object)
 └── Delete Marker
```

Lifecycle rule deletes non-current versions:

```
data.csv
 └── Delete Marker
```

Now the **delete marker is the only version**.

This is called an **Expired Delete Marker**.

---

## 3. Why Expired Delete Markers Are Removed

Expired delete markers **serve no purpose anymore** because:

* There are **no previous versions to hide**
* The object is already gone

So S3 lifecycle rules can automatically remove them.

---

## 4. Lifecycle Rule for Expired Delete Markers

In lifecycle configuration you can enable:

```
ExpiredObjectDeleteMarker = true
```

This tells S3:

> If a delete marker is the only remaining version, remove it.

Example lifecycle configuration:

```json
{
  "Rules": [
    {
      "ID": "RemoveExpiredDeleteMarkers",
      "Status": "Enabled",
      "Expiration": {
        "ExpiredObjectDeleteMarker": true
      }
    }
  ]
}
```

---

## 5. Why This Matters in Data Lakes

In large pipelines using:

* Amazon S3
* AWS Glue
* Amazon Athena

you may create **millions of delete markers**.

If not cleaned up:

* S3 LIST operations slow down
* Storage costs increase
* Metadata clutter grows

Lifecycle rules remove these automatically.

---

## 6. Interview Explanation (Simple)

**Question:** What is an expired delete marker in S3?

**Answer:**

> In a versioned S3 bucket, when all object versions are deleted and only the delete marker remains, the delete marker becomes an **expired delete marker**. Lifecycle rules can automatically remove it to clean up the bucket.

---

## 7. Quick Visual

```
Step 1: Object uploaded
file1.txt (v1)

Step 2: Object deleted
file1.txt (v1)
file1.txt (delete marker)

Step 3: Lifecycle deletes v1
file1.txt (delete marker only)

→ This is an EXPIRED DELETE MARKER
```

Lifecycle can now remove it.