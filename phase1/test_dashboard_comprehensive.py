import requests
import json
import time

def test_dashboard_comprehensive():
    base_url = "http://localhost:8000"
    
    print("Comprehensive Dashboard Test")
    print("=" * 60)
    
    # Test 1: Basic connectivity
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✓ Health Check: PASSED")
            print(f"  Status: {health_data.get('status', 'N/A')}")
        else:
            print("✗ Health Check: FAILED")
            return False
    except Exception as e:
        print(f"✗ Health Check: ERROR - {e}")
        return False
    
    # Test 2: Security metrics
    try:
        response = requests.get(f"{base_url}/api/security-metrics", timeout=10)
        if response.status_code == 200:
            metrics = response.json()
            print("✓ Security Metrics: PASSED")
            print(f"  Total Scans: {metrics.get('total_scans', 0)}")
            print(f"  Critical Findings: {metrics.get('critical_findings', 0)}")
        else:
            print("✗ Security Metrics: FAILED")
    except Exception as e:
        print(f"✗ Security Metrics: ERROR - {e}")
    
    # Test 3: Scan results
    try:
        response = requests.get(f"{base_url}/api/scan-results", timeout=10)
        if response.status_code == 200:
            results = response.json()
            scan_count = len(results.get('scans', []))
            print("✓ Scan Results: PASSED")
            print(f"  Available Scans: {scan_count}")
        else:
            print("✗ Scan Results: FAILED")
    except Exception as e:
        print(f"✗ Scan Results: ERROR - {e}")
    
    # Test 4: Main page
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✓ Main Page: PASSED")
            print(f"  Content Type: {response.headers.get('content-type', 'N/A')}")
        else:
            print("✗ Main Page: FAILED")
    except Exception as e:
        print(f"✗ Main Page: ERROR - {e}")
    
    print("=" * 60)
    print("Dashboard test completed.")

if __name__ == "__main__":
    test_dashboard_comprehensive()
