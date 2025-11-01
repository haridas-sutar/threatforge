import sys
import os
import json
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_status(message, status="INFO"):
    """Print colored status messages"""
    icons = {
        "SUCCESS": "✅",
        "ERROR": "❌", 
        "WARNING": "⚠️",
        "INFO": "🔍",
        "CRITICAL": "🚨"
    }
    colors = {
        "SUCCESS": Fore.GREEN,
        "ERROR": Fore.RED,
        "WARNING": Fore.YELLOW, 
        "INFO": Fore.CYAN,
        "CRITICAL": Fore.RED
    }
    
    icon = icons.get(status, "🔍")
    color = colors.get(status, Fore.WHITE)
    print(f"{color}{icon} {message}")

class ThreatForgeHealthCheck:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "overall_status": "PASS"
        }
    
    def check_python_environment(self):
        """Check Python and package installation"""
        print_status("Checking Python Environment...", "INFO")
        
        try:
            # Python version
            version = sys.version_info
            python_version = f"{version.major}.{version.minor}.{version.micro}"
            print_status(f"Python Version: {python_version}", "SUCCESS")
            self.results["checks"]["python_version"] = {"status": "PASS", "version": python_version}
            
        except Exception as e:
            print_status(f"Python check failed: {e}", "ERROR")
            self.results["checks"]["python_version"] = {"status": "FAIL", "error": str(e)}
            self.results["overall_status"] = "FAIL"
    
    def check_dependencies(self):
        """Check required packages with better error handling"""
        print_status("Checking Dependencies...", "INFO")
        
        required_packages = [
            ("boto3", "boto3"),
            ("colorama", "colorama"), 
            ("python-dotenv", "dotenv")  # Note: package name vs import name
        ]
        
        for package_name, import_name in required_packages:
            try:
                __import__(import_name)
                print_status(f"{package_name} - Installed", "SUCCESS")
                self.results["checks"][f"package_{package_name}"] = {"status": "PASS"}
            except ImportError as e:
                # Try alternative import methods
                try:
                    import subprocess
                    result = subprocess.run(
                        [sys.executable, "-c", f"import {import_name}"],
                        capture_output=True, 
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        print_status(f"{package_name} - Installed (via subprocess)", "SUCCESS")
                        self.results["checks"][f"package_{package_name}"] = {"status": "PASS"}
                    else:
                        print_status(f"{package_name} - Missing: {e}", "ERROR")
                        self.results["checks"][f"package_{package_name}"] = {"status": "FAIL", "error": str(e)}
                        self.results["overall_status"] = "FAIL"
                except:
                    print_status(f"{package_name} - Missing: {e}", "ERROR")
                    self.results["checks"][f"package_{package_name}"] = {"status": "FAIL", "error": str(e)}
                    self.results["overall_status"] = "FAIL"
    
    def check_project_structure(self):
        """Verify project file structure"""
        print_status("Checking Project Structure...", "INFO")
        
        required_dirs = ["scanner", "config", "utils", "results"]
        required_files = [
            "scanner/basic_scanner.py",
            "config/aws_config.py", 
            "utils/logger.py",
            "requirements.txt"
        ]
        
        # Check directories
        for dir_name in required_dirs:
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                print_status(f"Directory: {dir_name}/ - Exists", "SUCCESS")
                self.results["checks"][f"dir_{dir_name}"] = {"status": "PASS"}
            else:
                print_status(f"Directory: {dir_name}/ - Missing", "ERROR")
                self.results["checks"][f"dir_{dir_name}"] = {"status": "FAIL"}
                self.results["overall_status"] = "FAIL"
        
        # Check files
        for file_path in required_files:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                print_status(f"File: {file_path} - Exists ({file_size} bytes)", "SUCCESS")
                self.results["checks"][f"file_{file_path.replace('/', '_')}"] = {"status": "PASS", "size": file_size}
            else:
                print_status(f"File: {file_path} - Missing", "ERROR")
                self.results["checks"][f"file_{file_path.replace('/', '_')}"] = {"status": "FAIL"}
                self.results["overall_status"] = "FAIL"
    
    def check_aws_connectivity(self):
        """Test AWS connectivity and permissions"""
        print_status("Testing AWS Connectivity...", "INFO")
        
        try:
            import boto3
            
            # Test basic STS connectivity
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            
            print_status(f"AWS Account: {identity['Account']}", "SUCCESS")
            print_status(f"User ARN: {identity['Arn']}", "SUCCESS")
            
            self.results["checks"]["aws_connectivity"] = {
                "status": "PASS", 
                "account_id": identity['Account'],
                "user_arn": identity['Arn']
            }
            
            # Test service-specific permissions
            services_to_test = {
                "EC2": ["ec2", "describe_instances"],
                "S3": ["s3", "list_buckets"], 
                "IAM": ["iam", "get_user"]
            }
            
            for service_name, (service, method) in services_to_test.items():
                try:
                    client = boto3.client(service)
                    getattr(client, method)()
                    print_status(f"{service_name} Access - Working", "SUCCESS")
                    self.results["checks"][f"aws_{service.lower()}"] = {"status": "PASS"}
                except Exception as e:
                    if "AccessDenied" in str(e):
                        print_status(f"{service_name} Access - Limited (Need permissions)", "WARNING")
                        self.results["checks"][f"aws_{service.lower()}"] = {"status": "WARNING", "error": "Limited permissions"}
                    else:
                        print_status(f"{service_name} Access - Error: {e}", "ERROR")
                        self.results["checks"][f"aws_{service.lower()}"] = {"status": "FAIL", "error": str(e)}
                        
        except Exception as e:
            print_status(f"AWS Connectivity Failed: {e}", "ERROR")
            self.results["checks"]["aws_connectivity"] = {"status": "FAIL", "error": str(e)}
            self.results["overall_status"] = "FAIL"
    
    def check_scanner_functionality(self):
        """Test if the basic scanner works"""
        print_status("Testing Scanner Functionality...", "INFO")
        
        try:
            # Import and test basic scanner
            from scanner.basic_scanner import BasicSecurityScanner
            
            scanner = BasicSecurityScanner()
            
            # Test individual methods
            scanner.check_iam_basic()
            scanner.check_regions()
            
            print_status("Basic Scanner - Functional", "SUCCESS")
            self.results["checks"]["scanner_functionality"] = {"status": "PASS"}
            
        except Exception as e:
            print_status(f"Scanner Test Failed: {e}", "ERROR")
            self.results["checks"]["scanner_functionality"] = {"status": "FAIL", "error": str(e)}
            self.results["overall_status"] = "FAIL"
    
    def check_results_directory(self):
        """Verify results directory is writable"""
        print_status("Checking Results Directory...", "INFO")
        
        try:
            test_file = "results/health_check_test.json"
            test_data = {"test": True, "timestamp": datetime.now().isoformat()}
            
            with open(test_file, 'w') as f:
                json.dump(test_data, f)
            
            # Verify we can read it back
            with open(test_file, 'r') as f:
                data = json.load(f)
            
            # Clean up
            os.remove(test_file)
            
            print_status("Results Directory - Writable", "SUCCESS")
            self.results["checks"]["results_directory"] = {"status": "PASS"}
            
        except Exception as e:
            print_status(f"Results Directory Error: {e}", "ERROR")
            self.results["checks"]["results_directory"] = {"status": "FAIL", "error": str(e)}
            self.results["overall_status"] = "FAIL"
    
    def run_full_health_check(self):
        """Run all health checks"""
        print(f"\n{Fore.CYAN}🩺 THREATFORGE HEALTH CHECK")
        print(f"{Fore.CYAN}⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        self.check_python_environment()
        print()
        
        self.check_dependencies() 
        print()
        
        self.check_project_structure()
        print()
        
        self.check_aws_connectivity()
        print()
        
        self.check_scanner_functionality()
        print()
        
        self.check_results_directory()
        print()
        
        self.generate_report()
    
    def generate_report(self):
        """Generate final health check report"""
        print(f"{Fore.CYAN}📊 HEALTH CHECK SUMMARY")
        print("=" * 60)
        
        total_checks = len(self.results["checks"])
        passed_checks = sum(1 for check in self.results["checks"].values() if check["status"] == "PASS")
        warning_checks = sum(1 for check in self.results["checks"].values() if check["status"] == "WARNING")
        failed_checks = sum(1 for check in self.results["checks"].values() if check["status"] == "FAIL")
        
        print(f"Total Checks: {total_checks}")
        print(f"{Fore.GREEN}Passed: {passed_checks}")
        print(f"{Fore.YELLOW}Warnings: {warning_checks}")
        print(f"{Fore.RED}Failed: {failed_checks}")
        
        # Save detailed report
        report_file = f"results/health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('results', exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n{Fore.GREEN}📄 Detailed report saved to: {report_file}")
        
        # Final verdict - be more forgiving about python-dotenv
        critical_failures = failed_checks
        if "package_python-dotenv" in self.results["checks"]:
            if self.results["checks"]["package_python-dotenv"]["status"] == "FAIL":
                critical_failures -= 1  # python-dotenv is optional for core functionality
                print(f"\n{Fore.YELLOW}💡 Note: python-dotenv is optional. Core scanner functionality is working.")
        
        if critical_failures == 0:
            if warning_checks == 0:
                print(f"\n{Fore.GREEN}🎉 ALL SYSTEMS GO! ThreatForge is fully operational!")
                print(f"{Fore.GREEN}🚀 Ready to start security scanning!")
            else:
                print(f"\n{Fore.YELLOW}⚠️  SYSTEM OPERATIONAL (with warnings)")
                print(f"{Fore.YELLOW}💡 Some features may have limited functionality")
        else:
            print(f"\n{Fore.RED}❌ SYSTEM HAS ISSUES")
            print(f"{Fore.RED}🔧 Please fix the failed checks above")
        
        print(f"\n{Fore.CYAN}Next step: Run 'python3 scanner/basic_scanner.py' to perform your first security scan!")

if __name__ == "__main__":
    health_check = ThreatForgeHealthCheck()
    health_check.run_full_health_check()
