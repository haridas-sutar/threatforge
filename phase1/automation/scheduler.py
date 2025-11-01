import schedule
import time
import subprocess
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScanScheduler:
    def __init__(self):
        self.scan_script = "scanner/enhanced_scanner.py"
        
    def run_daily_scan(self):
        """Run daily security scan"""
        logging.info("Starting scheduled daily security scan")
        try:
            result = subprocess.run(
                ["python3", self.scan_script],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                logging.info("Daily scan completed successfully")
            else:
                logging.error(f"Daily scan failed: {result.stderr}")
                
        except Exception as e:
            logging.error(f"Error running daily scan: {e}")
    
    def run_weekly_report(self):
        """Generate weekly security report"""
        logging.info("Generating weekly security report")
        try:
            from utils.security_reporter import SecurityReporter
            reporter = SecurityReporter()
            report = reporter.generate_comprehensive_report()
            
            # Save weekly report with date
            week = datetime.now().strftime("%Y-%U")
            report_file = f"results/weekly_report_{week}.json"
            
            with open(report_file, 'w') as f:
                import json
                json.dump(report, f, indent=2)
                
            logging.info(f"Weekly report saved: {report_file}")
            
        except Exception as e:
            logging.error(f"Error generating weekly report: {e}")
    
    def start_scheduler(self):
        """Start the automated scheduling"""
        # Daily scan at 2 AM
        schedule.every().day.at("02:00").do(self.run_daily_scan)
        
        # Weekly report on Monday at 6 AM
        schedule.every().monday.at("06:00").do(self.run_weekly_report)
        
        logging.info("Scheduler started - Daily scans at 02:00, Weekly reports on Monday at 06:00")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    scheduler = ScanScheduler()
    scheduler.start_scheduler()
