import boto3
import os
from colorama import Fore, Style

def test_aws_connection():
    print(f"{Fore.CYAN}🔐 Testing AWS Connection...{Style.RESET_ALL}")
    print("=" * 50)
    
    # Method 1: Test environment variables
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if access_key and secret_key:
        print(f"{Fore.GREEN}✅ AWS credentials found in environment variables{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️  No AWS credentials in environment variables{Style.RESET_ALL}")
    
    # Method 2: Test boto3 session
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials:
            print(f"{Fore.GREEN}✅ AWS credentials found in boto3 session{Style.RESET_ALL}")
            print(f"   Access Key: {credentials.access_key[:10]}...")
        else:
            print(f"{Fore.RED}❌ No credentials in boto3 session{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error checking boto3 session: {e}{Style.RESET_ALL}")
    
    # Method 3: Test actual AWS API call
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"{Fore.GREEN}✅ AWS API call successful!{Style.RESET_ALL}")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        
        # Test additional services
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        print(f"{Fore.GREEN}✅ S3 access verified - {len(buckets['Buckets'])} buckets found{Style.RESET_ALL}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ AWS API call failed: {e}{Style.RESET_ALL}")
        return False

if __name__ == "__main__":
    success = test_aws_connection()
    print("=" * 50)
    if success:
        print(f"{Fore.GREEN}🎉 AWS Connection Successful! Ready for security scanning.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ AWS Connection Failed. Please check credentials.{Style.RESET_ALL}")
