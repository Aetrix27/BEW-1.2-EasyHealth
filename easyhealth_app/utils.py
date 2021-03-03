"""Import current_user, login_manager, and wraps."""
from flask_login import current_user
from easyhealth_app import login_manager

from functools import wraps

def doctor_required(func):
    """Admin required decorator."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Check is current user is an admin."""
        if current_user.is_doctor:
            return func(*args, **kwargs)
        return login_manager.unauthorized()

    return wrapper


def patient_required(func):
    """Super admin required decorator."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Check is current user is a employee."""
        if not current_user.is_doctor:
            return func(*args, **kwargs)
        return login_manager.unauthorized()

    return wrapper