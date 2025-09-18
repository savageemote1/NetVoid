#!/usr/bin/env python3
"""
Simple web server for NetVoid website
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory="website", **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    """Start the web server"""
    print("🚀 Starting NetVoid Website Server...")
    print("=" * 50)
    
    # Check if website directory exists
    if not os.path.exists("website"):
        print("❌ Error: 'website' directory not found!")
        return
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"📁 Serving files from: {os.path.abspath('website')}")
            print("=" * 50)
            print("📋 Available pages:")
            print(f"   • Homepage: http://localhost:{PORT}/")
            print(f"   • Purchase: http://localhost:{PORT}/purchase.html")
            print("=" * 50)
            print("Press Ctrl+C to stop the server")
            print()
            
            # Try to open browser
            try:
                webbrowser.open(f'http://localhost:{PORT}')
                print("🚀 Opening website in your browser...")
            except:
                print("💡 Open your browser and go to the URL above")
            
            print()
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 48:
            print(f"❌ Error: Port {PORT} is already in use!")
        else:
            print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    main()
