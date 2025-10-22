## Kafka Consumers : Eager and Cooperative Rebalancing

Here’s a **deep technical explanation** of **Kafka Consumer Group Rebalancing**, including the difference between **Eager Rebalancing** and **Cooperative (Incremental) Rebalancing**, and how both interact with **Static Membership (KIP-345)**.

---

## 1. What is Consumer Group Rebalancing

In Apache Kafka, **consumer groups** allow multiple consumers to share the work of reading messages from one or more topics. Each **partition** of a topic is consumed by exactly one consumer in a group at a time.

**Rebalancing** is the process where Kafka redistributes partitions among consumers when:

* A new consumer joins the group.
* A consumer leaves (crash, shutdown, or timeout).
* Topic partitions are added or removed.
* Consumer subscription changes (e.g., new topics are subscribed).

Rebalancing ensures **load balancing** and **fault tolerance**, but it also causes a **temporary pause** in message consumption — this is what Kafka aims to minimize with newer protocols.

---

## 2. How Rebalancing Works (at a high level)

Rebalancing is coordinated by the **Group Coordinator** (a broker responsible for managing a specific consumer group).

The process involves two key phases:

1. **JoinGroup** — Consumers send a request to join the group.
2. **SyncGroup** — The leader (one of the consumers) assigns partitions and shares the plan with others.

### Typical sequence:

1. A consumer joins or leaves → triggers rebalance.
2. All consumers stop fetching messages.
3. All consumers send `JoinGroup` requests.
4. Group coordinator elects a leader.
5. Leader calculates partition assignment.
6. Assignment is distributed via `SyncGroup`.
7. Consumers resume consumption with new assignments.

During this time, no messages are processed — this **pause** is the main drawback of rebalancing.

---

## 3. Eager Rebalancing (Default / Traditional)

**Eager Rebalancing** (used before Kafka 2.4) is the **original protocol**.

### Behavior:

* **All consumers stop consuming** and **revoke all partitions** immediately when a rebalance starts.
* The entire group must rejoin, even if most members and assignments didn’t change.
* After reassignment, consumers receive their new partitions and resume processing.

### Drawbacks:

1. **Full stop of consumption** — all consumers pause during rebalance.
2. **Unnecessary disruption** — even unaffected consumers lose partitions.
3. **High latency** in large groups or frequent joins/leaves.
4. **Impact on availability** — the system is effectively idle during the rebalance.

Example scenario:
If a single new consumer joins a group of 10, **all 10 must revoke partitions** and wait for reassignment, even though only a few partitions need redistribution.

---

## 4. Cooperative (Incremental) Rebalancing (KIP-429, KIP-441)

To overcome these issues, Kafka introduced **Incremental Cooperative Rebalancing** in **KIP-429** (Kafka 2.4+).

### Key idea:

Instead of revoking *all* partitions during every rebalance, only the **affected** partitions are revoked and reassigned.

This makes rebalancing **incremental** and **non-disruptive**.

### How it works:

1. **Phase 1: Detect change**

   * A new consumer joins or one leaves.
   * Group coordinator initiates rebalance.

2. **Phase 2: Cooperative assignment**

   * Only partitions that *need to move* are revoked.
   * Unaffected consumers keep their existing partitions and continue processing.
   * The leader proposes a partial reassignment.

3. **Phase 3: Gradual synchronization**

   * The reassignment happens in steps (incrementally).
   * Once all members confirm readiness, partitions move to the new consumers.

4. **Result:**

   * The group stabilizes **without full disruption**.
   * Latency and downtime drop drastically.

### Example:

| Event              | Eager Rebalancing                      | Cooperative Rebalancing                                |
| ------------------ | -------------------------------------- | ------------------------------------------------------ |
| New consumer joins | All 10 consumers revoke all partitions | Only a few partitions are reallocated to new consumer  |
| Consumer leaves    | All remaining revoke and rebalance     | Only partitions of the leaving consumer are reassigned |
| Duration           | Long, seconds to tens of seconds       | Very short, often milliseconds                         |
| Consumption pause  | Entire group stops                     | Only small subset pauses                               |

---

## 5. CooperativeStickyAssignor

Kafka provides a **partition assignment strategy** called `CooperativeStickyAssignor`.

* It ensures **stickiness** — tries to keep existing assignments stable.
* It performs **incremental (cooperative) changes** during rebalance.
* It uses **two-phase partition revocation** to achieve smooth transition.

Configuration example:

```properties
partition.assignment.strategy=org.apache.kafka.clients.consumer.CooperativeStickyAssignor
```

If some consumers in a group use `CooperativeStickyAssignor` and others use `RangeAssignor` or `RoundRobinAssignor`, **they will be incompatible** — all members of the group must use cooperative-compatible assignors.

Awesome — this is one of those **Kafka consumer group** topics that sounds complicated (😵‍💫 "cooperative sticky assignor") but actually makes *perfect sense* once you visualize what’s happening.

Let’s explain it step by step — **like you’re 10 years old**, using a fun analogy.

---

## 🧃 1. Imagine a group of friends sharing juice boxes 🍹

Let’s say you and your friends (Kafka **consumers**) are sharing a bunch of **juice boxes** (Kafka **partitions**).

Each friend gets a few juice boxes to drink from.
Kafka’s job is to decide **who gets which juice boxes** — that’s called the **partition assignment**.

---

## ⚙️ 2. Rebalancing = when friends reshuffle the juice boxes

Sometimes new friends join, or someone leaves:

* Maybe you get a new friend joining the group.
* Or someone leaves early.

When that happens, the group needs to **rebalance** —
meaning everyone has to share the juice boxes again so everyone gets their fair share.

---

## 😣 3. The old way — “eager rebalancing”

In the *old system*, Kafka used what’s called the **RangeAssignor** or **RoundRobinAssignor**.
These use a process called **eager rebalancing**.

Here’s what happens there:

1. When something changes (someone joins or leaves), **everyone must put down all their juice boxes**.
2. Then Kafka redistributes *all* of them from scratch.
3. Every friend gets new boxes again — maybe some old, maybe new.

This means:

* Everyone stops drinking (processing messages).
* Even people who could’ve kept the same boxes must stop.
* There’s a brief “pause” where the group does no work.

That’s wasteful, right?

---

## 🤝 4. The new way — “Cooperative Sticky Assignor”

Kafka 2.4+ introduced the **Cooperative Sticky Assignor**, which works much smarter.

Think of it like this:
When a new friend joins, Kafka says:

> “Okay, nobody panic! You can *keep drinking your current juice boxes*.
> I’ll just move around a few so the new friend gets some too.”

🎯 **Key idea:**
Instead of everyone dropping all their boxes,
Kafka changes only *what’s necessary* — step by step.

---

## 💡 5. What “cooperative” and “sticky” mean

| Word            | Meaning                                                          | Example                                                                          |
| --------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Cooperative** | Everyone works together smoothly instead of stopping everything. | “Keep what you have until we need to move it.”                                   |
| **Sticky**      | Try to keep the same assignments whenever possible.              | “If you already have a juice box, keep it unless I really have to take it away.” |

So, the **Cooperative Sticky Assignor**:

* Moves *only* what’s needed during rebalancing.
* Keeps each consumer’s existing partitions “sticky” (unchanged) if possible.
* Allows **incremental rebalancing** (partial reshuffles).

---

## 🔁 6. How it changes rebalancing (step-by-step)

Let’s walk through an example:

### Before

You have 3 friends (C1, C2, C3) and 6 juice boxes (P0–P5).

| Consumer | Juice boxes |
| -------- | ----------- |
| C1       | P0, P1      |
| C2       | P2, P3      |
| C3       | P4, P5      |

Now a **new friend (C4)** joins.

### Old way (eager rebalancing)

1. Everyone puts down all juice boxes.
2. Kafka redistributes from scratch.
3. Everyone gets new boxes (like musical chairs).
4. During that time, no one is drinking (processing paused).

### New way (cooperative sticky)

1. Kafka says:

   * “Okay, most of you can keep what you already have.”
   * “C4, I’ll take one box from each of you and give them to you.”
2. C1, C2, and C3 *keep one box each*.
3. C4 gets a few boxes gradually.
4. Everyone else keeps working while this happens.

→ Nobody drops everything. Only small adjustments happen.

That’s why it’s called **cooperative** — everyone works together instead of stopping.

---

## ⚡ 7. Why this matters in real Kafka use

### With old rebalancing:

* Consumers stop reading messages.
* Offsets may need to be re-synced.
* Big pause in data flow.

### With cooperative sticky assignor:

* Rebalancing is *incremental* and much faster.
* Minimal interruption.
* Less network traffic.
* More predictable processing.

---

## 🧩 8. Behind the scenes (what Kafka actually does)

When cooperative sticky is used, rebalancing happens in **two phases**:

1. **Revoke phase:**
   Kafka tells only some consumers to give up certain partitions.
2. **Assign phase:**
   Those partitions are reassigned to the new (or remaining) consumers.

Everyone else continues processing without interruption.

Contrast that with eager rebalancing, which revokes *everything* from everyone before reassigning.

---

## 🧰 9. How to enable it

In the consumer config:

```properties
partition.assignment.strategy=org.apache.kafka.clients.consumer.CooperativeStickyAssignor
```

Kafka supports multiple assignors — this one is the modern default for smooth, incremental rebalances.

---

## 🧠 10. TL;DR — Like you’re explaining to a kid

Imagine a classroom where kids share crayons.

* **Eager rebalancing:**
  Every time a new kid comes in, the teacher makes *everyone* put their crayons back, then redistributes them all.
  → Lots of waiting.

* **Cooperative Sticky Assignor:**
  The teacher says, “Keep your crayons! I’ll just ask one or two of you to share a few with the new kid.”
  → Minimal disruption, no chaos.

---

✅ **In short:**

| Term            | Meaning                                                    | Why it’s good                             |
| --------------- | ---------------------------------------------------------- | ----------------------------------------- |
| **Cooperative** | Change assignments gradually                               | Consumers keep working during rebalancing |
| **Sticky**      | Keep partitions with the same consumer as long as possible | Fewer moves, faster recovery              |
| **Result**      | Incremental rebalancing                                    | Faster, smoother, minimal downtime        |

---

## 6. Static Membership (KIP-345)

Even with cooperative rebalancing, frequent consumer restarts (for example, due to container redeployments) can still cause unnecessary rebalances, because Kafka sees a new consumer as a new member.

**Static Membership (KIP-345)** reduces this.

### How it works:

* Each consumer has a **stable identity** (`group.instance.id`).
* As long as the same ID rejoins before `session.timeout.ms` expires, Kafka treats it as **the same member**.
* Therefore, no rebalance is triggered.

### Example:

Without static membership:

* Consumer restarts → considered a new member → triggers rebalance.

With static membership:

* Consumer restarts with same `group.instance.id` → no rebalance → resumes same partitions instantly.

Configuration example:

```properties
group.instance.id=consumer-app-01
```

**Result:** Minimal churn and faster recovery during rolling deployments or container restarts.

---

## 7. Combining Cooperative Rebalancing + Static Membership

These two features together provide **near-continuous availability**:

| Feature                               | Role                                                    |
| ------------------------------------- | ------------------------------------------------------- |
| **Cooperative Rebalancing (KIP-429)** | Minimizes partition movement; incremental changes only. |
| **Static Membership (KIP-345)**       | Prevents rebalances during temporary restarts.          |

Together, they drastically reduce downtime and consumer lag, particularly in **large consumer groups** or **microservice-based deployments**.

---

## 8. Summary: Eager vs Cooperative Rebalancing

| Aspect                       | Eager Rebalancing             | Cooperative Rebalancing   |
| ---------------------------- | ----------------------------- | ------------------------- |
| Revoke all partitions        | Yes                           | No (only affected)        |
| Pause during rebalance       | Entire group                  | Partial                   |
| Rebalance duration           | Long                          | Short                     |
| Impact on availability       | High                          | Minimal                   |
| Protocol version             | Default (pre-2.4)             | KIP-429 (2.4+)            |
| Assignor type                | RangeAssignor, StickyAssignor | CooperativeStickyAssignor |
| Supports incremental changes | No                            | Yes                       |
| Works with static membership | Yes, but less useful          | Very effective            |

---

## 9. In summary

* **Rebalancing** is how Kafka redistributes partitions in a consumer group.
* **Eager rebalancing** stops everyone, causing latency and disruption.
* **Cooperative (Incremental) rebalancing** (KIP-429) performs non-disruptive, stepwise reassignments.
* **Static Membership** (KIP-345) prevents unnecessary rebalances during client restarts.
* The **CooperativeStickyAssignor** ensures smooth partition handovers.

Together, these improvements make modern Kafka consumer groups **highly stable**, **low-latency**, and **resilient** even in dynamic, cloud-native environments.

Consumers maintain membership in a consumer group and ownership of partitions assigned to them by sending *heartbeats*
to a Kafka broker designated as a group coordinator (differs for different consumer groups)

The heartbeats are sent by a background thread and as long as it keeps sending within session timeout duration, the consumer is considered to be alive.

If consumer stops sending heartbeats, the consumer is considered dead and a rebalance is triggered.
When closing a consumer cleanly, the consumer will notify group coordinator that its leaving.