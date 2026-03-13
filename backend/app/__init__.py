"""Flask application factory."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.profiles import profiles as profiles_blueprint
    app.register_blueprint(profiles_blueprint, url_prefix='/profiles')
    
    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    # Register error handlers
    from app import errors
    errors.register_error_handlers(app)
    
    # Home route
    @app.route('/')
    def index():
        from flask import render_template, redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('profiles.list_profiles'))
        return render_template('index.html')
    
    return app

