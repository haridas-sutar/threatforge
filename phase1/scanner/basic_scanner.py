
import boto3
import json
from datetime import datetime
import os
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

class BasicSecurityScanner:
    def __init__(self):
        self.findings = []
        self.session = boto3.Session()
        self.scan_time = datetime.utcnow().isoformat()
        
    def check_ec2_instances(self):
        """Check EC2 instances for basic information"""
        print(f"{Fore.CYAN}🔍 Scanning EC2 instances...")
        
        try:
            ec2 = self.session.client('ec2')
            response = ec2.describe_instances()
            
            instance_count = 0
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_count += 1
                    instance_id = instance['InstanceId']
                    state = instance['State']['Name']
                    
                    # Basic instance info
                    print(f"   Instance: {instance_id} - State: {state}")
                    
                    # Check if instance is running
                    if state == 'running':
                        self.findings.append({
                            'severity': 'INFO',
                            'service': 'EC2',
                            'resource': instance_id,
                            'title': 'Running EC2 Instance',
                            'description': f'EC2 instance {instance_id} is running',
                            'recommendation': 'Monitor for unnecessary running instances to save costs',
                            'timestamp': self.scan_time
                        })
            
            print(f"   Found {instance_count} EC2 instances")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error scanning EC2: {e}")
    
    def check_regions(self):
        """Check available AWS regions"""
        print(f"{Fore.CYAN}🌍 Checking available regions...")
        
        try:
            ec2 = self.session.client('ec2')
            regions = ec2.describe_regions()
            
            region_names = [region['RegionName'] for region in regions['Regions']]
            print(f"   Available in {len(region_names)} regions")
            print(f"   Regions: {', '.join(region_names[:5])}..." if len(region_names) > 5 else f"   Regions: {', '.join(region_names)}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error checking regions: {e}")
    
    def check_iam_basic(self):
        """Basic IAM checks"""
        print(f"{Fore.CYAN}👤 Checking IAM basic info...")
        
        try:
            sts = self.session.client('sts')
            identity = sts.get_caller_identity()
            
            print(f"   Account ID: {identity['Account']}")
            print(f"   User ARN: {identity['Arn']}")
            
            # Store account info
            self.findings.append({
                'severity': 'INFO',
                'service': 'IAM',
                'resource': identity['Account'],
                'title': 'AWS Account Information',
                'description': f'Scanning account {identity["Account"]} as {identity["Arn"]}',
                'recommendation': 'Regular security scanning helps maintain cloud security',
                'timestamp': self.scan_time
            })
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error checking IAM: {e}")
    
    def run_scan(self):
        """Run all available security checks"""
        print(f"{Fore.GREEN}🚀 Starting Basic AWS Security Scan...")
        print(f"{Fore.GREEN}⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.YELLOW}📝 Note: Some checks may show limited access - this is normal")
        print("-" * 60)
        
        # Run available checks
        self.check_iam_basic()
        self.check_regions()
        self.check_ec2_instances()
        
        # Save results
        self.save_findings()
        
        # Show summary
        self.show_summary()
    
    def save_findings(self):
        """Save findings to JSON file"""
        try:
            os.makedirs('results', exist_ok=True)
            filename = f"results/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    'scan_time': self.scan_time,
                    'findings': self.findings,
                    'total_findings': len(self.findings)
                }, f, indent=2)
            
            print(f"{Fore.GREEN}💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving results: {e}")
    
    def show_summary(self):
        """Display scan summary"""
        print("\n" + "=" * 60)
        print(f"{Fore.GREEN}📊 SCAN SUMMARY")
        print("=" * 60)
        
        # Count findings by severity
        severity_count = {}
        for finding in self.findings:
            severity = finding['severity']
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        # Print counts with colors
        colors = {
            'CRITICAL': Fore.RED,
            'HIGH': Fore.RED, 
            'MEDIUM': Fore.YELLOW,
            'LOW': Fore.BLUE,
            'INFO': Fore.CYAN
        }
        
        for severity, count in severity_count.items():
            color = colors.get(severity, Fore.WHITE)
            print(f"{color}{severity}: {count}")
        
        total = len(self.findings)
        print(f"{Fore.CYAN}TOTAL FINDINGS: {total}")
        
        if total == 0:
            print(f"{Fore.GREEN}🎉 No security issues found in basic scan!")
        else:
            print(f"{Fore.YELLOW}⚠️  Review findings in results/ directory")
        
        print(f"\n{Fore.YELLOW}💡 Next: Add S3 permissions to scan for public buckets")

if __name__ == "__main__":
    scanner = BasicSecurityScanner()
    scanner.run_scan()

