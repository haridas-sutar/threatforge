import requests
import json

def test_all_endpoints():
    base_url = "http://localhost:8000"
    
    endpoints = [
        ("GET", "/api/health"),
        ("GET", "/api/security-metrics"),
        ("GET", "/api/scan-results"), 
        ("GET", "/api/security-report"),
        ("GET", "/api/fix-recommendations"),
    ]
    
    print("Testing All API Endpoints")
    print("=" * 50)
    
    for method, endpoint in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            elif method == "POST":
                response = requests.post(f"{base_url}{endpoint}", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ {method} {endpoint} - SUCCESS")
                if endpoint == "/api/security-metrics":
                    print(f"  Scans: {data.get('total_scans', 0)}, Critical: {data.get('critical_findings', 0)}")
                elif endpoint == "/api/security-report":
                    summary = data.get('executive_summary', {})
                    print(f"  Findings: {summary.get('total_findings', 0)}")
                elif endpoint == "/api/fix-recommendations":
                    print(f"  Recommendations: {data.get('total_recommendations', 0)}")
            else:
                print(f"✗ {method} {endpoint} - {response.status_code}")
                
        except Exception as e:
            print(f"✗ {method} {endpoint} - ERROR: {e}")
    
    print("=" * 50)
    print("API testing completed.")

if __name__ == "__main__":
    test_all_endpoints()
