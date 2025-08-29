from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration - Use environment variables with fallback defaults
    database_path = os.environ.get('DATABASE_PATH', '/Users/Azrael/Development/Fichub SQL/metadata-full.sqlite')
    
    app.config.update(
        DATABASE_PATH=database_path,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production'),
        DEBUG=os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes'],
        JSON_SORT_KEYS=False
    )
    
    # Register blueprints
    from app.routes import main_bp
    from app.api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Set up logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/fanfiction_explorer.log',
                                         maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Fanfiction Explorer startup')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        return render_template('errors/500.html'), 500
    
    # Initialize database connection management
    from app.utils import init_db
    init_db(app)
    
    return app
