import os

# -------- App deploy preferences --------
host = '0.0.0.0'
port = 5000
debug = True
# ----------------------------------------


BASEDIR = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '?iu_V-8[InY2vo@ZqHD8|nZuFTu&0{'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbadmin:security1338@trabobdb.corzsedgktxs.us-west-2.rds.amazonaws.com:3306/trabobdb'

TELEGRAM_BOT_TOKEN = '356224566:AAEvmWALrQkLRmKhZ-Fs3AY2dqd4wLMkj80'

DEFAULT_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive',
                   'Content-Length': '96',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Cookie': 'sess_id=0948a947332fade30ff074a6797ea97c; lowRes=0; T3E=Wgp51I5rBTD8iz513h7z%2Bw%3D%3D%3A1KW%2FuiNX1B9KEE0iNWPyPVbEBsqWO8Lf%2BrefgefHSkbQWIuEjnWCsGmqWXRlvJL8XVczabds4LNsm1SlCGm1%2B4OR4TYsx4%2F9McDKSiXrBM2Zs7VIoRhZrJdK7ahhdifu%3AJ%2FJrhb9DzSSIlhSyYtZByvgzS84ngggKGwFtuqa1u8Y%3D',
                   'Host': 'ts6.travian.ru',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'X-Compress': 'null'}

LOGIN_URL = '/login.php'
LOGIN_POST_URL = '/dorf1.php'
