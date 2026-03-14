"""Application configuration."""
import os
from pathlib import Path

basedir = Path(__file__).parent.parent


class Config:
    """Base configuration."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads/resumes'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 2097152))  # 2MB default
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Ensure upload folder exists
    @staticmethod
    def init_app(app):
        """Initialize application."""
        upload_path = Path(app.config['UPLOAD_FOLDER'])
        upload_path.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "intern_crud.db"}'


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    # Support both DATABASE_URL formats (with and without sqlite:///)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "backend" / "instance" / "intern_crud.db"}'

    # Trust proxy headers (for Cloudflare Tunnel / reverse proxy)
    PREFERRED_URL_SCHEME = 'https'

    @classmethod
    def init_app(cls, app):
        """Initialize production app."""
        Config.init_app(app)

        # Ensure instance directory exists
        instance_path = basedir / "backend" / "instance"
        instance_path.mkdir(parents=True, exist_ok=True)

        # Trust proxy headers for Cloudflare Tunnel
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

        # Log to stdout/stderr in production
        import logging
        from logging import StreamHandler
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        stream_handler.setFormatter(formatter)
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Intern CRUD application startup')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

