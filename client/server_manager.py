#!/usr/bin/env python3
"""
NetVoid Server Manager
Manages the authentication server and provides admin functions
"""

import requests
import json
import time
import os
import sys
from pathlib import Path

SERVER_URL = "http://127.0.0.1:8000"
ADMIN_KEY = "NetVoidAdmin2024"

def print_banner():
    print("=" * 60)
    print("           NETVOID SERVER MANAGER")
    print("=" * 60)
    print()

def check_server_status():
    """Check if server is running"""
    try:
        response = requests.get(f"{SERVER_URL}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('code', 0)
        return 0
    except:
        return 0

def start_server():
    """Start the authentication server"""
    print("🚀 Starting NetVoid Authentication Server...")
    
    # Check if server is already running
    if check_server_status() == 1:
        print("✅ Server is already running")
        return True
    
    # Start server in background
    import subprocess
    import threading
    
    def run_server():
        os.chdir('server')
        subprocess.run([sys.executable, 'start_server.py'])
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    for i in range(10):
        time.sleep(1)
        if check_server_status() == 1:
            print("✅ Server started successfully")
            return True
        print(f"   Attempt {i+1}/10...")
    
    print("❌ Failed to start server")
    return False

def stop_server():
    """Stop the server (set offline)"""
    print("🛑 Stopping server...")
    
    try:
        response = requests.post(f"{SERVER_URL}/api/server_offline", 
                               json={"admin_key": ADMIN_KEY}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 1:
                print("✅ Server stopped")
                return True
    except:
        pass
    
    print("❌ Failed to stop server")
    return False

def restart_server():
    """Restart the server"""
    print("🔄 Restarting server...")
    stop_server()
    time.sleep(2)
    return start_server()

def generate_key():
    """Generate a new key"""
    print("🔑 Generating new key...")
    
    try:
        response = requests.post(f"{SERVER_URL}/api/generate_key", 
                               json={"admin_key": ADMIN_KEY}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 1:
                key = data.get('key')
                print(f"✅ New key generated: {key}")
                return key
    except Exception as e:
        print(f"❌ Failed to generate key: {e}")
    
    return None

def get_server_stats():
    """Get server statistics"""
    print("📊 Getting server statistics...")
    
    try:
        response = requests.get(f"{SERVER_URL}/api/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Total valid keys: {data.get('total_valid_keys', 0)}")
            print(f"✅ Bound keys: {data.get('bound_keys', 0)}")
            print(f"✅ Unused keys: {data.get('unused_keys', 0)}")
            return data
    except Exception as e:
        print(f"❌ Failed to get stats: {e}")
    
    return None

def list_keys():
    """List all valid keys"""
    print("📋 Listing all valid keys...")
    
    try:
        response = requests.get(f"{SERVER_URL}/api/keys", timeout=5)
        if response.status_code == 200:
            data = response.json()
            keys = data.get('valid_keys', [])
            print(f"✅ Found {len(keys)} valid keys:")
            for i, key in enumerate(keys, 1):
                print(f"   {i}. {key}")
            return keys
    except Exception as e:
        print(f"❌ Failed to list keys: {e}")
    
    return []

def show_menu():
    """Show the main menu"""
    print("\n📋 Server Manager Menu:")
    print("1. Start Server")
    print("2. Stop Server")
    print("3. Restart Server")
    print("4. Generate New Key")
    print("5. Show Server Stats")
    print("6. List All Keys")
    print("7. Check Server Status")
    print("8. Exit")
    print()

def main():
    """Main server manager function"""
    print_banner()
    
    # Check if server is running
    if check_server_status() == 1:
        print("✅ Server is currently online")
    else:
        print("❌ Server is offline")
    
    while True:
        show_menu()
        choice = input("Select an option (1-8): ").strip()
        
        if choice == "1":
            start_server()
        elif choice == "2":
            stop_server()
        elif choice == "3":
            restart_server()
        elif choice == "4":
            generate_key()
        elif choice == "5":
            get_server_stats()
        elif choice == "6":
            list_keys()
        elif choice == "7":
            if check_server_status() == 1:
                print("✅ Server is online")
            else:
                print("❌ Server is offline")
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    main()
