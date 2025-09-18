#!/usr/bin/env python3
"""
GitHub Two-Way Sync for NetVoid Server
Syncs changes between local code and GitHub repository
"""

import os
import sys
import subprocess
import time
import threading
from datetime import datetime
from pathlib import Path

def print_banner():
    print("=" * 70)
    print("    NETVOID GITHUB TWO-WAY SYNC")
    print("=" * 70)
    print()

def log(message):
    """Log sync message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_git_status():
    """Check git status"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return None

def pull_from_github():
    """Pull latest changes from GitHub"""
    try:
        log("Pulling latest changes from GitHub...")
        
        # Fetch latest changes
        subprocess.run(['git', 'fetch', 'origin'], check=True)
        
        # Check if there are remote changes (try main first, then master)
        result = subprocess.run(['git', 'log', 'HEAD..origin/main', '--oneline'], 
                              capture_output=True, text=True)
        
        # If no changes on main, check master
        if not result.stdout.strip():
            result = subprocess.run(['git', 'log', 'HEAD..origin/master', '--oneline'], 
                                  capture_output=True, text=True)
        
        if result.stdout.strip():
            log(f"Found {len(result.stdout.strip().split(chr(10)))} new commits from GitHub")
            
            # Pull changes (try main first, then master)
            try:
                subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
            except:
                subprocess.run(['git', 'pull', 'origin', 'master'], check=True)
            log("Successfully pulled changes from GitHub")
            return True
        else:
            log("No new changes from GitHub")
            return False
            
    except subprocess.CalledProcessError as e:
        log(f"Error pulling from GitHub: {e}")
        return False

def push_to_github():
    """Push local changes to GitHub"""
    try:
        # Check for local changes
        status = check_git_status()
        if not status:
            return False
            
        log("Found local changes, pushing to GitHub...")
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        commit_message = f"Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to GitHub (try main first, then master)
        try:
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        except:
            subprocess.run(['git', 'push', 'origin', 'master'], check=True)
        log("Successfully pushed changes to GitHub")
        return True
        
    except subprocess.CalledProcessError as e:
        log(f"Error pushing to GitHub: {e}")
        return False

def restart_server():
    """Restart the NetVoid server"""
    try:
        log("Restarting NetVoid server...")
        
        # Kill existing server processes
        try:
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, check=False)
        except:
            pass
        
        # Wait a moment
        time.sleep(2)
        
        # Start server in background
        subprocess.Popen([sys.executable, 'secure_web_server.py'], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        for i in range(10):
            time.sleep(2)
            try:
                import requests
                response = requests.get('http://localhost:8080/api/status', timeout=5)
                if response.status_code == 200:
                    log("Server restarted successfully!")
                    return True
            except:
                pass
                
        log("Server restart failed!")
        return False
        
    except Exception as e:
        log(f"Error restarting server: {e}")
        return False

def sync_loop():
    """Main sync loop"""
    log("Starting GitHub two-way sync...")
    log("Monitoring for changes every 30 seconds...")
    
    last_local_commit = None
    last_remote_commit = None
    
    while True:
        try:
            # Check local changes
            current_local_commit = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                                capture_output=True, text=True).stdout.strip()
            
            # Check remote changes
            subprocess.run(['git', 'fetch', 'origin'], check=False)
            current_remote_commit = subprocess.run(['git', 'rev-parse', 'origin/master'], 
                                                 capture_output=True, text=True).stdout.strip()
            
            # Check if we need to pull from GitHub
            if last_remote_commit and current_remote_commit != last_remote_commit:
                log("Remote changes detected, pulling from GitHub...")
                if pull_from_github():
                    restart_server()
                last_remote_commit = current_remote_commit
            
            # Check if we need to push to GitHub
            if last_local_commit and current_local_commit != last_local_commit:
                log("Local changes detected, pushing to GitHub...")
                push_to_github()
                last_local_commit = current_local_commit
            
            # Update commit hashes
            if not last_local_commit:
                last_local_commit = current_local_commit
            if not last_remote_commit:
                last_remote_commit = current_remote_commit
            
            # Wait before next check
            time.sleep(30)
            
        except KeyboardInterrupt:
            log("Sync stopped by user")
            break
        except Exception as e:
            log(f"Sync error: {e}")
            time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main function"""
    print_banner()
    
    print("🔧 Setting up GitHub two-way sync...")
    print()
    
    # Check if we're in a git repository
    try:
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        log("Git repository detected")
    except:
        log("Not a git repository!")
        return
    
    # Check remote
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        log(f"Remote repository: {result.stdout.strip()}")
    except:
        log("No remote repository configured!")
        return
    
    print()
    print("🔄 Two-way sync features:")
    print("   • Pulls changes from GitHub every 30 seconds")
    print("   • Pushes local changes to GitHub automatically")
    print("   • Restarts server when changes are detected")
    print("   • Monitors both local and remote changes")
    print()
    print("🌐 Server URLs:")
    print("   • Homepage: http://localhost:8080")
    print("   • Admin: http://localhost:8080/admin")
    print("   • API: http://localhost:8080/api/status")
    print()
    print("Press Ctrl+C to stop sync")
    print()
    
    # Start sync loop
    try:
        sync_loop()
    except KeyboardInterrupt:
        log("Sync stopped by user")
        print("\n🛑 GitHub sync stopped.")

if __name__ == '__main__':
    main()
