## Broker Properties in Kafka

### broker.id

<img width="846" height="462" alt="image" src="https://github.com/user-attachments/assets/149d52a3-03b5-4be0-a2c7-a4c23a86ff70" />

### listeners

<img width="827" height="558" alt="image" src="https://github.com/user-attachments/assets/769049f4-fcca-42d7-827b-2a3b3ae83e13" />


Example Config


```bash
# The address the socket server listens on. If not configured, the host name will be equal to the value of
# java.net.InetAddress.getCanonicalHostName(), with PLAINTEXT listener name, and port 9092.
#   FORMAT:
#     listeners = listener_name://host_name:port
#   EXAMPLE:
#     listeners = PLAINTEXT://your.host.name:9092
listeners=PLAINTEXT://localhost:9092

# Name of listener used for communication between brokers.
inter.broker.listener.name=PLAINTEXT

# Listener name, hostname and port the broker will advertise to clients.
# If not set, it uses the value for "listeners".
advertised.listeners=PLAINTEXT://localhost:9092

# A comma-separated list of the names of the listeners used by the controller.
# This is required if running in KRaft mode. On a node with `process.roles=broker`, only the first listed listener will be used by the broker.
controller.listener.names=CONTROLLER

# Maps listener names to security protocols, the default is for them to be the same. See the config documentation for more details
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
```

### zookeeper.connect

<img width="567" height="587" alt="image" src="https://github.com/user-attachments/assets/5ea976e5-a6cf-4c80-a35d-93c69a215d86" />

### log.dirs

<img width="906" height="574" alt="image" src="https://github.com/user-attachments/assets/37a00347-9692-420a-ad5e-4901f497023e" />

### num.recovery.thread.per.data.dir

<img width="913" height="731" alt="image" src="https://github.com/user-attachments/assets/669a6303-eb7b-47a3-80ec-179e616e6ef9" />

Alright, let’s simplify this 👇

---

#### 📝 What’s happening?

* Kafka stores messages on disk in **log segments** (files).
* When a broker starts or shuts down, it needs to **open, check, or close** all these log files.
* To do this work, Kafka uses a **pool of threads**.

---

#### 🔑 Where threads are used:

1. **Normal startup** → open each partition’s log files.
2. **Startup after a crash** → carefully check + truncate log files (takes longer).
3. **Shutdown** → close log files properly.

---

#### ⚙️ Default setting

* By default, Kafka uses **1 thread per log directory**.
* Example: if you have 3 log directories → 3 threads total.

---

#### 🚀 Why increase threads?

* If you have **many partitions** and a broker crashed, recovery can take **hours** with just 1 thread per directory.
* Increasing threads allows **parallel recovery** → much faster startup.

---

#### 📌 Important note

The config is called:

```properties
num.recovery.threads.per.data.dir
```

* If you set it to `8` and you have `3` log.dirs, total = `8 × 3 = 24 threads`.
* More threads → faster startup/recovery.

---

👉 **Layman analogy:**
Imagine you have 10,000 books (partitions) to put back on shelves after a storm (broker crash).

* With 1 librarian per shelf (default), it takes hours.
* With 8 librarians per shelf (more threads), all books are sorted much faster.

#### Why Truncate Log Segments?

Great question 👍 Let’s break it down simply.

---

#### 📝 Why truncation is needed after a crash

* Kafka writes data to disk in **log segments**.
* Each segment has an **ordered sequence of messages**.
* When a broker crashes (power cut, OOM, kill -9, etc.), some data may have been **partially written** (corrupted, incomplete).

---

#### 🔎 What happens after restart

1. Kafka reopens the log files.
2. It checks the last segment for **incomplete or corrupted records**.
3. If it finds bad records at the end of the file → it **truncates** (cuts off) the broken part so only valid data remains.

---

#### ✅ Why this is important

* Ensures **data consistency**: no half-written messages are exposed to consumers.
* Keeps the **log index aligned** with the actual data.
* Avoids strange errors like “message length mismatch” or “invalid checksum.”

---

#### 📌 Example

Imagine writing messages to a notebook:

```
Page 1: OK
Page 2: OK
Page 3: crash halfway through sentence...
```

When you reopen, Kafka **erases the half-written sentence** on Page 3, so the notebook only contains complete entries.

---

#### 🔒 Safety net

* Kafka only truncates data that wasn’t **fully acknowledged** (not committed).
* So producers/consumers won’t lose *confirmed* messages — only the garbage left behind by the crash.

---

👉 In short: **Truncation after a crash = clean up the mess at the end of the log so the broker can continue safely.**

### auto.create.topics.enable

<img width="852" height="362" alt="image" src="https://github.com/user-attachments/assets/a83b3dbd-7c00-48cd-a717-57115adc60db" />

### auto.leader.rebalance.enable

<img width="859" height="337" alt="image" src="https://github.com/user-attachments/assets/e081c20c-b890-40d3-bd29-5d0c7b60e754" />

### delete.topic.enable

<img width="894" height="154" alt="image" src="https://github.com/user-attachments/assets/a3276d16-01a9-4766-a69e-342d06d26d21" />

