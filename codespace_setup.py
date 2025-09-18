#!/usr/bin/env python3
"""
GitHub Codespace Setup for NetVoid Server
Configures the server for GitHub Codespace deployment
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def print_banner():
    print("=" * 70)
    print("    NETVOID GITHUB CODESPACE SETUP")
    print("=" * 70)
    print()

def check_codespace_environment():
    """Check if running in GitHub Codespace"""
    codespace_name = os.getenv('CODESPACE_NAME')
    codespace_domain = os.getenv('CODESPACE_DOMAIN')
    
    if codespace_name and codespace_domain:
        print(f"✅ GitHub Codespace detected: {codespace_name}")
        print(f"   Domain: {codespace_domain}")
        return True
    else:
        print("⚠️  Not running in GitHub Codespace")
        return False

def create_codespace_config():
    """Create Codespace-specific configuration"""
    print("🔧 Creating Codespace configuration...")
    
    # Create .devcontainer directory
    devcontainer_dir = Path('.devcontainer')
    devcontainer_dir.mkdir(exist_ok=True)
    
    # Create devcontainer.json
    devcontainer_config = {
        "name": "NetVoid Server",
        "image": "mcr.microsoft.com/devcontainers/python:3.11",
        "features": {
            "ghcr.io/devcontainers/features/git:1": {},
            "ghcr.io/devcontainers/features/github-cli:1": {}
        },
        "customizations": {
            "vscode": {
                "extensions": [
                    "ms-python.python",
                    "ms-python.flake8",
                    "ms-python.black-formatter",
                    "ms-vscode.vscode-json"
                ],
                "settings": {
                    "python.defaultInterpreterPath": "/usr/local/bin/python",
                    "python.linting.enabled": True,
                    "python.linting.flake8Enabled": True,
                    "python.formatting.provider": "black"
                }
            }
        },
        "forwardPorts": [8080, 8081],
        "portsAttributes": {
            "8080": {
                "label": "NetVoid Server",
                "onAutoForward": "notify"
            },
            "8081": {
                "label": "Webhook Server",
                "onAutoForward": "silent"
            }
        },
        "postCreateCommand": "pip install -r requirements_secure.txt",
        "remoteUser": "vscode"
    }
    
    with open(devcontainer_dir / 'devcontainer.json', 'w') as f:
        json.dump(devcontainer_config, f, indent=2)
    
    print("✅ .devcontainer/devcontainer.json created")
    
    # Create Codespace environment file
    codespace_env = """# NetVoid Server Codespace Environment
# GitHub Integration
GITHUB_REPO=savageemote1/NetVoid
GITHUB_TOKEN=${GITHUB_TOKEN}
GITHUB_WEBHOOK_SECRET=NetVoid2024Secret!

# Server Configuration
NETVOID_SECRET_KEY=NetVoidCodespace2024!
NETVOID_JWT_SECRET=NetVoidJWT2024!
NETVOID_ENCRYPTION_KEY=NetVoidEncryption2024!
NETVOID_ADMIN_PASSWORD=NetVoidAdmin2024!

# Server Settings
HOST=0.0.0.0
PORT=8080
DEBUG=False

# Codespace Settings
CODESPACE_NAME=${CODESPACE_NAME}
CODESPACE_DOMAIN=${CODESPACE_DOMAIN}
"""
    
    with open('.env.codespace', 'w', encoding='utf-8') as f:
        f.write(codespace_env)
    
    print("✅ .env.codespace created")
    
    # Create Codespace startup script
    startup_script = """#!/bin/bash
# NetVoid Server Codespace Startup Script

echo "🚀 Starting NetVoid Server in Codespace..."

# Load environment variables
if [ -f .env.codespace ]; then
    export $(cat .env.codespace | grep -v '^#' | xargs)
fi

# Install dependencies
pip install -r requirements_secure.txt

# Start the server
python secure_web_server.py
"""
    
    with open('start_codespace.sh', 'w', encoding='utf-8') as f:
        f.write(startup_script)
    
    os.chmod('start_codespace.sh', 0o755)
    print("✅ start_codespace.sh created")

def create_codespace_workflow():
    """Create Codespace-specific GitHub workflow"""
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    codespace_workflow = """name: Deploy to Codespace

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  deploy-to-codespace:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements_secure.txt
        
    - name: Run tests
      run: |
        python -c "import sys; print('Python version:', sys.version)"
        python -c "import flask; print('Flask version:', flask.__version__)"
        python -c "import Crypto; print('PyCrypto version:', Crypto.__version__)"
        
    - name: Create deployment package
      run: |
        mkdir -p deployment
        cp -r server deployment/
        cp -r client deployment/
        cp -r config deployment/
        cp -r templates deployment/
        cp -r static deployment/
        cp secure_web_server.py deployment/
        cp requirements_secure.txt deployment/
        cp install.py deployment/
        cp *.bat deployment/
        cp start_codespace.sh deployment/
        cp .env.codespace deployment/
        
        # Create deployment info
        echo "Deployment created at $(date)" > deployment/deployment_info.txt
        echo "Commit: ${{ github.sha }}" >> deployment/deployment_info.txt
        echo "Branch: ${{ github.ref_name }}" >> deployment/deployment_info.txt
        echo "Codespace: ${{ github.codespace_name }}" >> deployment/deployment_info.txt
        
    - name: Upload deployment artifacts
      uses: actions/upload-artifact@v3
      with:
        name: netvoid-codespace-deployment
        path: deployment/
        
    - name: Deploy notification
      run: |
        echo "🚀 NetVoid Server deployment ready for Codespace!"
        echo "Repository: savageemote1/NetVoid"
        echo "Commit: ${{ github.sha }}"
        echo "Branch: ${{ github.ref_name }}"
        echo "Deployment package created successfully"
"""
    
    with open(workflow_dir / 'codespace-deploy.yml', 'w', encoding='utf-8') as f:
        f.write(codespace_workflow)
    
    print("✅ .github/workflows/codespace-deploy.yml created")

def setup_git_remote():
    """Set up git remote for the repository"""
    print("🔧 Setting up git remote...")
    
    try:
        # Check if remote already exists
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            current_remote = result.stdout.strip()
            print(f"Current remote: {current_remote}")
            
            if 'savageemote1/NetVoid' in current_remote:
                print("✅ Remote already configured correctly")
                return True
            else:
                print("⚠️  Remote doesn't match expected repository")
        else:
            print("No remote origin found")
            
        # Set the correct remote
        subprocess.run(['git', 'remote', 'remove', 'origin'], capture_output=True)
        subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/savageemote1/NetVoid.git'], check=True)
        print("✅ Remote origin set to https://github.com/savageemote1/NetVoid.git")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting remote: {e}")
        return False

def test_github_connection():
    """Test connection to GitHub repository"""
    print("🔍 Testing GitHub connection...")
    
    try:
        import requests
        url = "https://api.github.com/repos/savageemote1/NetVoid"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Repository found: {data['full_name']}")
            print(f"   Description: {data.get('description', 'No description')}")
            print(f"   Private: {data['private']}")
            print(f"   Stars: {data['stargazers_count']}")
            return True
        else:
            print(f"❌ Repository not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    print("🔧 Setting up NetVoid Server for GitHub Codespace...")
    print()
    
    # Check Codespace environment
    is_codespace = check_codespace_environment()
    
    # Test GitHub connection
    if test_github_connection():
        print("✅ GitHub repository is accessible")
    else:
        print("⚠️  GitHub repository may not be accessible")
        print("   Make sure the repository exists and is public")
    
    print()
    
    # Set up git remote
    if setup_git_remote():
        print("✅ Git remote configured")
    else:
        print("❌ Failed to configure git remote")
        return
    
    # Create Codespace configuration
    create_codespace_config()
    create_codespace_workflow()
    
    print()
    print("🎉 Codespace setup complete!")
    print()
    print("📋 Next steps:")
    print("1. Commit and push your changes:")
    print("   git add .")
    print("   git commit -m 'Add Codespace configuration'")
    print("   git push origin master")
    print()
    print("2. Start the server in Codespace:")
    print("   python secure_web_server.py")
    print("   # or")
    print("   ./start_codespace.sh")
    print()
    print("3. Access your server:")
    print("   • Main server: http://localhost:8080")
    print("   • Admin panel: http://localhost:8080/admin")
    print("   • API status: http://localhost:8080/api/status")
    print()
    print("4. For auto-updates from GitHub:")
    print("   python update_system.py")
    print()
    print("🔒 Security reminder:")
    print("- Change default passwords in production")
    print("- Use environment variables for secrets")
    print("- Enable HTTPS for production deployment")
    print()
    print("✅ NetVoid is ready for GitHub Codespace!")

if __name__ == '__main__':
    main()
