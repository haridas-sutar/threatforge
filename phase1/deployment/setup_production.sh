#!/bin/bash

echo "Setting up ThreatForge for production..."

# Create systemd service
sudo tee /etc/systemd/system/threatforge.service > /dev/null << EOL
[Unit]
Description=ThreatForge Security Scanner
After=network.target

[Service]
Type=exec
User=ec2-user
WorkingDirectory=/home/ec2-user/threatforge/phase1
ExecStart=/usr/bin/python3 -m uvicorn dashboard.app:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

# Create log directory
sudo mkdir -p /var/log/threatforge
sudo chown ec2-user:ec2-user /var/log/threatforge

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable threatforge
sudo systemctl start threatforge

echo "ThreatForge production setup complete"
echo "Status: systemctl status threatforge"
echo "Logs: journalctl -u threatforge -f"
