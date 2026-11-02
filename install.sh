#!/usr/bin/env bash
# RedRoot Installer Script
set -e

RED="\033[1;31m"
GREEN="\033[1;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${RED}"
cat << "EOF"
  ____           _ ____             _   
 |  _ \ ___   __| |  _ \ ___   ___ | |_ 
 | |_) / _ \ / _` | |_) / _ \ / _ \| __|
 |  _ <  __/| (_| |  _ < (_) | (_) | |_ 
 |_| \_\___| \__,_|_| \_\___/ \___/ \__|
                                         
   Autonomous Cybersecurity & Coding Agent
EOF
echo -e "${RESET}"

echo -e "${CYAN}==> Starting RedRoot Installation...${RESET}"

# 1. Check Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${RESET}"
    exit 1
fi
echo -e "${GREEN}✔ Python 3 detected.${RESET}"

# 2. Setup install directory
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
chmod +x "$SCRIPT_DIR/redroot.py"

# Copy or symlink redroot executable
ln -sf "$SCRIPT_DIR/redroot.py" "$INSTALL_DIR/redroot"
echo -e "${GREEN}✔ Installed executable to $INSTALL_DIR/redroot${RESET}"

# 3. Ensure ~/.local/bin is in PATH
add_to_path() {
    local rc_file="$1"
    if [ -f "$rc_file" ]; then
        if ! grep -q 'export PATH=.*\.local/bin' "$rc_file"; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc_file"
            echo -e "${GREEN}✔ Added ~/.local/bin to PATH in $rc_file${RESET}"
        fi
    fi
}

add_to_path "$HOME/.bashrc"
add_to_path "$HOME/.zshrc"

# 4. Prompt for API key if missing
CONFIG_DIR="$HOME/.config/redroot"
KEY_FILE="$CONFIG_DIR/api_key"

if [ -z "$OPENROUTER_API_KEY" ] && [ ! -f "$KEY_FILE" ]; then
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${RESET}"
    echo -e "${BOLD}🔑 API Key Configuration${RESET}"
    echo -e "RedRoot uses OpenRouter's free tier for AI inference."
    echo -e "Get your free API key at: ${CYAN}https://openrouter.ai/keys${RESET}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${RESET}"
    read -p "Enter your OpenRouter API Key (press Enter to skip for now): " user_key
    if [ -n "$user_key" ]; then
        mkdir -p "$CONFIG_DIR"
        echo "$user_key" > "$KEY_FILE"
        chmod 600 "$KEY_FILE"
        echo -e "${GREEN}✔ Saved API key to $KEY_FILE${RESET}"
    fi
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}${GREEN}🎉 RedRoot Installed Successfully!${RESET}"
echo -e "${CYAN}Quick Usage:${RESET}"
echo -e "  Interactive Mode : ${BOLD}redroot${RESET}"
echo -e "  Single Query     : ${BOLD}redroot \"scan localhost ports\"${RESET}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "Note: If 'redroot' is not found immediately, run: ${YELLOW}source ~/.bashrc${RESET} (or restart terminal)."
