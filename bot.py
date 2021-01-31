import telebot
import os
import redis
import json



REDIS_URL = os.environ.get('REDIS_URL')

dict_db = {}

def save(key, value):
    if REDIS_URL:
        redis_db = redis.from_url(REDIS_URL)
        redis_db.set(key,value)
    else:
        dict_db[key] = value

def load(key, value):
    if REDIS_URL:
        redis_db = redis.from_url(REDIS_URL)
        return redis_db.get(key)
    else:
        return dict_db.get(key)

token = os.environ['TELEGRAM_TOKEN']
IS_HEROKU = os.environ.get('HEROKU', False)

ADMINS = (0,1,2)

bot = telebot.TeleBot(token)
# MAIN_STATE = 'main'
# DATE_STATE = 'date_state'


@bot.message_handler(commands=['start'])
def start_cmd(message):

    # save('state:{}'.format(message.from_user.id), MAIN_STATE)
    # # save(str(message.from_user.id), MAIN_STATE)
    #
    # user_state = load('state:{}'.format(message.from_user.id))
    # # user_state = load(str(message.from_user.id))
    #
    # my_dict = {
    #     'a':10,
    #     'b': '223'
    #
    # }
    # my_dict_str = json.dumps(my_dict)
    #
    # save('key', my_dict_str)
    #
    #
    # my_dict = json.load(load('key'))

    if IS_HEROKU:
        bot.reply_to(message, 'Привет! я на Heroku\n'+str(REDIS_URL))
    else:
        bot.reply_to(message, 'Привет')

# https://devcenter.heroku.com/articles/python-runtimes

bot.polling()