#!/bin/bash
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
