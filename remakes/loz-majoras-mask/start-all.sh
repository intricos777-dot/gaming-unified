#!/usr/bin/env bash
set -euo pipefail

echo "╔══════════════════════════════════════════════════╗"
echo "║           Starting All Services                  ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

BASE=/home/sin/Projects

check_port() {
  local port=$1 name=$2
  if ss -tlnp | grep -q ":$port "; then
    echo "  ✓ $name (port $port)"
  else
    echo "  ✗ $name (port $port) — not responding"
  fi
}

# ── Python services ────────────────────────────────────────
start_py() {
  local name=$1 module=$2 port=$3 dir=$4
  if ss -tlnp | grep -q ":$port "; then
    echo "  • $name already running on $port"
    return
  fi
  cd "$BASE/$dir"
  nohup /home/sin/.local/bin/uvicorn "$module" --host 127.0.0.1 --port "$port" \
    > "/tmp/$name.log" 2>&1 &
  echo "  • $name PID: $!  log: /tmp/$name.log"
  sleep 1
}

start_py beverage-company      src.beverage_service:app   5310 beverage-company
start_py japanese-imports-llc   src.imports_service:app    5311 japanese-imports-llc
start_py sen-isp-business       backend.app.main:app       5320 sen-isp-business
start_py local-emergency-patrol backend.app.main:app       5330 local-emergency-patrol
start_py space-edge-network     backend.app.standalone_health:app 5340 space-edge-network
start_py polsia-cli             backend.app.main:app       5350 polsia-cli
start_py quantum-loop           backend.app.main:app       5360 quantum-loop
start_py profit-widget          service:app                5370 profit-widget

# ── Node / JS services ─────────────────────────────────────
start_node() {
  local name=$1 script=$2 port=$3 dir=$4
  if ss -tlnp | grep -q ":$port "; then
    echo "  • $name already running on $port"
    return
  fi
  cd "$BASE/$dir"
  nohup /usr/bin/env node "$script" \
    > "/tmp/$name.log" 2>&1 &
  echo "  • $name PID: $!  log: /tmp/$name.log"
  sleep 1
}

start_node lia-groq-bridge      src/health.js             4125 lia-groq-bridge

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║           Status Check                           ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
sleep 2
check_port 5310 "Beverage Company"
check_port 5311 "Japanese Imports"
check_port 5320 "SEN ISP"
check_port 5330 "Local Emergency Patrol"
check_port 5340 "Space Edge Network"
check_port 5350 "Polsia CLI"
check_port 5360 "Quantum Loop"
check_port 5370 "Profit Widget"
check_port 4125 "Lia Groq Bridge"

echo ""
echo "All services started. Use 'ss -tlnp' to verify ports."