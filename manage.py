#!/usr/bin/env python3
"""
Management commands for Fanfiction Explorer
Provides utilities for database indexing and maintenance.
"""

import sys
import os
from app.db_indexes import DatabaseIndexer


def create_indexes():
    """Create database indexes for better performance."""
    db_path = '/Users/Azrael/Development/Fichub SQL/metadata-full.sqlite'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("   Please check the database path in app/__init__.py")
        return False
    
    indexer = DatabaseIndexer(db_path)
    
    print("🚀 Creating database indexes for better search performance...")
    print("⏱️  This may take several minutes for large databases...")
    
    try:
        results = indexer.create_indexes()
        
        if results['created']:
            print(f"\n✅ Successfully created {len(results['created'])} indexes:")
            for idx in results['created']:
                print(f"   • {idx}")
        
        if results['skipped']:
            print(f"\n⏭️  Skipped {len(results['skipped'])} existing indexes:")
            for idx in results['skipped']:
                print(f"   • {idx}")
        
        if results['errors']:
            print(f"\n❌ {len(results['errors'])} errors occurred:")
            for error in results['errors']:
                print(f"   • {error}")
            return False
        
        print("\n🎉 Database indexing complete! Search performance should be significantly improved.")
        return True
        
    except Exception as e:
        print(f"❌ Error creating indexes: {e}")
        return False


def analyze_performance():
    """Analyze current database performance."""
    db_path = '/Users/Azrael/Development/Fichub SQL/metadata-full.sqlite'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    indexer = DatabaseIndexer(db_path)
    
    print("🔍 Analyzing database performance...")
    try:
        performance_results = indexer.analyze_current_performance()
        
        print("\n📊 Performance Analysis Results:")
        print("-" * 40)
        for query_name, execution_time in performance_results.items():
            status = "🐌 SLOW" if execution_time > 1.0 else "🚀 FAST" if execution_time < 0.1 else "⚡ OK"
            print(f"{query_name:20} | {execution_time:6.3f}s | {status}")
        
        # Check if indexes exist
        existing_indexes = indexer.check_existing_indexes()
        if existing_indexes:
            print(f"\n📋 Found {len(existing_indexes)} existing indexes:")
            for idx in existing_indexes:
                print(f"   • {idx}")
        else:
            print("\n⚠️  No custom indexes found. Consider running 'create-indexes' for better performance.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing performance: {e}")
        return False


def remove_indexes():
    """Remove all custom database indexes."""
    db_path = '/Users/Azrael/Development/Fichub SQL/metadata-full.sqlite'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    print("⚠️  This will remove ALL custom indexes from the database.")
    confirm = input("Are you sure you want to continue? (yes/no): ").lower().strip()
    
    if confirm != 'yes':
        print("Operation cancelled.")
        return False
    
    indexer = DatabaseIndexer(db_path)
    
    try:
        results = indexer.remove_indexes(confirm=True)
        
        if results['removed']:
            print(f"\n✅ Removed {len(results['removed'])} indexes:")
            for idx in results['removed']:
                print(f"   • {idx}")
        
        if results['errors']:
            print(f"\n❌ {len(results['errors'])} errors occurred:")
            for error in results['errors']:
                print(f"   • {error}")
            return False
        
        print("\n🗑️  All custom indexes removed.")
        return True
        
    except Exception as e:
        print(f"❌ Error removing indexes: {e}")
        return False


def show_help():
    """Show available commands."""
    print("""
🚀 Fanfiction Explorer - Management Commands

Available commands:
  create-indexes    Create database indexes for better search performance
  analyze          Analyze current database performance
  remove-indexes   Remove all custom database indexes
  help             Show this help message

Usage:
  python3 manage.py <command>

Examples:
  python3 manage.py create-indexes
  python3 manage.py analyze
  python3 manage.py help
""")


def main():
    """Main entry point for management commands."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'create-indexes': create_indexes,
        'analyze': analyze_performance,
        'remove-indexes': remove_indexes,
        'help': show_help,
        '--help': show_help,
        '-h': show_help
    }
    
    if command in commands:
        success = commands[command]()
        sys.exit(0 if success or command in ['help', '--help', '-h'] else 1)
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
