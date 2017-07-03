from app import app, db
import requests
import pickle
import datetime
from bs4 import BeautifulSoup


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(16), index=True, unique=True)
    password = db.Column(db.String(60))
    telegram_chat_id = db.Column(db.Integer, index=True)

    default_account_id = db.Column(db.Integer)

    accounts = db.relationship('Account', backref='local_user', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    server_url = db.Column(db.String(30))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    server_timezone = db.Column(db.SmallInteger)
    busy_until = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    session = requests.Session()
    session_dump = db.Column(db.PickleType)

    proxies = db.relationship('Proxy', backref='account', lazy='dynamic')

    def request(self, url, data={}):
        if self.session_dump is not None:
            self.session = pickle.loads(self.session_dump)

        try:
            if len(data) == 0:
                response = self.session.get(url, headers=app.config['DEFAULT_HEADERS'])
            else:
                response = self.session.post(url, headers=app.config['DEFAULT_HEADERS'], data=data)

        except Exception:
            print('[ERROR] Network problem, the URL {} cannot be fetched.'.format(url))
            return False

        if 'href="login.php"' in response.text and 'login.php' not in url and len(url) >= 22:
            print('[WARNING] Player {} suddenly logged off, trying to relogin.'.format(self.username))

            if not self.login():
                return False
            return self.request(url=url, data=data)

        self.session_dump = pickle.dumps(self.session, 2)
        db.session.commit()

        return response.text

    def login(self):
        page = self.request(self.server_url + app.config['LOGIN_URL'])
        if not page:
            print('[ERROR] Could not get the login page for {}, login failed.'.format(self.username))
            return False

        parser = BeautifulSoup(page, 'html5lib')

        s1 = parser.find('button', {'name': 's1'})['value'].encode('utf-8')
        login_code = parser.find('input', {'name': 'login'})['value']

        login_data = {
            'name': self.username,
            'password': self.password,
            's1': s1,
            'w': '1366:768',
            'login': login_code}

        page = self.request(self.server_url + app.config['LOGIN_POST_URL'], login_data)
        if not page:
            print('[ERROR] Could not post login data for {}, login failed.'.format(self.username))
            return False

        if 'href="login.php"' in page:
            print('[ERROR] Could not log in player {}, probably incorrect account data provided.'.format(self.username))
            return False

        return True

    def get_server_timezone(self):
        page = self.request(self.server_url + app.config['VILLAGE_URL'])
        if not page:
            print('[ERROR] Could not get the village page for {}.'.format(self.username))
            return False

        utc_timestamp = int(datetime.datetime.utcnow().timestamp())

        parser = BeautifulSoup(page, 'html5lib')
        server_timestamp = int(parser.find('div', {'id': 'servertime'}).span['value'])

        self.server_timezone = round((server_timestamp - utc_timestamp) / 3600)
        return self.server_timezone


class Proxy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(21))  # max: 255.255.255.255:65535

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def ping(self):
        ''' Return availability of proxy '''
        import json
        resp = requests.get('httpbin.org/ip', proxies = {'http' : self.url})
        if resp.status_code is requests.codes.ok:
            if json.loads(resp.text)['origin'] is self.url.split(':')[0]:
                return True

        return False
