# -*- coding: utf-8 -*-
"""User resources."""

from flask_jwt import jwt_required
from flask_restful import Resource, fields, marshal, marshal_with
from webargs import fields as argfields
from webargs.flaskparser import use_args

from vimcar.models.users import User

user_args = {
    'username': argfields.Str(),
    'password': argfields.Str(),
    'email': argfields.Str(),
}


resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
}


class UserView(Resource):
    """UserView API."""

    def get(self, user_id):
        """Get a user."""
        user = User.get_by_id(user_id)
        if user:
            return marshal(user, resource_fields), 201
        return 'User not found', 404

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

    @marshal_with(resource_fields)
    def get(self):
        """List users."""
        return User.query.all(), 200

    @use_args(user_args)
    def post(self, args):
        """Register user."""
        user = User.query.filter_by(username=args['username']).first()

        if user:
            return 'User already exists', 409

        user = User.query.filter_by(email=args['email']).first()
        if user:
            return 'Email already registered', 409

        return marshal(User.create(username=args['username'],
                                   email=args['email'],
                                   password=args['password']), resource_fields), 201
