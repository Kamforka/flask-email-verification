# -*- coding: utf-8 -*-
"""User resources."""
from flask import render_template, url_for
from flask_restful import Resource, fields, marshal, marshal_with
from webargs import fields as argfields
from webargs.flaskparser import use_args

from vimcar.auth import auth
from vimcar.models.users import User
from vimcar.utils import confirm_token, generate_confirmation_token, send_email

user_args = {
    'email': argfields.Str(),
    'password': argfields.Str(),
}


resource_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'active': fields.Boolean,
}


class UserView(Resource):
    """UserView API."""

    @auth.login_required
    def get(self, user_id):
        """Get a user."""
        user = User.get_by_id(user_id)
        if user:
            return marshal(user, resource_fields), 201
        return 'User not found', 404

    @auth.login_required
    @use_args(user_args)
    def put(self, args, user_id):
        """Update a user."""
        user = User.get_by_id(user_id)
        if user:
            user = user.update(**args)
            return marshal(user, resource_fields), 201

        return 'User not found', 404


class UserViewList(Resource):
    """UserViewList API."""

    @auth.login_required
    @marshal_with(resource_fields)
    def get(self):
        """List users."""
        return User.query.all(), 200

    @use_args(user_args)
    def post(self, args):
        """Register user."""
        user = User.query.filter_by(email=args['email']).first()
        if user:
            return 'Email already registered', 409

        new_user = User.create(email=args['email'],
                               password=args['password'])

        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for('confirmationview', token=token, _external=True)
        html = render_template('confirmation.html', confirm_url=confirm_url)
        send_email(to=new_user.email, subject='Vimcar - confirm your registration', template=html)

        return marshal(new_user, resource_fields), 201


class ConfirmationView(Resource):
    """ConfirmationView API."""

    def get(self, token):
        """Check confirmation token."""
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first()
        if user.active:
            return 'Account is already confirmed.'
        if user:
            user.update(active=True)
            return 'Account confirmation was sucessful.', 200
        return 'Invalid confirmation token.', 406
