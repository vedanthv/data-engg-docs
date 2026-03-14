# Securing S3 Buckets

![alt text](https://snipboard.io/8tjkuv.jpg)

## Server-Side Encryption with S3 (SSE-S3)

**SSE-S3** is a server-side encryption method provided by Amazon S3 where **AWS automatically encrypts your data when it is stored and decrypts it when accessed**.

The encryption keys are **fully managed by AWS**.

---

## 1. How SSE-S3 Works

![Image](https://media.amazonwebservices.com/blog/s3_sse_3.png)

![Image](https://miro.medium.com/1%2AUNZjXEUVBBCVCSXEjKz7wg.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2AmN0ML58u-CDrEgQwEWR_vg.png)

![Image](https://image.slidesharecdn.com/amazons3server-sideencryptionwiths3-managedkeyssse-s3-220531134935-ee138caf/95/Amazon-S3-Server-Side-Encryption-with-S3-Managed-Keys-SSE-S3-pptx-5-638.jpg)

Process:

1. Client uploads object to S3
2. S3 encrypts the object using **AES-256 encryption**
3. Encrypted object is stored on disk
4. When a user retrieves the object, S3 **decrypts it automatically**

Encryption and decryption are **transparent to the user**.

---

## 2. Encryption Algorithm

SSE-S3 uses:

```
AES-256
```

This is a **symmetric encryption algorithm** widely used for secure storage.

---

## 3. Enabling SSE-S3

You can enable SSE-S3 in **three ways**.

### 1. Default Bucket Encryption

Configure encryption on the bucket so **all objects are encrypted automatically**.

Steps:

1. Open S3 console
2. Select bucket
3. Go to **Properties**
4. Enable **Default encryption**
5. Choose **SSE-S3**

Now every uploaded object is encrypted.

---

### 2. During Object Upload

You can specify encryption when uploading.

Example CLI:

```bash
aws s3 cp file.txt s3://my-bucket/ --sse AES256
```

This instructs S3 to encrypt using **SSE-S3**.

---

### 3. Using API Headers

When using the REST API:

```
x-amz-server-side-encryption: AES256
```

---

## 4. Checking if an Object is Encrypted

Run:

```bash
aws s3api head-object --bucket my-bucket --key file.txt
```

Output includes:

```
ServerSideEncryption: AES256
```

This confirms **SSE-S3 encryption**.

---

## 5. SSE-S3 vs Other S3 Encryption Methods

S3 supports three major server-side encryption methods.

| Encryption Type | Key Managed By             | Use Case               |
| --------------- | -------------------------- | ---------------------- |
| SSE-S3          | AWS                        | Simple encryption      |
| SSE-KMS         | AWS Key Management Service | Audit + control        |
| SSE-C           | Customer                   | Customer provides keys |

---

### SSE-S3

* Keys managed entirely by S3
* Simplest option
* No extra cost

---

### SSE-KMS

Uses:

AWS Key Management Service

Advantages:

* Key rotation
* Access auditing
* Fine-grained permissions

Common in **enterprise pipelines**.

---

### SSE-C

Customer provides encryption key with every request.

Rarely used because:

* Hard to manage
* AWS never stores the key

---

## 6. Example Data Engineering Scenario

Pipeline:

```
Kinesis → Lambda → S3 → Athena
```

Services involved:

* Amazon Kinesis
* AWS Lambda
* Amazon Athena

If the S3 bucket has **default SSE-S3 encryption enabled**:

* Lambda uploads data normally
* S3 encrypts objects automatically

No changes required in the pipeline.

---

## 7. Example Bucket Policy Enforcing Encryption

You can enforce encryption by denying uploads without it.

Example:

```json
{
 "Version":"2012-10-17",
 "Statement":[
  {
   "Effect":"Deny",
   "Principal":"*",
   "Action":"s3:PutObject",
   "Resource":"arn:aws:s3:::secure-bucket/*",
   "Condition":{
     "StringNotEquals":{
       "s3:x-amz-server-side-encryption":"AES256"
     }
   }
  }
 ]
}
```

Meaning:

Objects must be uploaded with **SSE-S3 encryption**.

---

## 8. Advantages of SSE-S3

✔ Automatic encryption
✔ No key management
✔ High performance
✔ No additional cost
✔ Simple configuration

---

✅ **Interview Answer (Short)**

> SSE-S3 is a server-side encryption method in Amazon S3 where AWS automatically encrypts objects using AES-256 before storing them. The encryption keys are managed by AWS and decryption happens automatically when the object is retrieved.
