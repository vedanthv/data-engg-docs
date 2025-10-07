## Serializing and Sending Data in Avro without Classes

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer",
"io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("value.serializer",
"io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", url);
String schemaString =
"{\"namespace\": \"customerManagement.avro\",
"\"type\": \"record\", " +
"\"name\": \"Customer\"," +
"\"fields\": [" +
"{\"name\": \"id\", \"type\": \"int\"}," +
"{\"name\": \"name\", \"type\": \"string\"}," +
"{\"name\": \"email\", \"type\": " + "[\"null\",\"string\"], " +
"\"default\":\"null\" }" +
"]}";
Producer<String, GenericRecord> producer =
new KafkaProducer<String, GenericRecord>(props);
Schema.Parser parser = new Schema.Parser();
Schema schema = parser.parse(schemaString);
for (int nCustomers = 0; nCustomers < customers; nCustomers++) {
String name = "exampleCustomer" + nCustomers;
String email = "example " + nCustomers + "@example.com";
GenericRecord customer = new GenericData.Record(schema);
customer.put("id", nCustomers);
customer.put("name", name);
customer.put("email", email);
ProducerRecord<String, GenericRecord> data =
new ProducerRecord<>("customerContacts", name, customer);
producer.send(data);
}
```

Perfect — this is another **Kafka producer example** that uses **Avro serialization**, but this time **without pre-generated Avro classes**.

Let’s unpack it **line-by-line** so you can see exactly what’s happening and how it differs from the previous one that used the generated `Customer` class. 👇

---

## 🧩 1️⃣ Overview — What This Code Does

This program:

1. Defines an **Avro schema as a JSON string** (inline in the code).
2. Uses **Confluent’s Avro serializer** to send Avro-encoded messages to Kafka.
3. Creates **`GenericRecord`** objects (Avro records that use the schema at runtime, instead of pre-generated classes).
4. Sends multiple Avro messages to a Kafka topic called `"customerContacts"`.

---

## 🧱 2️⃣ Step-by-Step Explanation

---

### 🧾 Create configuration properties

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
```

🔹 `Properties` holds the producer configuration.
🔹 `bootstrap.servers` = address of your Kafka broker(s).
It’s where the producer initially connects to the Kafka cluster.

---

### 🧰 Configure Avro serialization and schema registry

```java
props.put("key.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", url);
```

🔹 Both the **key** and **value** use Confluent’s **Avro serializer**.
🔹 `schema.registry.url` tells Kafka where the **Schema Registry** is running (e.g., `http://localhost:8081`).

When the producer sends data:

1. The serializer registers or looks up the Avro schema in the Schema Registry.
2. The registry assigns a **schema ID**.
3. The serializer encodes the message as:

   ```
   [Magic Byte][Schema ID][Avro Binary Payload]
   ```

---

### 🧮 Define the Avro schema (as a string)

```java
String schemaString =
"{\"namespace\": \"customerManagement.avro\"," +
"\"type\": \"record\", " +
"\"name\": \"Customer\"," +
"\"fields\": [" +
"{\"name\": \"id\", \"type\": \"int\"}," +
"{\"name\": \"name\", \"type\": \"string\"}," +
"{\"name\": \"email\", \"type\": [\"null\",\"string\"], \"default\":\"null\" }" +
"]}";
```

🔹 This JSON string defines the **Avro schema** for the `Customer` record:

* **namespace**: `customerManagement.avro`
* **type**: `record` (structured data type)
* **fields**:

  * `id` → int
  * `name` → string
  * `email` → nullable string (`["null","string"]` with default `"null"`)

This schema is **not pre-compiled** into a Java class — instead it will be parsed and used dynamically.

---

### 🧱 Create the Kafka producer

```java
Producer<String, GenericRecord> producer =
    new KafkaProducer<String, GenericRecord>(props);
```

🔹 Creates a Kafka producer instance.

* **Key type**: `String`
* **Value type**: `GenericRecord` (an Avro object that follows a schema but is built dynamically).

---

### 🧠 Parse the schema string into an Avro Schema object

```java
Schema.Parser parser = new Schema.Parser();
Schema schema = parser.parse(schemaString);
```

🔹 The Avro library’s `Schema.Parser` reads the JSON string and turns it into a **Schema** object.
🔹 This object describes the structure of each message we’ll send.

---

### 🏗️ Produce messages in a loop

```java
for (int nCustomers = 0; nCustomers < customers; nCustomers++) {
    String name = "exampleCustomer" + nCustomers;
    String email = "example" + nCustomers + "@example.com";
```

🔹 Generates sample data for multiple customers.
Each message will have a unique name and email.

---

### 🧩 Create a GenericRecord (Avro record instance)

```java
GenericRecord customer = new GenericData.Record(schema);
customer.put("id", nCustomers);
customer.put("name", name);
customer.put("email", email);
```

🔹 `GenericData.Record(schema)` creates a new Avro record **using the parsed schema**.
🔹 Each field’s value is added with `put(fieldName, value)`.

This is how you create an Avro object **without** generating a Java class.

---

### 📨 Create and send the Kafka message

```java
ProducerRecord<String, GenericRecord> data =
    new ProducerRecord<>("customerContacts", name, customer);
producer.send(data);
```

🔹 `ProducerRecord` defines the Kafka message:

* **Topic**: `customerContacts`
* **Key**: the customer’s name (used for partitioning)
* **Value**: the Avro `GenericRecord`

🔹 `producer.send(data)` asynchronously sends it to Kafka.
The serializer:

1. Registers or retrieves the Avro schema from the Schema Registry.
2. Encodes the record into binary Avro format.
3. Sends the data to Kafka brokers.

---

## ⚙️ 3️⃣ What’s the Key Difference vs. Previous Example

| Concept             | Previous Example (`Customer` class)             | This Example (`GenericRecord`)          |
| ------------------- | ----------------------------------------------- | --------------------------------------- |
| **Schema Handling** | Schema compiled ahead of time (code generation) | Schema defined at runtime (JSON string) |
| **Object Type**     | `SpecificRecord` (`Customer.java`)              | `GenericRecord`                         |
| **Code Generation** | Required (via `avro-tools` or Maven plugin)     | Not required                            |
| **Flexibility**     | Fixed schema, better performance                | Dynamic schema, more flexible           |
| **Serializer Used** | `KafkaAvroSerializer`                           | `KafkaAvroSerializer` (same)            |

So both use the **same serializer and Schema Registry**, but one uses **generated Avro classes**, while this one uses **runtime schema parsing with GenericRecord**.

---

## 🧩 4️⃣ Summary of What Happens Internally

1. **Schema is parsed** from JSON → Avro Schema object.
2. **GenericRecord** is created based on that schema and filled with values.
3. **KafkaAvroSerializer**:

   * Registers the schema in Schema Registry (if new).
   * Gets a schema ID.
   * Serializes the record as `[Magic Byte][Schema ID][Binary Avro Data]`.
4. **Kafka producer** sends the message to the `customerContacts` topic.

Consumers with access to the same Schema Registry can then **deserialize** this data automatically back into Avro or POJO form.

---

## 🧠 In Short

> This code shows how to produce Avro messages to Kafka **without generating Java classes**.
> It defines an Avro schema at runtime, creates `GenericRecord` objects that follow it, and sends them through Kafka using the Confluent Avro serializer and Schema Registry.

---
