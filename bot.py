import telebot
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, 'Привет!')



bot.polling()