# 🛠 Steps to Setup Databricks CLI on Linux

---

## **1. Install Python & pip**

Databricks CLI is a Python package.
Check if you have Python 3 installed:

```bash
python3 --version
```

If not, install it:

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

---

## **2. Install Databricks CLI**

Run:

```bash
pip3 install databricks-cli --upgrade
```

Check installation:

```bash
databricks --version
```

---

## **3. Generate a Personal Access Token (PAT) in Databricks**

1. Go to your **Databricks workspace** in the browser.
2. Click on your username (top right) → **User Settings**.
3. Under **Access Tokens**, click **Generate New Token**.
4. Copy the token (you won’t see it again).

---

## **4. Configure Databricks CLI**

Run:

```bash
databricks configure --token
```

It will ask:

* **Databricks Host (URL)** → Example:

  * AWS: `https://<workspace-url>.cloud.databricks.com`
  * Azure: `https://<workspace-name>.azuredatabricks.net`
* **Token** → Paste the token you generated.

---

## **5. Test the CLI**

Run a test command to list clusters:

```bash
databricks clusters list
```

If successful, you’ll see details of your clusters.

---

## **6. (Optional) Store Multiple Profiles**

You can save multiple workspace logins using profiles in `~/.databricks/config`.
Example:

```ini
[DEFAULT]
host = https://myworkspace.azuredatabricks.net
token = dapi123abc

[staging]
host = https://staging-workspace.azuredatabricks.net
token = dapi456def
```

Then use:

```bash
databricks --profile staging clusters list
```

---

## **7. Use CLI for Common Tasks**

Examples:

```bash
# List jobs
databricks jobs list

# Upload a Python file to DBFS
databricks fs cp myscript.py dbfs:/FileStore/scripts/myscript.py

# Run a job
databricks jobs run-now --job-id <job_id>
```
