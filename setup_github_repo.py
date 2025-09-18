#!/usr/bin/env python3
"""
Setup GitHub Repository for NetVoid Server
Helps configure the GitHub repository for auto-updates
"""

import os
import subprocess
import sys

def print_banner():
    print("=" * 60)
    print("    NETVOID GITHUB REPOSITORY SETUP")
    print("=" * 60)
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

def get_remote_url():
    """Get current remote URL"""
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except:
        return None

def set_github_repo():
    """Set up GitHub repository"""
    print("🔧 Setting up GitHub repository...")
    print()
    
    # Check if remote already exists
    current_remote = get_remote_url()
    if current_remote:
        print(f"Current remote: {current_remote}")
        choice = input("Do you want to change it? (y/n): ").lower()
        if choice != 'y':
            return current_remote
    
    print("📋 GitHub Repository Setup:")
    print("1. Go to https://github.com/new")
    print("2. Create a new repository named 'NetVoidServer'")
    print("3. Make it public or private (your choice)")
    print("4. Don't initialize with README (we already have one)")
    print()
    
    repo_url = input("Enter your GitHub repository URL (e.g., https://github.com/username/NetVoidServer.git): ").strip()
    
    if not repo_url:
        print("❌ No URL provided")
        return None
        
    if not repo_url.startswith('https://github.com/') or not repo_url.endswith('.git'):
        print("❌ Invalid GitHub URL format")
        return None
    
    # Set remote origin
    try:
        # Remove existing remote if any
        subprocess.run(['git', 'remote', 'remove', 'origin'], capture_output=True)
        
        # Add new remote
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
        print("✅ Remote origin set")
        
        # Extract repo name for environment variable
        repo_name = repo_url.replace('https://github.com/', '').replace('.git', '')
        return repo_name
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting remote: {e}")
        return None

def push_to_github():
    """Push code to GitHub"""
    print("🚀 Pushing code to GitHub...")
    
    try:
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', 'Initial NetVoid server with GitHub integration'], check=True)
        
        # Push to GitHub
        subprocess.run(['git', 'push', '-u', 'origin', 'master'], check=True)
        
        print("✅ Code pushed to GitHub successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing to GitHub: {e}")
        return False

def create_env_file(repo_name):
    """Create .env file with GitHub configuration"""
    env_content = f"""# NetVoid Server Environment Variables
# GitHub Integration
GITHUB_REPO={repo_name}
GITHUB_TOKEN=your-github-token-here
GITHUB_WEBHOOK_SECRET=NetVoid2024Secret!

# Server Configuration
NETVOID_SECRET_KEY=your-secret-key-here
NETVOID_JWT_SECRET=your-jwt-secret-here
NETVOID_ENCRYPTION_KEY=your-encryption-key-here
NETVOID_ADMIN_PASSWORD=NetVoidAdmin2024!

# Server Settings
HOST=127.0.0.1
PORT=8080
DEBUG=False
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ .env file created with GitHub configuration")

def test_github_connection(repo_name):
    """Test GitHub connection"""
    print("🔍 Testing GitHub connection...")
    
    try:
        import requests
        url = f"https://api.github.com/repos/{repo_name}"
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
    
    print("🔧 Setting up GitHub repository for NetVoid Server...")
    print()
    
    # Check git status
    if not check_git_status():
        print("Please run this from a git repository directory")
        return
    
    # Set up GitHub repository
    repo_name = set_github_repo()
    if not repo_name:
        print("❌ Failed to set up GitHub repository")
        return
    
    print()
    
    # Test connection
    if test_github_connection(repo_name):
        print("✅ GitHub repository is accessible")
    else:
        print("⚠️  GitHub repository may not be accessible yet")
        print("   Make sure the repository exists and is public")
    
    print()
    
    # Ask if user wants to push
    choice = input("Do you want to push your code to GitHub now? (y/n): ").lower()
    if choice == 'y':
        if push_to_github():
            print("🎉 GitHub setup complete!")
        else:
            print("❌ Failed to push to GitHub")
            return
    else:
        print("💡 You can push later with: git push -u origin master")
    
    # Create environment file
    create_env_file(repo_name)
    
    print()
    print("📋 Next steps:")
    print("1. Update .env file with your GitHub token (optional)")
    print("2. Start the server with GitHub integration:")
    print("   python start_netvoid_with_github.py")
    print("3. Or start auto-updater separately:")
    print("   python update_system.py")
    print()
    print("🔒 Security reminder:")
    print("- Keep your .env file secure and don't commit it")
    print("- Use GitHub tokens for private repositories")
    print("- Enable webhooks for instant updates")
    print()
    print("✅ NetVoid is ready for GitHub integration!")

if __name__ == '__main__':
    main()
