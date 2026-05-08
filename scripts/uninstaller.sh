#!/usr/bin/env bash

set -e

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
RESET="\033[0m"


# Paths
WLX_DIR="$HOME/.wlx"
LOCAL_BIN="$HOME/.local/bin"


# Detect Shell
CURRENT_SHELL=$(basename "$SHELL")

case "$CURRENT_SHELL" in
    bash)
        SHELL_RC="$HOME/.bashrc"
        ;;
    
    zsh)
        SHELL_RC="$HOME/.zshrc"
        ;;
    
    *)
        SHELL_RC="$HOME/.bashrc"
        ;;
esac


# Banner
echo
echo -e "${CYAN}========================================${RESET}"
echo -e "${CYAN}         WLX Uninstaller${RESET}"
echo -e "${CYAN}========================================${RESET}"
echo


# Warning
echo -e "${YELLOW}[!] This will remove:${RESET}"
echo "    • WLX virtual environment"
echo "    • WLX database"
echo "    • WLX configuration"
echo "    • WLX shell integration"
echo "    • WLX runtime files"
echo "    • WLX command symlink"
echo

read -p "Are you sure? [y/N]: " CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo
    echo -e "${YELLOW}[-] Uninstall cancelled.${RESET}"
    exit 0
fi


# Remove WLX Environment
echo
echo -e "${CYAN}[*] Removing WLX environment...${RESET}"

rm -rf "$WLX_DIR"

echo -e "${GREEN}[+] WLX environment removed.${RESET}"


# Remove Symlink
echo
echo -e "${CYAN}[*] Removing WLX command symlink...${RESET}"

rm -f "$LOCAL_BIN/wlx"

echo -e "${GREEN}[+] WLX command removed.${RESET}"


# Remove Shell Integration
echo
echo -e "${CYAN}[*] Removing shell integration...${RESET}"

if [ -f "$SHELL_RC" ]; then

    sed -i '/# >>> WLX START >>>/,/# <<< WLX END <<</d' "$SHELL_RC"

    echo -e "${GREEN}[+] Shell integration removed.${RESET}"
fi


# Remove PATH Export
echo
echo -e "${CYAN}[*] Cleaning PATH configuration...${RESET}"

sed -i '\|export PATH="$HOME/.local/bin:$PATH"|d' "$SHELL_RC" || true

echo -e "${GREEN}[+] PATH configuration cleaned.${RESET}"


# Output
echo
echo -e "${GREEN}[+] WLX uninstalled successfully.${RESET}"

echo
echo -e "${CYAN}[*] Reload your shell:${RESET}"
echo
echo "    exec \$SHELL"

echo