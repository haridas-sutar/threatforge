from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
import asyncio
import subprocess
import os
from datetime import datetime
from pathlib import Path

app = FastAPI(title="ThreatForge Dashboard", version="1.0.0")

# Get the current directory and parent directory
current_dir = Path(__file__).parent
parent_dir = current_dir.parent

# Mount static files and templates
app.mount("/static", StaticFiles(directory=current_dir / "static"), name="static")
templates = Jinja2Templates(directory=current_dir / "templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/scan-results")
async def get_scan_results():
    """Get latest scan results from JSON files"""
    results_dir = parent_dir / "results"
    scan_files = list(results_dir.glob("*.json"))
    scan_files.sort(key=os.path.getmtime, reverse=True)
    
    latest_results = []
    for file_path in scan_files[:5]:  # Last 5 scans
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                data['filename'] = file_path.name
                data['file_time'] = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                latest_results.append(data)
        except Exception as e:
            continue
    
    return {"scans": latest_results}

@app.post("/api/run-scan")
async def run_scan():
    """Execute security scan and return results"""
    try:
        # Run the enhanced scanner from the parent directory
        scanner_path = parent_dir / "scanner" / "enhanced_scanner.py"
        result = subprocess.run(
            ["python3", str(scanner_path)],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=str(parent_dir)  # Run from project root
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.websocket("/ws/scan-updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send periodic updates about system status
            await asyncio.sleep(10)
            
            # Check for new scan results
            results_dir = parent_dir / "results"
            scan_files = list(results_dir.glob("*.json"))
            if scan_files:
                latest_file = max(scan_files, key=os.path.getmtime)
                file_age = datetime.now().timestamp() - latest_file.stat().st_mtime
                
                if file_age < 30:  # File created in last 30 seconds
                    with open(latest_file, 'r') as f:
                        scan_data = json.load(f)
                    
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "new_scan",
                            "data": scan_data
                        }),
                        websocket
                    )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/security-metrics")
async def get_security_metrics():
    """Calculate security metrics from scan results"""
    results_dir = parent_dir / "results"
    scan_files = list(results_dir.glob("*scan*.json"))
    
    total_critical = 0
    total_high = 0
    total_medium = 0
    scan_count = len(scan_files)
    
    for file_path in scan_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for finding in data.get('findings', []):
                    if finding['severity'] == 'CRITICAL':
                        total_critical += 1
                    elif finding['severity'] == 'HIGH':
                        total_high += 1
                    elif finding['severity'] == 'MEDIUM':
                        total_medium += 1
        except:
            continue
    
    return {
        "total_scans": scan_count,
        "critical_findings": total_critical,
        "high_findings": total_high,
        "medium_findings": total_medium,
        "overall_risk_score": min(100, (total_critical * 10 + total_high * 7 + total_medium * 4))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/security-report")
async def get_security_report():
    """Generate comprehensive security report"""
    try:
        # Import and use the security reporter
        import sys
        sys.path.append('..')
        from utils.security_reporter import SecurityReporter
        
        reporter = SecurityReporter()
        report = reporter.generate_comprehensive_report()
        
        return report
    except Exception as e:
        return {"error": f"Failed to generate report: {str(e)}"}

@app.get("/api/fix-recommendations")
async def get_fix_recommendations():
    """Get specific fix recommendations for critical issues"""
    try:
        import subprocess
        result = subprocess.run(
            ["python3", "scanner/enhanced_scanner.py"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Parse the output for critical issues and generate fixes
        critical_issues = []
        if "CRITICAL: SSH open to world" in result.stdout:
            critical_issues.append({
                "issue": "Open SSH to world",
                "fix_command": "aws ec2 revoke-security-group-ingress --group-id SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0",
                "description": "Remove SSH access from entire internet"
            })
        
        return {
            "critical_issues": critical_issues,
            "total_critical": len(critical_issues)
        }
    except Exception as e:
        return {"error": str(e)}
