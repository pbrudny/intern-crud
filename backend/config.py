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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "intern_crud.db"}'
    
    @classmethod
    def init_app(cls, app):
        """Initialize production app."""
        Config.init_app(app)
        
        # Log to stderr in production
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

