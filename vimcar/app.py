# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask

from vimcar import commands
from vimcar.auth import jwt
from vimcar.extensions import api, bcrypt, cache, cors, db, migrate
from vimcar.resources import users
from vimcar.settings import ProdConfig


def create_app(config_object=ProdConfig, api=api):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    :param api: The Flask-restful API instance.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    register_resources(api)  # must add resources before calling init_app on the api
    register_extensions(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions.

    :param app: The Flask application instance.
    """
    api.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_resources(api):
    """Register Flask-restful resources.

    :param api: The Flask-restful API instance.
    """
    api.add_resource(users.UserViewList, '/api/users')
    api.add_resource(users.UserView, '/api/users/<user_id>')
    return None


def register_shellcontext(app):
    """Register shell context objects.

    :param app: The Flask application instance.
    """
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': users.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands.

    :param app: The Flask application instance.
    """
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
