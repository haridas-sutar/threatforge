import json
import os
from datetime import datetime
from pathlib import Path

class SecurityReporter:
    def __init__(self, results_dir="results"):
        self.results_dir = Path(results_dir)
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive security report"""
        scan_files = list(self.results_dir.glob("*scan*.json"))
        scan_files.sort(key=os.path.getmtime, reverse=True)
        
        if not scan_files:
            return {"error": "No scan results found"}
        
        latest_scan = scan_files[0]
        with open(latest_scan, 'r') as f:
            scan_data = json.load(f)
        
        report = {
            "report_generated": datetime.utcnow().isoformat(),
            "scan_file": latest_scan.name,
            "scan_time": scan_data.get('scan_time'),
            "executive_summary": self._generate_executive_summary(scan_data),
            "critical_findings": self._categorize_findings(scan_data, 'CRITICAL'),
            "high_findings": self._categorize_findings(scan_data, 'HIGH'),
            "medium_findings": self._categorize_findings(scan_data, 'MEDIUM'),
            "recommendations": self._generate_recommendations(scan_data),
            "risk_assessment": self._calculate_risk_assessment(scan_data)
        }
        
        return report
    
    def _generate_executive_summary(self, scan_data):
        findings = scan_data.get('findings', [])
        critical_count = len([f for f in findings if f['severity'] == 'CRITICAL'])
        high_count = len([f for f in findings if f['severity'] == 'HIGH'])
        medium_count = len([f for f in findings if f['severity'] == 'MEDIUM'])
        
        return {
            "total_findings": len(findings),
            "critical_findings": critical_count,
            "high_findings": high_count,
            "medium_findings": medium_count,
            "overall_risk": "CRITICAL" if critical_count > 0 else "HIGH" if high_count > 0 else "MEDIUM",
            "summary": f"Found {critical_count} critical, {high_count} high, and {medium_count} medium security issues requiring attention."
        }
    
    def _categorize_findings(self, scan_data, severity):
        findings = [f for f in scan_data.get('findings', []) if f['severity'] == severity]
        categorized = {}
        
        for finding in findings:
            service = finding['service']
            if service not in categorized:
                categorized[service] = []
            categorized[service].append({
                "title": finding['title'],
                "resource": finding['resource'],
                "description": finding['description'],
                "recommendation": finding['recommendation']
            })
        
        return categorized
    
    def _generate_recommendations(self, scan_data):
        findings = scan_data.get('findings', [])
        recommendations = []
        
        # Prioritize by severity
        critical_findings = [f for f in findings if f['severity'] == 'CRITICAL']
        high_findings = [f for f in findings if f['severity'] == 'HIGH']
        
        # Critical recommendations
        for finding in critical_findings:
            if "SSH" in finding['title'] or "RDP" in finding['title']:
                recommendations.append({
                    "priority": "IMMEDIATE",
                    "action": "Restrict SSH/RDP access",
                    "description": f"Close {finding['title']} in security group {finding['resource']}",
                    "impact": "Prevents unauthorized remote access"
                })
        
        # High recommendations
        for finding in high_findings:
            if "IAM" in finding['title']:
                recommendations.append({
                    "priority": "HIGH",
                    "action": "Configure IAM password policy",
                    "description": "Set strong password requirements for IAM users",
                    "impact": "Improves account security"
                })
        
        # Medium recommendations
        medium_findings = [f for f in findings if f['severity'] == 'MEDIUM']
        for finding in medium_findings:
            if "EBS" in finding['title']:
                recommendations.append({
                    "priority": "MEDIUM",
                    "action": "Enable EBS encryption",
                    "description": f"Encrypt EBS volume {finding['resource']}",
                    "impact": "Protects data at rest"
                })
        
        return recommendations
    
    def _calculate_risk_assessment(self, scan_data):
        findings = scan_data.get('findings', [])
        risk_score = 0
        
        for finding in findings:
            if finding['severity'] == 'CRITICAL':
                risk_score += 10
            elif finding['severity'] == 'HIGH':
                risk_score += 7
            elif finding['severity'] == 'MEDIUM':
                risk_score += 4
        
        return {
            "risk_score": min(100, risk_score),
            "risk_level": "CRITICAL" if risk_score >= 50 else "HIGH" if risk_score >= 30 else "MEDIUM",
            "compliance_status": "NON-COMPLIANT" if risk_score >= 30 else "PARTIALLY_COMPLIANT"
        }

def generate_html_report(report_data, output_file="security_report.html"):
    """Generate an HTML security report"""
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ThreatForge Security Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
            .critical {{ color: #e74c3c; font-weight: bold; }}
            .high {{ color: #e67e22; }}
            .medium {{ color: #f39c12; }}
            .finding {{ border-left: 4px solid; padding: 10px; margin: 10px 0; background: #f8f9fa; }}
            .recommendation {{ background: #e8f4fd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>ThreatForge Security Assessment Report</h1>
            <p>Generated: {report_data['report_generated']}</p>
        </div>
        
        <h2>Executive Summary</h2>
        <p>Total Findings: {report_data['executive_summary']['total_findings']}</p>
        <p class="critical">Critical: {report_data['executive_summary']['critical_findings']}</p>
        <p class="high">High: {report_data['executive_summary']['high_findings']}</p>
        <p class="medium">Medium: {report_data['executive_summary']['medium_findings']}</p>
        
        <h2>Critical Findings</h2>
        {_generate_findings_html(report_data['critical_findings'])}
        
        <h2>Recommendations</h2>
        {_generate_recommendations_html(report_data['recommendations'])}
        
        <h2>Risk Assessment</h2>
        <p>Risk Score: {report_data['risk_assessment']['risk_score']}/100</p>
        <p>Risk Level: {report_data['risk_assessment']['risk_level']}</p>
        <p>Compliance Status: {report_data['risk_assessment']['compliance_status']}</p>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html_template)

def _generate_findings_html(findings_dict):
    html = ""
    for service, findings in findings_dict.items():
        html += f"<h3>{service}</h3>"
        for finding in findings:
            html += f"""
            <div class="finding">
                <strong>{finding['title']}</strong>
                <p>Resource: {finding['resource']}</p>
                <p>{finding['description']}</p>
                <p><em>Recommendation: {finding['recommendation']}</em></p>
            </div>
            """
    return html

def _generate_recommendations_html(recommendations):
    html = ""
    for rec in recommendations:
        html += f"""
        <div class="recommendation">
            <strong>{rec['priority']} Priority: {rec['action']}</strong>
            <p>{rec['description']}</p>
            <p>Impact: {rec['impact']}</p>
        </div>
        """
    return html

if __name__ == "__main__":
    reporter = SecurityReporter()
    report = reporter.generate_comprehensive_report()
    
    # Save JSON report
    with open("results/security_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Generate HTML report
    generate_html_report(report, "results/security_report.html")
    
    print("Security reports generated:")
    print("- results/security_report.json")
    print("- results/security_report.html")
