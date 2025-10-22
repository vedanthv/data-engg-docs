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

You can think of this as explaining “how Kafka knows which door to use when someone wants to talk to it.”

---

## 🏠 1. Kafka is like a house with doors

Kafka brokers are like **houses**, and to talk to a broker (send messages, get data, etc.),
you need to know **which door to knock on**.

Each door has:

* A **name** (like “PLAINTEXT” or “SSL”)
* A **street address** (hostname or IP)
* A **door number** (port)

---

## 🚪 2. `listeners=PLAINTEXT://localhost:9092`

This says:

> “Open a door called **PLAINTEXT** on address **localhost**, port **9092**.”

That means:

* Kafka will **listen** on port `9092`
* It will accept **plain (unencrypted)** connections
* Clients and other brokers can connect through that door.

So if a producer or consumer wants to connect, it says:

```
bootstrap.servers=localhost:9092
```

→ They’re knocking on that door!

Think of this as the **door Kafka listens at**.

---

## 🗣️ 3. `inter.broker.listener.name=PLAINTEXT`

Kafka brokers in the same cluster talk to each other — they need their own “private line.”

This setting says:

> “When brokers talk to each other, use the **PLAINTEXT** door.”

So if you have multiple brokers:

* Broker 1, Broker 2, and Broker 3
* They’ll all use the **PLAINTEXT** channel to sync data and share cluster info.

This just tells Kafka:

> “Which of the doors we opened should the brokers use to chat among themselves?”

---

## 📢 4. `advertised.listeners=PLAINTEXT://localhost:9092`

Imagine you live inside your house, and you tell your friends:

> “Hey, if you want to visit me, come to **localhost:9092**.”

That’s what this does.

Kafka uses **advertised.listeners** to tell *clients and other brokers*
“this is the address you should use to reach me.”

### Why this matters:

If Kafka runs inside Docker, Kubernetes, or the cloud, the `listeners` address might be something *internal* (like `0.0.0.0`),
but the `advertised.listeners` should be the **public or reachable** hostname (like `my-broker.company.com`).

So:

* `listeners` = the **actual door** inside Kafka.
* `advertised.listeners` = the **address label** you give out to the world.

---

## 🧠 5. `controller.listener.names=CONTROLLER`

Kafka needs a “controller” — one special broker that coordinates the cluster (decides leaders, handles elections, etc.).

This line says:

> “The controller will use a listener called **CONTROLLER** to do its work.”

In Kafka’s new mode (called **KRaft mode** — Kafka without ZooKeeper),
the controller uses its **own special private door** (`CONTROLLER`) for cluster management.

You can ignore this if you’re running a simple single-node Kafka —
it’s just for internal communication between controller nodes.

---

## 🔐 6. `listener.security.protocol.map=...`

Now this is like a dictionary that tells Kafka:

> “What kind of security each door uses.”

Here’s what it means:

```
CONTROLLER:PLAINTEXT
PLAINTEXT:PLAINTEXT
SSL:SSL
SASL_PLAINTEXT:SASL_PLAINTEXT
SASL_SSL:SASL_SSL
```

So:

* Door named **PLAINTEXT** → normal unencrypted connection
* Door named **SSL** → encrypted HTTPS-style connection
* Door named **SASL_SSL** → encrypted + username/password
* Door named **CONTROLLER** → internal plain connection for controller traffic

Basically, this says:

> “Each door name matches its security type.”

---

## 🎯 7. Putting it all together

| Config                           | Think of it as                                | What it does                                              |
| -------------------------------- | --------------------------------------------- | --------------------------------------------------------- |
| `listeners`                      | 🏠 The doors Kafka opens                      | Where Kafka waits for connections                         |
| `inter.broker.listener.name`     | 📞 The door brokers use to talk to each other | Chooses which listener for broker-to-broker communication |
| `advertised.listeners`           | 📢 The address Kafka tells others to use      | How clients and brokers find this broker                  |
| `controller.listener.names`      | 🧠 The private control door                   | Used by the controller in KRaft mode                      |
| `listener.security.protocol.map` | 🗺️ The security rulebook                     | Maps each door to its security protocol                   |

---

## 🧩 8. Simple example story

Imagine:

* You (Kafka broker) live in a house.
* You have a few doors:

  * “Front door” (PLAINTEXT) → anyone can visit
  * “Back door” (CONTROLLER) → for your best friend (controller)
  * “Secret door” (SSL) → only for trusted people with keys

You tell your friends:

> “Use the front door at localhost:9092 to visit me!”

That’s:

```
advertised.listeners=PLAINTEXT://localhost:9092
```

And you decide that you and your best friend (another broker) will use the same door to talk:

```
inter.broker.listener.name=PLAINTEXT
```

---

## ✅ 9. In short — the “kid” version:

* **listeners** → Kafka opens this door to listen.
* **advertised.listeners** → Kafka tells everyone, “Hey! Knock on *this* door.”
* **inter.broker.listener.name** → Brokers talk to each other through this door.
* **controller.listener.names** → The controller uses this door to manage the cluster.
* **listener.security.protocol.map** → Explains which door uses which kind of lock (security).

---

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

