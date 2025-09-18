#!/usr/bin/env python3
"""
Create GitHub Repository for NetVoid Server
Helps create the GitHub repository and push the code
"""

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

def print_banner():
    print("=" * 70)
    print("    CREATE GITHUB REPOSITORY FOR NETVOID")
    print("=" * 70)
    print()

def check_git_status():
    """Check git status"""
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

def create_github_repository():
    """Guide user to create GitHub repository"""
    print("🔧 Creating GitHub Repository...")
    print()
    print("📋 Steps to create your GitHub repository:")
    print("1. Go to https://github.com/new")
    print("2. Repository name: NetVoid")
    print("3. Description: Secure premium software access with encrypted authentication keys")
    print("4. Make it Public (recommended) or Private")
    print("5. DO NOT initialize with README, .gitignore, or license")
    print("6. Click 'Create repository'")
    print()
    
    input("Press Enter after you've created the repository...")
    
    # Open GitHub in browser
    try:
        webbrowser.open("https://github.com/new")
        print("🌐 Opening GitHub in your browser...")
    except:
        print("⚠️  Could not open browser automatically")
        print("   Please go to https://github.com/new manually")

def test_repository_access():
    """Test if repository is accessible"""
    print("🔍 Testing repository access...")
    
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

def push_to_github():
    """Push code to GitHub"""
    print("🚀 Pushing code to GitHub...")
    
    try:
        # Check if remote exists
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            # Add remote
            subprocess.run(['git', 'remote', 'add', 'origin', 
                          'https://github.com/savageemote1/NetVoid.git'], check=True)
            print("✅ Remote origin added")
        
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Files staged")
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', 'Initial NetVoid server with GitHub integration'], check=True)
        print("✅ Changes committed")
        
        # Push to GitHub
        subprocess.run(['git', 'push', '-u', 'origin', 'master'], check=True)
        print("✅ Code pushed to GitHub successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing to GitHub: {e}")
        return False

def create_readme():
    """Create a proper README for GitHub"""
    readme_content = """# NetVoid Server

Secure premium software access with encrypted authentication keys.

## 🚀 Features

- **Military-Grade Security**: AES-256 encryption, CSRF protection, rate limiting
- **Zero Vulnerabilities**: Comprehensive security headers and input validation
- **Auto-Deployment**: Automatic updates from GitHub Codespaces
- **Admin Dashboard**: Complete server management interface
- **Key Management**: Secure key generation and hardware binding

## 🔧 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/savageemote1/NetVoid.git
   cd NetVoid
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

The server automatically updates when you push changes to the master branch:

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
python local_updater.py
```

### GitHub Integration
```bash
python update_system.py
```

## 📁 Project Structure

```
NetVoid/
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
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ README.md created")

def main():
    """Main function"""
    print_banner()
    
    print("🔧 Setting up GitHub repository for NetVoid Server...")
    print()
    
    # Check git status
    if not check_git_status():
        print("Please run this from a git repository directory")
        return
    
    # Create README
    create_readme()
    
    # Guide user to create repository
    create_github_repository()
    
    print()
    print("⏳ Waiting for repository to be created...")
    input("Press Enter when you've created the repository...")
    
    # Test repository access
    if test_repository_access():
        print("✅ Repository is accessible")
    else:
        print("⚠️  Repository may not be accessible yet")
        print("   Make sure the repository exists and is public")
        choice = input("Continue anyway? (y/n): ").lower()
        if choice != 'y':
            return
    
    print()
    
    # Push to GitHub
    if push_to_github():
        print("🎉 GitHub repository setup complete!")
        print()
        print("📋 Next steps:")
        print("1. Your repository is now at: https://github.com/savageemote1/NetVoid")
        print("2. Start the server with auto-updates:")
        print("   python update_system.py")
        print("3. Or use local auto-updater:")
        print("   python local_updater.py")
        print()
        print("✅ NetVoid is ready for GitHub integration!")
    else:
        print("❌ Failed to push to GitHub")
        print("   Please check your repository settings and try again")

if __name__ == '__main__':
    main()
