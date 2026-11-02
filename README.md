# 💀 RedRoot

> **Autonomous Terminal AI Agent for Hackers, Bug Hunters & Linux Developers.**  
> Powered by NVIDIA Nemotron 3.5 via OpenRouter Free Tier. Zero dependencies. 100% Free.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-lightgrey.svg)]()
[![Free Tier](https://img.shields.io/badge/API-100%25%20Free-green.svg)](https://openrouter.ai/)

---

## ⚡ What is RedRoot?

**RedRoot** is a lightweight, zero-dependency autonomous terminal AI agent. Unlike regular chatbots that only print code to your screen, RedRoot has **agentic tools** that allow it to **create files, inspect your codebase, and execute Linux commands** directly from your terminal (always with your explicit permission).

Tailored specifically for:
- 🎯 **Ethical Bug Hunting & Recon Automation**
- 🛡️ **Source Code Auditing & Vulnerability Research**
- 💻 **Fast Bash / Python Scripting**
- 🧠 **CTF Challenges & Exploit Analysis**

---

## ✨ Features

- **Autonomous File Operations**: Tell RedRoot *"Create a port scanner in Python"*, and it will draft the script and prompt you (`Y/n`) to save it directly to disk.
- **System Command Execution**: Can run and test Linux commands (with user confirmation).
- **Live Real-time Streaming**: Instant word-by-word streaming responses (no lag).
- **Zero External Python Dependencies**: Built entirely on standard Python libraries (`urllib`, `json`, `readline`, `subprocess`).
- **Terminal Native**: Full arrow-key command history, reverse-search (`Ctrl+R`), and vibrant ANSI themes.
- **100% Free Inference**: Connects directly to NVIDIA's Nemotron models via OpenRouter's free tier.

---

## 🚀 Quick Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/redroot.git
cd redroot
```

### 2. Run the Installer
```bash
chmod +x install.sh
./install.sh
```

The installer will:
1. Link `redroot` to `~/.local/bin/redroot`.
2. Ensure `~/.local/bin` is in your `$PATH`.
3. Prompt for your free [OpenRouter API Key](https://openrouter.ai/keys) (only once).

---

## 💡 Usage

### 1. Interactive Chat & Agent Mode
Start an interactive terminal session:
```bash
redroot
```

**Commands inside chat:**
- `/clear` or `/reset` — Clear screen and reset conversation memory.
- `/pwd` — Display the current working directory.
- `/help` — Display help instructions.
- `exit`, `quit`, or `q` — Exit cleanly.

---

### 2. Quick One-Liner CLI Queries
Ask questions or generate tools directly from your shell without opening interactive mode:

```bash
# Ask technical questions
redroot "How to check listening TCP ports in Linux using ss"

# Generate scripts directly on disk
redroot "Create a python script called dir_bruter.py with multi-threading and custom user-agent"
```

RedRoot will stream the solution and prompt:
```text
[RedRoot Action] Write file to '/path/to/dir_bruter.py'? (Y/n): 
```
Press **Enter** to write the file directly!

---

## 🛡️ Example Use Cases in Bug Hunting

### 1. Automating Recon Pipelines
```bash
redroot "Create a bash script that chains subfinder, httpx, and nuclei for scanning CVE-2024-XXXX"
```

### 2. White-Box Code Audit
```bash
redroot "Read app.py and audit the authentication flow for IDOR or race conditions"
```

### 3. Custom Exploit PoC Drafting
```bash
redroot "Draft a Python PoC script to test an unauthenticated blind SSRF on localhost:8080"
```

---

## 🛠️ Configuration

You can configure your OpenRouter API key in either of two ways:

1. **Environment Variable:**
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-xxxxxxxx"
   ```
2. **Config File:**
   Saved automatically to `~/.config/redroot/api_key`.

---

## 🤝 Pairing with Aider (Multi-File Coding Agent)

If you need full git-integrated, multi-file refactoring, RedRoot pairs seamlessly with [Aider](https://aider.chat/):

```bash
# Install Aider
pip install aider-chat

# Run Aider with Nemotron (Free)
aider --model openrouter/nvidia/nemotron-3.5-lightning:free
```

---

## ⚖️ Disclaimer

RedRoot is intended strictly for authorized security assessments, academic research, and defensive development. Users are responsible for complying with all applicable local, state, and international laws. Do not use this tool on systems without explicit permission.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
