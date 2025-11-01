import smtplib
import json
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import logging
from pathlib import Path

class AlertNotifier:
    def __init__(self, config_file="config/alerts.json"):
        self.config_file = Path(config_file)
        self.load_config()
    
    def load_config(self):
        """Load alert configuration"""
        default_config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipients": []
            },
            "critical_severity_threshold": 1
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
    
    def check_critical_findings(self, scan_file):
        """Check if scan contains critical findings"""
        try:
            with open(scan_file, 'r') as f:
                scan_data = json.load(f)
            
            critical_count = 0
            for finding in scan_data.get('findings', []):
                if finding['severity'] == 'CRITICAL':
                    critical_count += 1
            
            return critical_count >= self.config['critical_severity_threshold']
            
        except Exception as e:
            logging.error(f"Error checking critical findings: {e}")
            return False
    
    def send_email_alert(self, scan_file, critical_count):
        """Send email alert for critical findings"""
        if not self.config['email']['enabled']:
            return
        
        try:
            with open(scan_file, 'r') as f:
                scan_data = json.load(f)
            
            subject = f"ThreatForge Alert: {critical_count} Critical Security Issues Found"
            
            body = f"""
Critical security issues detected in your AWS environment.

Scan Time: {scan_data.get('scan_time')}
Total Critical Issues: {critical_count}

Immediate attention required for:
"""
            
            for finding in scan_data.get('findings', []):
                if finding['severity'] == 'CRITICAL':
                    body += f"\n- {finding['title']} ({finding['resource']})"
            
            body += f"\n\nView full report: http://localhost:8000"
            
            self._send_email(subject, body)
            logging.info(f"Email alert sent for {critical_count} critical issues")
            
        except Exception as e:
            logging.error(f"Error sending email alert: {e}")
    
    def _send_email(self, subject, body):
        """Send email using SMTP"""
        msg = MimeMultipart()
        msg['From'] = self.config['email']['sender_email']
        msg['To'] = ", ".join(self.config['email']['recipients'])
        msg['Subject'] = subject
        
        msg.attach(MimeText(body, 'plain'))
        
        server = smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port'])
        server.starttls()
        server.login(self.config['email']['sender_email'], self.config['email']['sender_password'])
        server.send_message(msg)
        server.quit()
    
    def process_scan_alerts(self, scan_file):
        """Process alerts for a new scan"""
        if self.check_critical_findings(scan_file):
            with open(scan_file, 'r') as f:
                scan_data = json.load(f)
            
            critical_count = len([f for f in scan_data.get('findings', []) if f['severity'] == 'CRITICAL'])
            
            if self.config['email']['enabled']:
                self.send_email_alert(scan_file, critical_count)

if __name__ == "__main__":
    notifier = AlertNotifier()
    latest_scan = max(Path("results").glob("*scan*.json"), key=lambda x: x.stat().st_mtime)
    notifier.process_scan_alerts(latest_scan)
