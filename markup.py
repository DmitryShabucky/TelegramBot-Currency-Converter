from telebot import types
from config import currency

def create_markup(base=None):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for cur in currency:
        if cur != base:
            buttons.append(types.KeyboardButton(cur.capitalize()))
    markup.add(*buttons)
    return markup