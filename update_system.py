#!/usr/bin/env python3
"""
NetVoid Auto-Update System
Monitors GitHub for changes and automatically updates the server
"""

import os
import sys
import json
import time
import requests
import subprocess
import threading
from datetime import datetime
from pathlib import Path

# Configuration
GITHUB_REPO = "your-username/NetVoidServer"  # Replace with your actual repo
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
CHECK_INTERVAL = 300  # Check every 5 minutes
WEBHOOK_URL = "http://localhost:8081/webhook"

class NetVoidUpdater:
    def __init__(self):
        self.last_commit = None
        self.running = False
        self.update_log = []
        
    def log(self, message):
        """Log update message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.update_log.append(log_message)
        
    def get_latest_commit(self):
        """Get latest commit from GitHub"""
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/commits/main"
            headers = {}
            if GITHUB_TOKEN:
                headers['Authorization'] = f'token {GITHUB_TOKEN}'
                
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['sha']
            else:
                self.log(f"Failed to get latest commit: {response.status_code}")
                return None
        except Exception as e:
            self.log(f"Error getting latest commit: {e}")
            return None
            
    def download_latest_code(self):
        """Download latest code from GitHub"""
        try:
            self.log("Downloading latest code from GitHub...")
            
            # Create temp directory
            temp_dir = "temp_update"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir, exist_ok=True)
            
            # Download and extract
            url = f"https://github.com/{GITHUB_REPO}/archive/main.zip"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(os.path.join(temp_dir, "main.zip"), "wb") as f:
                    f.write(response.content)
                    
                # Extract zip
                import zipfile
                with zipfile.ZipFile(os.path.join(temp_dir, "main.zip"), 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                    
                # Move files to deployment directory
                extracted_dir = os.path.join(temp_dir, f"{GITHUB_REPO.split('/')[1]}-main")
                deployment_dir = "deployment"
                
                if os.path.exists(deployment_dir):
                    shutil.rmtree(deployment_dir)
                shutil.copytree(extracted_dir, deployment_dir)
                
                # Cleanup
                shutil.rmtree(temp_dir)
                
                self.log("Code downloaded successfully")
                return True
            else:
                self.log(f"Failed to download code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"Error downloading code: {e}")
            return False
            
    def trigger_deployment(self):
        """Trigger deployment process"""
        try:
            self.log("Triggering deployment...")
            
            # Run deployment script
            result = subprocess.run([
                sys.executable, 'deploy_server.py'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("Deployment completed successfully")
                return True
            else:
                self.log(f"Deployment failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"Error triggering deployment: {e}")
            return False
            
    def check_for_updates(self):
        """Check for updates and deploy if needed"""
        try:
            latest_commit = self.get_latest_commit()
            if not latest_commit:
                return
                
            if self.last_commit is None:
                self.last_commit = latest_commit
                self.log(f"Initial commit set: {latest_commit[:8]}")
                return
                
            if latest_commit != self.last_commit:
                self.log(f"New commit detected: {latest_commit[:8]}")
                self.log(f"Previous commit: {self.last_commit[:8]}")
                
                # Download and deploy
                if self.download_latest_code():
                    if self.trigger_deployment():
                        self.last_commit = latest_commit
                        self.log("Update completed successfully!")
                    else:
                        self.log("Deployment failed!")
                else:
                    self.log("Failed to download latest code!")
            else:
                self.log("No updates available")
                
        except Exception as e:
            self.log(f"Error checking for updates: {e}")
            
    def run_update_loop(self):
        """Run the update loop"""
        self.log("Starting NetVoid auto-updater...")
        self.running = True
        
        while self.running:
            try:
                self.check_for_updates()
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
        
    def get_status(self):
        """Get updater status"""
        return {
            'running': self.running,
            'last_commit': self.last_commit,
            'last_check': datetime.now().isoformat(),
            'logs': self.update_log[-10:]  # Last 10 log entries
        }

def main():
    """Main function"""
    updater = NetVoidUpdater()
    
    try:
        updater.run_update_loop()
    except KeyboardInterrupt:
        updater.stop()
        print("\nAuto-updater stopped.")

if __name__ == '__main__':
    main()
