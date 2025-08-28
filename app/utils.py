import sqlite3
from flask import g, current_app


def get_db():
    """Get database connection for current request"""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_PATH'])
        g.db.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return g.db


def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    """Initialize database connection management"""
    app.teardown_appcontext(close_db)


def format_number(num):
    """Format numbers with commas"""
    if num is None:
        return "N/A"
    return f"{num:,}"


def truncate_text(text, max_length=100):
    """Truncate text to specified length"""
    if not text:
        return "N/A"
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def get_basic_stats():
    """Get basic database statistics"""
    db = get_db()
    cursor = db.cursor()
    
    # Total stories
    cursor.execute("SELECT COUNT(*) FROM metadata_full")
    total_stories = cursor.fetchone()[0]
    
    # Unique authors
    cursor.execute("SELECT COUNT(DISTINCT Author) FROM metadata_full WHERE Author IS NOT NULL AND Author != ''")
    unique_authors = cursor.fetchone()[0]
    
    # Total words
    cursor.execute("SELECT SUM(word_count) FROM metadata_full WHERE word_count IS NOT NULL")
    total_words = cursor.fetchone()[0]
    
    # Average word count
    cursor.execute("SELECT AVG(word_count) FROM metadata_full WHERE word_count > 0")
    avg_words = cursor.fetchone()[0]
    
    return {
        'total_stories': total_stories,
        'unique_authors': unique_authors,
        'total_words': total_words,
        'avg_words': int(avg_words) if avg_words else 0
    }


def get_top_fandoms(limit=10):
    """Get top fandoms by story count"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT Category, COUNT(*) as story_count 
        FROM metadata_full 
        WHERE Category IS NOT NULL AND Category != ''
        GROUP BY Category 
        ORDER BY story_count DESC 
        LIMIT ?
    """, (limit,))
    
    return [list(row) for row in cursor.fetchall()]


def get_top_authors(limit=10):
    """Get top authors by story count"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT Author, COUNT(*) as story_count,
               AVG(word_count) as avg_words,
               SUM(word_count) as total_words
        FROM metadata_full 
        WHERE Author IS NOT NULL AND Author != ''
        GROUP BY Author 
        ORDER BY story_count DESC 
        LIMIT ?
    """, (limit,))
    
    return cursor.fetchall()


def get_longest_stories(limit=10):
    """Get longest stories by word count"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT Title, Author, word_count, chapter_count, Category, Status, rowid
        FROM metadata_full 
        WHERE word_count > 0
        ORDER BY word_count DESC 
        LIMIT ?
    """, (limit,))
    
    return cursor.fetchall()


def search_stories(query_params, page=1, per_page=50):
    """Search stories with various filters"""
    db = get_db()
    cursor = db.cursor()
    
    # Build WHERE clause dynamically
    where_conditions = []
    params = []
    
    if query_params.get('title'):
        where_conditions.append("Title LIKE ?")
        params.append(f"%{query_params['title']}%")
    
    if query_params.get('author'):
        where_conditions.append("Author LIKE ?")
        params.append(f"%{query_params['author']}%")
    
    if query_params.get('category'):
        where_conditions.append("Category LIKE ?")
        params.append(f"%{query_params['category']}%")
    
    if query_params.get('genre'):
        where_conditions.append("Genre LIKE ?")
        params.append(f"%{query_params['genre']}%")
    
    if query_params.get('language'):
        where_conditions.append("Language = ?")
        params.append(query_params['language'])
    
    if query_params.get('status'):
        where_conditions.append("Status = ?")
        params.append(query_params['status'])
    
    if query_params.get('rating'):
        where_conditions.append("Rating = ?")
        params.append(query_params['rating'])
    
    if query_params.get('min_words'):
        where_conditions.append("word_count >= ?")
        params.append(int(query_params['min_words']))
    
    if query_params.get('max_words'):
        where_conditions.append("word_count <= ?")
        params.append(int(query_params['max_words']))
    
    # Build final query
    base_query = """
        SELECT Title, Author, Category, Genre, Language, Status, 
               word_count, chapter_count, Rating, Updated, rowid
        FROM metadata_full
    """
    
    if where_conditions:
        base_query += " WHERE " + " AND ".join(where_conditions)
    
    # Add ordering and pagination
    base_query += " ORDER BY Updated DESC LIMIT ? OFFSET ?"
    params.extend([per_page, (page - 1) * per_page])
    
    cursor.execute(base_query, params)
    results = cursor.fetchall()
    
    # Get total count for pagination
    count_query = "SELECT COUNT(*) FROM metadata_full"
    if where_conditions:
        count_query += " WHERE " + " AND ".join(where_conditions)
    
    cursor.execute(count_query, params[:-2])  # Exclude limit and offset params
    total_count = cursor.fetchone()[0]
    
    return results, total_count


def get_story_by_id(story_id):
    """Get full story details by rowid"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM metadata_full WHERE rowid = ?", (story_id,))
    return cursor.fetchone()


def get_language_stats():
    """Get language distribution"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT Language, COUNT(*) as count 
        FROM metadata_full 
        WHERE Language IS NOT NULL AND Language != ''
        GROUP BY Language 
        ORDER BY count DESC 
        LIMIT 10
    """)
    
    return cursor.fetchall()


def get_rating_stats():
    """Get rating distribution"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT Rating, COUNT(*) as count 
        FROM metadata_full 
        WHERE Rating IS NOT NULL AND Rating != ''
        GROUP BY Rating 
        ORDER BY count DESC
    """)
    
    return cursor.fetchall()


def get_status_stats():
    """Get status distribution"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT Status, COUNT(*) as count 
        FROM metadata_full 
        WHERE Status IS NOT NULL AND Status != ''
        GROUP BY Status 
        ORDER BY count DESC
    """)
    
    return cursor.fetchall()
