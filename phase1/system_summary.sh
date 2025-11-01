#!/bin/bash

echo "==============================================="
echo "          THREATFORGE SYSTEM SUMMARY"
echo "==============================================="

# Dashboard info
echo "DASHBOARD:"
./manage_dashboard.sh status | head -3

# Security status
echo -e "\nSECURITY STATUS:"
if curl -s http://localhost:8000/api/security-metrics > /dev/null 2>&1; then
    curl -s http://localhost:8000/api/security-metrics | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'  Scans: {data.get(\"total_scans\", 0)}')
print(f'  Critical Issues: {data.get(\"critical_findings\", 0)}')
print(f'  Risk Score: {data.get(\"overall_risk_score\", 0)}/100')
"
else
    echo "  Unable to fetch security metrics"
fi

# Recent activity
echo -e "\nRECENT ACTIVITY:"
ls -lt results/*.json 2>/dev/null | head -3 | awk '{print "  " $6 " " $7 " " $8 " - " $9}' || echo "  No recent activity"

# Access information
echo -e "\nACCESS:"
echo "  Local:  http://localhost:8000"
echo "  Network: http://$(hostname -I | awk '{print $1}'):8000"

# Quick actions
echo -e "\nQUICK ACTIONS:"
echo "  Run scan:    curl -X POST http://localhost:8000/api/run-scan"
echo "  View report: python3 view_security_report.py"
echo "  Dashboard:   ./manage_dashboard.sh status"

echo "==============================================="
