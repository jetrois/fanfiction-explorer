from flask import Blueprint, jsonify, request, current_app
from app.utils import (
    get_basic_stats, get_top_fandoms, get_top_authors, 
    get_longest_stories, search_stories, get_story_by_id,
    get_language_stats, get_rating_stats, get_status_stats
)

api_bp = Blueprint('api', __name__)


@api_bp.route('/stats/basic')
def api_basic_stats():
    """Get basic database statistics as JSON"""
    try:
        stats = get_basic_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        current_app.logger.error(f"API basic stats error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch basic statistics'
        }), 500


@api_bp.route('/stats/fandoms')
def api_fandom_stats():
    """Get top fandoms as JSON"""
    try:
        limit = int(request.args.get('limit', 10))
        fandoms = get_top_fandoms(limit)
        
        data = [{'name': row[0], 'story_count': row[1]} for row in fandoms]
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        current_app.logger.error(f"API fandom stats error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch fandom statistics'
        }), 500


@api_bp.route('/stats/authors')
def api_author_stats():
    """Get top authors as JSON"""
    try:
        limit = int(request.args.get('limit', 10))
        authors = get_top_authors(limit)
        
        data = [{
            'name': row[0], 
            'story_count': row[1],
            'avg_words': int(row[2]) if row[2] else 0,
            'total_words': int(row[3]) if row[3] else 0
        } for row in authors]
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        current_app.logger.error(f"API author stats error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch author statistics'
        }), 500


@api_bp.route('/stats/languages')
def api_language_stats():
    """Get language distribution as JSON"""
    try:
        languages = get_language_stats()
        
        data = [{'name': row[0], 'count': row[1]} for row in languages]
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        current_app.logger.error(f"API language stats error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch language statistics'
        }), 500


@api_bp.route('/stats/ratings')
def api_rating_stats():
    """Get rating distribution as JSON"""
    try:
        ratings = get_rating_stats()
        
        data = [{'name': row[0], 'count': row[1]} for row in ratings]
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        current_app.logger.error(f"API rating stats error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch rating statistics'
        }), 500


@api_bp.route('/stats/status')
def api_status_stats():
    """Get status distribution as JSON"""
    try:
        statuses = get_status_stats()
        
        data = [{'name': row[0], 'count': row[1]} for row in statuses]
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        current_app.logger.error(f"API status stats error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch status statistics'
        }), 500


@api_bp.route('/search')
def api_search():
    """Search stories and return JSON"""
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
        per_page = min(int(request.args.get('per_page', 50)), 100)  # Max 100 results
        
        results, total_count = search_stories(query_params, page, per_page)
        
        # Convert results to list of dicts
        data = []
        for row in results:
            data.append({
                'title': row[0],
                'author': row[1],
                'category': row[2],
                'genre': row[3],
                'language': row[4],
                'status': row[5],
                'word_count': row[6],
                'chapter_count': row[7],
                'rating': row[8],
                'updated': row[9],
                'id': row[10]
            })
        
        return jsonify({
            'success': True,
            'data': data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': (total_count + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"API search error: {e}")
        return jsonify({
            'success': False,
            'error': 'Search failed'
        }), 500


@api_bp.route('/story/<int:story_id>')
def api_story_detail(story_id):
    """Get story details as JSON"""
    try:
        story = get_story_by_id(story_id)
        if not story:
            return jsonify({
                'success': False,
                'error': 'Story not found'
            }), 404
        
        # Convert row to dict
        data = dict(story)
        data['id'] = story_id
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        current_app.logger.error(f"API story detail error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch story details'
        }), 500


@api_bp.route('/top/longest')
def api_longest_stories():
    """Get longest stories as JSON"""
    try:
        limit = min(int(request.args.get('limit', 10)), 100)  # Max 100
        stories = get_longest_stories(limit)
        
        data = [{
            'title': row[0],
            'author': row[1],
            'word_count': row[2],
            'chapter_count': row[3],
            'category': row[4],
            'status': row[5],
            'id': row[6]
        } for row in stories]
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        current_app.logger.error(f"API longest stories error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch longest stories'
        }), 500


# Error handlers for API routes
@api_bp.errorhandler(404)
def api_not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@api_bp.errorhandler(500)
def api_internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500
