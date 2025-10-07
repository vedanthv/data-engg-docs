## Serializing with Apache Avro

---

### 🧩 **What is Avro?**

**Apache Avro** is a **data serialization system** — meaning it defines how data is **structured, stored, and transmitted** between systems in a compact and efficient way.

It was created by **Doug Cutting** (also the creator of Hadoop and Lucene) to solve a common problem in distributed systems:

> “How do you exchange complex structured data between systems written in different languages — without losing type information or causing compatibility issues?”

---

### ⚙️ **How Avro Works**

At its core, Avro works with **two components:**

1. **Schema** – Defines the structure (fields, types, defaults) of your data.
2. **Data** – The actual binary or JSON-encoded data following that schema.

So Avro separates **“what the data looks like” (schema)** from **“what the data is” (values)**.

---

### 📄 **Avro Schema Example (in JSON)**

Here’s how a simple Avro schema looks:

```json
{
  "type": "record",
  "name": "Employee",
  "namespace": "com.company",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "department", "type": ["null", "string"], "default": null}
  ]
}
```

This defines a record with three fields:

* `id` (integer)
* `name` (string)
* `department` (optional string — can be null)

---

### 💾 **Serialization and Deserialization**

* **Serialization:** Converting data (e.g., a Python object) into Avro binary using the schema.
* **Deserialization:** Reading Avro binary data back into a usable form using the same or compatible schema.

Because the **schema is embedded** in Avro files, they are **self-describing** — any system can read them if it supports Avro.

---

### 🧠 **Why Avro Is Special**

Here are Avro’s **key advantages**:

| Feature                            | Description                                                                                            |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 🗂️ **Schema-based**               | Data has a well-defined structure stored in JSON format.                                               |
| ⚡ **Compact Binary Format**        | Binary encoding reduces file size and improves I/O performance.                                        |
| 🔄 **Schema Evolution**            | You can change schemas over time (add, rename, remove fields) **without breaking existing consumers**. |
| 🌐 **Language Neutral**            | Works with many languages (Java, Python, C++, Go, etc.).                                               |
| 💬 **Great for Messaging Systems** | Used in **Kafka**, **Redpanda**, and **Schema Registry** setups.                                       |
| 🧱 **Splittable and Compressible** | Ideal for big data systems (Hadoop, Spark, Hive).                                                      |

---

### 🔄 **Schema Evolution in Avro**

This is **the most powerful part** — and the reason Avro is heavily used in Kafka.

Suppose your producer’s old schema was:

```json
{"name": "id", "type": "int"}
```

Now you update it to:

```json
{
  "type": "record",
  "name": "Employee",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

✅ Avro allows **backward and forward compatibility**:

* **Backward-compatible:** New consumers can read old data.
* **Forward-compatible:** Old consumers can read new data (using defaults for new fields).

That’s why Kafka uses Avro with a **Schema Registry** — to ensure producers and consumers can evolve independently.

---

### 🧰 **Where Avro is Commonly Used**

| Use Case                     | Description                                                             |
| ---------------------------- | ----------------------------------------------------------------------- |
| 🪣 **Data Lakes (HDFS, S3)** | Store schema-defined data for Spark/Hive.                               |
| 🧵 **Kafka Messaging**       | Producers publish Avro messages, Schema Registry keeps schema versions. |
| 🧬 **ETL Pipelines**         | Efficient and schema-safe data transfer between stages.                 |
| 🧮 **Analytics**             | Compact binary format makes large datasets efficient to query.          |

---

### 📊 **Avro vs. Other Formats**

| Feature            | **Avro**           | **JSON**        | **Parquet**     | **ORC**         |
| ------------------ | ------------------ | --------------- | --------------- | --------------- |
| **Storage Type**   | Row-based          | Text            | Columnar        | Columnar        |
| **Schema**         | Yes (JSON-defined) | No              | Yes             | Yes             |
| **Compression**    | Yes                | Poor            | Excellent       | Excellent       |
| **Best For**       | Streaming, Kafka   | Debugging, APIs | Analytics, OLAP | Analytics, OLAP |
| **Human Readable** | No                 | Yes             | No              | No              |

So Avro is ideal for **data interchange** (Kafka, APIs, log pipelines), while Parquet/ORC are better for **data storage and querying**.

---

### 🧩 **Summary**

> **Apache Avro** = Schema + Compact Binary + Evolution Support
> It’s designed for:

* **Cross-language data exchange**
* **Streaming and message serialization**
* **Schema evolution without breaking systems**

And that’s why it’s **a favorite in modern data pipelines**, especially with **Kafka, Redpanda, Spark, and Schema Registry**.

---

### Caveats While Using Avro

---

## 🧩 Caveat 1:

> “The schema used for writing the data and the schema expected by the reading application must be compatible.”

### 🔍 What this means

When Avro serializes (writes) and deserializes (reads) data, both sides must **agree on the structure of the data** — at least enough to interpret the fields correctly.

If the producer (writer) and consumer (reader) use **incompatible schemas**, the data can’t be decoded properly.

---

### 🧠 Example

#### Writer’s Schema (v1)

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"}
  ]
}
```

#### Reader’s Schema (v2)

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "full_name", "type": "string"}
  ]
}
```

Here, the **field name** changed from `"name"` → `"full_name"`.

💥 Result: **Not compatible** — Avro won’t know how to map `"name"` to `"full_name"`.
The reader will fail to interpret the data.

---

### ✅ Compatible Evolution Example

If we **add a new optional field**, Avro can handle that gracefully.

#### Writer’s Schema (old)

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"}
  ]
}
```

#### Reader’s Schema (new)

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

🟢 Compatible — The new field `email` has a **default value**, so old data still works fine.

---

### ⚖️ Compatibility Rules (Simplified)

Avro defines several compatibility types:

| Compatibility Type | Meaning                                                                    |
| ------------------ | -------------------------------------------------------------------------- |
| **Backward**       | New readers can read old data.                                             |
| **Forward**        | Old readers can read new data.                                             |
| **Full**           | Both backward + forward.                                                   |
| **Breaking**       | Schema changes that break both directions (e.g. removing required fields). |

You can configure which rule to enforce in systems like the **Confluent Schema Registry**.

---

## 🧩 Caveat 2:

> “The deserializer will need access to the schema that was used when writing the data, even when it is different from the schema expected by the application that accesses the data.”

### 🔍 What this means

To **read Avro data**, you always need:

* The **writer’s schema** (used when data was created)
* The **reader’s schema** (used by your application)

Avro uses both together to **resolve differences**.

If your application only knows its own schema (reader schema) but not the original one, it can’t interpret the binary data — because Avro binary doesn’t include field names, just encoded values.

---

### 🧠 Analogy

Think of Avro data as a **compressed shopping list**:

* The **writer’s schema** says the order of items:
  1️⃣ "Milk" → string
  2️⃣ "Eggs" → int
* The **data** only stores the values: `"Amul", 12`

If the **reader doesn’t know the original order (schema)**, it can’t tell which value corresponds to which field.

---

## 🧩 Caveat 3:

> “In Avro files, the writing schema is included in the file itself, but there is a better way to handle this for Kafka messages.”

### 🔍 What this means

When Avro is used for **files** (like on HDFS or S3), the schema is **embedded inside the file header**.
That’s fine for static data — every file carries its own schema.

But in **Kafka**, embedding the full schema inside every message would be inefficient:

* Each message might be just a few KB,
* But the schema (JSON) could be several hundred bytes.

That would cause **massive duplication and network overhead**.

---

### 🧠 The “Better Way” (Hinted at in the text)

Instead of embedding schemas in every Kafka message, systems like **Confluent Schema Registry** store schemas **centrally**.

Here’s how it works:

1. When a producer sends a message:

   * It registers its schema once with the Schema Registry.
   * It gets a **schema ID** (like `42`).
   * It sends the binary Avro data prefixed with that schema ID.

2. When a consumer reads a message:

   * It looks up schema ID `42` in the Schema Registry.
   * It retrieves the writer’s schema and deserializes the message correctly.

This way:

* ✅ Small message sizes
* ✅ Centralized schema management
* ✅ Schema evolution tracking

---

### 🏗️ Summary Table

| Concept                 | In Avro Files                  | In Kafka Messages                   |
| ----------------------- | ------------------------------ | ----------------------------------- |
| Where is schema stored? | Embedded inside file           | Stored in Schema Registry           |
| Message overhead        | Higher (includes schema)       | Lower (schema ID only)              |
| Schema evolution        | File-based                     | Centrally managed (versioned)       |
| Typical use case        | Batch systems (HDFS, S3, Hive) | Streaming systems (Kafka, Redpanda) |

---

### 🧩 In Short

| Caveat                                          | Meaning                                | Solution                                      |
| ----------------------------------------------- | -------------------------------------- | --------------------------------------------- |
| **1️⃣ Writer/Reader schema must be compatible** | Data won’t deserialize if incompatible | Follow Avro compatibility rules               |
| **2️⃣ Reader needs writer’s schema**            | Required to decode binary data         | Include schema in file or fetch from registry |
| **3️⃣ Don’t embed schema per message in Kafka** | Wasteful and redundant                 | Use Schema Registry (stores schema IDs)       |

---

## Demo Producer Code with Schema Registry in Python

```python
from confluent_kafka.avro import AvroProducer
import json

# Avro schema as JSON string or loaded from file
user_schema_str = """
{
  "namespace": "example.avro",
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
"""

# Kafka + Schema Registry configuration (example placeholders)
conf = {
    'bootstrap.servers': 'kafka-broker1:9092,kafka-broker2:9092',
    'schema.registry.url': 'http://schema-registry-host:8081',
    # If SR needs auth, add 'schema.registry.basic.auth.user.info': 'user:password'
}

# The AvroProducer takes the schema used for the value (and optionally key schema)
producer = AvroProducer(conf, default_value_schema=json.loads(user_schema_str))

topic = "users-avro"

def produce_user(user_obj):
    # key_schema can also be provided; here we use string keys
    key = str(user_obj["id"])
    producer.produce(topic=topic, value=user_obj, key=key)
    producer.flush()   # flush per message for demo; in production batch/async flush

if __name__ == "__main__":
    user = {"id": 1, "name": "Alice", "email": "alice@example.com"}
    produce_user(user)
    print("Sent Avro message to", topic)

```

### Demo Producer Code In Java

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer",
"io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("value.serializer",
"io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", schemaUrl);
String topic = "customerContacts";
Producer<String, Customer> producer = new KafkaProducer<>(props);
// We keep producing new events until someone ctrl-c
while (true) {
Customer customer = CustomerGenerator.getNext();
System.out.println("Generated customer " +
customer.toString());
ProducerRecord<String, Customer> record =
new ProducerRecord<>(topic, customer.getName(), customer);
producer.send(record);
}
```

---

## 🧩 The Big Picture

This Java code is an **Avro Kafka producer**.
It:

1. Connects to Kafka.
2. Uses Confluent’s Avro serializers.
3. Generates Avro objects (`Customer` records).
4. Sends them continuously to a Kafka topic.

---

## 🧱 Step-by-step Explanation

### 1️⃣ Create configuration properties

```java
Properties props = new Properties();
```

👉 `Properties` is a Java `Map`-like object that stores key-value configuration settings for the Kafka producer.

---

### 2️⃣ Configure Kafka connection and serialization

```java
props.put("bootstrap.servers", "localhost:9092");
```

🔹 **`bootstrap.servers`** — tells the producer where Kafka brokers are located.
The producer will connect to this address to find the rest of the cluster.

---

```java
props.put("key.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
```

🔹 These lines configure **how keys and values are converted into bytes** before being sent over the network.

* Both the **key** and **value** use the **Confluent Avro serializer**.
* The serializer:

  * Converts Avro objects (like `Customer`) into Avro binary format.
  * Registers the Avro **schema** with the **Schema Registry**.
  * Sends the **schema ID** (a small integer) along with the serialized message.

So the consumer can later retrieve the schema and deserialize properly.

---

```java
props.put("schema.registry.url", schemaUrl);
```

🔹 This tells the serializer **where the Schema Registry is** (e.g., `http://localhost:8081`).

The serializer uses this URL to:

* Check if the schema for `Customer` already exists in the registry.
* Register it if not.
* Retrieve schema IDs for encoding messages.

---

### 3️⃣ Create Kafka topic variable

```java
String topic = "customerContacts";
```

Just defines the target Kafka topic to send messages to.

---

### 4️⃣ Create the producer instance

```java
Producer<String, Customer> producer = new KafkaProducer<>(props);
```

🔹 This creates the Kafka producer client.

* `Producer<K, V>` — a generic class parameterized by key and value types.
  Here:

  * `K` = `String` (customer name, used as key)
  * `V` = `Customer` (the Avro object)

The producer will use the serializers defined earlier to encode these before sending.

---

### 5️⃣ Generate and send Avro messages in a loop

```java
while (true) {
    Customer customer = CustomerGenerator.getNext();
    System.out.println("Generated customer " + customer.toString());
    ProducerRecord<String, Customer> record =
        new ProducerRecord<>(topic, customer.getName(), customer);
    producer.send(record);
}
```

Let’s break this down line by line.

---

#### 🧠 `Customer customer = CustomerGenerator.getNext();`

This uses a helper class `CustomerGenerator` (not shown here) that probably:

* Creates random or mock customer data.
* Returns a `Customer` object (which is an Avro-generated Java class).

---

#### 🖨️ `System.out.println(...)`

Just logs the generated customer to the console for visibility.

---

#### 🧾 `ProducerRecord<String, Customer> record = new ProducerRecord<>(topic, customer.getName(), customer);`

This creates the **message record** to be sent to Kafka.

* The **topic**: `"customerContacts"`.
* The **key**: `customer.getName()`.
* The **value**: the entire `Customer` Avro object.

Kafka uses the **key** to determine which partition the message goes to (same keys → same partition).

---

#### 🚀 `producer.send(record);`

This sends the record asynchronously to Kafka.

The Avro serializer will:

1. Serialize `Customer` into binary Avro.
2. Register or look up the schema in Schema Registry.
3. Encode the schema ID + binary payload.
4. Send the message to the Kafka broker.

---

### 🌀 `while (true) {...}`

Runs indefinitely — keeps producing customer messages until you stop it with **Ctrl + C**.

In a real-world app, you might:

* Add a `Thread.sleep()` for pacing,
* Limit message count, or
* Gracefully close the producer with `producer.close()`.

---

## 🧩 What the `Customer` class is

This class is likely generated automatically from an **Avro schema** using the Avro Java code generator.

For example, the Avro schema could look like:

```json
{
  "namespace": "example.avro",
  "type": "record",
  "name": "Customer",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "phoneNumber", "type": ["null", "string"], "default": null}
  ]
}
```

After generating Java classes from this schema (`avro-maven-plugin` or `avro-tools`), you can use the `Customer` object directly in code — the Avro serializer knows how to handle it.

---

## 🧠 Summary Table

| Line                                  | What it does          | Why it matters                  |
| ------------------------------------- | --------------------- | ------------------------------- |
| `bootstrap.servers`                   | Broker list           | Connect to Kafka cluster        |
| `key.serializer` / `value.serializer` | Avro serializers      | Convert Java objects to bytes   |
| `schema.registry.url`                 | Registry URL          | Store and retrieve schemas      |
| `KafkaProducer<>(props)`              | Creates producer      | Main client that talks to Kafka |
| `CustomerGenerator.getNext()`         | Generates Avro object | Produces mock data              |
| `new ProducerRecord<>(...)`           | Wraps message         | Defines topic, key, and value   |
| `producer.send(record)`               | Sends async           | Pushes data to Kafka            |
| `while (true)`                        | Infinite loop         | Keeps producing                 |

---

## ⚙️ What Happens Behind the Scenes

1. You produce a `Customer` Avro object.
2. Serializer looks up (or registers) its schema in Schema Registry.
3. Schema Registry returns a unique schema ID.
4. Producer encodes:

   ```
   [Magic Byte 0][Schema ID (4 bytes)][Avro serialized data]
   ```
5. Kafka stores the message.
6. Consumer later reads the message → uses Schema ID → fetches schema → deserializes back to a `Customer` object.

---

## 🧩 In Simple Terms

This Java code:

> Continuously generates random customer data, serializes each record in Avro format using Confluent Schema Registry, and sends it to a Kafka topic named `customerContacts`.

---

Customer Class is not a regular Plain Old Java Object but rather specialized one generated from a schema. We can generate these classes using avro-tools.jar or Maven plugin.

