"""Admin routes - placeholder."""
from flask import redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app.admin import admin


def admin_required(f):
    """Decorator to require admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need administrator privileges to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/users')
@login_required
@admin_required
def list_users():
    """List all users - placeholder."""
    flash('Admin user management will be available soon.', 'info')
    return redirect(url_for('index'))

