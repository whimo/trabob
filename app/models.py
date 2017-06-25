from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(16))
    password = db.Column(db.String(60))

    default_account = db.Column(db.Integer, db.ForeignKey('account.id'))

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

    server_url = db.Column(db.String(16))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
