#!/usr/bin/env bash
# Base wrapper template for launching a native Linux game via Steam or directly.
# Copy to ~/.local/bin/<game>-launcher and edit paths.
set -euo pipefail

PROJECT_DIR="/home/sin/Projects/<REPLACE>"
BINARY="$PROJECT_DIR/build/<REPLACE>"
LOG_DIR="$HOME/.local/share/<REPLACE>/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/launch-$(date +%Y%m%d-%H%M%S).log"

LAUNCH_MODE="${1:-steam}"
LOG_ENABLED=false
for arg in "$@"; do
    [[ "$arg" == "--logs" ]] && LOG_ENABLED=true
done

log() {
    if $LOG_ENABLED; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
    else
        echo "$*"
    fi
}

log "=== <REPLACE> Launcher ==="
log "Mode: $LAUNCH_MODE"

if [[ ! -x "$BINARY" ]]; then
    log "ERROR: Binary not found at $BINARY"
    exit 1
fi

export PROTON_LOG=1
export DXVK_LOG_LEVEL=info
export DXVK_ASYNC=1

if [[ "$LAUNCH_MODE" == "--direct" ]]; then
    log "Launching directly..."
    "$BINARY" "$@" 2>&1 | tee -a "$LOG_FILE"
    log "Game exited."
elif [[ "$LAUNCH_MODE" == "--steam" ]]; then
    log "Launching via Steam..."
    if command -v steamtinkerlaunch >/dev/null 2>&1; then
        steamtinkerlaunch play <REPLACE> 2>&1 | tee -a "$LOG_FILE" || true
    else
        xdg-open "steam://launch/<REPLACE>" >/dev/null 2>&1 || {
            log "ERROR: Could not launch via Steam"
            exit 1
        }
    fi
else
    log "Usage: $0 [--steam|--direct] [--logs]"
    exit 1
fi
