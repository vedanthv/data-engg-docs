## Lakehouse Federation in Databricks

This feature allows us to query external system data without replicating storage on databricks.

### Steps to Setup Federation

We need the external location to setup connection.

<img width="914" height="730" alt="image" src="https://github.com/user-attachments/assets/0fe6bf15-e7c6-4d2c-9538-a6f9ac9f28d6" />

Create a new Connection.

<img width="1641" height="625" alt="image" src="https://github.com/user-attachments/assets/21ab49b3-6961-4eb5-9d74-4eb97f5b2246" />

<img width="1595" height="729" alt="image" src="https://github.com/user-attachments/assets/0098fea5-76fa-478d-ab03-909d7a5dcdae" />

<img width="1593" height="794" alt="image" src="https://github.com/user-attachments/assets/c5759020-508b-4342-bfce-7372f82c90ed" />

<img width="1534" height="661" alt="image" src="https://github.com/user-attachments/assets/0e87d6a8-b902-443e-941f-99a86a4bcdf4" />

<img width="1646" height="640" alt="image" src="https://github.com/user-attachments/assets/a360078f-25db-47d7-b855-81bda55d7ce2" />

- Foreign catalogs are read only.
- Any catalog that doesnt come under Unity Catalog scheme of things is Foreign Catalog.
- We can manage permissions and also check lineage of tables of Foreign Catalogs.

Creating Catalogs using SQL

<img width="927" height="489" alt="image" src="https://github.com/user-attachments/assets/d8703e49-e469-4e35-838b-41ea539974a2" />




