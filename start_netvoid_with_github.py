#!/usr/bin/env python3
"""
NetVoid Server with GitHub Integration
Starts the server with automatic updates from GitHub
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path

def print_banner():
    print("=" * 70)
    print("    NETVOID SERVER WITH GITHUB INTEGRATION")
    print("=" * 70)
    print()

def start_webhook_server():
    """Start webhook server for GitHub integration"""
    print("🔗 Starting webhook server...")
    try:
        subprocess.Popen([
            sys.executable, 'deploy_server.py', 'webhook'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Webhook server started on port 8081")
        return True
    except Exception as e:
        print(f"❌ Failed to start webhook server: {e}")
        return False

def start_auto_updater():
    """Start auto-updater"""
    print("🔄 Starting auto-updater...")
    try:
        subprocess.Popen([
            sys.executable, 'update_system.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Auto-updater started")
        return True
    except Exception as e:
        print(f"❌ Failed to start auto-updater: {e}")
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
    
    print("🔧 Starting NetVoid with GitHub integration...")
    print()
    
    # Check if required files exist
    required_files = [
        'secure_web_server.py',
        'deploy_server.py',
        'update_system.py'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file not found: {file}")
            print("Please run setup_github_integration.py first")
            return
    
    print("✅ All required files found")
    print()
    
    # Start webhook server
    if not start_webhook_server():
        print("⚠️  Webhook server failed to start - continuing without it")
    
    time.sleep(2)
    
    # Start auto-updater
    if not start_auto_updater():
        print("⚠️  Auto-updater failed to start - continuing without it")
    
    time.sleep(2)
    
    print()
    print("🌐 NetVoid Server URLs:")
    print("   • Homepage: http://localhost:8080")
    print("   • Purchase: http://localhost:8080/purchase")
    print("   • Admin: http://localhost:8080/admin")
    print("   • API: http://localhost:8080/api/status")
    print("   • Webhook: http://localhost:8081/webhook")
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
