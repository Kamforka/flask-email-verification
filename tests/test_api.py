# -*- coding: utf-8 -*-
"""Model unit tests."""
import pytest

from vimcar.models.users import User


@pytest.mark.usefixtures('db')
class TestAuth:
    """JWT Auth test."""

    def test_auth_invalid_credentials(self, testapp):
        """Test auth with invalid credentials."""
        res = testapp.post_json('/auth', dict(username='foo',
                                              password='bar',), status=401)
        assert res.json['description'] == 'Invalid credentials'

    def test_auth_valid_credentials(self, testapp):
        """Test auth with valid credentials."""
        user = User('foo', 'foo@bar.com', 'bar')
        user.save()

        res = testapp.post_json('/auth', dict(username='foo',
                                              password='bar'), status=200)

        assert res.json['access_token']  # token available


@pytest.mark.usefixtures('db')
class TestUserView:
    """UserView tests."""

    def test_user_not_found(self, testapp_with_auth):
        """Test user not found through api."""
        testapp_with_auth.get('/api/users/10', status=404)

    def test_get_user_by_id(self, testapp_with_auth, user):
        """Test get user by id with api."""
        res = testapp_with_auth.get('/api/users/{user_id}'.format(user_id=user.id), status=201)

        assert res.json['id'] == user.id
        assert res.json['username'] == user.username
        assert res.json['email'] == user.email

    def test_update_user_not_found(self, testapp_with_auth, user):
        """Test non-existent user update with api."""
        res = testapp_with_auth.put_json('/api/users/10', status=404)
        assert res.json == 'User not found'

    def test_update_user(self, testapp_with_auth, user):
        """Test user update with api."""
        testapp_with_auth.put('/api/users/{user_id}'.format(user_id=user.id),
                              {'username': 'updated_user',
                               'email': 'email@updated.com',
                               }, status=201)

        assert user.username == 'updated_user'
        assert user.email == 'email@updated.com'
        assert user.check_password('myprecious')  # password remain unchanged


@pytest.mark.usefixtures('db')
class TestUserViewList:
    """UserViewList tests."""

    def test_get_user_list(self, testapp_with_auth, user):
        """Test get list of users with api."""
        res = testapp_with_auth.get('/api/users')

        assert res.status_int == 200
        assert res.json[0]['username'] == user.username
        assert res.json[0]['email'] == user.email

    def test_create_user(self, testapp):
        """Test create user through api."""
        res = testapp.post('/api/users', {'username': 'foo',
                                          'password': 'bar',
                                          'email': 'foo@bar.com', }, status=201)
        user_id = res.json['id']

        assert res.json['username'] == 'foo'
        assert res.json['email'] == 'foo@bar.com'
        assert User.get_by_id(user_id)

    def test_user_already_exists(self, testapp, user):
        """Test create an already existent user."""
        res = testapp.post('/api/users', {'username': user.username,
                                          'password': 'bar',
                                          'email': 'foo@bar.com', }, status=409)

        assert 'User already exists' == res.json

    def test_email_already_registered(self, testapp, user):
        """Test create a user with an already registered email."""
        res = testapp.post('/api/users', {'username': 'foo',
                                          'password': 'bar',
                                          'email': user.email, }, status=409)

        assert 'Email already registered' == res.json
