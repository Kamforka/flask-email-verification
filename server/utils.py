# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""

from flask import render_template, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from server.extensions import mail
from server.settings import Config


def generate_confirmation_token(email):
    """Confirmation email token."""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt=Config.SECURITY_SALT)


def confirm_token(token, expiration=3600):
    """Plausibility check of confirmation token."""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=Config.SECURITY_SALT, max_age=expiration)
    except:
        return False
    return email


def send_email(to, subject, template):
    """Send an email."""
    msg = Message(subject, recipients=[to], html=template)
    mail.send(msg)

def send_confirmation_email(to):
    """Send a confirmation email to the registered user."""
    token = generate_confirmation_token(to)
    confirm_url = url_for('confirmationview', token=token, _external=True)
    html = render_template('confirmation.html', confirm_url=confirm_url)
    send_email(to, 'Test server - confirm your registration', html)
