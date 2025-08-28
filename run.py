#!/usr/bin/env python3
"""
Fanfiction Explorer - Main Application Entry Point
"""

import os
from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes']
    
    print(f"🚀 Starting Fanfiction Explorer on http://{host}:{port}")
    print(f"📊 Database: {app.config['DATABASE_PATH']}")
    print(f"🐛 Debug mode: {debug}")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True  # Enable threading for better performance
    )
