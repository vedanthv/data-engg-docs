## S3 Rules and Policies

![alt text](https://snipboard.io/NZ62bO.jpg)

### S3 Storage Classes

Amazon Amazon S3 provides different **storage classes** so you can balance **cost, availability, and access frequency**. Each class is designed for a different data access pattern.

Below are the main **S3 Storage Classes** used in data engineering and cloud architectures.

---

## 1. S3 Standard

![Image](https://cdn.prod.website-files.com/6758716c1db67a29ec00ebb4/681c9b5b592d590a9a5502d5_Amazon%20S3.png)

![Image](https://www.cloudkeeper.com/cms-assets/s3fs-public/2023-07/diagram%203.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2AC-ZxhDnfSBsrxWAwGX5Hww.png)

**Best for:** Frequently accessed data.

**Examples**

* Data lakes
* Websites
* Streaming data
* Mobile apps
* Analytics datasets

**Key Features**

* 99.99% availability
* 11 9’s durability (99.999999999%)
* Stored across **multiple Availability Zones**
* Low latency and high throughput

**Example (your use case):**
Streaming data from **Amazon Kinesis → **AWS Lambda → **S3 Standard** for real-time analytics.

---

## 2. S3 Intelligent-Tiering

![Image](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/product-categories/storage/approved/images/d8e93003-d19d-4adc-9fad-9b9cc9cfbab9.df4161bde3ab9ab6fecdd2173dbda7ee622366c1.png)

![Image](https://d2908q01vomqb2.cloudfront.net/da4b9237bacccdf19c0760cab7aec4a8359010b0/2021/08/31/how_it_works.png)

![Image](https://d1tcczg8b21j1t.cloudfront.net/strapi-assets/24_S3_intelligent_tiering_4_d99f106832.png)

![Image](https://awsfundamentals.com/assets/blog/amazon-s3-intelligent-tiering/animation-how-the-intelligent-tiering-works.gif)

**Best for:** Data with **unknown or changing access patterns**.

**Key Features**

* Automatically moves data between tiers:

  * Frequent Access
  * Infrequent Access
  * Archive Instant
  * Archive
  * Deep Archive
* Small monitoring fee
* No retrieval charges for frequent tiers

**Example**
Log files where you **don’t know how often they will be accessed**.

---

## 3. S3 Standard-IA (Infrequent Access)

![Image](https://miro.medium.com/1%2AzVPY77i24bsAGIpTzylxGw.jpeg)

![Image](https://cdn.prod.website-files.com/6758716c1db67a29ec00ebb4/681c9b5b592d590a9a5502d5_Amazon%20S3.png)

![Image](https://kodekloud.com/kk-media/image/upload/v1752866092/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-S3-Storage-Classes/aws-s3-standard-storage-model.jpg)

![Image](https://kodekloud.com/kk-media/image/upload/v1752869345/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Storage-Classes/aws-s3-standard-storage-replication-diagram.jpg)

**Best for:** Data accessed **occasionally but requires fast access**.

**Examples**

* Backups
* Disaster recovery
* Older analytics data

**Features**

* Lower storage cost than Standard
* Retrieval fee when accessed
* Minimum storage duration: **30 days**

---

## 4. S3 One Zone-IA

![Image](https://miro.medium.com/1%2AkRccsi23X5NZuywBTclgXg.png)

![Image](https://d2908q01vomqb2.cloudfront.net/e1822db470e60d090affd0956d743cb0e7cdf113/2024/09/27/By-writing-the-infrequently-changed-data-to-S3-Express-One-Zone-Aura-was-able-to-offload-subsequent-retrievals-to-the-cached-copy-while-maintaining-1.png)

![Image](https://docs.aws.amazon.com/images/AmazonS3/latest/userguide/images/s3-express-one-zone.png)

![Image](https://kodekloud.com/kk-media/image/upload/v1752861109/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-S3-Storage-Tiers-and-Their-Uses-The-Cost-and-Performance-Perspective/aws-s3-standard-storage-model.jpg)

**Best for:** Infrequently accessed **re-creatable data**.

**Examples**

* Secondary backups
* Temporary processing data
* Data that can be regenerated

**Features**

* Stored in **single AZ**
* Cheaper than Standard-IA
* Retrieval charges
* Minimum storage duration: **30 days**

---

## 5. S3 Glacier Instant Retrieval

![Image](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/product-categories/storage/approved/images/9217cf0d435e86882bb9211d9af8eb1e.a9a0c99d2a08a7df38c0d8e0592e04c61a26210e.png)

![Image](https://media.licdn.com/dms/image/v2/D5612AQG3LlxbsOuYRw/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1725503876830?e=2147483647\&t=a8DCDKN9RPcdgdE34k749UGH_so9_HZcdHkBkkoFd4M\&v=beta)

**Best for:** Rarely accessed data that still needs **instant retrieval**.

**Examples**

* Medical images
* Media archives
* Long-term analytics data

**Features**

* Very low storage cost
* **Milliseconds retrieval**
* Minimum storage: **90 days**

---

## 6. S3 Glacier Flexible Retrieval

![Image](https://kodekloud.com/kk-media/image/upload/v1752861113/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-S3-Storage-Tiers-and-Their-Uses-The-Cost-and-Performance-Perspective/aws-s3-glacier-infographic.jpg)

**Best for:** Archive data accessed **occasionally**.

**Retrieval Options**

* Expedited: 1–5 minutes
* Standard: 3–5 hours
* Bulk: 5–12 hours

**Examples**

* Backup archives
* Compliance data

---

## 7. S3 Glacier Deep Archive

**Best for:** **Long-term archival** data rarely accessed.

**Examples**

* Financial records
* Regulatory archives
* Historical logs

**Features**

* Cheapest S3 storage class
* Retrieval time: **12–48 hours**
* Minimum storage: **180 days**

---

**Quick Interview Summary**

| Storage Class          | Access Frequency | AZs       | Retrieval Speed |
| ---------------------- | ---------------- | --------- | --------------- |
| S3 Standard            | Frequent         | Multi AZ  | Milliseconds    |
| S3 Intelligent Tiering | Unknown          | Multi AZ  | Milliseconds    |
| S3 Standard-IA         | Infrequent       | Multi AZ  | Milliseconds    |
| S3 One Zone-IA         | Infrequent       | Single AZ | Milliseconds    |
| Glacier Instant        | Rare             | Multi AZ  | Milliseconds    |
| Glacier Flexible       | Rare             | Multi AZ  | Minutes–Hours   |
| Deep Archive           | Very Rare        | Multi AZ  | Hours           |

---

**Data Engineering Tip (relevant to your work):**

For pipelines like **Kinesis → Lambda → S3 → Athena**:

* **Hot streaming data** → S3 Standard
* **After 30–90 days** → lifecycle rule → Standard-IA
* **After 1 year** → Glacier / Deep Archive

Using **S3 Lifecycle Policies** automatically moves objects between classes.

![alt text](https://snipboard.io/96xkDp.jpg)

