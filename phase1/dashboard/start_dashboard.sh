#!/bin/bash

# Start the ThreatForge dashboard from the correct directory
cd "$(dirname "$0")/.."
echo "Starting ThreatForge Dashboard from: $(pwd)"
echo "Dashboard will be available at: http://0.0.0.0:8000"
echo "Press Ctrl+C to stop the server"

python3 -m uvicorn dashboard.app:app --host 0.0.0.0 --port 8000 --reload
