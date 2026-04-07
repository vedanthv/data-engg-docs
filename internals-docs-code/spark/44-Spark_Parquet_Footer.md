# 1. Correct Structure of a Parquet File

```text
[ Row Group 1 ]
[ Row Group 2 ]
[ Row Group 3 ]
...
[ Footer ]
```

 Key point:

* **Footer is global (file-level)**
* Not repeated for each row group

---

# 2. What the Footer Contains

The footer is extremely important. It stores metadata for the **entire file**, including:

### File-level metadata

* Schema
* Number of rows
* Number of row groups

### Row group metadata (for each row group)

For every row group, it contains:

* Row group location (offset in file)
* Number of rows
* Size

### Column-level metadata (inside each row group)

* Column chunk offsets
* Compression type
* Encoding
* Statistics:

  * min
  * max
  * null count

---

# 3. So Where is Row Group Info Stored?

 Inside the **footer**, not inside the row group itself

Think of it like an index:

```text
Footer:
  RowGroup1 → starts at byte X, min(age)=10, max(age)=20
  RowGroup2 → starts at byte Y, min(age)=25, max(age)=60
```

---

# 4. Why Only One Footer?

Because Spark (or any engine) does this:

1. Reads **last few bytes of file**
2. Locates footer
3. Gets:

   * Schema
   * Row group metadata
4. Decides:

   * Which row groups to read
   * Which to skip

 This avoids scanning the whole file

---

# 5. How Predicate Pushdown Uses Footer

Example:

```python
df.filter("age > 30")
```

From footer:

```text
RowGroup1: min=10, max=20 → skip
RowGroup2: min=25, max=60 → read
```

 This is possible because metadata is centralized in footer

---

# 6. Do Row Groups Contain Any Metadata?

Yes, but limited:

* They contain **data + encoded pages**
* Not full metadata like schema or stats

 Detailed metadata is only in footer

---

# 7. Common Misconception

 “Each row group has its own footer”
 Reality:

* Each row group has metadata
* But that metadata is **stored in the file footer**

---

# 8. Interview-Ready Answer

If asked:

**“Does each row group have a footer?”**

You can say:

> No, a Parquet file has a single footer at the end. The footer contains metadata for all row groups, including their offsets, sizes, and column statistics. Row groups themselves only store the actual columnar data and pages, not separate footers.
