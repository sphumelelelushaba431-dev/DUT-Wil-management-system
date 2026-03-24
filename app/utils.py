from functools import wraps
from flask import abort
from flask_login import current_user


def student_required(f):
    """Only students can access this route."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or \
                current_user.role != 'student':
            abort(403)
        return f(*args, **kwargs)
    return decorated


def coordinator_required(f):
    """Only coordinators can access this route."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or \
                current_user.role != 'coordinator':
            abort(403)
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Only admins can access this route."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or \
                current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated
