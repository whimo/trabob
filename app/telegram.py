from app import app, models, db, bcrypt
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
            return

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


bot.polling()
