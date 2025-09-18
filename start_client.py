#!/usr/bin/env python3
"""
NetVoid Client Launcher
Starts the NetVoid client application
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("    NETVOID CLIENT LAUNCHER")
    print("=" * 60)
    print()

def check_server_connection():
    """Check if NetVoid server is running"""
    try:
        import requests
        response = requests.get('http://localhost:8080/api/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server connected: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

def start_client():
    """Start the NetVoid client"""
    print("🚀 Starting NetVoid client...")
    
    try:
        # Check if client file exists
        client_path = Path("client/encrypted_main.py")
        if not client_path.exists():
            print("❌ Client file not found: client/encrypted_main.py")
            return False
        
        # Start client
        subprocess.run([sys.executable, str(client_path)])
        return True
        
    except Exception as e:
        print(f"❌ Failed to start client: {e}")
        return False

def main():
    """Main function"""
    print_banner()
    
    print("🔧 Starting NetVoid Client...")
    print()
    
    # Check server connection
    print("🔍 Checking server connection...")
    if not check_server_connection():
        print()
        print("⚠️  Server not running!")
        print("   Please start the server first:")
        print("   python start_netvoid.py")
        print()
        choice = input("Continue anyway? (y/n): ").lower()
        if choice != 'y':
            return
    
    print()
    
    # Start client
    if start_client():
        print("✅ Client started successfully!")
    else:
        print("❌ Failed to start client")

if __name__ == '__main__':
    main()
