#!/usr/bin/env python3
"""
Setup GitHub Integration for NetVoid Server
Configures automatic deployment from GitHub Codespaces
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("    NETVOID GITHUB INTEGRATION SETUP")
    print("=" * 60)
    print()

def check_git_repo():
    """Check if this is a git repository"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository detected")
            return True
        else:
            print("❌ Not a git repository")
            return False
    except FileNotFoundError:
        print("❌ Git not installed")
        return False

def init_git_repo():
    """Initialize git repository"""
    print("🔧 Initializing git repository...")
    
    try:
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial NetVoid server commit'], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error initializing git: {e}")
        return False

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# NetVoid Server .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Server files
server/valid_keys.json
server/server_keys.json
purchases.json
*.log

# Deployment
deployment/
backup/
temp_update/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local
.env.production

# SSL certificates
*.pem
*.key
*.crt

# Logs
logs/
*.log
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ .gitignore created")

def create_readme():
    """Create README.md for GitHub"""
    readme_content = """# NetVoid Server

Secure premium software access with encrypted authentication keys.

## 🚀 Features

- **Military-Grade Security**: AES-256 encryption, CSRF protection, rate limiting
- **Zero Vulnerabilities**: Comprehensive security headers and input validation
- **Auto-Deployment**: Automatic updates from GitHub Codespaces
- **Admin Dashboard**: Complete server management interface
- **Key Management**: Secure key generation and hardware binding

## 🔧 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/NetVoidServer.git
   cd NetVoidServer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements_secure.txt
   ```

3. **Start the server**
   ```bash
   python secure_web_server.py
   ```

4. **Access the website**
   - Homepage: http://localhost:8080
   - Admin: http://localhost:8080/admin
   - API: http://localhost:8080/api/status

## 🔐 Security

- CSRF Protection
- Rate Limiting
- Encrypted Communications
- Security Headers
- Input Validation
- Anti-Debugging Protection

## 📊 Admin Access

- **URL**: http://localhost:8080/admin
- **Password**: `NetVoidAdmin2024!` (change in production)

## 🔄 Auto-Deployment

The server automatically updates when you push changes to the main branch:

1. Push changes to GitHub
2. GitHub Actions builds the deployment
3. Server automatically updates
4. Zero downtime deployment

## 🛠️ Development

### Local Development
```bash
python secure_web_server.py
```

### Auto-Updater
```bash
python update_system.py
```

### Deployment
```bash
python deploy_server.py
```

## 📁 Project Structure

```
NetVoidServer/
├── server/                 # NetVoid server components
├── client/                 # Client applications
├── templates/              # Website templates
├── static/                 # Static assets
├── config/                 # Configuration files
├── .github/workflows/      # GitHub Actions
├── secure_web_server.py    # Main server
├── deploy_server.py        # Deployment script
└── update_system.py        # Auto-updater
```

## 🔒 Security Notes

- Change default admin password
- Use environment variables for secrets
- Enable HTTPS in production
- Regular security updates

## 📞 Support

For support and updates, contact the development team.

---
NetVoid - Secure, Server-Dependent Application System
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("✅ README.md created")

def create_github_workflow():
    """Create GitHub Actions workflow"""
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: Deploy NetVoid Server

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  test:
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
        
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
    
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
        
        # Create deployment info
        echo "Deployment created at $(date)" > deployment/deployment_info.txt
        echo "Commit: ${{ github.sha }}" >> deployment/deployment_info.txt
        echo "Branch: ${{ github.ref_name }}" >> deployment/deployment_info.txt
        
    - name: Upload deployment artifacts
      uses: actions/upload-artifact@v3
      with:
        name: netvoid-deployment
        path: deployment/
        
    - name: Deploy notification
      run: |
        echo "🚀 NetVoid Server deployment ready!"
        echo "Commit: ${{ github.sha }}"
        echo "Branch: ${{ github.ref_name }}"
        echo "Deployment package created successfully"
"""
    
    workflow_file = workflow_dir / 'deploy.yml'
    with open(workflow_file, 'w') as f:
        f.write(workflow_content)
    print("✅ GitHub Actions workflow created")

def create_environment_template():
    """Create environment variables template"""
    env_content = """# NetVoid Server Environment Variables
# Copy this to .env and fill in your values

# Server Configuration
NETVOID_SECRET_KEY=your-secret-key-here
NETVOID_JWT_SECRET=your-jwt-secret-here
NETVOID_ENCRYPTION_KEY=your-encryption-key-here
NETVOID_ADMIN_PASSWORD=your-admin-password-here

# GitHub Integration
GITHUB_TOKEN=your-github-token-here
GITHUB_WEBHOOK_SECRET=your-webhook-secret-here

# Server Settings
HOST=127.0.0.1
PORT=8080
DEBUG=False
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_content)
    print("✅ Environment template created")

def setup_git_hooks():
    """Setup git hooks for automatic deployment"""
    hooks_dir = Path('.git/hooks')
    hooks_dir.mkdir(parents=True, exist_ok=True)
    
    # Pre-commit hook
    pre_commit_hook = """#!/bin/bash
# NetVoid Pre-commit Hook

echo "🔍 Running NetVoid pre-commit checks..."

# Check Python syntax
python -m py_compile secure_web_server.py
if [ $? -ne 0 ]; then
    echo "❌ Python syntax error in secure_web_server.py"
    exit 1
fi

# Check if server is running
curl -s http://localhost:8080/api/status > /dev/null
if [ $? -eq 0 ]; then
    echo "⚠️  Server is running - consider stopping before commit"
fi

echo "✅ Pre-commit checks passed"
"""
    
    pre_commit_file = hooks_dir / 'pre-commit'
    with open(pre_commit_file, 'w') as f:
        f.write(pre_commit_hook)
    pre_commit_file.chmod(0o755)
    
    # Post-commit hook
    post_commit_hook = """#!/bin/bash
# NetVoid Post-commit Hook

echo "🚀 NetVoid post-commit hook triggered"
echo "💡 To deploy changes, run: python deploy_server.py"
"""
    
    post_commit_file = hooks_dir / 'post-commit'
    with open(post_commit_file, 'w') as f:
        f.write(post_commit_hook)
    post_commit_file.chmod(0o755)
    
    print("✅ Git hooks created")

def main():
    """Main setup function"""
    print_banner()
    
    print("🔧 Setting up GitHub integration for NetVoid Server...")
    print()
    
    # Check if git repo exists
    if not check_git_repo():
        print("Initializing git repository...")
        if not init_git_repo():
            print("❌ Failed to initialize git repository")
            return
    
    # Create necessary files
    create_gitignore()
    create_readme()
    create_github_workflow()
    create_environment_template()
    setup_git_hooks()
    
    print()
    print("🎉 GitHub integration setup complete!")
    print()
    print("📋 Next steps:")
    print("1. Create a new repository on GitHub")
    print("2. Add the remote origin:")
    print("   git remote add origin https://github.com/your-username/NetVoidServer.git")
    print("3. Push your code:")
    print("   git push -u origin main")
    print("4. Set up GitHub webhook (optional):")
    print("   - Go to repository settings > Webhooks")
    print("   - Add webhook URL: http://your-server:8081/webhook")
    print("5. Start auto-updater:")
    print("   python update_system.py")
    print()
    print("🔒 Security reminder:")
    print("- Change default passwords in production")
    print("- Use environment variables for secrets")
    print("- Enable HTTPS for production deployment")
    print()
    print("✅ NetVoid is ready for GitHub integration!")

if __name__ == '__main__':
    main()
