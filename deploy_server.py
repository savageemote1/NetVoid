#!/usr/bin/env python3
"""
NetVoid Server Deployment Script
Handles automatic updates and deployment
"""

import os
import sys
import json
import shutil
import subprocess
import time
import requests
import hashlib
from datetime import datetime
from pathlib import Path

# Configuration
DEPLOYMENT_DIR = "deployment"
BACKUP_DIR = "backup"
SERVER_DIR = "."
WEBHOOK_PORT = 8081
GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', 'NetVoid2024Secret!')

class NetVoidDeployer:
    def __init__(self):
        self.server_process = None
        self.deployment_log = []
        
    def log(self, message):
        """Log deployment message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.deployment_log.append(log_message)
        
    def backup_current(self):
        """Backup current server files"""
        self.log("Creating backup of current server...")
        
        if os.path.exists(BACKUP_DIR):
            shutil.rmtree(BACKUP_DIR)
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Backup important files
        backup_files = [
            'server/valid_keys.json',
            'server/server_keys.json',
            'config/bind.json',
            'purchases.json'
        ]
        
        for file_path in backup_files:
            if os.path.exists(file_path):
                backup_path = os.path.join(BACKUP_DIR, file_path)
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                shutil.copy2(file_path, backup_path)
                self.log(f"Backed up: {file_path}")
                
    def stop_server(self):
        """Stop the current server"""
        self.log("Stopping current server...")
        
        try:
            # Try to stop gracefully
            response = requests.get('http://localhost:8080/api/status', timeout=5)
            if response.status_code == 200:
                self.log("Server is running, attempting graceful shutdown...")
                # In a real implementation, you'd send a shutdown signal
        except:
            self.log("Server appears to be stopped")
            
        # Kill any Python processes running the server
        try:
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, check=False)
            self.log("Killed Python processes")
        except:
            pass
            
    def deploy_new_version(self):
        """Deploy new version from deployment directory"""
        self.log("Deploying new version...")
        
        if not os.path.exists(DEPLOYMENT_DIR):
            self.log("No deployment directory found!")
            return False
            
        # Copy new files
        for item in os.listdir(DEPLOYMENT_DIR):
            src = os.path.join(DEPLOYMENT_DIR, item)
            dst = os.path.join(SERVER_DIR, item)
            
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
                
            self.log(f"Deployed: {item}")
            
        return True
        
    def restore_backup(self):
        """Restore from backup if deployment fails"""
        self.log("Restoring from backup...")
        
        if not os.path.exists(BACKUP_DIR):
            self.log("No backup found!")
            return False
            
        # Restore backed up files
        for root, dirs, files in os.walk(BACKUP_DIR):
            for file in files:
                src = os.path.join(root, file)
                dst = src.replace(BACKUP_DIR + os.sep, SERVER_DIR + os.sep)
                
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                self.log(f"Restored: {dst}")
                
        return True
        
    def start_server(self):
        """Start the server"""
        self.log("Starting server...")
        
        try:
            # Start server in background
            self.server_process = subprocess.Popen([
                sys.executable, 'secure_web_server.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            for i in range(10):
                time.sleep(2)
                try:
                    response = requests.get('http://localhost:8080/api/status', timeout=5)
                    if response.status_code == 200:
                        self.log("Server started successfully!")
                        return True
                except:
                    pass
                    
            self.log("Server failed to start!")
            return False
            
        except Exception as e:
            self.log(f"Error starting server: {e}")
            return False
            
    def verify_deployment(self):
        """Verify deployment is working"""
        self.log("Verifying deployment...")
        
        try:
            response = requests.get('http://localhost:8080/api/status', timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log(f"Server status: {data.get('status')}")
                self.log(f"Version: {data.get('version')}")
                return True
            else:
                self.log(f"Server returned status code: {response.status_code}")
                return False
        except Exception as e:
            self.log(f"Verification failed: {e}")
            return False
            
    def deploy(self):
        """Main deployment process"""
        self.log("Starting NetVoid deployment...")
        
        try:
            # Step 1: Backup current
            self.backup_current()
            
            # Step 2: Stop server
            self.stop_server()
            
            # Step 3: Deploy new version
            if not self.deploy_new_version():
                self.log("Deployment failed!")
                self.restore_backup()
                return False
                
            # Step 4: Start server
            if not self.start_server():
                self.log("Failed to start server!")
                self.restore_backup()
                self.start_server()
                return False
                
            # Step 5: Verify deployment
            if not self.verify_deployment():
                self.log("Deployment verification failed!")
                self.restore_backup()
                self.start_server()
                return False
                
            self.log("Deployment completed successfully!")
            return True
            
        except Exception as e:
            self.log(f"Deployment error: {e}")
            self.restore_backup()
            self.start_server()
            return False
            
    def create_webhook_server(self):
        """Create webhook server for GitHub integration"""
        from flask import Flask, request, jsonify
        
        app = Flask(__name__)
        
        @app.route('/webhook', methods=['POST'])
        def webhook():
            """Handle GitHub webhook"""
            try:
                # Verify webhook signature
                signature = request.headers.get('X-Hub-Signature-256', '')
                if not self.verify_webhook_signature(request.data, signature):
                    return jsonify({'error': 'Invalid signature'}), 403
                    
                # Parse webhook data
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No data'}), 400
                    
                # Check if it's a push to main branch
                if (data.get('ref') == 'refs/heads/main' or 
                    data.get('ref') == 'refs/heads/master'):
                    
                    self.log("GitHub webhook received - starting deployment")
                    
                    # Start deployment in background
                    import threading
                    deploy_thread = threading.Thread(target=self.deploy)
                    deploy_thread.daemon = True
                    deploy_thread.start()
                    
                    return jsonify({'status': 'Deployment started'})
                else:
                    return jsonify({'status': 'Ignored - not main branch'})
                    
            except Exception as e:
                self.log(f"Webhook error: {e}")
                return jsonify({'error': str(e)}), 500
                
        @app.route('/status')
        def status():
            """Deployment status"""
            return jsonify({
                'status': 'running',
                'logs': self.deployment_log[-10:]  # Last 10 log entries
            })
            
        return app
        
    def verify_webhook_signature(self, payload, signature):
        """Verify GitHub webhook signature"""
        if not signature.startswith('sha256='):
            return False
            
        expected = 'sha256=' + hashlib.sha256(
            (GITHUB_WEBHOOK_SECRET + payload.decode()).encode()
        ).hexdigest()
        
        return signature == expected
        
    def run_webhook_server(self):
        """Run webhook server"""
        app = self.create_webhook_server()
        self.log(f"Starting webhook server on port {WEBHOOK_PORT}")
        app.run(host='0.0.0.0', port=WEBHOOK_PORT, debug=False)

def main():
    """Main function"""
    deployer = NetVoidDeployer()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'webhook':
        # Run webhook server
        deployer.run_webhook_server()
    else:
        # Run deployment
        success = deployer.deploy()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
