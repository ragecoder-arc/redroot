#!/usr/bin/env bash
# RedRoot Uninstaller Script
set -e

RED="\033[1;31m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RESET="\033[0m"

echo -e "${YELLOW}==> Uninstalling RedRoot...${RESET}"

rm -f "$HOME/.local/bin/redroot"
echo -e "${GREEN}✔ Removed $HOME/.local/bin/redroot${RESET}"

read -p "Do you want to delete your saved API key in ~/.config/redroot? (y/N): " rm_config
if [[ "$rm_config" =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/.config/redroot"
    echo -e "${GREEN}✔ Removed config directory${RESET}"
fi

echo -e "${GREEN}RedRoot has been uninstalled successfully.${RESET}"
