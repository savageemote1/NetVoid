#!/usr/bin/env python3
"""
NetVoid Package Installer
Installs the complete NetVoid system
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("           NETVOID PACKAGE INSTALLER")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    packages = [
        'flask',
        'pycryptodome',
        'requests',
        'tkinter'
    ]
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def setup_directories():
    """Setup required directories"""
    print("📁 Setting up directories...")
    
    directories = [
        'config',
        'logs',
        'temp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def generate_initial_keys():
    """Generate initial authentication keys"""
    print("🔑 Generating initial keys...")
    
    try:
        # Create a simple key generator
        import random
        import string
        
        def generate_key():
            chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
            key_parts = []
            for i in range(4):
                part = ''.join(random.choice(chars) for _ in range(4))
                key_parts.append(part)
            return '-'.join(key_parts)
        
        # Generate 10 initial keys
        keys = [generate_key() for _ in range(10)]
        
        # Save to server directory
        server_keys_file = Path('server/valid_keys.json')
        with open(server_keys_file, 'w') as f:
            import json
            json.dump(keys, f, indent=2)
        
        print(f"✅ Generated {len(keys)} initial keys")
        print("Sample keys:")
        for i, key in enumerate(keys[:3]):
            print(f"   {i+1}. {key}")
        if len(keys) > 3:
            print(f"   ... and {len(keys) - 3} more")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating keys: {e}")
        return False

def create_startup_scripts():
    """Create startup scripts"""
    print("📝 Creating startup scripts...")
    
    # Server startup script
    server_script = """@echo off
echo Starting NetVoid Server...
cd server
python start_server.py
pause
"""
    
    with open('start_server.bat', 'w') as f:
        f.write(server_script)
    
    # Client startup script
    client_script = """@echo off
echo Starting NetVoid Client...
cd client
python encrypted_main.py
pause
"""
    
    with open('start_client.bat', 'w') as f:
        f.write(client_script)
    
    print("✅ Created startup scripts")
    return True

def main():
    """Main installation function"""
    print_banner()
    
    print("🚀 Starting NetVoid installation...")
    print()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Installation failed: Could not install dependencies")
        return
    
    # Setup directories
    if not setup_directories():
        print("❌ Installation failed: Could not setup directories")
        return
    
    # Generate initial keys
    if not generate_initial_keys():
        print("❌ Installation failed: Could not generate keys")
        return
    
    # Create startup scripts
    if not create_startup_scripts():
        print("❌ Installation failed: Could not create startup scripts")
        return
    
    print()
    print("🎉 Installation completed successfully!")
    print()
    print("📋 Next steps:")
    print("1. Start the server: run start_server.bat or python server_manager.py")
    print("2. Run the client: run start_client.bat or python encrypted_main.py")
    print("3. Use one of the generated keys to authenticate")
    print()
    print("🛠️  Server management: python server_manager.py")
    print("📚 Documentation: Check the docs/ directory")
    print()
    print("✅ NetVoid is ready to use!")

if __name__ == '__main__':
    main()
