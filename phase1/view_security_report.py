import json
from colorama import Fore, Style, init

init(autoreset=True)

def display_security_report():
    try:
        with open('results/security_report.json', 'r') as f:
            report = json.load(f)
        
        print(f"{Fore.CYAN}ThreatForge Security Report")
        print("=" * 60)
        
        # Executive Summary
        summary = report.get('executive_summary', {})
        print(f"{Fore.WHITE}Executive Summary:")
        print(f"  Total Findings: {summary.get('total_findings', 0)}")
        print(f"{Fore.RED}  Critical: {summary.get('critical_findings', 0)}")
        print(f"{Fore.YELLOW}  High: {summary.get('high_findings', 0)}")
        print(f"{Fore.BLUE}  Medium: {summary.get('medium_findings', 0)}")
        print(f"  Overall Risk: {summary.get('overall_risk', 'Unknown')}")
        
        # Critical Findings
        critical = report.get('critical_findings', {})
        if critical:
            print(f"\n{Fore.RED}Critical Findings:")
            for service, findings in critical.items():
                print(f"  {service}:")
                for finding in findings[:3]:  # Show first 3 per service
                    print(f"    - {finding['title']}")
                    print(f"      Resource: {finding['resource']}")
        
        # Recommendations
        recommendations = report.get('recommendations', [])
        if recommendations:
            print(f"\n{Fore.GREEN}Top Recommendations:")
            for rec in recommendations[:5]:  # Show top 5
                print(f"  [{rec['priority']}] {rec['action']}")
                print(f"     {rec['description']}")
        
        # Risk Assessment
        risk = report.get('risk_assessment', {})
        print(f"\n{Fore.WHITE}Risk Assessment:")
        print(f"  Risk Score: {risk.get('risk_score', 0)}/100")
        print(f"  Risk Level: {risk.get('risk_level', 'Unknown')}")
        print(f"  Compliance: {risk.get('compliance_status', 'Unknown')}")
        
        print("\n" + "=" * 60)
        print(f"Full report: results/security_report.json")
        print(f"HTML report: results/security_report.html")
        
    except FileNotFoundError:
        print(f"{Fore.RED}Security report not found. Run a scan first.")
    except Exception as e:
        print(f"{Fore.RED}Error reading report: {e}")

if __name__ == "__main__":
    display_security_report()
