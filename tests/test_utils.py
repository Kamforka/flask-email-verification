# -*- coding: utf-8 -*-
"""Utility unit tests."""
import pytest

from server.utils import confirm_token, generate_confirmation_token


class TestUtilities:
    """Project utility methods tests."""

    def test_token_confirmation(self):
        """Test confirmation of email token."""
        email = 'foo@bar.com'
        token = generate_confirmation_token(email)
        assert email == confirm_token(token)
