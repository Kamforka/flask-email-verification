# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

api = Api()
bcrypt = Bcrypt()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
