import requests
import json
import os
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

def verify_complete_system():
    print(f"{Fore.CYAN}ThreatForge Complete System Verification")
    print("=" * 60)
    
    # Check 1: Dashboard process
    print(f"{Fore.WHITE}1. Dashboard Process:")
    pid_file = Path("dashboard.pid")
    if pid_file.exists():
        pid = pid_file.read_text().strip()
        print(f"   ✓ Dashboard running (PID: {pid})")
    else:
        print(f"   ✗ Dashboard not running")
        return False
    
    # Check 2: API endpoints
    print(f"{Fore.WHITE}2. API Endpoints:")
    base_url = "http://localhost:8000"
    endpoints = [
        "/api/health",
        "/api/security-metrics", 
        "/api/scan-results",
        "/api/security-report",
        "/api/fix-recommendations"
    ]
    
    all_endpoints_ok = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✓ {endpoint}")
            else:
                print(f"   ✗ {endpoint} - HTTP {response.status_code}")
                all_endpoints_ok = False
        except Exception as e:
            print(f"   ✗ {endpoint} - {e}")
            all_endpoints_ok = False
    
    if not all_endpoints_ok:
        return False
    
    # Check 3: Security reports
    print(f"{Fore.WHITE}3. Security Reports:")
    results_dir = Path("results")
    scan_files = list(results_dir.glob("*scan*.json"))
    report_files = list(results_dir.glob("security_report*"))
    
    if scan_files:
        print(f"   ✓ Scan results: {len(scan_files)} files")
        latest_scan = max(scan_files, key=os.path.getmtime)
        print(f"   ✓ Latest scan: {latest_scan.name}")
    else:
        print(f"   ✗ No scan results found")
        return False
    
    if report_files:
        print(f"   ✓ Security reports: {len(report_files)} files")
    else:
        print(f"   ⚠ No security reports (run utils/security_reporter.py)")
    
    # Check 4: Scanner modules
    print(f"{Fore.WHITE}4. Scanner Modules:")
    scanner_dir = Path("scanner")
    scanner_files = list(scanner_dir.glob("*.py"))
    if scanner_files:
        for sf in scanner_files:
            print(f"   ✓ {sf.name}")
    else:
        print(f"   ✗ No scanner modules found")
        return False
    
    # Check 5: Latest scan findings
    print(f"{Fore.WHITE}5. Latest Security Findings:")
    try:
        with open(latest_scan, 'r') as f:
            scan_data = json.load(f)
        findings = scan_data.get('findings', [])
        critical = len([f for f in findings if f['severity'] == 'CRITICAL'])
        high = len([f for f in findings if f['severity'] == 'HIGH'])
        medium = len([f for f in findings if f['severity'] == 'MEDIUM'])
        
        print(f"   ✓ Total findings: {len(findings)}")
        print(f"   ✓ Critical: {critical}, High: {high}, Medium: {medium}")
        
    except Exception as e:
        print(f"   ✗ Error reading scan data: {e}")
        return False
    
    print("=" * 60)
    print(f"{Fore.GREEN}✓ SYSTEM VERIFICATION COMPLETE")
    print(f"{Fore.GREEN}✓ ThreatForge is fully operational")
    return True

if __name__ == "__main__":
    success = verify_complete_system()
    exit(0 if success else 1)
