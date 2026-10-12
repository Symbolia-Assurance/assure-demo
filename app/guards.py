"""Route guards. Every page outside the public ones carries one or both."""
import functools

from flask import abort, session

from .store import role_of


def current_user_role():
    return role_of(session.get("user_id"))


def login_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            abort(401)
        return view(*args, **kwargs)
    return wrapper


def admin_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if current_user_role() != "admin":
            abort(403)
        return view(*args, **kwargs)
    return wrapper
