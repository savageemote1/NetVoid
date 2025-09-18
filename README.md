# NetVoid Server

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
python local_updater.py
```

### GitHub Integration
```bash
python update_system.py
```

### Two-Way Sync
```bash
python github_sync.py
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
├── update_system.py        # Auto-updater
├── github_sync.py          # Two-way sync
└── webhook_receiver.py     # Webhook receiver
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
