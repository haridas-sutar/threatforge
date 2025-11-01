import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_environment():
    """Test if the environment is properly set up"""
    print("🧪 Testing ThreatForge Setup...")
    print("=" * 40)
    
    # Test Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Test imports
    try:
        import boto3
        print("✅ boto3 imported successfully")
    except ImportError as e:
        print(f"❌ boto3 import failed: {e}")
        return False
    
    try:
        from colorama import Fore, Style
        print("✅ colorama imported successfully")
    except ImportError as e:
        print(f"❌ colorama import failed: {e}")
        return False
    
    # Test file structure
    required_dirs = ['scanner', 'config', 'utils', 'results']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory '{dir_name}' exists")
        else:
            print(f"❌ Directory '{dir_name}' missing")
            return False
    
    # Test AWS credentials with better error handling
    try:
        import boto3
        print("🔐 Testing AWS credentials...")
        
        # Try multiple ways to get credentials
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials:
            print("✅ AWS credentials found in boto3 session")
        else:
            print("❌ No credentials in boto3 session")
            
        # Test actual AWS API call
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print("✅ AWS credentials are valid!")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        
    except Exception as e:
        print(f"❌ AWS credentials test failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Run: aws configure")
        print("2. Check ~/.aws/credentials file exists")
        print("3. Verify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
        print("4. Ensure IAM user has proper permissions")
        return False
    
    print("=" * 40)
    print("🎉 All tests passed! Environment is ready.")
    return True

if __name__ == "__main__":
    test_environment()
