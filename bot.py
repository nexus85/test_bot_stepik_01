import telebot
import os

token = os.environ['TELEGRAM_TOKEN']
IS_HEROKU = os.environ.get('HEROKU', False)

ADMINS = (0,1,2)

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    if IS_HEROKU:
        bot.reply_to(message, 'Привет! я на Heroku')
    else:
        bot.reply_to(message, 'Привет')

# https://devcenter.heroku.com/articles/python-runtimes

bot.polling()