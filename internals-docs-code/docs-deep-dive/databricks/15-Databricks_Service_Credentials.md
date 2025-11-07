# Connecting to External Cloud Services With Service Credentials

You create a service credential object in Unity Catalog. A service credential encapsulates a long-term cloud credential that grants access to such services.

You control access to the service credential using Unity Catalog privileges.

Privileged users or service principals reference that service credential in code that calls the external service.

This article describes how to create a service credential object in Unity Catalog that lets you govern access from Databricks to external cloud services like AWS Glue or AWS Secrets Manager. A service credential in Unity Catalog encapsulates a long-term cloud credential that grants access to such services.

Service credentials are not intended for governing access to cloud storage that is used as a Unity Catalog managed storage location or external storage location.

Important point to note is that the workspace should be in same region as cloud service.

Four Key Steps for Configuration are:

1. Create an IAM Role
2. Give Databricks Access to that IAM Role
3. Update the IAM Policy
4. Validate the service credential

## Managing Service Credentials

[Click here](https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-services/manage-service-credentials) to know more about creating, modifying, renaming and deleting service credentials.

## Python3 Example of Connecting to Boto3

```python
import boto3
boto3_session = boto3.Session(botocore_session=dbutils.credentials.getServiceCredentialsProvider('your-service-credential'), region_name='your-aws-region')
sm = boto3_session.client('secretsmanager')
```

