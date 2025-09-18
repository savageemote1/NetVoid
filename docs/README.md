# NetVoid Complete Package

This package contains the complete NetVoid system with server dependency and encryption.

## 📁 Package Contents

### Server (Backbone)
- `app.py` - Main authentication server
- `start_server.py` - Server startup script
- `requirements.txt` - Server dependencies

### Client (Dependent)
- `encrypted_main.py` - Main encrypted client
- `server_manager.py` - Server management tool

### Configuration
- `version.txt` - Version information
- `bind.json` - Key binding data

## 🚀 Installation

1. **Extract the package** to your desired location
2. **Run the installer**: `python install.py`
3. **Start the server**: `python server_manager.py`
4. **Run the client**: `python encrypted_main.py`

## 🔐 Security Features

- **Server Dependency**: Client returns Code 0 if server is offline
- **Encrypted Communication**: All data encrypted between client and server
- **HWID Binding**: Keys are bound to specific hardware IDs
- **Anti-Reverse Engineering**: Code is obfuscated and encrypted
- **Version Control**: Server manages all updates

## 📊 System Requirements

- Python 3.7+
- Windows 10/11
- Administrator privileges
- Internet connection (for server communication)

## 🛠️ Management

- Use `server_manager.py` to manage the server
- Generate new keys through the server manager
- Monitor server status and statistics
- Control server online/offline status

## 📞 Support

For support, visit our Discord server or contact the development team.

---
NetVoid - Secure, Server-Dependent Application System
