#!/bin/bash

DASHBOARD_PID_FILE="dashboard.pid"
DASHBOARD_LOG="dashboard.log"

get_instance_ip() {
    # Try multiple methods to get IP
    IP=""
    
    # Method 1: Check public IP from metadata
    if IP=$(curl -s -f http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null); then
        if [ -n "$IP" ] && [ "$IP" != "" ]; then
            echo "$IP"
            return 0
        fi
    fi
    
    # Method 2: Check local IP
    if IP=$(hostname -I 2>/dev/null | awk '{print $1}'); then
        if [ -n "$IP" ]; then
            echo "$IP"
            return 0
        fi
    fi
    
    # Method 3: Fallback
    echo "localhost"
}

start_dashboard() {
    if [ -f "$DASHBOARD_PID_FILE" ]; then
        PID=$(cat "$DASHBOARD_PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "Dashboard is already running (PID: $PID)"
            return 1
        fi
    fi
    
    echo "Starting ThreatForge Dashboard..."
    nohup python3 -m uvicorn dashboard.app:app --host 0.0.0.0 --port 8000 > "$DASHBOARD_LOG" 2>&1 &
    PID=$!
    echo $PID > "$DASHBOARD_PID_FILE"
    
    # Wait a moment and check if it's still running
    sleep 2
    if ps -p $PID > /dev/null 2>&1; then
        INSTANCE_IP=$(get_instance_ip)
        echo "Dashboard started successfully (PID: $PID)"
        echo "Access at: http://${INSTANCE_IP}:8000"
        echo "Log file: $DASHBOARD_LOG"
    else
        echo "Dashboard failed to start. Check $DASHBOARD_LOG for errors."
        rm -f "$DASHBOARD_PID_FILE"
        return 1
    fi
}

stop_dashboard() {
    if [ -f "$DASHBOARD_PID_FILE" ]; then
        PID=$(cat "$DASHBOARD_PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID
            echo "Dashboard stopped (PID: $PID)"
        else
            echo "Dashboard was not running"
        fi
        rm -f "$DASHBOARD_PID_FILE"
    else
        echo "No PID file found. Dashboard may not be running."
    fi
}

status_dashboard() {
    if [ -f "$DASHBOARD_PID_FILE" ]; then
        PID=$(cat "$DASHBOARD_PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "Dashboard is running (PID: $PID)"
            echo "Recent log entries:"
            tail -10 "$DASHBOARD_LOG" | grep -v "INFO:"
        else
            echo "Dashboard PID file exists but process is not running"
            echo "Last log entries:"
            tail -20 "$DASHBOARD_LOG"
        fi
    else
        echo "Dashboard is not running"
    fi
}

case "$1" in
    start)
        start_dashboard
        ;;
    stop)
        stop_dashboard
        ;;
    restart)
        stop_dashboard
        sleep 2
        start_dashboard
        ;;
    status)
        status_dashboard
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
