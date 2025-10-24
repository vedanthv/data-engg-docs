# What happens when Out of Sync Replica becomes Leader?

When an out-of-sync replica is promoted to follower of a new leader, it will **truncate** (delete) any log records that the new leader doesn’t have. Those truncated records are permanently lost if no other replica holds them. The truncation is how Kafka enforces *single truth* (the leader’s log) and prevents the follower and leader remaining permanently inconsistent.

---

## What actually happens (step-by-step)

1. **Divergence happened earlier.**

   * While Replica A was leader, followers B and C fell behind (crashed or lagged). A accepted writes with offsets 100–200. B and C only have offsets 0–99.

2. **Leader A fails.**

   * If `unclean.leader.election.enable=true`, Kafka may elect Replica B (which only has 0–99) as the new leader even though it lacks 100–200.

3. **Replica A later comes back online.**

   * Replica A still contains 100–200 (the records written while B/C were out-of-sync). But now B is the leader and B’s log is the canonical log for that partition.

4. **Replica A becomes a follower and must catch up.**

   * The follower fetcher reads the leader’s state and realizes Replica A contains offsets that the leader *does not* have (100–200).
   * Kafka decides the follower’s local log beyond the leader’s log end offset is invalid relative to the leader.

5. **Log truncation on the follower.**

   * Replica A deletes (or truncates) those suffix records (100–200) from its local log so its log matches the leader’s log. In Kafka code this is a controlled truncation, not a merge — the follower’s log is brought to the leader’s last offset.

6. **Result: those records are gone cluster-wide.**

   * Because B (the new leader) never had 100–200 and other replicas lack them as well (or were out-of-sync), there is no remaining copy anywhere. Consumers can no longer access those messages.

---

## Why Kafka does this (the reason behind deletion)

Kafka enforces that the **leader’s log is the authoritative copy**. To keep all replicas consistent, followers must match the leader exactly. If followers kept their extra records, different replicas would disagree about the content and order of the partition — which would break correctness guarantees and make future leader elections chaotic.

So when a replica sees that the leader doesn’t have some suffix of its log, the follower truncates that suffix. That preserves the invariant: *every replica’s log is a prefix of the current leader’s log*.

---

## What “delete” means technically

* Kafka doesn’t just hide the messages; it actually truncates log segments or removes suffixes so those records are physically removed from the follower’s local storage (or at least logically discarded from the replica’s log).
* The follower’s log end offset is reduced to match the leader’s log end offset. The follower will request new data from the leader starting at that matched offset.

---

## Consequences for consumers and applications

1. **Some consumers may have already read the now-deleted messages.**

   * If consumers read offsets 100–150 when Replica A was leader, but later those offsets are deleted when logs are truncated, those messages are no longer available to read again. Consumers that recorded or acted on that data have seen information that no one else can reproduce from the topic.

2. **Inconsistent views across consumers.**

   * Different consumers may have read different sets (some saw the old 100–200, others saw the new   leader’s sequence). Downstream systems that aggregate or reconcile data can end up with inconsistent results.

3. **Offset problems (OffsetOutOfRange).**

   * A consumer whose committed offset points to a now-deleted range will hit `OffsetOutOfRange` on fetch and must decide how to proceed (reset to earliest/latest or use stored checkpoints).

4. **No recovery from Kafka alone.**

   * Once truncated and no other replica retains the messages, Kafka cannot restore those records. They are lost unless some external copy existed (e.g., an external log, sink, or backup).

5. **Transactional / exactly-once implications.**

   * If producers used transactions or relied on idempotence, the loss of committed-looking data can violate application-level invariants (for example, duplicated side effects or missing transactions).

---

## Analogies

### 1. Library copies analogy

Imagine a book where pages are numbered:

* Librarian A (leader) distributes copies and adds pages 100–200 to her copy while assistants B and C are away.
* Librarian A’s copy is the *latest* and patrons read pages 100–200 from it.
* A goes home. Assistant B returns and is made the new head librarian, but B only has pages up to 99.
* When A returns, A’s extra pages (100–200) are removed from A’s copy because the library now uses B’s copy as the canonical edition. The extra pages disappear from the library — nobody has them anymore. Patrons who read those pages earlier have read material that no longer exists in the library collection.

### 2. Ledger / bank account analogy

A partition is like a ledger:

* Leader A wrote transactions T100–T200 while B and C were disconnected.
* When A goes offline and B becomes the ledger owner, the ledger that B holds does not contain T100–T200.
* When A rejoins, A’s extra transactions are removed to reconcile with B’s ledger. Those transactions are permanently erased from the official ledger; if any customer saw those transactions earlier, their view is now inconsistent with the official ledger.

### 3. Git force-push analogy

Think of leader A’s log like a branch that had commits C100–C200. If B becomes the canonical branch at an earlier commit and the project decides to reset the branch to B’s commit, then commits C100–C200 are lost from the canonical history (unless someone kept a separate copy). That’s like a forced reset (force-push) that discards commits.

---

## How to avoid or mitigate this risk

* **Keep unclean leader election disabled (`false`)** (default) so Kafka never promotes out-of-sync replicas — prevents this class of data loss at the expense of availability.
* **Tune replication and ISR settings**:

  * `replication.factor >= 3` and `min.insync.replicas` to ensure enough replicas remain in ISR before commits are acknowledged.
* **Use `acks=all` on producers** to ensure writes are replicated to ISRs before being acknowledged.
* **Avoid long follower lag**: ensure network, disk I/O, and broker health are monitored; use rack awareness and capacity planning to reduce chance of slow followers.
* **Controlled broker shutdowns** (graceful shutdown) so leadership transfers cleanly and followers remain in sync.
* **Back up critical data externally** (mirror to durable storage) if any data loss is unacceptable.
* **Operational plan**: if you ever enable unclean leader election in an emergency to restore availability, be aware you may lose messages and should reconcile downstream systems accordingly; switch it back to false after recovery.

---

## Final takeaway

When a follower deletes records that the current leader does not have, Kafka is enforcing that the leader is the single source of truth. That deletion is permanent inside the Kafka cluster — if no replica retained those messages, they are irrecoverably lost from the topic. This behavior is the exact trade-off controlled by `unclean.leader.election.enable`: higher availability with possible data loss versus strong durability and consistency with possible temporary unavailability.
