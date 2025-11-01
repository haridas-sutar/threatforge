#!/bin/bash

echo "ThreatForge Dashboard Access Information"
echo "========================================"

# Get private IP
PRIVATE_IP=$(hostname -I | awk '{print $1}')
echo "Private IP Access: http://${PRIVATE_IP}:8000"
echo "Local Access:      http://localhost:8000"

# Try to get public IP
PUBLIC_IP=$(curl -s --connect-timeout 2 http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "Not available")
if [ "$PUBLIC_IP" != "Not available" ] && [ -n "$PUBLIC_IP" ]; then
    echo "Public IP Access:  http://${PUBLIC_IP}:8000"
else
    echo "Public IP:         Not assigned or not accessible"
fi

echo ""
echo "To enable public access:"
echo "1. Go to AWS EC2 Console → Security Groups"
echo "2. Find your instance's security group"
echo "3. Add Inbound Rule: Custom TCP, Port 8000, Source 0.0.0.0/0"
echo ""
echo "Current dashboard status:"
./manage_dashboard.sh status
