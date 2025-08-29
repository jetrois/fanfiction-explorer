#!/usr/bin/env python3
"""
Fanfiction Explorer - Run with NAS Database
Sets the DATABASE_PATH environment variable to use the NAS location
"""

import os
import sys
from app import create_app

# Set the database path to your NAS location
os.environ['DATABASE_PATH'] = '/Volumes/UNPS1/Linux/Web/Fanfiction Search/metadata-full.sqlite'

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes']
    
    # Check if database file exists
    db_path = app.config['DATABASE_PATH']
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("Please ensure:")
        print("1. The NAS is mounted at /Volumes/UNPS1/")
        print("2. The database file exists at the specified location")
        print("3. You have read permissions for the file")
        sys.exit(1)
    
    print(f"🚀 Starting Fanfiction Explorer on http://{host}:{port}")
    print(f"📊 Database: {db_path}")
    print(f"🐛 Debug mode: {debug}")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True  # Enable threading for better performance
    )
