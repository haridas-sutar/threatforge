import boto3
import json
import asyncio
from datetime import datetime
from botocore.config import Config

class ProductionSecurityScanner:
    def __init__(self):
        self.findings = []
        self.config = Config(
            retries={'max_attempts': 10, 'mode': 'adaptive'},
            max_pool_connections=50
        )
        
    async def scan_all_regions(self):
        """Scan all enabled regions concurrently"""
        ec2 = boto3.client('ec2', config=self.config)
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
        
        tasks = [self.scan_region(region) for region in regions]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def scan_region(self, region):
        """Scan a specific AWS region"""
        print(f"Scanning region: {region}")
        
        try:
            session = boto3.Session(region_name=region)
            
            await asyncio.gather(
                self.check_regional_ec2(session),
                self.check_regional_rds(session),
                return_exceptions=True
            )
            
        except Exception as e:
            print(f"Error scanning region {region}: {e}")
    
    async def check_regional_ec2(self, session):
        """Check EC2 security for region"""
        ec2 = session.client('ec2', config=self.config)
        
        try:
            sgs = ec2.describe_security_groups()
            for sg in sgs['SecurityGroups']:
                self._check_security_group_rules(sg, session.region_name)
                
        except Exception as e:
            print(f"Error checking EC2 in {session.region_name}: {e}")
    
    async def check_regional_rds(self, session):
        """Check RDS security for region"""
        rds = session.client('rds', config=self.config)
        
        try:
            instances = rds.describe_db_instances()
            for instance in instances['DBInstances']:
                if instance['PubliclyAccessible']:
                    self.findings.append({
                        'severity': 'CRITICAL',
                        'service': 'RDS',
                        'resource': instance['DBInstanceIdentifier'],
                        'title': 'Public RDS Instance',
                        'description': f'RDS instance {instance["DBInstanceIdentifier"]} is publicly accessible',
                        'recommendation': 'Modify RDS instance to be private',
                        'region': session.region_name,
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    
        except Exception as e:
            print(f"Error checking RDS in {session.region_name}: {e}")
    
    def _check_security_group_rules(self, sg, region):
        """Check individual security group rules"""
        for permission in sg.get('IpPermissions', []):
            for ip_range in permission.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    if permission.get('FromPort') == 22 and permission.get('ToPort') == 22:
                        self.findings.append({
                            'severity': 'CRITICAL',
                            'service': 'EC2',
                            'resource': sg['GroupId'],
                            'title': 'SSH Open to World',
                            'description': f'Security group {sg["GroupName"]} allows SSH from anywhere',
                            'recommendation': 'Restrict SSH to specific IP ranges',
                            'region': region,
                            'timestamp': datetime.utcnow().isoformat()
                        })
    
    def run_scan(self):
        """Main scan execution method"""
        print("Starting production security scan...")
        
        asyncio.run(self.scan_all_regions())
        
        self.save_results()
        
        print(f"Scan complete. Found {len(self.findings)} security issues.")
    
    def save_results(self):
        """Save scan results"""
        filename = f"results/production_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'scan_time': datetime.utcnow().isoformat(),
                'findings': self.findings,
                'scan_type': 'production_multi_region'
            }, f, indent=2)
        
        print(f"Results saved to: {filename}")

if __name__ == "__main__":
    scanner = ProductionSecurityScanner()
    scanner.run_scan()
