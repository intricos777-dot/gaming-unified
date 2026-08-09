#!/bin/bash
# Law Library + Himalaya Integration Start Script

cd /home/sin/Projects/law-library

# Activate virtual environment
source venv/bin/activate

# Start API server in background
echo "[*] Starting Law Library API server on port 4130..."
python api_server.py &
API_PID=$!
sleep 2

# Verify server is running
if curl -s http://localhost:4130/health > /dev/null 2>&1; then
    echo "[+] API server running (PID: $API_PID)"
else
    echo "[-] API server failed to start"
    exit 1
fi

# Run legal scanner
echo "[*] Running legal scanner..."
python legal_scanner.py

# Keep API running if requested
if [ "$1" = "--keep" ]; then
    echo "[*] API server running in background. Press Ctrl+C to stop."
    wait $API_PID
else
    echo "[*] Scanner complete. Stopping API server..."
    kill $API_PID 2>/dev/null
fi
