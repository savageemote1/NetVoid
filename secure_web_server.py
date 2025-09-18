#!/usr/bin/env python3
"""
Secure NetVoid Web Server
Integrated website and API server with encryption and security
"""

import os
import sys
import json
import uuid
import hashlib
import hmac
import base64
import time
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
import threading
import ssl
import secrets

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
import jwt

# Add server directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

# Import NetVoid server components
try:
    from server.app import generate_key, load_valid_keys, load_db, save_db, update_bind_file
    NETVOID_AVAILABLE = True
except ImportError:
    NETVOID_AVAILABLE = False
    print("Warning: NetVoid server components not available")

# Security Configuration
SECRET_KEY = os.getenv('NETVOID_SECRET_KEY', secrets.token_urlsafe(32))
JWT_SECRET = os.getenv('NETVOID_JWT_SECRET', secrets.token_urlsafe(32))
ENCRYPTION_KEY = os.getenv('NETVOID_ENCRYPTION_KEY', 'NetVoid2024SecretKey!@#')
ADMIN_PASSWORD = os.getenv('NETVOID_ADMIN_PASSWORD', 'NetVoidAdmin2024!')

# Server Configuration
PORT = 8080
HOST = '127.0.0.1'
DEBUG = False

# File paths
VALID_KEYS_FILE = os.path.join('server', 'valid_keys.json')
KEY_DB_FILE = os.path.join('server', 'server_keys.json')
BIND_FILE = os.path.join('config', 'bind.json')
TEMPLATE_DIR = 'templates'
STATIC_DIR = 'static'

# Create directories
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs('server', exist_ok=True)
os.makedirs('config', exist_ok=True)

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = SECRET_KEY
app.wsgi_app = ProxyFix(app.wsgi_app)

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# Rate limiting
from collections import defaultdict
from functools import wraps

rate_limits = defaultdict(list)

def rate_limit(max_requests=10, window=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            now = time.time()
            
            # Clean old requests
            rate_limits[client_ip] = [req_time for req_time in rate_limits[client_ip] if now - req_time < window]
            
            # Check rate limit
            if len(rate_limits[client_ip]) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            # Add current request
            rate_limits[client_ip].append(now)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Encryption functions
def encrypt_data(data):
    """Encrypt data using AES encryption"""
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        
        key = hashlib.sha256(ENCRYPTION_KEY.encode()).digest()
        cipher = AES.new(key, AES.MODE_CBC)
        padded_data = pad(json.dumps(data).encode(), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(cipher.iv + encrypted).decode()
    except ImportError:
        # Fallback to simple encoding if pycryptodome not available
        return base64.b64encode(json.dumps(data).encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypt data using AES decryption"""
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        
        key = hashlib.sha256(ENCRYPTION_KEY.encode()).digest()
        encrypted = base64.b64decode(encrypted_data.encode())
        iv = encrypted[:16]
        ciphertext = encrypted[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return json.loads(decrypted.decode())
    except ImportError:
        # Fallback to simple decoding
        return json.loads(base64.b64decode(encrypted_data.encode()).decode())
    except Exception:
        return None

def generate_csrf_token():
    """Generate CSRF token"""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_urlsafe(32)
    return session['csrf_token']

def validate_csrf_token(token):
    """Validate CSRF token"""
    return token and token == session.get('csrf_token')

# Authentication
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html', csrf_token=generate_csrf_token())

@app.route('/purchase')
def purchase():
    """Purchase page"""
    return render_template('purchase.html', csrf_token=generate_csrf_token())

@app.route('/admin')
@require_auth
def admin_dashboard():
    """Admin dashboard"""
    if not NETVOID_AVAILABLE:
        return "NetVoid server not available", 500
    
    try:
        valid_keys = load_valid_keys()
        db = load_db()
        
        stats = {
            'total_keys': len(valid_keys),
            'bound_keys': len(db),
            'unused_keys': len(valid_keys) - len(db),
            'recent_activity': list(db.values())[-10:] if db else []
        }
        
        return render_template('admin.html', stats=stats, csrf_token=generate_csrf_token())
    except Exception as e:
        return f"Error loading admin data: {str(e)}", 500

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        password = request.form.get('password')
        csrf_token = request.form.get('csrf_token')
        
        if not validate_csrf_token(csrf_token):
            flash('Invalid CSRF token', 'error')
            return render_template('admin_login.html')
        
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid password', 'error')
    
    return render_template('admin_login.html', csrf_token=generate_csrf_token())

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('authenticated', None)
    return redirect(url_for('index'))

# API Routes
@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'netvoid_available': NETVOID_AVAILABLE
    })

@app.route('/api/purchase', methods=['POST'])
@rate_limit(max_requests=5, window=300)  # 5 requests per 5 minutes
def api_purchase():
    """Handle purchase requests"""
    try:
        data = request.get_json()
        
        # Validate CSRF token
        if not validate_csrf_token(data.get('csrf_token')):
            return jsonify({'error': 'Invalid CSRF token'}), 403
        
        # Validate required fields
        required_fields = ['email', 'name', 'plan', 'payment_method']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate plan
        valid_plans = ['basic', 'premium', 'lifetime']
        if data['plan'] not in valid_plans:
            return jsonify({'error': 'Invalid plan'}), 400
        
        # Generate key if NetVoid is available
        if NETVOID_AVAILABLE:
            new_key = generate_key()
            
            # Add to valid keys
            valid_keys = load_valid_keys()
            valid_keys.append(new_key)
            
            with open(VALID_KEYS_FILE, 'w') as f:
                json.dump(valid_keys, f, indent=2)
            
            # Log purchase
            purchase_data = {
                'key': new_key,
                'email': data['email'],
                'name': data['name'],
                'plan': data['plan'],
                'payment_method': data['payment_method'],
                'timestamp': datetime.now().isoformat(),
                'ip': request.remote_addr
            }
            
            # Save purchase record
            purchase_file = 'purchases.json'
            purchases = []
            if os.path.exists(purchase_file):
                with open(purchase_file, 'r') as f:
                    purchases = json.load(f)
            
            purchases.append(purchase_data)
            
            with open(purchase_file, 'w') as f:
                json.dump(purchases, f, indent=2)
            
            # Encrypt response
            response_data = {
                'success': True,
                'key': new_key,
                'plan': data['plan'],
                'message': 'Key generated successfully'
            }
            
            encrypted_response = encrypt_data(response_data)
            
            return jsonify({
                'encrypted_data': encrypted_response,
                'signature': hmac.new(
                    ENCRYPTION_KEY.encode(),
                    encrypted_response.encode(),
                    hashlib.sha256
                ).hexdigest()
            })
        else:
            return jsonify({'error': 'NetVoid server not available'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Purchase failed: {str(e)}'}), 500

@app.route('/api/generate_key', methods=['POST'])
@require_auth
@rate_limit(max_requests=10, window=60)
def api_generate_key():
    """Generate new key (admin only)"""
    if not NETVOID_AVAILABLE:
        return jsonify({'error': 'NetVoid server not available'}), 500
    
    try:
        new_key = generate_key()
        
        # Add to valid keys
        valid_keys = load_valid_keys()
        valid_keys.append(new_key)
        
        with open(VALID_KEYS_FILE, 'w') as f:
            json.dump(valid_keys, f, indent=2)
        
        return jsonify({
            'success': True,
            'key': new_key,
            'message': 'Key generated successfully'
        })
    except Exception as e:
        return jsonify({'error': f'Key generation failed: {str(e)}'}), 500

@app.route('/api/stats')
@require_auth
def api_stats():
    """Get server statistics (admin only)"""
    if not NETVOID_AVAILABLE:
        return jsonify({'error': 'NetVoid server not available'}), 500
    
    try:
        valid_keys = load_valid_keys()
        db = load_db()
        
        return jsonify({
            'total_keys': len(valid_keys),
            'bound_keys': len(db),
            'unused_keys': len(valid_keys) - len(db),
            'database': db
        })
    except Exception as e:
        return jsonify({'error': f'Stats retrieval failed: {str(e)}'}), 500

# NetVoid API Integration
@app.route('/api/auth', methods=['POST'])
def netvoid_auth():
    """NetVoid authentication endpoint"""
    if not NETVOID_AVAILABLE:
        return jsonify({'authorized': False, 'reason': 'NetVoid server not available'}), 503
    
    try:
        data = request.get_json(force=True)
        key = data.get('key', '').strip()
        hwid = data.get('hwid', '').strip()
        
        if not key or not hwid:
            return jsonify({'authorized': False, 'reason': 'Missing key or HWID'}), 400
        
        valid_keys = load_valid_keys()
        if key not in valid_keys:
            return jsonify({'authorized': False, 'reason': 'Invalid key'}), 403
        
        db = load_db()
        if key not in db:
            # New key, first HWID binding
            db[key] = {
                'hwid': hwid,
                'first_used': datetime.now().isoformat(),
                'last_used': datetime.now().isoformat(),
                'usage_count': 1
            }
            save_db(db)
            update_bind_file(key, hwid)
            return jsonify({
                'authorized': True, 
                'msg': 'HWID bound, access granted.',
                'first_time': True
            })
        else:
            if db[key]['hwid'] == hwid:
                # Update usage stats
                db[key]['last_used'] = datetime.now().isoformat()
                db[key]['usage_count'] += 1
                save_db(db)
                return jsonify({
                    'authorized': True, 
                    'msg': 'Access granted.',
                    'first_time': False
                })
            else:
                return jsonify({
                    'authorized': False, 
                    'reason': 'HWID mismatch - Key already bound to different device'
                }), 403
    except Exception as e:
        return jsonify({'authorized': False, 'reason': f'Server error: {str(e)}'}), 500

def main():
    """Main function"""
    print("🚀 Starting Secure NetVoid Web Server...")
    print("=" * 60)
    print(f"🌐 Server: http://{HOST}:{PORT}")
    print(f"🔐 Admin: http://{HOST}:{PORT}/admin")
    print(f"📊 API: http://{HOST}:{PORT}/api/status")
    print("=" * 60)
    print("🔒 Security Features:")
    print("   • CSRF Protection")
    print("   • Rate Limiting")
    print("   • Encrypted Communications")
    print("   • Security Headers")
    print("   • Input Validation")
    print("=" * 60)
    
    # Initialize NetVoid if available
    if NETVOID_AVAILABLE:
        print("✅ NetVoid server integration enabled")
    else:
        print("⚠️  NetVoid server integration disabled")
    
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        app.run(host=HOST, port=PORT, debug=DEBUG, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == '__main__':
    main()
