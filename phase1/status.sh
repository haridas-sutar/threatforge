#!/bin/bash

echo "ThreatForge System Status"
echo "========================="

# Dashboard status
echo "Dashboard:"
./manage_dashboard.sh status | grep -v "Recent log"

# Security findings
echo -e "\nSecurity Findings:"
if [ -f "results/security_report.json" ]; then
    python3 -c "
import json
try:
    with open('results/security_report.json') as f:
        data = json.load(f)
    summary = data.get('executive_summary', {})
    print(f'  Total Findings: {summary.get(\"total_findings\", 0)}')
    print(f'  Critical: {summary.get(\"critical_findings\", 0)}')
    print(f'  High: {summary.get(\"high_findings\", 0)}')
    print(f'  Medium: {summary.get(\"medium_findings\", 0)}')
except:
    print('  No security report found')
"
else
    echo "  No security report found"
fi

# Recent scans
echo -e "\nRecent Scans:"
ls -lt results/*.json 2>/dev/null | head -3 | awk '{print "  " $6 " " $7 " " $8 " " $9}' || echo "  No scans found"

echo -e "\nAccess: http://localhost:8000"
