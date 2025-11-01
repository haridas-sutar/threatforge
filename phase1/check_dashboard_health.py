import requests
import json
import sys

def check_dashboard_health():
    base_url = "http://localhost:8000"
    
    print("Dashboard Health Check")
    print("=" * 50)
    
    # Test basic connectivity
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✓ Dashboard Status: {health_data.get('status', 'UNKNOWN')}")
            print(f"✓ Version: {health_data.get('version', 'N/A')}")
        else:
            print(f"✗ Dashboard Health: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Dashboard Health: {e}")
        return False
    
    # Test security metrics
    try:
        response = requests.get(f"{base_url}/api/security-metrics", timeout=5)
        if response.status_code == 200:
            metrics = response.json()
            print(f"✓ Security Metrics: {metrics.get('total_scans', 0)} scans, {metrics.get('critical_findings', 0)} critical")
        else:
            print(f"✗ Security Metrics: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ Security Metrics: {e}")
    
    # Test security report
    try:
        response = requests.get(f"{base_url}/api/security-report", timeout=10)
        if response.status_code == 200:
            report = response.json()
            if 'error' not in report:
                summary = report.get('executive_summary', {})
                print(f"✓ Security Report: {summary.get('total_findings', 0)} total findings")
            else:
                print(f"✗ Security Report: {report.get('error')}")
        else:
            print(f"✗ Security Report: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ Security Report: {e}")
    
    # Test fix recommendations
    try:
        response = requests.get(f"{base_url}/api/fix-recommendations", timeout=5)
        if response.status_code == 200:
            fixes = response.json()
            print(f"✓ Fix Recommendations: {fixes.get('total_recommendations', 0)} available")
        else:
            print(f"✗ Fix Recommendations: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ Fix Recommendations: {e}")
    
    print("=" * 50)
    print("Health check completed.")
    return True

if __name__ == "__main__":
    success = check_dashboard_health()
    sys.exit(0 if success else 1)
