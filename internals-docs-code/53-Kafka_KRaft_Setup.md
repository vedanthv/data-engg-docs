# 📝 Kafka 4.x (KRaft Mode) – Single Broker Setup

## 1. Install Java (required for Kafka)

Kafka 4.x requires Java 11+.

```bash
sudo apt update
sudo apt install openjdk-11-jdk -y
java -version
```

✅ Verify you see `openjdk version "11..."`.

---

## 2. Download Kafka

```bash
cd /home/ubuntu/kafka-book
wget https://dlcdn.apache.org/kafka/4.1.0/kafka_2.13-4.1.0.tgz
tar -xvzf kafka_2.13-4.1.0.tgz
cd kafka_2.13-4.1.0
```

---

## 3. Configure Kafka (KRaft mode, no ZooKeeper)

Edit `config/server.properties`:

```properties
# Node identity
process.roles=broker,controller
node.id=1

# Listeners (broker + controller)
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
controller.listener.names=CONTROLLER

# Required for KRaft mode
controller.quorum.voters=1@localhost:9093

# Storage directory
log.dirs=/tmp/kraft-combined-logs
```

---

## 4. Format the Storage Directory

```bash
# Remove any old logs (important when retrying!)
rm -rf /tmp/kraft-combined-logs

# Generate a cluster ID
bin/kafka-storage.sh random-uuid
# Example output: 8dR1yJ7sT-u64QYy9mNQwQ

# Format logs with the generated ID
bin/kafka-storage.sh format -t <uuid-from-above> -c config/server.properties
```

---

## 5. Start the Kafka Broker

```bash
bin/kafka-server-start.sh config/server.properties
```

Kafka should now start without errors.

---

## 6. Create a Test Topic

```bash
bin/kafka-topics.sh --create \
  --topic test-topic \
  --partitions 1 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092
```

---

## 7. Produce Messages

```bash
bin/kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092
# Type messages, hit Enter after each
```

---

## 8. Consume Messages

```bash
bin/kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092
```

---

# ❌ Mistakes Made (and Fixes)

### 1. Looking for `zookeeper-server-start.sh`

* Kafka 4.x uses **KRaft mode** (no ZooKeeper).
* Solution: use `config/server.properties` with `controller.quorum.voters`.

---

### 2. "Classpath is empty"

* This happens if you download the **source code** instead of the **binary release**.
* Fix: download `kafka_2.13-4.1.0.tgz` (binary).

---

### 3. "java: not found"

* Java wasn’t installed.
* Fix: `sudo apt install openjdk-11-jdk -y`.

---

### 4. "No readable meta.properties files found"

* Means storage wasn’t formatted before starting broker.
* Fix: run `kafka-storage.sh format`.

---

### 5. "config/kraft/server.properties not found"

* Looked for the wrong file path (some docs show `config/kraft/…`).
* Fix: edit `config/server.properties`.

---

### 6. "controller.quorum.voters not set"

* Mandatory with one broker config so that kafka knows that this sole broker is to be bootstrapped.
* Fix: add

  ```properties
  controller.quorum.voters=1@localhost:9093
  ```
