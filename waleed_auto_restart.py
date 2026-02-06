#!/usr/bin/env python3
"""
WALEED AUTO-RESTART + KEEP ALIVE MANAGER
Server ko kabhi band nahi hone dega
"""

import subprocess
import time
import sys
import os
import requests
import threading
from datetime import datetime

# Configuration
STREAMLIT_PORT = 8501
PING_INTERVAL = 60  # seconds
MAX_RESTART_DELAY = 60

def log_message(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    print(f"[{timestamp}] {icons.get(level, 'ℹ️')} {msg}")

def ping_server():
    """Server ko ping karte raho"""
    url = f"http://localhost:{STREAMLIT_PORT}"
    while True:
        try:
            response = requests.get(url, timeout=10)
            log_message(f"Server alive - Status: {response.status_code}", "SUCCESS")
        except:
            log_message("Server not responding, will be handled by restart loop", "WARNING")
        time.sleep(PING_INTERVAL)

def run_streamlit():
    """Streamlit app run karo"""
    log_message("Starting Waleed Streamlit App...", "INFO")
    
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        f"--server.port={STREAMLIT_PORT}",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--server.runOnSave=true",
        "--browser.gatherUsageStats=false"
    ]
    
    try:
        process = subprocess.Popen(cmd)
        log_message(f"Streamlit started with PID: {process.pid}", "SUCCESS")
        process.wait()
        log_message(f"Process ended with code: {process.returncode}", "WARNING")
        return process.returncode
        
    except KeyboardInterrupt:
        log_message("Keyboard interrupt received", "WARNING")
        process.terminate()
        return -1
    except Exception as e:
        log_message(f"Error: {e}", "ERROR")
        return 1

def main():
    """Main loop - server ko hamesha chalu rakho"""
    log_message("=" * 50, "INFO")
    log_message("WALEED AUTO-RESTART MANAGER STARTED", "SUCCESS")
    log_message("=" * 50, "INFO")
    
    # Start ping thread
    ping_thread = threading.Thread(target=ping_server, daemon=True)
    ping_thread.start()
    log_message("Keep-alive ping thread started", "SUCCESS")
    
    restart_count = 0
    
    while True:
        restart_count += 1
        log_message(f"Starting attempt #{restart_count}", "INFO")
        
        exit_code = run_streamlit()
        
        if exit_code == -1:
            log_message("User requested stop. Exiting...", "INFO")
            break
        
        restart_delay = min(restart_count * 2, MAX_RESTART_DELAY)
        log_message(f"Restarting in {restart_delay} seconds...", "WARNING")
        
        try:
            time.sleep(restart_delay)
        except KeyboardInterrupt:
            log_message("Exiting...", "INFO")
            break

if __name__ == "__main__":
    main()
