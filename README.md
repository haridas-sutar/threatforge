

```markdown
# ThreatForge

A comprehensive cloud security platform for AWS that provides automated security scanning, real-time monitoring, and compliance reporting. ThreatForge helps organizations identify and remediate security risks in their cloud infrastructure.

## Features

- **Multi-Region Security Scanning** - Automated scanning across all AWS regions
- **Real-time Dashboard** - FastAPI-based web interface with live metrics
- **Automated Scheduling** - Daily scans and weekly compliance reports
- **Alert System** - Email notifications for critical security findings
- **Comprehensive Reporting** - Technical and executive-level security reports
- **REST API** - Full API for integration and automation
- **Production Ready** - Systemd service and deployment scripts

## Security Checks

- **S3 Buckets** - Public access and bucket policies
- **EC2 Instances** - Security groups, open ports, encryption
- **IAM Policies** - Password policies, user permissions
- **RDS Databases** - Public accessibility, encryption
- **EBS Volumes** - Encryption status
- **Network Security** - VPC configurations, NACLs

## Quick Start

### Prerequisites
- AWS account with appropriate IAM permissions
- Python 3.9+
- AWS CLI configured

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/haridas-sutar/threatforge.git
cd threatforge/phase1

# Install dependencies
pip3 install -r requirements.txt

# Start the dashboard
./manage_dashboard.sh start
```

### Basic Usage

1. **Access Dashboard**: http://localhost:8000
2. **Run Security Scan**:
   ```bash
   curl -X POST http://localhost:8000/api/run-scan
   ```
3. **View Security Report**:
   ```bash
   python3 view_security_report.py
   ```

## Architecture

```
threatforge/
├── phase1/
│   ├── scanner/              # Security scanning modules
│   │   ├── basic_scanner.py          # Basic AWS checks
│   │   ├── enhanced_scanner.py       # Comprehensive security checks
│   │   └── production_scanner.py     # Multi-region scanning
│   ├── dashboard/            # Web interface
│   │   ├── app.py                   # FastAPI backend
│   │   ├── templates/               # HTML templates
│   │   └── static/                  # CSS/JS assets
│   ├── automation/           # Scheduled tasks
│   │   └── scheduler.py             # Automated scanning
│   ├── alerts/               # Notification system
│   │   └── notifier.py              # Email alerts
│   ├── deployment/           # Production setup
│   │   └── setup_production.sh      # Systemd service
│   ├── config/               # Configuration
│   │   ├── production.json          # Production settings
│   │   └── alerts.json              # Alert configuration
│   ├── utils/                # Helper functions
│   │   ├── security_reporter.py     # Report generation
│   │   └── logger.py                # Logging utilities
│   └── results/              # Scan results (gitignored)
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Service health check |
| `/api/security-metrics` | GET | Overall security metrics |
| `/api/scan-results` | GET | Latest scan results |
| `/api/run-scan` | POST | Execute security scan |
| `/api/security-report` | GET | Comprehensive security report |
| `/api/fix-recommendations` | GET | Remediation steps |
| `/ws/scan-updates` | WebSocket | Real-time scan updates |

### Example API Usage

```bash
# Get security metrics
curl http://localhost:8000/api/security-metrics

# Run security scan
curl -X POST http://localhost:8000/api/run-scan

# Generate security report
curl http://localhost:8000/api/security-report
```

## Production Deployment

### Systemd Service Setup

```bash
cd deployment
./setup_production.sh
```

### Manual Service Management

```bash
# Start service
systemctl start threatforge

# Check status
systemctl status threatforge

# View logs
journalctl -u threatforge -f
```

### Configuration

Edit `config/production.json`:

```json
{
    "scanning": {
        "daily_scan_time": "02:00",
        "regions": ["us-east-1", "us-west-2"],
        "max_resources_per_scan": 1000
    },
    "alerts": {
        "email_enabled": false,
        "critical_threshold": 1,
        "recipients": ["security-team@company.com"]
    }
}
```

## Dashboard Features

- **Real-time Security Metrics** - Live risk scoring and findings
- **Interactive Scan Results** - Detailed vulnerability information
- **Historical Trends** - Security posture over time
- **Risk Prioritization** - Critical issues highlighted
- **Exportable Reports** - PDF and JSON report generation

## Security Findings Examples

ThreatForge identifies critical security issues like:

- **Public S3 buckets** exposing sensitive data
- **SSH/RDP open to internet** allowing unauthorized access
- **Unencrypted EBS volumes** risking data exposure
- **Weak IAM password policies** compromising account security
- **Public RDS instances** exposing databases

## Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is designed for educational and authorized security assessment purposes only. Always ensure you have proper authorization before scanning any AWS environment. The developers are not responsible for any misuse or damage caused by this tool.

## Reporting Issues

If you find any bugs or have feature requests, please open an issue on GitHub with:
- Detailed description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

## Show Your Support

If you find this project useful, please give it a star on GitHub!

---

**Built with love for the cloud security community**

*Helping organizations secure their cloud infrastructure, one scan at a time.*
```

## Key Highlights of This README:

1. **Professional Structure** - Clear sections without emojis
2. **Comprehensive Documentation** - Covers all features and usage
3. **API Documentation** - Clear endpoint descriptions with examples
4. **Architecture Overview** - Visual project structure
5. **Production Ready** - Deployment and configuration guidance
6. **Security Focused** - Emphasizes the security value proposition
7. **Community Friendly** - Contributing guidelines and support information

## To Add This README to Your Repository:

```bash
# Navigate to your project
cd /home/ec2-user/threatforge

# Create the README.md file
cat > README.md << 'EOF'
[PASTE THE ENTIRE README CONTENT ABOVE HERE]
EOF

# Add and commit the README
git add README.md
git commit -m "docs: Add comprehensive README with usage instructions"

# Push to GitHub
git push origin main
```

