# VS Code Tunnel Setup

## Creating EC2

Create an EC2 t2.medium Ubuntu instance with 50GB storage.

## 1. Connect to EC2

Use one of:

* EC2 Instance Connect (browser terminal)

You only need this once to start the tunnel.

---

# 2. Download the VS Code CLI on EC2

Run:

```bash
cd ~
wget https://update.code.visualstudio.com/latest/cli-linux-x64/stable -O vscode-cli.tar.gz
tar -xzf vscode-cli.tar.gz
```

This extracts a binary named `code`.

---

# 3. Start the tunnel

Run:

```bash
chmod +x code
./code tunnel
```

You will see:

* A login URL
* A device code

---

# 4. Authenticate

1. Open the URL in your laptop browser
2. Sign in with:

   * GitHub, or
   * Microsoft account
3. Approve the device

After approval, the terminal will show that the tunnel is running.

Leave this process running.

---

# 5. Open The link

You would get a link like this open it and enjoy!

https://vscode.dev/tunnel/xxxx/home/ubuntu

---

# 7. Common issues and fixes

Permission errors saving files
→ Fix ownership:

```bash
sudo chown -R ubuntu:ubuntu <project-folder>
```

If the tunnel stops repeat the same steps.
