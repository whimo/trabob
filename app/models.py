from app import app, db, logger
import requests
import pickle
import datetime
from bs4 import BeautifulSoup
import re
import random
import time


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(16), index=True, unique=True)
    password = db.Column(db.String(60))
    telegram_chat_id = db.Column(db.Integer, index=True)

    default_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    default_account = db.relationship('Account', uselist=False, foreign_keys='[User.default_account_id]')

    accounts = db.relationship('Account', backref='local_user', lazy='dynamic',
                               foreign_keys='[Account.user_id]')

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

    is_roman = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    session = requests.Session()
    session_dump = db.Column(db.PickleType)

    build_queue =  []
    resources_build_queue = []  # Only for romans

    def request(self, url, data={}):
        if self.session_dump is not None:
            self.session = pickle.loads(self.session_dump)

        try:
            if len(data) == 0:
                response = self.session.get(url, headers=app.config['DEFAULT_HEADERS'])
            else:
                response = self.session.post(url, headers=app.config['DEFAULT_HEADERS'], data=data)

        except Exception:
            logger.error('Network problem, the URL {} cannot be fetched.'.format(url))
            return False

        if 'href="login.php"' in response.text and 'login.php' not in url and len(url) >= 22:
            logger.warning('Player {} suddenly logged off, trying to relogin.'.format(self.username))

            if not self.login():
                return False
            return self.request(url=url, data=data)

        self.session_dump = pickle.dumps(self.session, 2)
        db.session.commit()

        if 'dorf' in url:
            self.get_busy_until(response.text)

        time.sleep(random.randint(0, 4) + random.random())  # Sleep a bit to avoid being caught

        return response.text

    def login(self):
        page = self.request(self.server_url + app.config['LOGIN_URL'])
        if not page:
            logger.error('Could not get the login page for {}, login failed.'.format(self.username))
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
            logger.error('Could not post login data for {}, login failed.'.format(self.username))
            return False

        if 'href="login.php"' in page:
            logger.error('Could not log in player {}, probably incorrect account data provided.'
                  .format(self.username))

            return False

        parser = BeautifulSoup(page, 'html5lib')

        self.is_roman = bool(parser.find('img', {'class': 'nation nation1'}))
        db.session.commit()

        return True

    def get_server_timezone(self):
        page = self.request(self.server_url + app.config['VILLAGE_URL'])
        if not page:
            logger.error('Could not get the village page for {}.'.format(self.username))
            return False

        utc_timestamp = int(datetime.datetime.utcnow().timestamp())

        parser = BeautifulSoup(page, 'html5lib')
        server_timestamp = int(parser.find('div', {'id': 'servertime'}).span['value'])

        self.server_timezone = round((server_timestamp - utc_timestamp) / 3600)
        return self.server_timezone

    def add_to_queue(self, item, resources=False):
        if not resources:
            self.build_queue.append(item)
        else:
            self.resources_build_queue.append(item)

    def build(self, name, place=None):
        page = self.request(self.server_url + (app.config['RESOURCES_URL'] if not place else
                                               app.config['VILLAGE_URL']))
        parser = BeautifulSoup(page, 'html5lib')

        area = parser.find('area', {'title': re.compile(name + '(?i)')})
        if area is None:
            if place is None:
                return self.build(name, place=1)

            elif place == 1:
                try:
                    area = random.choice(parser.find_all('area', {'title': lambda string: len(string) <= 20}))
                except IndexError:
                    logger.error('Could not find building area in place {} for {}, player {}.'.format(place, name, self.username))
                    return False
            else:
                logger.error('Could not find building area in place {} for {}, player {}.'.format(place, name, self.username))
                return False

        page = self.request(self.server_url + '/' + area['href'])
        parser = BeautifulSoup(page, 'html5lib')

        try:
            build_page = self.request(self.server_url + '/' + parser.find('button', {'class': 'green build'})['onclick'].split('\'')[1])
            return True

        except TypeError:
            try:
                build_page = self.request(self.server_url +
                                          '/' + parser.find('img', {'alt': re.compile(name + '(?i)')}).
                                          parent.parent.parent.
                                          find('button', {'class': 'green new'})['onclick'].split('\'')[1])
                return True

            except TypeError:
                logger.error('Could not build in place {} for {}, player {}.'.format(place, name, self.username))

            except AttributeError:
                logger.error('Could not build in place {} for {}, player {}.'.format(place, name, self.username))

        return False

    def get_busy_until(self, page=None):
        if page is None:
            page = self.request(self.server_url + app.config['VILLAGE_URL'])

        parser = BeautifulSoup(page, 'html5lib')

        try:
            build_duration = min([int(i.span['value']) for i in parser.find_all('div', {'class': 'buildDuration'})])
        except ValueError:
            build_duration = 0

        self.busy_until = datetime.datetime.utcnow() + datetime.timedelta(seconds=build_duration)
        db.session.commit()

        return self.busy_until
