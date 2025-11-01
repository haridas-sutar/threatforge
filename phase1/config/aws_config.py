# config/aws_config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class AWSConfig:
    # Get credentials from environment variables or use defaults
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '') 
    AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    @classmethod
    def validate_credentials(cls):
        """Check if AWS credentials are available"""
        if not cls.AWS_ACCESS_KEY or not cls.AWS_SECRET_KEY:
            print("❌ AWS credentials not found!")
            print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
            return False
        return True
