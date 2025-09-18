#!/usr/bin/env python3
"""
NetVoid Server Starter
This script starts the authentication server and generates initial keys
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Add the parent directory to the path to import telegram modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def generate_initial_keys():
    """Generate initial keys using the telegram reporter"""
    try:
        from python_core._private.telegram_reporter import generate_keys, save_valid_keys
        
        # Generate 20 keys for the server
        keys = generate_keys(20)
        
        # Save to server's valid_keys.json
        keys_file = os.path.join(os.path.dirname(__file__), 'valid_keys.json')
        with open(keys_file, 'w') as f:
            json.dump(keys, f, indent=2)
        
        print(f"Generated {len(keys)} keys for server")
        return keys
    except Exception as e:
        print(f"Error generating keys: {e}")
        return []

def start_server():
    """Start the Flask server"""
    try:
        print("Starting NetVoid Authentication Server...")
        print("Server will be available at: http://127.0.0.1:8000")
        print("API Endpoints:")
        print("  POST /api/auth - Authentication")
        print("  GET  /api/keys - Get valid keys")
        print("  GET  /api/stats - Server statistics")
        print("  GET  /api/health - Health check")
        print("\nPress Ctrl+C to stop the server")
        
        # Start the server
        from app import app
        app.run(host='127.0.0.1', port=8000, debug=False)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == '__main__':
    # Generate keys first
    keys = generate_initial_keys()
    if keys:
        print(f"Keys generated successfully: {len(keys)}")
        print("Sample keys:")
        for i, key in enumerate(keys[:5]):  # Show first 5 keys
            print(f"  {i+1}. {key}")
        if len(keys) > 5:
            print(f"  ... and {len(keys) - 5} more")
    else:
        print("Warning: No keys generated, server will start with empty key list")
    
    print("\n" + "="*50)
    start_server()
