# -*- coding: utf-8 -*-
"""Basic authentication moduel for the app."""
from flask_httpauth import HTTPBasicAuth

from server.models.users import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    """Basic authentication password verification."""
    user = User.query.filter_by(email=email).first()
    if user:
        return user.check_password(password)
    return False
