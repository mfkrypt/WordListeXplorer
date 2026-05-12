#!/usr/bin/env bash

set -e


# WLX Production Installer
VERSION="1.0.1"


# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
RESET="\033[0m"


# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

WLX_DIR="$HOME/.wlx"
WLX_VENV="$WLX_DIR/venv"
LOCAL_BIN="$HOME/.local/bin"


# Banner
echo
echo -e "${CYAN}========================================${RESET}"
echo -e "${CYAN}      WordListeXplorer (WLX)${RESET}"
echo -e "${CYAN}              v${VERSION}${RESET}"
echo -e "${CYAN}========================================${RESET}"
echo


# Prevent sudo
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}[!] Please do not run this installer with sudo.${RESET}"
    exit 1
fi


# Dependency Checks
echo -e "${CYAN}[*] Checking system requirements...${RESET}"

if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[!] Python3 is not installed.${RESET}"
    exit 1
fi

if ! command -v git &>/dev/null; then
    echo -e "${RED}[!] Git is not installed.${RESET}"
    exit 1
fi

if ! python3 -m venv --help &>/dev/null; then
    echo -e "${RED}[!] python3-venv is not installed.${RESET}"
    echo
    echo "Install it using:"
    echo
    echo "    sudo apt install python3-venv"
    echo
    exit 1
fi

echo -e "${GREEN}[+] System requirements satisfied.${RESET}"


# Shell Detection
CURRENT_SHELL=$(basename "$SHELL")

case "$CURRENT_SHELL" in
    bash)
        SHELL_RC="$HOME/.bashrc"
        ;;
    
    zsh)
        SHELL_RC="$HOME/.zshrc"
        ;;
    
    *)
        echo -e "${RED}[!] Unsupported shell: $CURRENT_SHELL${RESET}"
        exit 1
        ;;
esac

echo -e "${GREEN}[+] Detected shell:${RESET} $CURRENT_SHELL"


# Create WLX Directories
mkdir -p "$WLX_DIR"
mkdir -p "$LOCAL_BIN"


# Store Installation Path
echo "$PROJECT_ROOT" > "$WLX_DIR/install_path"


# Create Virtual Environment
echo
echo -e "${CYAN}[*] Creating isolated WLX environment...${RESET}"

if ! python3 -m venv "$WLX_VENV"; then

    echo
    echo -e "${RED}[!] Failed to create WLX virtual environment.${RESET}"

    echo
    echo "Possible causes:"
    echo "  • insufficient permissions"
    echo "  • broken python3-venv package"
    echo "  • read-only filesystem"
    echo

    exit 1
fi

echo -e "${GREEN}[+] Virtual environment created.${RESET}"


# Activate Environment
source "$WLX_VENV/bin/activate"


# Upgrade pip
echo
echo -e "${CYAN}[*] Updating pip...${RESET}"

pip install --upgrade pip >/dev/null


# Install WLX
echo
echo -e "${CYAN}[*] Installing WLX...${RESET}"

if ! pip install "$PROJECT_ROOT"; then

    echo
    echo -e "${RED}[!] Failed to install WLX.${RESET}"

    echo
    echo "Possible causes:"
    echo "  • insufficient repository permissions"
    echo "  • corrupted virtual environment"
    echo "  • missing dependencies"
    echo

    exit 1
fi

echo -e "${GREEN}[+] WLX installed successfully.${RESET}"


# Create Symlink
ln -sf "$WLX_VENV/bin/wlx" "$LOCAL_BIN/wlx"

echo -e "${GREEN}[+] WLX command linked globally.${RESET}"


# PATH Setup
LOCAL_BIN_EXPORT='export PATH="$HOME/.local/bin:$PATH"'

if ! grep -q "$LOCAL_BIN_EXPORT" "$SHELL_RC"; then

    echo
    echo -e "${YELLOW}[?] Add ~/.local/bin to PATH? [Y/n]${RESET}"
    read -r ADD_PATH

    if [[ "$ADD_PATH" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then

        echo "$LOCAL_BIN_EXPORT" >> "$SHELL_RC"

        echo -e "${GREEN}[+] PATH updated successfully.${RESET}"

    else
        echo -e "${YELLOW}[-] Skipping PATH setup.${RESET}"
    fi
fi


# WLX Shell Integration
if ! grep -q "wlxuse()" "$SHELL_RC"; then

    echo
    echo -e "${YELLOW}[?] Enable WLX shell integration (wlxuse)? [Y/n]${RESET}"
    read -r ENABLE_WLXUSE

    if [[ "$ENABLE_WLXUSE" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then

cat << 'EOF' >> "$SHELL_RC"

# >>> WLX START >>>

rm -f ~/.wlx/session.env

wlxuse() {

    export_cmd="$(wlx use "$@")"

    eval "$export_cmd"

    var_name=$(echo "$export_cmd" | cut -d' ' -f2 | cut -d'=' -f1)
    var_value=$(echo "$export_cmd" | cut -d'"' -f2)

    mkdir -p ~/.wlx

    touch ~/.wlx/session.env

    grep -v "^${var_name}=" ~/.wlx/session.env > ~/.wlx/session.tmp || true
    mv ~/.wlx/session.tmp ~/.wlx/session.env

    echo "${var_name}=${var_value}" >> ~/.wlx/session.env
}

# <<< WLX END <<<

EOF

        echo -e "${GREEN}[+] WLX shell integration enabled.${RESET}"

    else
        echo -e "${YELLOW}[-] Skipping shell integration setup.${RESET}"
    fi
fi


# Installation Complete
echo
echo -e "${GREEN}[+] WLX installation completed successfully.${RESET}"

echo
echo -e "${CYAN}[*] Reload your shell:${RESET}"
echo
echo "    exec \$SHELL"

echo
echo -e "${CYAN}[*] Verify installation:${RESET}"
echo
echo "    wlx --help"

echo
echo -e "${GREEN}[+] Welcome to WLX.${RESET}"
echo