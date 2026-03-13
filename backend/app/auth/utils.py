"""Authentication utilities and decorators."""
from functools import wraps
from flask import abort
from flask_login import current_user


def is_owner_or_admin(profile):
    """Check if current user is the profile owner or an administrator.
    
    Args:
        profile: StudentProfile instance
        
    Returns:
        bool: True if user is owner or admin, False otherwise
    """
    if not current_user.is_authenticated:
        return False
    
    return current_user.id == profile.user_id or current_user.is_admin


def admin_required(f):
    """Decorator to require admin privileges for a route.
    
    Usage:
        @app.route('/admin/users')
        @login_required
        @admin_required
        def admin_users():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def owner_or_admin_required(get_profile_func):
    """Decorator to require owner or admin privileges for a route.
    
    Args:
        get_profile_func: Function that returns the profile from route args
        
    Usage:
        @app.route('/profiles/<int:profile_id>/edit')
        @login_required
        @owner_or_admin_required(lambda profile_id: StudentProfile.query.get_or_404(profile_id))
        def edit_profile(profile_id):
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            profile = get_profile_func(**kwargs)
            if not is_owner_or_admin(profile):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

