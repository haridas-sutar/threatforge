import boto3
import json
from datetime import datetime
import os
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

class EnhancedSecurityScanner:
    def __init__(self):
        self.findings = []
        self.session = boto3.Session()
        self.scan_time = datetime.utcnow().isoformat()
        
    def check_s3_public_buckets(self):
        """Check for publicly accessible S3 buckets - CRITICAL SECURITY RISK"""
        print(f"{Fore.CYAN}Scanning S3 buckets for public access...")
        
        try:
            s3 = self.session.client('s3')
            buckets = s3.list_buckets()
            
            public_buckets_found = 0
            
            for bucket in buckets['Buckets']:
                bucket_name = bucket['Name']
                try:
                    # Check bucket ACL for public access
                    acl = s3.get_bucket_acl(Bucket=bucket_name)
                    
                    for grant in acl['Grants']:
                        if 'URI' in grant['Grantee'] and 'AllUsers' in grant['Grantee']['URI']:
                            public_buckets_found += 1
                            self.findings.append({
                                'severity': 'CRITICAL',
                                'service': 'S3',
                                'resource': bucket_name,
                                'title': 'Public S3 Bucket',
                                'description': f'Bucket "{bucket_name}" is publicly accessible to everyone on the internet',
                                'recommendation': 'Immediately apply bucket policy to restrict public access. Enable S3 Block Public Access.',
                                'timestamp': self.scan_time,
                                'risk_score': 10
                            })
                            print(f"{Fore.RED}CRITICAL: Public S3 Bucket: {bucket_name}")
                            
                except Exception as e:
                    # Some buckets might not be accessible, skip them
                    continue
            
            if public_buckets_found == 0:
                print(f"{Fore.GREEN}No public S3 buckets found")
            else:
                print(f"{Fore.RED}Found {public_buckets_found} public S3 buckets!")
                    
        except Exception as e:
            print(f"{Fore.RED}Error scanning S3: {e}")
    
    def check_ec2_security_groups(self):
        """Check security groups for overly permissive rules - HIGH SECURITY RISK"""
        print(f"{Fore.CYAN}Scanning EC2 security groups for open ports...")
        
        try:
            ec2 = self.session.client('ec2')
            security_groups = ec2.describe_security_groups()
            
            open_ssh_found = 0
            open_rdp_found = 0
            open_all_ports_found = 0
            
            for sg in security_groups['SecurityGroups']:
                sg_id = sg['GroupId']
                sg_name = sg['GroupName']
                
                for permission in sg.get('IpPermissions', []):
                    for ip_range in permission.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            # SSH (Port 22) open to world - CRITICAL
                            if permission.get('FromPort') == 22 and permission.get('ToPort') == 22:
                                open_ssh_found += 1
                                self.findings.append({
                                    'severity': 'CRITICAL',
                                    'service': 'EC2',
                                    'resource': sg_id,
                                    'title': 'SSH Port Open to World',
                                    'description': f'Security group "{sg_name}" ({sg_id}) allows SSH access from ANY IP address (0.0.0.0/0)',
                                    'recommendation': 'Immediately restrict SSH to specific IP ranges only. Use VPN or bastion host.',
                                    'timestamp': self.scan_time,
                                    'risk_score': 9
                                })
                                print(f"{Fore.RED}CRITICAL: SSH open to world: {sg_name} ({sg_id})")
                            
                            # RDP (Port 3389) open to world - CRITICAL
                            if permission.get('FromPort') == 3389 and permission.get('ToPort') == 3389:
                                open_rdp_found += 1
                                self.findings.append({
                                    'severity': 'CRITICAL',
                                    'service': 'EC2',
                                    'resource': sg_id,
                                    'title': 'RDP Port Open to World',
                                    'description': f'Security group "{sg_name}" ({sg_id}) allows RDP access from ANY IP address (0.0.0.0/0)',
                                    'recommendation': 'Immediately restrict RDP to specific IP ranges only. Use VPN for remote access.',
                                    'timestamp': self.scan_time,
                                    'risk_score': 9
                                })
                                print(f"{Fore.RED}CRITICAL: RDP open to world: {sg_name} ({sg_id})")
                            
                            # All ports open to world - CRITICAL
                            if permission.get('FromPort') == 0 and permission.get('ToPort') == 65535:
                                open_all_ports_found += 1
                                self.findings.append({
                                    'severity': 'CRITICAL',
                                    'service': 'EC2',
                                    'resource': sg_id,
                                    'title': 'ALL PORTS Open to World',
                                    'description': f'Security group "{sg_name}" ({sg_id}) allows ALL ports from ANY IP address (0.0.0.0/0)',
                                    'recommendation': 'IMMEDIATE ACTION REQUIRED: Remove this rule. Use specific port ranges only.',
                                    'timestamp': self.scan_time,
                                    'risk_score': 10
                                })
                                print(f"{Fore.RED}CRITICAL: ALL PORTS open to world: {sg_name} ({sg_id})")
            
            # Summary
            if open_ssh_found == 0 and open_rdp_found == 0 and open_all_ports_found == 0:
                print(f"{Fore.GREEN}No critical open ports found in security groups")
            else:
                print(f"{Fore.YELLOW}Security Group Summary:")
                if open_ssh_found > 0:
                    print(f"{Fore.RED}   Open SSH to world: {open_ssh_found}")
                if open_rdp_found > 0:
                    print(f"{Fore.RED}   Open RDP to world: {open_rdp_found}")
                if open_all_ports_found > 0:
                    print(f"{Fore.RED}   ALL PORTS open to world: {open_all_ports_found}")
                    
        except Exception as e:
            print(f"{Fore.RED}Error scanning security groups: {e}")
    
    def check_iam_password_policy(self):
        """Check IAM password policy - MEDIUM SECURITY RISK"""
        print(f"{Fore.CYAN}Checking IAM password policy...")
        
        try:
            iam = self.session.client('iam')
            
            try:
                policy = iam.get_account_password_policy()
                policy_details = policy['PasswordPolicy']
                
                checks = [
                    ('Minimum password length', policy_details.get('MinimumPasswordLength', 0) >= 8, 8),
                    ('Requires symbols', policy_details.get('RequireSymbols', False), True),
                    ('Requires numbers', policy_details.get('RequireNumbers', False), True),
                    ('Requires uppercase', policy_details.get('RequireUppercaseCharacters', False), True),
                    ('Requires lowercase', policy_details.get('RequireLowercaseCharacters', False), True),
                    ('Password expiration', policy_details.get('MaxPasswordAge', 0) <= 90, 90),
                ]
                
                weak_policies = []
                for check_name, actual, expected in checks:
                    if not actual:
                        weak_policies.append(check_name)
                
                if weak_policies:
                    self.findings.append({
                        'severity': 'MEDIUM',
                        'service': 'IAM',
                        'resource': 'AccountPasswordPolicy',
                        'title': 'Weak IAM Password Policy',
                        'description': f'Password policy has weak settings: {", ".join(weak_policies)}',
                        'recommendation': 'Strengthen IAM password policy to meet security best practices',
                        'timestamp': self.scan_time,
                        'risk_score': 5
                    })
                    print(f"{Fore.YELLOW}Weak IAM password policy: {', '.join(weak_policies)}")
                else:
                    print(f"{Fore.GREEN}IAM password policy is strong")
                    
            except iam.exceptions.NoSuchEntityException:
                self.findings.append({
                    'severity': 'HIGH',
                    'service': 'IAM',
                    'resource': 'AccountPasswordPolicy',
                    'title': 'No IAM Password Policy',
                    'description': 'No IAM password policy configured for the account',
                    'recommendation': 'Create an IAM password policy with strong requirements',
                    'timestamp': self.scan_time,
                    'risk_score': 7
                })
                print(f"{Fore.RED}No IAM password policy configured!")
                
        except Exception as e:
            print(f"{Fore.RED}Error checking IAM password policy: {e}")
    
    def check_unencrypted_volumes(self):
        """Check for unencrypted EBS volumes - MEDIUM SECURITY RISK"""
        print(f"{Fore.CYAN}Checking for unencrypted EBS volumes...")
        
        try:
            ec2 = self.session.client('ec2')
            volumes = ec2.describe_volumes()
            
            unencrypted_volumes = []
            
            for volume in volumes['Volumes']:
                if not volume.get('Encrypted', False):
                    unencrypted_volumes.append(volume['VolumeId'])
                    self.findings.append({
                        'severity': 'MEDIUM',
                        'service': 'EC2',
                        'resource': volume['VolumeId'],
                        'title': 'Unencrypted EBS Volume',
                        'description': f'EBS volume {volume["VolumeId"]} is not encrypted',
                        'recommendation': 'Enable encryption for EBS volumes to protect data at rest',
                        'timestamp': self.scan_time,
                        'risk_score': 6
                    })
                    print(f"{Fore.YELLOW}Unencrypted EBS volume: {volume['VolumeId']}")
            
            if not unencrypted_volumes:
                print(f"{Fore.GREEN}All EBS volumes are encrypted")
            else:
                print(f"{Fore.YELLOW}Found {len(unencrypted_volumes)} unencrypted EBS volumes")
                
        except Exception as e:
            print(f"{Fore.RED}Error checking EBS volumes: {e}")
    
    def run_scan(self):
        """Run enhanced security scan"""
        print(f"{Fore.GREEN}Starting ENHANCED AWS Security Scan...")
        print(f"{Fore.GREEN}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.CYAN}Scanning for CRITICAL security misconfigurations...")
        print("-" * 70)
        
        # Run all security checks
        self.check_s3_public_buckets()
        print()
        
        self.check_ec2_security_groups() 
        print()
        
        self.check_iam_password_policy()
        print()
        
        self.check_unencrypted_volumes()
        print()
        
        # Save results
        self.save_findings()
        
        # Show comprehensive summary
        self.show_summary()
    
    def save_findings(self):
        """Save findings to JSON file"""
        try:
            os.makedirs('results', exist_ok=True)
            filename = f"results/enhanced_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    'scan_time': self.scan_time,
                    'findings': self.findings,
                    'total_findings': len(self.findings),
                    'scan_type': 'enhanced_security_scan'
                }, f, indent=2)
            
            print(f"{Fore.GREEN}Detailed results saved to: {filename}")
            
        except Exception as e:
            print(f"{Fore.RED}Error saving results: {e}")
    
    def show_summary(self):
        """Display comprehensive scan summary"""
        print("\n" + "=" * 70)
        print(f"{Fore.GREEN}ENHANCED SECURITY SCAN SUMMARY")
        print("=" * 70)
        
        # Count findings by severity
        severity_count = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0, 
            'LOW': 0,
            'INFO': 0
        }
        
        total_risk_score = 0
        
        for finding in self.findings:
            severity_count[finding['severity']] += 1
            total_risk_score += finding.get('risk_score', 0)
        
        # Print counts with colors
        print(f"{Fore.RED}CRITICAL: {severity_count['CRITICAL']}")
        print(f"{Fore.YELLOW}HIGH: {severity_count['HIGH']}")
        print(f"{Fore.BLUE}MEDIUM: {severity_count['MEDIUM']}")
        print(f"{Fore.CYAN}LOW: {severity_count['LOW']}")
        print(f"{Fore.WHITE}INFO: {severity_count['INFO']}")
        
        total_findings = len(self.findings)
        print(f"{Fore.CYAN}TOTAL FINDINGS: {total_findings}")
        
        if total_risk_score > 0:
            print(f"{Fore.YELLOW}OVERALL RISK SCORE: {total_risk_score}/100")
        
        print("\n" + "=" * 70)
        
        if total_findings == 0:
            print(f"{Fore.GREEN}EXCELLENT! No security issues found!")
            print(f"{Fore.GREEN}Your AWS environment appears secure!")
        else:
            if severity_count['CRITICAL'] > 0:
                print(f"{Fore.RED}URGENT ACTION REQUIRED!")
                print(f"{Fore.RED}{severity_count['CRITICAL']} CRITICAL issues need immediate attention!")
            else:
                print(f"{Fore.YELLOW}Review findings above and address accordingly")
        
        print(f"\n{Fore.GREEN}Next: Review detailed findings in the results/ directory")

if __name__ == "__main__":
    scanner = EnhancedSecurityScanner()
    scanner.run_scan()
