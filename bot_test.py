import telebot
import json
from telebot import types
from settings import TOKEN


def chende_date(key, user_id, value):
    data[key][user_id] = value
    json.dump(data, open('db/db.json', 'w', encoding='utf-8')
              , indent=2, ensure_ascii=False)


MAIN_STATE = 'main'
CITY_STATE = 'city'
WEATHER_DATE_STATE = 'weather_date_handler'

bot = telebot.TeleBot(TOKEN)

try:
    data = json.load(open('db/db.json', 'r', encoding='utf-8'))
except FileNotFoundError:
    data = {
        'states': {},
        MAIN_STATE: {

        },
        CITY_STATE: {

        },
        WEATHER_DATE_STATE: {

        }
    }
@bot.message_handler(func=lambda message: True)
def dispatcher(message):
    user_id = str(message.from_user.id)
    state = data['states'].get(user_id, MAIN_STATE)

    if state == MAIN_STATE:
        main_handler(message)
    elif state == CITY_STATE:
        city_handler(message)
    elif state == WEATHER_DATE_STATE:
        weather_date(message)

def main_handler(message):
    user_id = str(message.from_user.id)

    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Погода'))
        bot.send_message(user_id, 'Этот бот умеет предсказывать погоду', reply_markup=markup)
        chende_date('states', user_id, MAIN_STATE)

    elif message.text == 'Погода':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(
            *[types.KeyboardButton(button) for button in ['мск', 'спб']]
        )
        bot.send_message(user_id, 'А какой город? Я могу в спб или мск', reply_markup=markup)

        chende_date('states', user_id, CITY_STATE)


    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Погода'))
        bot.send_message(user_id, 'Этот бот умеет предсказывать погоду', reply_markup=markup)
        chende_date('states', user_id, MAIN_STATE)
        # markup = types.ReplyKeyboardRemove()
        # bot.send_message(user_id, 'Я тебя не понял', reply_markup=markup)




def city_handler(message):
    user_id = str(message.from_user.id)
    print(message.text)
    if message.text.lower() in ['мск', 'спб']:
        chende_date(WEATHER_DATE_STATE, user_id, message.text.lower())
        # data[WEATHER_DATE_STATE][user_id] = message.text.lower()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(
            *[types.KeyboardButton(button) for button in ['сегодня', 'завтра']]
        )
        bot.send_message(user_id, 'А какая дата? Введи "сегодня" или "завтра"', reply_markup=markup)
        chende_date('states', user_id, WEATHER_DATE_STATE)
        # data['states'][user_id] = WEATHER_DATE_STATE
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(
            *[types.KeyboardButton(button) for button in ['мск', 'спб']]
        )
        # bot.reply_to(message, 'Я тебя не понял1111')
        bot.send_message(user_id, 'Я тебя не понял1111', reply_markup=markup)

WEATHER = {
    'спб': {
        'сегодня': "27",
        'завтра': "32"
    },
    'мск': {
        'сегодня': '23',
        'завтра': '24'
    },
}

def weather_date(message):
    user_id = str(message.from_user.id)
    city = data[WEATHER_DATE_STATE][user_id]

    if message.text == 'сегодня':
        bot.send_message(user_id, WEATHER[city][message.text.lower()])
        chende_date('states', user_id, MAIN_STATE)
        # data['states'][user_id] = MAIN_STATE
    elif message.text == 'завтра':
        bot.send_message(user_id, WEATHER[city][message.text.lower()])
        chende_date('states', user_id, MAIN_STATE)
        # data['states'][user_id] = MAIN_STATE
    elif message.text == 'Назад':
        bot.send_message(user_id, 'Вернулся назад')
        chende_date('states', user_id, MAIN_STATE)
        # data['states'][user_id] = MAIN_STATE
    else:
        bot.reply_to(message, 'Я тебя не понял')



if __name__ == '__main__':
    bot.polling()
    print('бот остановлен')