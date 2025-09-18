from flask import Flask, request, jsonify
import json
import threading
import os
import uuid
import hashlib
import hmac
import base64
import time
from datetime import datetime, timedelta
from pathlib import Path
import random
import string

# Server configuration
VALID_KEYS_FILE = os.path.join(os.path.dirname(__file__), 'valid_keys.json')
KEY_DB_FILE = os.path.join(os.path.dirname(__file__), 'server_keys.json')
BIND_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'bind.json')
VERSION_FILE = os.path.join(os.path.dirname(__file__), 'version.json')
ENCRYPTION_KEY = os.getenv('NETVOID_ENCRYPTION_KEY', 'NetVoid2024SecretKey!@#')

# Server status
SERVER_ONLINE = True
CURRENT_VERSION = "1.0.0"

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

def generate_key():
    """Generate a new NetVoid key"""
    # Format: XXXX-XXXX-XXXX-XXXX (16 chars total)
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    key_parts = []
    for i in range(4):
        part = ''.join(random.choice(chars) for _ in range(4))
        key_parts.append(part)
    return '-'.join(key_parts)

def generate_hwid():
    """Generate a hardware ID"""
    return str(uuid.uuid4())

def load_valid_keys():
    """Load valid keys from the telegram-generated file"""
    try:
        with open(VALID_KEYS_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []

def load_db():
    """Load the server database"""
    try:
        with open(KEY_DB_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_db(db):
    """Save the server database"""
    with open(KEY_DB_FILE, 'w') as f:
        json.dump(db, f, indent=2)

def update_bind_file(key, hwid):
    """Update the local bind.json file"""
    try:
        bind_data = {}
        if os.path.exists(BIND_FILE):
            with open(BIND_FILE, 'r') as f:
                bind_data = json.load(f)
        
        bind_data[key] = hwid
        with open(BIND_FILE, 'w') as f:
            json.dump(bind_data, f, indent=2)
    except Exception as e:
        print(f"Error updating bind file: {e}")

app = Flask(__name__)
lock = threading.Lock()
VALID_KEYS = load_valid_keys()

@app.route('/api/auth', methods=['POST'])
def auth():
    """Main authentication endpoint"""
    try:
        data = request.get_json(force=True)
        key = data.get('key', '').strip()
        hwid = data.get('hwid', '').strip()
        
        if not key or not hwid:
            return jsonify({'authorized': False, 'reason': 'Missing key or HWID'}), 400
        
        if key not in VALID_KEYS:
            return jsonify({'authorized': False, 'reason': 'Invalid key'}), 403
        
        with lock:
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

@app.route('/api/keys', methods=['GET'])
def get_keys():
    """Get all valid keys (admin endpoint)"""
    return jsonify({
        'valid_keys': VALID_KEYS,
        'total_keys': len(VALID_KEYS)
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get server statistics"""
    with lock:
        db = load_db()
        return jsonify({
            'total_valid_keys': len(VALID_KEYS),
            'bound_keys': len(db),
            'unused_keys': len(VALID_KEYS) - len(db),
            'database': db
        })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'valid_keys_loaded': len(VALID_KEYS),
        'server_online': SERVER_ONLINE,
        'version': CURRENT_VERSION
    })

@app.route('/api/status', methods=['GET'])
def status():
    """Server status endpoint - returns code 0 if offline"""
    if not SERVER_ONLINE:
        return jsonify({'code': 0, 'message': 'Server offline'}), 503
    
    return jsonify({
        'code': 1,
        'status': 'online',
        'version': CURRENT_VERSION,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/version', methods=['GET'])
def version():
    """Get current version and update info"""
    if not SERVER_ONLINE:
        return jsonify({'code': 0, 'message': 'Server offline'}), 503
    
    version_info = {
        'code': 1,
        'current_version': CURRENT_VERSION,
        'latest_version': CURRENT_VERSION,
        'update_available': False,
        'update_url': None,
        'force_update': False
    }
    
    # Check for updates
    try:
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, 'r') as f:
                update_data = json.load(f)
                version_info.update(update_data)
    except Exception:
        pass
    
    return jsonify(version_info)

@app.route('/api/generate_key', methods=['POST'])
def generate_new_key():
    """Generate a new key (admin only)"""
    if not SERVER_ONLINE:
        return jsonify({'code': 0, 'message': 'Server offline'}), 503
    
    data = request.get_json(force=True)
    admin_key = data.get('admin_key', '')
    
    # Simple admin key check (in production, use proper authentication)
    if admin_key != 'NetVoidAdmin2024':
        return jsonify({'code': 0, 'message': 'Unauthorized'}), 403
    
    # Generate new key
    new_key = generate_key()
    
    # Add to valid keys
    with lock:
        VALID_KEYS.append(new_key)
        with open(VALID_KEYS_FILE, 'w') as f:
            json.dump(VALID_KEYS, f, indent=2)
    
    return jsonify({
        'code': 1,
        'key': new_key,
        'message': 'Key generated successfully'
    })

@app.route('/api/validate_hwid', methods=['POST'])
def validate_hwid():
    """Validate HWID and return encrypted response"""
    if not SERVER_ONLINE:
        return jsonify({'code': 0, 'message': 'Server offline'}), 503
    
    data = request.get_json(force=True)
    hwid = data.get('hwid', '')
    
    if not hwid:
        return jsonify({'code': 0, 'message': 'Invalid HWID'}), 400
    
    # Check if HWID is already bound
    with lock:
        db = load_db()
        bound_keys = [k for k, v in db.items() if v.get('hwid') == hwid]
    
    response_data = {
        'code': 1,
        'hwid_valid': True,
        'bound_keys': bound_keys,
        'timestamp': datetime.now().isoformat()
    }
    
    # Encrypt the response
    encrypted_response = encrypt_data(response_data)
    
    return jsonify({
        'encrypted_data': encrypted_response,
        'server_signature': hmac.new(
            ENCRYPTION_KEY.encode(),
            encrypted_response.encode(),
            hashlib.sha256
        ).hexdigest()
    })

@app.route('/api/server_offline', methods=['POST'])
def set_server_offline():
    """Set server offline (admin only)"""
    global SERVER_ONLINE
    data = request.get_json(force=True)
    admin_key = data.get('admin_key', '')
    
    if admin_key != 'NetVoidAdmin2024':
        return jsonify({'code': 0, 'message': 'Unauthorized'}), 403
    
    SERVER_ONLINE = False
    return jsonify({'code': 1, 'message': 'Server set to offline'})

@app.route('/api/server_online', methods=['POST'])
def set_server_online():
    """Set server online (admin only)"""
    global SERVER_ONLINE
    data = request.get_json(force=True)
    admin_key = data.get('admin_key', '')
    
    if admin_key != 'NetVoidAdmin2024':
        return jsonify({'code': 0, 'message': 'Unauthorized'}), 403
    
    SERVER_ONLINE = True
    return jsonify({'code': 1, 'message': 'Server set to online'})

if __name__ == '__main__':
    print("Starting NetVoid Authentication Server...")
    print(f"Valid keys loaded: {len(VALID_KEYS)}")
    print("Server running on http://127.0.0.1:8000")
    app.run(host='127.0.0.1', port=8000, debug=True)
