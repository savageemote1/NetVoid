#!/usr/bin/env python3
"""
Start NetVoid Server with GitHub Two-Way Sync
Handles both local changes and GitHub webhooks
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def print_banner():
    print("=" * 70)
    print("    NETVOID SERVER WITH GITHUB TWO-WAY SYNC")
    print("=" * 70)
    print()

def start_webhook_receiver():
    """Start webhook receiver in background"""
    print("🔗 Starting webhook receiver...")
    try:
        subprocess.Popen([sys.executable, 'webhook_receiver.py'], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Webhook receiver started on port 8081")
        return True
    except Exception as e:
        print(f"❌ Failed to start webhook receiver: {e}")
        return False

def start_github_sync():
    """Start GitHub two-way sync in background"""
    print("🔄 Starting GitHub two-way sync...")
    try:
        subprocess.Popen([sys.executable, 'github_sync.py'], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ GitHub sync started")
        return True
    except Exception as e:
        print(f"❌ Failed to start GitHub sync: {e}")
        return False

def start_main_server():
    """Start main NetVoid server"""
    print("🚀 Starting NetVoid server...")
    try:
        subprocess.run([sys.executable, 'secure_web_server.py'])
        return True
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return False
    except Exception as e:
        print(f"❌ Failed to start main server: {e}")
        return False

def main():
    """Main function"""
    print_banner()
    
    print("🔧 Starting NetVoid with GitHub two-way sync...")
    print()
    
    # Check if required files exist
    required_files = [
        'secure_web_server.py',
        'github_sync.py',
        'webhook_receiver.py'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file not found: {file}")
            return
    
    print("✅ All required files found")
    print()
    
    # Start webhook receiver
    if not start_webhook_receiver():
        print("⚠️  Webhook receiver failed to start - continuing without it")
    
    time.sleep(2)
    
    # Start GitHub sync
    if not start_github_sync():
        print("⚠️  GitHub sync failed to start - continuing without it")
    
    time.sleep(2)
    
    print()
    print("🌐 NetVoid Server URLs:")
    print("   • Homepage: http://localhost:8080")
    print("   • Purchase: http://localhost:8080/purchase")
    print("   • Admin: http://localhost:8080/admin")
    print("   • API: http://localhost:8080/api/status")
    print("   • Webhook: http://localhost:8081/webhook")
    print()
    print("🔄 Two-Way Sync Features:")
    print("   • Local changes → GitHub (automatic push)")
    print("   • GitHub changes → Local (automatic pull)")
    print("   • Server restarts automatically on changes")
    print("   • Webhook support for instant updates")
    print()
    print("🔒 Security Features:")
    print("   • AES-256 Encryption")
    print("   • CSRF Protection")
    print("   • Rate Limiting")
    print("   • Security Headers")
    print("   • Auto-Updates from GitHub")
    print()
    print("Press Ctrl+C to stop all services")
    print()
    
    # Start main server (this will block)
    start_main_server()

if __name__ == '__main__':
    main()
