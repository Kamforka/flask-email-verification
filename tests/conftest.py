# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from flask_restful import Api
from webtest import TestApp

from vimcar.app import create_app
from vimcar.database import db as _db
from vimcar.settings import TestConfig

from .factories import UserFactory


@pytest.yield_fixture(scope='function')
def api():
    """An api for the application tests."""
    _api = Api()

    yield _api


@pytest.yield_fixture(scope='function')
def app(api):
    """An application for the tests."""
    _app = create_app(TestConfig, api)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """A user for the tests."""
    user = UserFactory(password='myprecious')
    db.session.commit()
    return user


@pytest.fixture(scope='function')
def testapp_with_auth(app, user):
    """A JWT authenticated Webtest App."""
    _testapp_with_auth = TestApp(app)

    # important to use `post_json` method here instead of `post`, with the latter
    # the jwt auth handler cannot find the request data for some reason
    token = _testapp_with_auth.post_json('/auth', dict(username=user.username,
                                                       password='myprecious')).json['access_token']

    _testapp_with_auth.authorization = ('JWT', token)
    return _testapp_with_auth
