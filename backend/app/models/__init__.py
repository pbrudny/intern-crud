"""Database models."""
from app import db
from app.models.user import User
from app.models.profile import StudentProfile

__all__ = ['db', 'User', 'StudentProfile']

