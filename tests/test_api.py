# -*- coding: utf-8 -*-
"""Model unit tests."""
import pytest
from server.models.users import User
from server.utils import generate_confirmation_token

from .factories import UserFactory

@pytest.mark.usefixtures('db')
class TestUserView:
    """UserView tests."""

    def test_auth(self, testapp, user):
        """Test login requirements."""
        user_id = user.id
        user_endpoint = '/api/users/{0}'.format(user_id)
        testapp.get(user_endpoint, status=401)
        testapp.put(user_endpoint, status=401)

    def test_user_not_found(self, testapp_with_auth):
        """Test user not found through api."""
        testapp_with_auth.get('/api/users/404', status=404)

    def test_get_user_by_id(self, testapp_with_auth, user):
        """Test get user by id with api."""
        res = testapp_with_auth.get('/api/users/{user_id}'.format(user_id=user.id), status=201)

        assert res.json['id'] == user.id
        assert res.json['email'] == user.email
        assert res.json['active'] == user.active

    def test_update_user_not_found(self, testapp_with_auth):
        """Test non-existent user update with api."""
        res = testapp_with_auth.put_json('/api/users/404', status=404)
        assert res.json == 'User not found'

    def test_update_user(self, testapp_with_auth, user):
        """Test user update with api."""
        testapp_with_auth.put('/api/users/{user_id}'.format(user_id=user.id),
                              {'email': 'email@updated.com',}, status=201)

        assert user.email == 'email@updated.com'
        assert user.check_password('myprecious')  # password remain unchanged


@pytest.mark.usefixtures('db')
class TestUserViewList:
    """UserViewList tests."""

    def test_auth(self, testapp, user):
        """Test login requirements."""
        testapp.get('/api/users', status=401)

    def test_get_user_list(self, testapp_with_auth, user):
        """Test get list of users with api."""
        res = testapp_with_auth.get('/api/users')

        assert res.status_int == 200
        assert res.json[0]['id'] == user.id
        assert res.json[0]['email'] == user.email
        assert res.json[0]['active'] == user.active

    def test_create_user(self, testapp):
        """Test create user through api."""
        res = testapp.post('/api/users',
                           {'email': 'foo@bar.com', 'password': 'bar',}, status=201)
        user_id = res.json['id']

        assert res.json['email'] == 'foo@bar.com'
        assert res.json['active'] is False
        assert User.get_by_id(user_id)


    def test_user_already_exists(self, testapp, user):
        """Test create an already existent user."""
        res = testapp.post('/api/users',
                           {'email': user.email, 'password': 'bar',}, status=409)

        assert 'Email already registered' == res.json

@pytest.mark.usefixtures('db')
class TestConfirmationView:
    """Confirmation endpoint tests."""

    def test_invalid_token(self, testapp):
        """Test invalid confirmation token."""
        res = testapp.get('/confirmation/1nv4l1d70k3n', status=406)
        assert 'Invalid confirmation token.' == res.json

    def test_confirmation(self, testapp, user):
        """Test token confirmation."""
        assert user.active is False  # user is inactive
        token = generate_confirmation_token(user.email)
        res = testapp.get('/confirmation/{0}'.format(token), status=200)
        assert user.active is True
        assert 'Account confirmation was successful.' == res.json

    def test_already_confirmed_user(self, testapp, user):
        """Test activated user confirmation."""
        user = UserFactory(active=True)
        assert user.active is True
        token = generate_confirmation_token(user.email)
        res = testapp.get('/confirmation/{0}'.format(token), status=200)
        assert 'Account is already confirmed.' == res.json
