from flask import Blueprint, render_template, request, current_app
from app.utils import (
    get_basic_stats, get_top_fandoms, get_top_authors, 
    get_longest_stories, search_stories, get_story_by_id,
    format_number, truncate_text
)
import math

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    """Main dashboard with overview statistics"""
    try:
        stats = get_basic_stats()
        top_fandoms = get_top_fandoms(10)
        
        return render_template('dashboard.html', 
                             stats=stats,
                             top_fandoms=top_fandoms,
                             format_number=format_number)
    except Exception as e:
        current_app.logger.error(f"Dashboard error: {e}")
        return render_template('errors/500.html'), 500


@main_bp.route('/search')
def search():
    """Search stories with filters"""
    try:
        # Get search parameters
        query_params = {
            'title': request.args.get('title', '').strip(),
            'author': request.args.get('author', '').strip(),
            'category': request.args.get('category', '').strip(),
            'genre': request.args.get('genre', '').strip(),
            'language': request.args.get('language', '').strip(),
            'status': request.args.get('status', '').strip(),
            'rating': request.args.get('rating', '').strip(),
            'min_words': request.args.get('min_words', '').strip(),
            'max_words': request.args.get('max_words', '').strip(),
        }
        
        # Clean up empty parameters
        query_params = {k: v for k, v in query_params.items() if v}
        
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        # Perform search if there are parameters
        if query_params or request.args.get('show_all'):
            results, total_count = search_stories(query_params, page, per_page)
            
            # Calculate pagination info
            total_pages = math.ceil(total_count / per_page)
            has_prev = page > 1
            has_next = page < total_pages
            
            pagination_info = {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_prev': has_prev,
                'has_next': has_next,
                'prev_num': page - 1 if has_prev else None,
                'next_num': page + 1 if has_next else None
            }
            
        else:
            results = []
            total_count = 0
            pagination_info = None
        
        return render_template('search.html',
                             results=results,
                             query_params=request.args,
                             pagination=pagination_info,
                             format_number=format_number,
                             truncate_text=truncate_text)
                             
    except Exception as e:
        current_app.logger.error(f"Search error: {e}")
        return render_template('errors/500.html'), 500


@main_bp.route('/story/<int:story_id>')
def story_detail(story_id):
    """Show detailed information for a specific story"""
    try:
        story = get_story_by_id(story_id)
        if not story:
            return render_template('errors/404.html'), 404
        
        return render_template('story_detail.html',
                             story=story,
                             format_number=format_number)
                             
    except Exception as e:
        current_app.logger.error(f"Story detail error: {e}")
        return render_template('errors/500.html'), 500


@main_bp.route('/top/fandoms')
def top_fandoms():
    """Show top fandoms by story count"""
    try:
        fandoms = get_top_fandoms(50)  # Show top 50
        return render_template('top_fandoms.html',
                             fandoms=fandoms,
                             format_number=format_number)
                             
    except Exception as e:
        current_app.logger.error(f"Top fandoms error: {e}")
        return render_template('errors/500.html'), 500


@main_bp.route('/top/authors')
def top_authors():
    """Show top authors by story count"""
    try:
        authors = get_top_authors(50)  # Show top 50
        return render_template('top_authors.html',
                             authors=authors,
                             format_number=format_number)
                             
    except Exception as e:
        current_app.logger.error(f"Top authors error: {e}")
        return render_template('errors/500.html'), 500


@main_bp.route('/top/longest')
def top_longest():
    """Show longest stories by word count"""
    try:
        stories = get_longest_stories(100)  # Show top 100
        return render_template('top_longest.html',
                             stories=stories,
                             format_number=format_number,
                             truncate_text=truncate_text)
                             
    except Exception as e:
        current_app.logger.error(f"Top longest error: {e}")
        return render_template('errors/500.html'), 500


@main_bp.route('/browse')
def browse():
    """Browse stories with simple pagination (no filters)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = 100
        
        results, total_count = search_stories({}, page, per_page)
        
        # Calculate pagination info
        total_pages = math.ceil(total_count / per_page)
        has_prev = page > 1
        has_next = page < total_pages
        
        pagination_info = {
            'page': page,
            'per_page': per_page,
            'total_count': total_count,
            'total_pages': total_pages,
            'has_prev': has_prev,
            'has_next': has_next,
            'prev_num': page - 1 if has_prev else None,
            'next_num': page + 1 if has_next else None
        }
        
        return render_template('browse.html',
                             results=results,
                             pagination=pagination_info,
                             format_number=format_number,
                             truncate_text=truncate_text)
                             
    except Exception as e:
        current_app.logger.error(f"Browse error: {e}")
        return render_template('errors/500.html'), 500


# Template filters
@main_bp.app_template_filter('number')
def number_filter(value):
    """Format numbers with commas"""
    return format_number(value)


@main_bp.app_template_filter('truncate')
def truncate_filter(value, length=100):
    """Truncate text to specified length"""
    return truncate_text(value, length)
