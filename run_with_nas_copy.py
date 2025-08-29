#!/usr/bin/env python3
"""
Fanfiction Explorer - Run with NAS Database Copy
Copies the database from NAS to local storage for optimal performance
"""

import os
import sys
import shutil
import time
from pathlib import Path
from app import create_app

# Paths
NAS_DB_PATH = '/Volumes/UNPS1/Linux/Web/Fanfiction Search/metadata-full.sqlite'
LOCAL_DB_PATH = '/Users/Azrael/fanfiction-explorer/data/metadata-full.sqlite'

def copy_database_from_nas():
    """Copy database from NAS to local storage"""
    print("🔄 Copying database from NAS to local storage...")
    
    # Check if NAS database exists
    if not os.path.exists(NAS_DB_PATH):
        print(f"❌ NAS database not found: {NAS_DB_PATH}")
        print("Please ensure:")
        print("1. The NAS is mounted at /Volumes/UNPS1/")
        print("2. The database file exists at the NAS location")
        return False
    
    # Create local data directory
    local_dir = Path(LOCAL_DB_PATH).parent
    local_dir.mkdir(exist_ok=True)
    
    # Get file sizes and modification times
    nas_stat = os.stat(NAS_DB_PATH)
    nas_size = nas_stat.st_size
    nas_mtime = nas_stat.st_mtime
    
    # Check if local copy exists and is up to date
    if os.path.exists(LOCAL_DB_PATH):
        local_stat = os.stat(LOCAL_DB_PATH)
        local_mtime = local_stat.st_mtime
        
        if nas_mtime <= local_mtime and nas_size == local_stat.st_size:
            print(f"✅ Local database is up to date ({nas_size:,} bytes)")
            return True
        else:
            print(f"📥 NAS database is newer, updating local copy...")
    else:
        print(f"📥 Creating local copy of database ({nas_size:,} bytes)")
    
    # Copy the database
    try:
        start_time = time.time()
        shutil.copy2(NAS_DB_PATH, LOCAL_DB_PATH)
        copy_time = time.time() - start_time
        
        print(f"✅ Database copied successfully in {copy_time:.1f} seconds")
        return True
        
    except Exception as e:
        print(f"❌ Failed to copy database: {e}")
        return False

def main():
    """Main function"""
    print("📚 Fanfiction Explorer - NAS Database Copy Mode")
    print("=" * 50)
    
    # Copy database from NAS
    if not copy_database_from_nas():
        sys.exit(1)
    
    # Set the database path to local copy
    os.environ['DATABASE_PATH'] = LOCAL_DB_PATH
    
    # Create Flask application
    app = create_app()
    
    # Get configuration from environment variables
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes']
    
    print(f"🚀 Starting Fanfiction Explorer on http://{host}:{port}")
    print(f"📊 Database: {LOCAL_DB_PATH}")
    print(f"🐛 Debug mode: {debug}")
    print("=" * 50)
    print("💡 Tip: Database is now local for optimal performance!")
    print("   To sync changes, restart this script to copy from NAS again.")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

if __name__ == '__main__':
    main()
