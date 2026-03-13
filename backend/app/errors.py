"""Error handlers for the application."""
from flask import render_template


def register_error_handlers(app):
    """Register error handlers with the Flask app."""
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors."""
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        return render_template('errors/500.html'), 500

