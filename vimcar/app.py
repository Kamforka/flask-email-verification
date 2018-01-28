# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask

from vimcar import commands
from vimcar.extensions import api, bcrypt, db, migrate, mail
from vimcar.resources import users
from vimcar.settings import ProdConfig


def create_app(config_object=ProdConfig, api=api):
    """An application factory."""
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    register_resources(api)  # must add resources before calling init_app on the api
    register_extensions(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    api.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    return None


def register_resources(api):
    """Register Flask-restful resources."""
    api.add_resource(users.UserViewList, '/api/users')
    api.add_resource(users.UserView, '/api/users/<user_id>')
    api.add_resource(users.ConfirmationView, '/confirmation/<token>')
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': users.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.urls)
