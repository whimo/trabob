from app import app, models, db, bcrypt, travian
import telebot

bot = telebot.TeleBot(app.config['TELEGRAM_BOT_TOKEN'])


@bot.message_handler(commands=['start', 'help'])
def hello(message):
    if models.User.query.filter_by(telegram_chat_id=message.chat.id).first() is None:
        bot.send_message(message.chat.id, 'You must /login to use this bot')


@bot.message_handler(commands=['login'])
def login(message):
    if models.User.query.filter_by(telegram_chat_id=message.chat.id).first() is None:
        try:
            username, password = message.text.split()[1:]
        except ValueError:
            bot.send_message(message.chat.id, 'Usage: `/login <username> <password>`')
            return False

        user = models.User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                user.telegram_chat_id = message.chat.id
                db.session.commit()
                bot.send_message(message.chat.id, 'Successfully logged in')
            else:
                bot.send_message(message.chat.id, 'But not')
        else:
            bot.send_message(message.chat.id, 'But not')

    else:
        bot.send_message(message.chat.id, 'You are already logged in')


@bot.message_handler(commands=['add_account'])
def add_account(message):
    user = models.User.query.filter_by(telegram_chat_id=message.chat.id).first()
    if user is None:
        return False

    try:
        server_name, username, password = message.text.split()[1:]
        server_url = 'http://' + server_name

    except ValueError:
        bot.send_message(message.chat.id, 'Usage: `/add_account <server (e.g. ts1.travian.net)> <username> <password>`')
        return False

    account = models.Account.query.filter_by(server_url=server_url, username=username).first()
    if account is not None:
        bot.send_message(message.chat.id, 'Account already added')
        return False

    account = models.Account(server_url=server_url, username=username, password=password, user_id=user.id)

    if account.login():
        bot.send_message(message.chat.id, 'Successfully added your account')
        db.session.add(account)
        db.session.commit()

        travian.travian_threads.append(travian.Travian(account.id))
        travian.travian_threads[-1].start()

    else:
        bot.send_message(message.chat.id, 'Could not login into your account, probably incorrect data provided')


@bot.message_handler(commands=['remove_account'])
def remove_account(message):
    user = models.User.query.filter_by(telegram_chat_id=message.chat.id).first()
    if user is None:
        return False

    try:
        server_name, username = message.text.split()[1:]

    except ValueError:
        bot.send_message(message.chat.id, 'Usage: `/remove_account <server (e.g. ts1.travian.net)> <username>`')
        return False

    account = models.Account.query.filter_by(server_url='http://' + server_name, username=username).first()
    if account is None or account.local_user.telegram_chat_id != message.chat.id:
        bot.send_message(message.chat.id, 'Account not found, probably incorrect data provided')
        return False

    db.session.delete(account)
    db.session.commit()
    bot.send_message(message.chat.id, 'Account removed successfully')


bot.polling()
