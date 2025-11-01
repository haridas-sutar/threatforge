# test_setup.py
import sys
import os

def test_environment():
    """Test if the environment is properly set up"""
    print(" Testing ThreatForge Setup...")
    print("=" * 40)
    
    # Test Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Test imports
    try:
        import boto3
        print(" boto3 imported successfully")
    except ImportError as e:
        print(f" boto3 import failed: {e}")
        return False
    
    try:
        from colorama import Fore, Style
        print(" colorama imported successfully")
    except ImportError as e:
        print(f" colorama import failed: {e}")
        return False
    
    # Test AWS credentials
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            print(" AWS credentials found")
        else:
            print(" No AWS credentials found")
            return False
    except Exception as e:
        print(f" AWS credentials test failed: {e}")
        return False
    
    # Test file structure
    required_dirs = ['scanner', 'config', 'utils', 'results']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f" Directory '{dir_name}' exists")
        else:
            print(f" Directory '{dir_name}' missing")
            return False
    
    print("=" * 40)
    print(" All tests passed! Environment is ready.")
    return True

if __name__ == "__main__":
    test_environment()
