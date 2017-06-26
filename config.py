import os

# -------- App deploy preferences --------
host = '0.0.0.0'
port = 5000
debug = True
# ----------------------------------------


BASEDIR = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '?iu_V-8[InY2vo@ZqHD8|nZuFTu&0{'

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

TELEGRAM_BOT_TOKEN = '356224566:AAEvmWALrQkLRmKhZ-Fs3AY2dqd4wLMkj80'
