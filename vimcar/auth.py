# -*- coding: utf-8 -*-
"""Auth module, including the JWT object and related handler methods."""

from flask_jwt import JWT

from vimcar.models.users import User

jwt = JWT()


@jwt.authentication_handler
def authenticate(username, password):
    """JWT authentication callback."""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@jwt.identity_handler
def identitiy(payload):
    """JWT identity callback."""
    user_id = payload['identity']
    return User.get_by_id(user_id)
