### Auto Loader Concept in Databricks

Auto Loader is a Databricks feature for incrementally and efficiently ingesting new data files from cloud storage (S3, ADLS, GCS) into Delta Lake tables.

It solves the problem of:

“How do I continuously load only the new files that arrive in my data lake, without reprocessing old files every time?”

**⚙️ How it works**

**New files detection**

Auto Loader uses file notification or directory listing to detect new files in cloud storage.

Each file is processed exactly once.

**Schema handling**

Auto Loader can infer schemas automatically and evolve them as new fields appear.

Supports schema evolution modes like:

addNewColumns → automatically adds new columns.

rescue → unexpected fields are captured in _rescued_data column instead of failing.

**Incremental state tracking**

Auto Loader stores state in a schema location checkpoint directory, so it knows which files are already ingested.

**Streaming or batch**

Auto Loader works as a Structured Streaming source but can also be triggered in a batch-like mode.

### 🔑 Key Features

Scalable ingestion: Handles billions of files.

Efficient: Processes only new/changed files, no need for full scans.

Schema evolution: Adapts to changing data over time.

Rescue data: Keeps unrecognized/mismatched fields safe for later analysis.

Integration: Works seamlessly with Delta Lake, Structured Streaming, and Databricks Workflows.

### 📊 Modes of schema evolution

none → no schema changes allowed.

addNewColumns → automatically add new columns to the table.

rescue → unexpected fields go into _rescued_data.

Manual → you evolve schema explicitly using ALTER TABLE.

**🔒 Why use Auto Loader instead of plain Structured Streaming?**

Without Auto Loader: you’d have to rescan directories and manually deduplicate files.

With Auto Loader: file discovery and state management are built-in → scalable & cost-efficient.
