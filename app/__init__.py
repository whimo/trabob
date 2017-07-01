from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager(app)
bcrypt = Bcrypt(app)

import logging
_default_format = '[%(asctime)] %(levelname): %(message)'
logging.basicConfig(format=_default_format)
logger = logging.getLogger()


from app import views, models, travian
