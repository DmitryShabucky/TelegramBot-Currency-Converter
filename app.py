import telebot

from config import *
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def message(message: telebot.types.Message):
    text = "Какие валюты хотите конвертировать?\nФормат ввода:\n<валюта>\
<в какую валюту><количество валюты>\nПример ввода: рубль доллар 100\nСписок доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def currenciec(message: telebot.types.Message):
    text = 'Список доступных валют: '
    for cur in currency.keys():
        text = '\n'.join((text, cur))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.lower()
    values = values.split(' ')
    try:
        text = CurrencyExchange.get_price(values)
        bot.send_message(message.chat.id, text)
    except APIExceptions as e:
         bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка сервера.\n{e}")

bot.polling(none_stop=True)
