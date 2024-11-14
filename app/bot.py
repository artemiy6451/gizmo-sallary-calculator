import telebot

from config import API_TOKEN
from commands import calculate


bot = telebot.TeleBot(API_TOKEN)

calculate.register_commands(bot)

bot.polling(none_stop=True)
