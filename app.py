import telebot

from config import *
from extensions import *
from markup import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['values'])
def currenciec(message: telebot.types.Message):
    text = 'Список доступных валют: '
    for cur in currency.keys():
        text = '\n'.join((text, cur))
    bot.reply_to(message, f'{text}\n/convert - конвертер')

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Начнем конвертацию валют! \n/convert - конвертер'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберете вылюту для конвертации: '
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, base_handler)

def base_handler(message:telebot.types.Message):
    base = message.text.lower()
    bot.send_message(message.chat.id, 'В какую валюту конвертировать?', reply_markup=create_markup(base))
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.lower()
    bot.send_message(message.chat.id, 'Сколько конвертировать?')
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message:telebot.types.Message, base,quote):
    amount = message.text
    values = base, quote, amount

    try:
        text = CurrencyExchange.get_price(values)
        bot.send_message(message.chat.id, 'Результат:\n\n' + text + '\n\n/convert - конвертер')
    except APIExceptions as e:
         bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка сервера.\n{e}\n/start")

bot.polling(none_stop=True)
