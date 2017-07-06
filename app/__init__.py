from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import config


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager(app)
bcrypt = Bcrypt(app)

# logging preparations

import logging
logger = logging.getLogger('trabob')

_console_handler = logging.StreamHandler()


_formatter = logging.Formatter('\x1b[36;1m[%(asctime)s]\x1b[0m %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

_console_handler.setFormatter(_formatter)
logger.addHandler(_console_handler)
logger.setLevel(getattr(logging, config.LOGLEVEL))


from app import views, models, travian
