# utils/logger.py
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class Logger:
    """Custom logger with colored output"""
    
    @staticmethod
    def info(message):
        print(f"{Fore.CYAN}ℹ️  INFO: {message}")
    
    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}✅ SUCCESS: {message}")
    
    @staticmethod
    def warning(message):
        print(f"{Fore.YELLOW}⚠️  WARNING: {message}")
    
    @staticmethod
    def error(message):
        print(f"{Fore.RED}❌ ERROR: {message}")
    
    @staticmethod
    def critical(message):
        print(f"{Fore.RED}🚨 CRITICAL: {message}")

# Create global logger instance
logger = Logger()
