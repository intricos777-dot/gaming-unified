#!/usr/bin/env bash
# Sync Law Library to lia-skillbridge
# This script registers the law library as a skill in the lia ecosystem

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LIA_CLI_DIR="/home/sin/Projects/lia-cli"
LIA_BRIDGE_DIR="/home/sin/Projects/lia-groq-bridge"
LAW_LIB_API="http://localhost:4130"
LAW_LIB_DATA="$SCRIPT_DIR/data"

echo "=== Law Library → lia-skillbridge Sync ==="
echo ""

# Check if law library API is running
if curl -s "$LAW_LIB_API/health" > /dev/null 2>&1; then
    echo "✓ Law Library API is running"
else
    echo "⚠ Law Library API not running. Starting..."
    cd "$SCRIPT_DIR"
    source venv/bin/activate
    python api_server.py &
    sleep 2
    if curl -s "$LAW_LIB_API/health" > /dev/null 2>&1; then
        echo "✓ Law Library API started successfully"
    else
        echo "✗ Failed to start Law Library API"
        exit 1
    fi
fi

# Check database stats
echo ""
echo "Database Stats:"
curl -s "$LAW_LIB_API/stats" | python3 -m json.tool 2>/dev/null || echo "  (empty database)"

# Register skill in lia-groq-bridge
echo ""
echo "Registering skill with lia-groq-bridge..."

# Copy skill.json to lia-groq-bridge skills directory
mkdir -p "$LIA_BRIDGE_DIR/skills" 2>/dev/null || true
cp "$SCRIPT_DIR/skill.json" "$LIA_BRIDGE_DIR/skills/law-library.json" 2>/dev/null && \
    echo "✓ Skill registered in lia-groq-bridge" || \
    echo "⚠ Could not copy to lia-groq-bridge (create skills/ dir first)"

# Create a symlink for easy access from lia-cli
if [ -d "$LIA_CLI_DIR/data" ]; then
    ln -sf "$LAW_LIB_DATA" "$LIA_CLI_DIR/data/law-library" 2>/dev/null && \
        echo "✓ Data linked to lia-cli" || \
        echo "⚠ Could not link data directory"
fi

# Add law library to PATH for easy CLI access
echo ""
echo "Setting up CLI alias..."
LAWLIB_BIN="$SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/lawlib.py"
echo "  Add to your shell profile:"
echo "    alias lawlib=\"$LAWLIB_BIN\""
echo ""

# Test the integration
echo "Testing integration..."
RESPONSE=$(curl -s "$LAW_LIB_API/search?q=self+defense&type=all" 2>/dev/null)
if echo "$RESPONSE" | grep -q "total"; then
    TOTAL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('total',0))" 2>/dev/null)
    echo "✓ Search API working ($TOTAL results for 'self defense')"
else
    echo "⚠ Search API returned unexpected response"
fi

echo ""
echo "=== Sync Complete ==="
echo ""
echo "Usage:"
echo "  CLI:    cd $SCRIPT_DIR && source venv/bin/activate && python lawlib.py --help"
echo "  API:    curl http://localhost:4130/search?q=constitutional+law"
echo "  Topics: curl http://localhost:4130/topics"
echo ""
echo "API Endpoints:"
echo "  GET  /health              - Health check"
echo "  GET  /stats               - Database statistics"
echo "  GET  /search?q=QUERY      - Search all databases"
echo "  GET  /cite/CITATION       - Look up by citation"
echo "  GET  /topics              - Browse legal topics"
echo "  GET  /sources             - View data sources"
echo "  GET  /state?code=XX       - State statute links"
echo "  POST /chat                - Natural language search"
echo ""
