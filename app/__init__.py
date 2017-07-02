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
_format = '[%(asctime)s] %(levelname)s: %(message)s'
_datefmt = '%m/%d/%Y %I:%M:%S %p'
logging.basicConfig(format=_format, datefmt=_datefmt)
logger = logging.getLogger('trabob')

_console_handler = logging.StreamHandler()

try:
    _console_handler.setLevel(getattr('logging', config.LOGLEVEL))
except AttributeError:
    _console_handler.setLevel(logging.ERROR)

_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

_console_handler.setFormatter(_formatter)
logger.addHandler(_console_handler)


from app import views, models, travian
