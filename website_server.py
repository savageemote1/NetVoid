#!/usr/bin/env python3
"""
Simple web server for NetVoid website
Serves the static website files
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 8080
WEBSITE_DIR = "website"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBSITE_DIR, **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Handle root path
        if self.path == '/':
            self.path = '/website/index.html'
        elif self.path.startswith('/website/'):
            # Remove /website prefix for file serving
            self.path = self.path[8:]  # Remove '/website' (8 characters)
        return super().do_GET()

def start_server():
    """Start the web server"""
    # Check if website directory exists
    if not os.path.exists(WEBSITE_DIR):
        print(f"❌ Error: Website directory '{WEBSITE_DIR}' not found!")
        print("Make sure you're running this from the NetVoid project root.")
        return False
    
    # Don't change directory, serve from current directory
    # os.chdir(WEBSITE_DIR)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("           NETVOID WEBSITE SERVER")
            print("=" * 60)
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print("=" * 60)
            print("📋 Available pages:")
            print(f"   • Homepage: http://localhost:{PORT}/")
            print(f"   • Purchase: http://localhost:{PORT}/purchase.html")
            print("=" * 60)
            print("Press Ctrl+C to stop the server")
            print()
            
            # Try to open browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}')
                print("🚀 Opening website in your default browser...")
            except:
                print("💡 Open your browser and go to the URL above")
            
            print()
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        return True
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: Port {PORT} is already in use!")
            print("Try closing other applications or use a different port.")
        else:
            print(f"❌ Error starting server: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting NetVoid Website Server...")
    
    # Check if we're in the right directory
    if not os.path.exists("website"):
        print("❌ Error: 'website' directory not found!")
        print("Please run this script from the NetVoid project root directory.")
        return
    
    success = start_server()
    if success:
        print("✅ Server stopped successfully")
    else:
        print("❌ Server failed to start")

if __name__ == '__main__':
    main()
