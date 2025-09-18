#!/usr/bin/env python3
"""
GitHub Webhook Receiver for NetVoid Server
Receives webhooks from GitHub and triggers updates
"""

import os
import sys
import json
import subprocess
import hashlib
import hmac
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Configuration
WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', 'NetVoid2024Secret!')
PORT = 8081

def log(message):
    """Log webhook message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def verify_webhook_signature(payload, signature):
    """Verify GitHub webhook signature"""
    if not signature.startswith('sha256='):
        return False
        
    expected = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)

def pull_and_restart():
    """Pull changes and restart server"""
    try:
        log("Webhook received - pulling changes from GitHub...")
        
        # Pull latest changes (try main first, then master)
        result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            result = subprocess.run(['git', 'pull', 'origin', 'master'], 
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            log("Successfully pulled changes from GitHub")
            
            # Restart server
            log("Restarting NetVoid server...")
            
            # Kill existing server
            try:
                subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                             capture_output=True, check=False)
            except:
                pass
            
            # Wait a moment
            import time
            time.sleep(2)
            
            # Start server
            subprocess.Popen([sys.executable, 'secure_web_server.py'], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            log("Server restart initiated")
            return True
        else:
            log(f"Failed to pull changes: {result.stderr}")
            return False
            
    except Exception as e:
        log(f"Error pulling and restarting: {e}")
        return False

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle GitHub webhook"""
    try:
        # Get the signature
        signature = request.headers.get('X-Hub-Signature-256', '')
        
        # Verify signature
        if not verify_webhook_signature(request.data, signature):
            log("Invalid webhook signature")
            return jsonify({'error': 'Invalid signature'}), 403
        
        # Parse webhook data
        data = request.get_json()
        if not data:
            log("No webhook data received")
            return jsonify({'error': 'No data'}), 400
        
        # Check if it's a push to main or master branch
        if (data.get('ref') == 'refs/heads/main' or 
            data.get('ref') == 'refs/heads/master'):
            
            log(f"Push detected to {data.get('ref')}")
            log(f"Commit: {data.get('head_commit', {}).get('id', 'unknown')[:8]}")
            
            # Pull and restart
            if pull_and_restart():
                return jsonify({'status': 'success', 'message': 'Server updated'})
            else:
                return jsonify({'status': 'error', 'message': 'Update failed'}), 500
        else:
            log(f"Ignoring webhook for ref: {data.get('ref')}")
            return jsonify({'status': 'ignored', 'message': 'Not master branch'})
            
    except Exception as e:
        log(f"Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def status():
    """Webhook receiver status"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'webhook_secret_configured': bool(WEBHOOK_SECRET)
    })

@app.route('/')
def index():
    """Webhook receiver info"""
    return """
    <h1>NetVoid Webhook Receiver</h1>
    <p>Status: Running</p>
    <p>Webhook URL: /webhook</p>
    <p>Status URL: /status</p>
    <p>Configure this URL in your GitHub repository webhooks settings.</p>
    """

def main():
    """Main function"""
    print("=" * 60)
    print("    NETVOID WEBHOOK RECEIVER")
    print("=" * 60)
    print()
    print(f"🔗 Webhook URL: http://localhost:{PORT}/webhook")
    print(f"📊 Status URL: http://localhost:{PORT}/status")
    print()
    print("🔧 GitHub Webhook Setup:")
    print("1. Go to your repository settings")
    print("2. Click 'Webhooks'")
    print("3. Add webhook URL: http://your-server:8081/webhook")
    print("4. Content type: application/json")
    print("5. Secret: NetVoid2024Secret!")
    print("6. Select 'Push events'")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    log("Starting webhook receiver...")
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    main()
