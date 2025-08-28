#!/usr/bin/env python3
"""
Database Indexing Utility for Fanfiction Explorer
Creates optimized indexes for better search performance on large datasets.
"""

import sqlite3
import time
from typing import List, Tuple
import os


class DatabaseIndexer:
    """Handles database indexing operations for performance optimization."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.indexes = [
            # Single column indexes for exact matches
            {
                'name': 'idx_author',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_author ON metadata_full(Author COLLATE NOCASE)',
                'description': 'Fast author searches and author pages'
            },
            {
                'name': 'idx_category',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_category ON metadata_full(Category COLLATE NOCASE)',
                'description': 'Fast fandom/category searches'
            },
            {
                'name': 'idx_language',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_language ON metadata_full(Language)',
                'description': 'Fast language filtering'
            },
            {
                'name': 'idx_status',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_status ON metadata_full(Status)',
                'description': 'Fast completion status filtering'
            },
            {
                'name': 'idx_rating',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_rating ON metadata_full(Rating)',
                'description': 'Fast rating filtering'
            },
            {
                'name': 'idx_word_count',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_word_count ON metadata_full(word_count)',
                'description': 'Fast word count range searches'
            },
            {
                'name': 'idx_chapter_count',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_chapter_count ON metadata_full(chapter_count)',
                'description': 'Fast chapter count filtering'
            },
            {
                'name': 'idx_updated',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_updated ON metadata_full(Updated DESC)',
                'description': 'Fast ordering by update date (newest first)'
            },
            {
                'name': 'idx_published',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_published ON metadata_full(Published DESC)',
                'description': 'Fast ordering by publication date'
            },
            
            # Full-text search indexes for partial matches
            {
                'name': 'idx_title_text',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_title_text ON metadata_full(Title COLLATE NOCASE)',
                'description': 'Improved title searches (case insensitive)'
            },
            {
                'name': 'idx_genre_text',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_genre_text ON metadata_full(Genre COLLATE NOCASE)',
                'description': 'Improved genre searches'
            },
            
            # Composite indexes for common search combinations
            {
                'name': 'idx_category_status',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_category_status ON metadata_full(Category, Status)',
                'description': 'Fast fandom + completion status searches'
            },
            {
                'name': 'idx_author_updated',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_author_updated ON metadata_full(Author, Updated DESC)',
                'description': 'Fast author searches ordered by recent updates'
            },
            {
                'name': 'idx_category_wordcount',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_category_wordcount ON metadata_full(Category, word_count DESC)',
                'description': 'Fast fandom searches ordered by word count'
            },
            {
                'name': 'idx_language_status',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_language_status ON metadata_full(Language, Status)',
                'description': 'Fast language + status combination searches'
            },
            {
                'name': 'idx_rating_wordcount',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_rating_wordcount ON metadata_full(Rating, word_count)',
                'description': 'Fast rating + word count searches'
            },
            
            # Performance indexes for analytics
            {
                'name': 'idx_author_count',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_author_count ON metadata_full(Author) WHERE Author IS NOT NULL AND Author != ""',
                'description': 'Fast author statistics and top author queries'
            },
            {
                'name': 'idx_category_count',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_category_count ON metadata_full(Category) WHERE Category IS NOT NULL AND Category != ""',
                'description': 'Fast fandom statistics and top fandom queries'
            },
            
            # Search optimization indexes
            {
                'name': 'idx_search_filter',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_search_filter ON metadata_full(Language, Status, Rating, word_count)',
                'description': 'Optimized for multi-filter searches'
            }
        ]
    
    def connect(self) -> sqlite3.Connection:
        """Create database connection with optimizations."""
        conn = sqlite3.connect(self.db_path)
        # Enable Write-Ahead Logging for better performance
        conn.execute('PRAGMA journal_mode=WAL')
        # Increase cache size for index operations
        conn.execute('PRAGMA cache_size=10000')
        # Optimize for fast writes during index creation
        conn.execute('PRAGMA synchronous=NORMAL')
        conn.execute('PRAGMA temp_store=MEMORY')
        return conn
    
    def analyze_current_performance(self) -> dict:
        """Analyze current query performance without indexes."""
        print("🔍 Analyzing current database performance...")
        
        conn = self.connect()
        cursor = conn.cursor()
        
        # Test queries that will benefit from indexes
        test_queries = [
            ("Author search", "SELECT COUNT(*) FROM metadata_full WHERE Author LIKE 'J%'"),
            ("Category search", "SELECT COUNT(*) FROM metadata_full WHERE Category LIKE 'Harry Potter%'"),
            ("Word count range", "SELECT COUNT(*) FROM metadata_full WHERE word_count BETWEEN 50000 AND 100000"),
            ("Multi-filter", "SELECT COUNT(*) FROM metadata_full WHERE Language='English' AND Status='Completed' AND word_count > 10000"),
            ("Top authors", "SELECT Author, COUNT(*) FROM metadata_full WHERE Author != '' GROUP BY Author ORDER BY COUNT(*) DESC LIMIT 10"),
        ]
        
        results = {}
        for name, query in test_queries:
            start_time = time.time()
            cursor.execute(query)
            cursor.fetchall()
            execution_time = time.time() - start_time
            results[name] = execution_time
            print(f"  {name}: {execution_time:.3f}s")
        
        conn.close()
        return results
    
    def check_existing_indexes(self) -> List[str]:
        """Check what indexes already exist."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, sql FROM sqlite_master 
            WHERE type='index' AND tbl_name='metadata_full' AND name NOT LIKE 'sqlite_%'
        """)
        existing = cursor.fetchall()
        conn.close()
        
        return [idx[0] for idx in existing]
    
    def create_indexes(self, force: bool = False) -> dict:
        """Create all performance indexes."""
        existing_indexes = self.check_existing_indexes()
        results = {'created': [], 'skipped': [], 'errors': []}
        
        if existing_indexes and not force:
            print(f"ℹ️  Found {len(existing_indexes)} existing indexes: {', '.join(existing_indexes)}")
            print("   Use force=True to recreate all indexes")
        
        conn = self.connect()
        cursor = conn.cursor()
        
        print(f"🚀 Creating {len(self.indexes)} performance indexes...")
        
        for i, index_config in enumerate(self.indexes, 1):
            index_name = index_config['name']
            index_sql = index_config['sql']
            description = index_config['description']
            
            try:
                if index_name in existing_indexes and not force:
                    print(f"  [{i:2d}/{len(self.indexes)}] ⏭️  Skipped {index_name} (already exists)")
                    results['skipped'].append(index_name)
                    continue
                
                print(f"  [{i:2d}/{len(self.indexes)}] 🔨 Creating {index_name}...")
                print(f"      📝 {description}")
                
                start_time = time.time()
                cursor.execute(index_sql)
                execution_time = time.time() - start_time
                
                print(f"      ✅ Created in {execution_time:.2f}s")
                results['created'].append(index_name)
                
            except sqlite3.Error as e:
                error_msg = f"Failed to create {index_name}: {e}"
                print(f"      ❌ {error_msg}")
                results['errors'].append(error_msg)
        
        # Commit all changes
        conn.commit()
        
        # Update table statistics for query optimizer
        print("📊 Updating table statistics for query optimizer...")
        cursor.execute("ANALYZE metadata_full")
        conn.commit()
        
        conn.close()
        return results
    
    def test_performance_improvement(self) -> dict:
        """Test query performance after index creation."""
        print("🏁 Testing performance improvements...")
        
        conn = self.connect()
        cursor = conn.cursor()
        
        # Same test queries as before
        test_queries = [
            ("Author search", "SELECT COUNT(*) FROM metadata_full WHERE Author LIKE 'J%'"),
            ("Category search", "SELECT COUNT(*) FROM metadata_full WHERE Category LIKE 'Harry Potter%'"),
            ("Word count range", "SELECT COUNT(*) FROM metadata_full WHERE word_count BETWEEN 50000 AND 100000"),
            ("Multi-filter", "SELECT COUNT(*) FROM metadata_full WHERE Language='English' AND Status='Completed' AND word_count > 10000"),
            ("Top authors", "SELECT Author, COUNT(*) FROM metadata_full WHERE Author != '' GROUP BY Author ORDER BY COUNT(*) DESC LIMIT 10"),
        ]
        
        results = {}
        for name, query in test_queries:
            start_time = time.time()
            cursor.execute(query)
            cursor.fetchall()
            execution_time = time.time() - start_time
            results[name] = execution_time
            print(f"  {name}: {execution_time:.3f}s")
        
        conn.close()
        return results
    
    def get_index_info(self) -> dict:
        """Get information about created indexes."""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Get index statistics
        cursor.execute("""
            SELECT 
                name,
                sql,
                CASE 
                    WHEN sql LIKE '%UNIQUE%' THEN 'UNIQUE'
                    WHEN sql LIKE '%(%,%' THEN 'COMPOSITE'
                    ELSE 'SINGLE'
                END as type
            FROM sqlite_master 
            WHERE type='index' AND tbl_name='metadata_full' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        indexes = cursor.fetchall()
        
        # Check database size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        db_size = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_indexes': len(indexes),
            'indexes': indexes,
            'database_size': db_size
        }
    
    def remove_indexes(self, confirm: bool = False) -> dict:
        """Remove all custom indexes (for testing or cleanup)."""
        if not confirm:
            print("⚠️  This will remove all custom indexes. Use confirm=True to proceed.")
            return {'removed': [], 'errors': []}
        
        existing_indexes = self.check_existing_indexes()
        if not existing_indexes:
            print("ℹ️  No custom indexes found to remove.")
            return {'removed': [], 'errors': []}
        
        conn = self.connect()
        cursor = conn.cursor()
        
        results = {'removed': [], 'errors': []}
        
        print(f"🗑️  Removing {len(existing_indexes)} indexes...")
        
        for index_name in existing_indexes:
            try:
                cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
                print(f"  ✅ Removed {index_name}")
                results['removed'].append(index_name)
            except sqlite3.Error as e:
                error_msg = f"Failed to remove {index_name}: {e}"
                print(f"  ❌ {error_msg}")
                results['errors'].append(error_msg)
        
        conn.commit()
        conn.close()
        return results


def main():
    """Main function for command-line usage."""
    db_path = '/Users/Azrael/Development/Fichub SQL/metadata-full.sqlite'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return
    
    indexer = DatabaseIndexer(db_path)
    
    print("=" * 60)
    print("🚀 FANFICTION EXPLORER - DATABASE INDEXING UTILITY")
    print("=" * 60)
    
    # Analyze current performance
    print("\n1️⃣  CURRENT PERFORMANCE ANALYSIS")
    before_performance = indexer.analyze_current_performance()
    
    # Create indexes
    print("\n2️⃣  CREATING PERFORMANCE INDEXES")
    creation_results = indexer.create_indexes()
    
    # Test improved performance
    print("\n3️⃣  PERFORMANCE AFTER INDEXING")
    after_performance = indexer.test_performance_improvement()
    
    # Show improvement summary
    print("\n4️⃣  PERFORMANCE IMPROVEMENT SUMMARY")
    print("=" * 40)
    for query_name in before_performance.keys():
        before = before_performance[query_name]
        after = after_performance[query_name]
        improvement = (before - after) / before * 100 if before > 0 else 0
        speedup = before / after if after > 0 else float('inf')
        
        print(f"{query_name:20} | {before:6.3f}s → {after:6.3f}s | "
              f"{improvement:5.1f}% faster ({speedup:.1f}x speedup)")
    
    # Show index information
    print("\n5️⃣  INDEX SUMMARY")
    index_info = indexer.get_index_info()
    print(f"✅ Created {len(creation_results['created'])} new indexes")
    print(f"⏭️  Skipped {len(creation_results['skipped'])} existing indexes")
    if creation_results['errors']:
        print(f"❌ {len(creation_results['errors'])} errors occurred")
    
    print(f"📊 Total indexes: {index_info['total_indexes']}")
    print(f"💾 Database size: {index_info['database_size'] / (1024*1024):.1f} MB")
    
    print("\n🎉 Database indexing complete! Your searches should now be much faster.")


if __name__ == '__main__':
    main()
