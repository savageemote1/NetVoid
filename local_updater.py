#!/usr/bin/env python3
"""
NetVoid Local Auto-Updater
Monitors local changes and automatically restarts the server
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime
from pathlib import Path
import hashlib

# Configuration
CHECK_INTERVAL = 30  # Check every 30 seconds
WATCH_FILES = [
    'secure_web_server.py',
    'templates/',
    'static/',
    'server/',
    'client/'
]

class LocalUpdater:
    def __init__(self):
        self.last_checksums = {}
        self.running = False
        self.server_process = None
        self.update_log = []
        
    def log(self, message):
        """Log update message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.update_log.append(log_message)
        
    def get_file_checksum(self, file_path):
        """Get MD5 checksum of a file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
            
    def get_directory_checksum(self, dir_path):
        """Get combined checksum of all files in directory"""
        checksums = []
        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    checksum = self.get_file_checksum(file_path)
                    if checksum:
                        checksums.append(f"{file_path}:{checksum}")
        except:
            pass
        return hashlib.md5('|'.join(checksums).encode()).hexdigest()
        
    def check_for_changes(self):
        """Check for file changes"""
        changes_detected = False
        
        for item in WATCH_FILES:
            if os.path.isfile(item):
                # Single file
                current_checksum = self.get_file_checksum(item)
                if current_checksum and current_checksum != self.last_checksums.get(item):
                    self.log(f"File changed: {item}")
                    self.last_checksums[item] = current_checksum
                    changes_detected = True
                    
            elif os.path.isdir(item):
                # Directory
                current_checksum = self.get_directory_checksum(item)
                if current_checksum and current_checksum != self.last_checksums.get(item):
                    self.log(f"Directory changed: {item}")
                    self.last_checksums[item] = current_checksum
                    changes_detected = True
                    
        return changes_detected
        
    def stop_server(self):
        """Stop the current server"""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                self.log("Server stopped gracefully")
            except:
                try:
                    self.server_process.kill()
                    self.log("Server force killed")
                except:
                    pass
            finally:
                self.server_process = None
                
    def start_server(self):
        """Start the server"""
        try:
            self.log("Starting server...")
            self.server_process = subprocess.Popen([
                sys.executable, 'secure_web_server.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            for i in range(10):
                time.sleep(2)
                try:
                    import requests
                    response = requests.get('http://localhost:8080/api/status', timeout=5)
                    if response.status_code == 200:
                        self.log("Server started successfully!")
                        return True
                except:
                    pass
                    
            self.log("Server failed to start!")
            return False
            
        except Exception as e:
            self.log(f"Error starting server: {e}")
            return False
            
    def restart_server(self):
        """Restart the server"""
        self.log("Restarting server due to file changes...")
        
        # Stop current server
        self.stop_server()
        time.sleep(2)
        
        # Start new server
        if self.start_server():
            self.log("Server restarted successfully!")
            return True
        else:
            self.log("Failed to restart server!")
            return False
            
    def initialize_checksums(self):
        """Initialize file checksums"""
        self.log("Initializing file monitoring...")
        
        for item in WATCH_FILES:
            if os.path.isfile(item):
                checksum = self.get_file_checksum(item)
                if checksum:
                    self.last_checksums[item] = checksum
                    self.log(f"Monitoring file: {item}")
                    
            elif os.path.isdir(item):
                checksum = self.get_directory_checksum(item)
                if checksum:
                    self.last_checksums[item] = checksum
                    self.log(f"Monitoring directory: {item}")
                    
    def run_update_loop(self):
        """Run the update loop"""
        self.log("Starting NetVoid local auto-updater...")
        self.running = True
        
        # Initialize checksums
        self.initialize_checksums()
        
        # Start server initially
        if not self.start_server():
            self.log("Failed to start server initially!")
            return
            
        while self.running:
            try:
                if self.check_for_changes():
                    self.restart_server()
                    
                time.sleep(CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                self.log("Update loop stopped by user")
                break
            except Exception as e:
                self.log(f"Update loop error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
                
    def stop(self):
        """Stop the updater"""
        self.log("Stopping auto-updater...")
        self.running = False
        self.stop_server()
        
    def get_status(self):
        """Get updater status"""
        return {
            'running': self.running,
            'server_running': self.server_process is not None,
            'monitored_files': len(self.last_checksums),
            'last_check': datetime.now().isoformat(),
            'logs': self.update_log[-10:]  # Last 10 log entries
        }

def main():
    """Main function"""
    print("=" * 60)
    print("    NETVOID LOCAL AUTO-UPDATER")
    print("=" * 60)
    print()
    print("🔍 Monitoring files for changes...")
    print("📁 Monitored items:")
    for item in WATCH_FILES:
        if os.path.exists(item):
            print(f"   • {item}")
    print()
    print("🔄 Auto-restart enabled when files change")
    print("Press Ctrl+C to stop")
    print()
    
    updater = LocalUpdater()
    
    try:
        updater.run_update_loop()
    except KeyboardInterrupt:
        updater.stop()
        print("\n🛑 Auto-updater stopped.")

if __name__ == '__main__':
    main()
