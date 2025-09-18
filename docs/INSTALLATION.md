# NetVoid Installation Guide

## Quick Start

1. **Extract Package**
   ```
   Extract NetVoid_Package.zip to your desired location
   ```

2. **Run Installer**
   ```
   python install.py
   ```

3. **Start Server**
   ```
   python server_manager.py
   Select option 1 to start server
   ```

4. **Run Client**
   ```
   python encrypted_main.py
   ```

## Detailed Installation

### Step 1: Prerequisites
- Ensure Python 3.7+ is installed
- Run as Administrator
- Have internet connection

### Step 2: Server Setup
1. Navigate to the `server` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Start server: `python start_server.py`

### Step 3: Client Setup
1. Navigate to the `client` directory
2. Run the encrypted client: `python encrypted_main.py`
3. Enter a valid key when prompted

### Step 4: Management
- Use `server_manager.py` for server management
- Generate new keys as needed
- Monitor server status

## Troubleshooting

### Server Issues
- Check if port 8000 is available
- Verify Python dependencies are installed
- Check firewall settings

### Client Issues
- Ensure server is running
- Check internet connection
- Verify key is valid

### Authentication Issues
- Check server status
- Verify key format
- Check HWID binding

## Security Notes

- Server must be running for client to work
- All communication is encrypted
- Keys are bound to specific hardware
- Code is obfuscated to prevent reverse engineering

---
For additional support, contact the development team.
