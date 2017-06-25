from app import app, models, db, forms, lm, bcrypt
from flask import render_template, redirect, url_for, g, session
from flask_login import login_user, logout_user, login_required, current_user


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if g.user.is_authenticated:
        return redirect(url_for('manage'))

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('manage'))

            else:
                return 'But not'
        else:
            return 'But not'

    return render_template(
        'index.html',
        form=form)


@app.route('/manage')
@login_required
def manage():
    try:
        account = models.Account.query.get(session['current_account'])
    except KeyError:
        account = g.user.default_account

    if account is None:
        return redirect(url_for('add_account'))

    return render_template('manage.html',
                           account=account)


@app.route('/add_account')
@login_required
def add_account():
    form = forms.AddAccountForm()
    if form.validate_on_submit():
        account = models.Account(server_url = form.server_url.data,
                                 username = form.username.data,
                                 password = form.password.data,
                                 user_id = g.user.id)
        db.session.add(account)
        db.session.commit()

        if form.default.data:
            g.user.default_account = account.id
            db.session.commit()

        return redirect(url_for('manage'))

    return render_template('add_account.html',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user(g.user)
    return redirect(url_for('index'))
