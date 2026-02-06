"""
WALEED SERVER KEEP ALIVE
Yeh script server ko 24/7 active rakhegi
"""

import requests
import time
import threading
from datetime import datetime

class KeepAlive:
    def __init__(self, url, interval=300):
        """
        url: Streamlit app ka URL
        interval: Kitne seconds baad ping karna hai (default 5 minutes)
        """
        self.url = url
        self.interval = interval
        self.running = False
        self.ping_count = 0
        
    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {msg}")
        
    def ping(self):
        """Server ko ping karo"""
        try:
            response = requests.get(self.url, timeout=30)
            self.ping_count += 1
            self.log(f"✅ Ping #{self.ping_count} successful - Status: {response.status_code}")
            return True
        except Exception as e:
            self.log(f"❌ Ping failed: {e}")
            return False
    
    def start(self):
        """Keep alive loop start karo"""
        self.running = True
        self.log(f"🚀 Keep Alive started for: {self.url}")
        self.log(f"⏱️ Ping interval: {self.interval} seconds")
        
        while self.running:
            self.ping()
            time.sleep(self.interval)
    
    def stop(self):
        """Keep alive band karo"""
        self.running = False
        self.log("🛑 Keep Alive stopped")

def run_keep_alive(url, interval=300):
    """Background thread mein keep alive run karo"""
    keeper = KeepAlive(url, interval)
    thread = threading.Thread(target=keeper.start, daemon=True)
    thread.start()
    return keeper

if __name__ == "__main__":
    # Apna Streamlit URL yahan dalo
    STREAMLIT_URL = "https://your-app-name.streamlit.app"
    
    keeper = KeepAlive(STREAMLIT_URL, interval=300)  # 5 minute interval
    
    try:
        keeper.start()
    except KeyboardInterrupt:
        keeper.stop()
