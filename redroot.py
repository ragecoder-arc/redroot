#!/usr/bin/env python3
"""
💀 RedRoot - Autonomous Terminal Coding & Cybersecurity AI Agent
Author: RedRoot Team / Community
License: MIT
"""

import json
import os
import readline
import re
import subprocess
import sys
import urllib.request

# Model Configuration
API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "nvidia/nemotron-3.5-lightning:free"
CONFIG_DIR = os.path.expanduser("~/.config/redroot")
KEY_FILE = os.path.join(CONFIG_DIR, "api_key")

# ANSI Colors (RedRoot Theme)
RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def get_api_key():
    """Retrieves API key from ENV or config file, or prompts the user."""
    # 1. Check environment variable
    key = os.getenv("OPENROUTER_API_KEY")
    if key and key.strip():
        return key.strip()

    # 2. Check config file
    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, "r", encoding="utf-8") as f:
                saved_key = f.read().strip()
                if saved_key:
                    return saved_key
        except Exception:
            pass

    # 3. Prompt user for key
    print(f"{YELLOW}═══════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}🔑 Welcome to RedRoot!{RESET}")
    print(f"RedRoot uses OpenRouter's Free NVIDIA Nemotron API.")
    print(f"Get your 100% free API key from: {CYAN}https://openrouter.ai/keys{RESET}")
    print(f"{YELLOW}═══════════════════════════════════════════════════════════════{RESET}")

    try:
        user_key = input(f"\n{CYAN}Enter your OpenRouter API Key (sk-or-v1-...): {RESET}").strip()
        if not user_key:
            print(f"{RED}Error: API key is required to run RedRoot.{RESET}")
            sys.exit(1)

        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(KEY_FILE, "w", encoding="utf-8") as f:
            f.write(user_key)
        os.chmod(KEY_FILE, 0o600)
        print(f"{GREEN}✔ API Key saved securely to {KEY_FILE}{RESET}\n")
        return user_key
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}Setup aborted.{RESET}")
        sys.exit(1)


API_KEY = get_api_key()

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/redroot-ai/redroot",
    "X-Title": "RedRoot-Terminal-Agent",
}

SYSTEM_PROMPT = f"""You are RedRoot, an elite autonomous AI coding agent, Linux power user, cybersecurity expert, and ethical bug hunter.
Current Working Directory: {os.getcwd()}

You have autonomous tools to interact directly with the user's Linux system. To use tools, you MUST output these exact markdown blocks:

1. To CREATE or OVERWRITE a file:
```write_file:/absolute/or/relative/path.ext
<full file contents here>
```

2. To READ an existing file from disk:
```read_file:/absolute/or/relative/path.ext
```

3. To EXECUTE a Linux terminal command:
```bash_exec
<command to execute>
```

GUIDELINES:
- When the user asks you to build, create, code, or fix a project or script, DO NOT just explain—use `write_file` to actually create the code files on disk!
- Keep explanations clear, practical, and concise.
- Always use working, secure code and reliable commands.
"""


def stream_chat(messages):
    """Streams the model response in real time and returns full text."""
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 4096,
        "include_reasoning": False,
        "stream": True,
    }

    req = urllib.request.Request(
        API_URL, data=json.dumps(payload).encode("utf-8"), headers=HEADERS
    )

    full_reply = []
    print(f"{RED}{BOLD}RedRoot ❯{RESET} ", end="", flush=True)

    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8").strip()
                if not line or not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        print(content, end="", flush=True)
                        full_reply.append(content)
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
        print("\n")
        return "".join(full_reply).strip()

    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"\n{RED}[API Error {e.code}]: {err_body}{RESET}\n")
        return None
    except urllib.error.URLError as e:
        print(f"\n{RED}[Network Error]: {e.reason}{RESET}\n")
        return None
    except TimeoutError:
        print(f"\n{RED}[Error]: Request timed out. Try again.{RESET}\n")
        return None


def execute_agent_actions(text):
    """Parses and executes write_file, read_file, and bash_exec blocks."""
    pattern = r"```(write_file:[^\n]+|read_file:[^\n]+|bash_exec)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    if not matches:
        return None

    results = []

    for action, content in matches:
        action = action.strip()
        content = content.rstrip()

        # 1. WRITE FILE ACTION
        if action.startswith("write_file:"):
            file_path = action.split(":", 1)[1].strip()
            abs_path = os.path.abspath(
                os.path.expanduser(
                    os.path.join(os.getcwd(), file_path)
                    if not os.path.isabs(file_path)
                    else file_path
                )
            )

            confirm = (
                input(
                    f"{YELLOW}[RedRoot Action] Write file to '{CYAN}{abs_path}{YELLOW}'? (Y/n): {RESET}"
                )
                .strip()
                .lower()
            )
            if confirm in ["", "y", "yes"]:
                try:
                    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                    with open(abs_path, "w", encoding="utf-8") as f:
                        f.write(content + "\n")
                    print(f"{GREEN}✔ [File Saved]: {abs_path}{RESET}\n")
                    results.append(
                        f"Action: write_file '{abs_path}' -> SUCCESS: File written ({len(content)} bytes)."
                    )
                except Exception as e:
                    print(f"{RED}✘ [Write Failed]: {e}{RESET}\n")
                    results.append(
                        f"Action: write_file '{abs_path}' -> FAILED: {e}"
                    )
            else:
                print(f"{DIM}[Write Skipped by user]{RESET}\n")
                results.append(
                    f"Action: write_file '{abs_path}' -> SKIPPED by user."
                )

        # 2. READ FILE ACTION
        elif action.startswith("read_file:"):
            file_path = action.split(":", 1)[1].strip()
            abs_path = os.path.abspath(
                os.path.expanduser(
                    os.path.join(os.getcwd(), file_path)
                    if not os.path.isabs(file_path)
                    else file_path
                )
            )

            try:
                if os.path.exists(abs_path):
                    with open(abs_path, "r", encoding="utf-8") as f:
                        file_data = f.read()
                    print(f"{GREEN}✔ [File Read]: {abs_path}{RESET}\n")
                    results.append(
                        f"Action: read_file '{abs_path}' -> SUCCESS Content:\n```\n{file_data}\n```"
                    )
                else:
                    print(f"{RED}✘ [Read Failed]: File not found{RESET}\n")
                    results.append(
                        f"Action: read_file '{abs_path}' -> FAILED: File does not exist."
                    )
            except Exception as e:
                print(f"{RED}✘ [Read Failed]: {e}{RESET}\n")
                results.append(f"Action: read_file '{abs_path}' -> FAILED: {e}")

        # 3. BASH COMMAND EXECUTION ACTION
        elif action == "bash_exec":
            command = content.strip()
            confirm = (
                input(
                    f"{YELLOW}[RedRoot Action] Execute bash command: '{CYAN}{command}{YELLOW}'? (y/N): {RESET}"
                )
                .strip()
                .lower()
            )
            if confirm in ["y", "yes"]:
                print(f"{DIM}Running command...{RESET}")
                try:
                    proc = subprocess.run(
                        command,
                        shell=True,
                        text=True,
                        capture_output=True,
                        timeout=60,
                        cwd=os.getcwd(),
                    )
                    stdout = proc.stdout.strip()
                    stderr = proc.stderr.strip()

                    output_str = ""
                    if stdout:
                        print(f"{DIM}{stdout}{RESET}")
                        output_str += f"STDOUT:\n{stdout}\n"
                    if stderr:
                        print(f"{RED}{stderr}{RESET}")
                        output_str += f"STDERR:\n{stderr}\n"

                    print(f"{GREEN}✔ [Command Finished (code {proc.returncode})]{RESET}\n")
                    results.append(
                        f"Action: bash_exec '{command}' -> EXIT {proc.returncode}:\n{output_str}"
                    )
                except subprocess.TimeoutExpired:
                    print(f"{RED}✘ [Command Timed Out (60s)]{RESET}\n")
                    results.append(
                        f"Action: bash_exec '{command}' -> TIMED OUT after 60s."
                    )
                except Exception as e:
                    print(f"{RED}✘ [Execution Failed]: {e}{RESET}\n")
                    results.append(
                        f"Action: bash_exec '{command}' -> ERROR: {e}"
                    )
            else:
                print(f"{DIM}[Command Skipped by user]{RESET}\n")
                results.append(
                    f"Action: bash_exec '{command}' -> SKIPPED by user."
                )

    return "\n\n".join(results) if results else None


def print_banner():
    banner = f"""{RED}
╔══════════════════════════════════════════════════════════════════════╗
║                    💀 REDROOT AUTONOMOUS AGENT 💀                    ║
║   Identity: Elite Linux & Cybersecurity Terminal Assistant           ║
║   Model: {DEFAULT_MODEL}             ║
║   Tools: File Creation (write_file) | Read File | Bash Exec          ║
║   Commands: /clear (reset) | /pwd | /help | exit / quit              ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}"""
    print(banner)


def main():
    # Direct CLI one-liner query mode
    if len(sys.argv) > 1:
        single_query = " ".join(sys.argv[1:])
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": single_query},
        ]
        reply = stream_chat(messages)
        if reply:
            execute_agent_actions(reply)
        return

    # Interactive Agent Mode
    print_banner()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            prompt = f"{CYAN}{BOLD}You ❯{RESET} "
            user_input = input(prompt).strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "q"]:
                print(f"{RED}RedRoot session terminated. Happy Hacking! 💀{RESET}")
                break

            if user_input.lower() in ["/clear", "/reset"]:
                os.system("clear")
                print_banner()
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                print(f"{DIM}[RedRoot context reset successfully]{RESET}\n")
                continue

            if user_input.lower() == "/pwd":
                print(f"{YELLOW}Working directory: {os.getcwd()}{RESET}\n")
                continue

            if user_input.lower() == "/help":
                print(f"""{YELLOW}
RedRoot Agent Commands:
  /clear  - Clear terminal and reset conversation memory
  /pwd    - Print current working directory
  /help   - Show this help menu
  exit    - Exit RedRoot

Agent Capabilities:
  - "Create a python script called scan.py that finds open ports"
  - "Read /etc/hosts and explain what is inside"
  - "Create a project folder 'recon' with 2 python files"
  RedRoot will automatically write the code and prompt you (Y/n) to save it directly!
{RESET}""")
                continue

            messages.append({"role": "user", "content": user_input})

            # Agent Loop (Up to 3 turns for tool outputs)
            for _ in range(3):
                reply = stream_chat(messages)
                if not reply:
                    messages.pop()
                    break

                messages.append({"role": "assistant", "content": reply})

                tool_output = execute_agent_actions(reply)
                if tool_output:
                    messages.append(
                        {
                            "role": "user",
                            "content": f"[SYSTEM TOOL EXECUTION REPORT]:\n{tool_output}\n\nPlease proceed or summarize completion.",
                        }
                    )
                else:
                    break

        except KeyboardInterrupt:
            print(f"\n{YELLOW}Press Ctrl+D or type 'exit' to quit.{RESET}\n")
            continue
        except EOFError:
            print(f"\n{RED}RedRoot session closed.{RESET}")
            break


if __name__ == "__main__":
    main()
