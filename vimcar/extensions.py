# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
bcrypt = Bcrypt()
cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
