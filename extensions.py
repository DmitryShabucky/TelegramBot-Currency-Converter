import requests
import json
from config import currency

class APIExceptions(Exception):
    pass

class CurrencyExchange:
    @staticmethod
    def get_price(values: list):
        if len(values) != 3:
            raise APIExceptions('Неверно введены параметры.\nПример ввода: рубль доллар 100\n/start')

        base, quote, amount = values

        if base == quote:
            raise APIExceptions(f"Нельзя конвертировать {currency[base]} в {currency[base]}.\
            \nПример ввода: рубль доллар 100\n/start")

        if base not in currency.keys() or quote not in currency.keys():
            raise APIExceptions('Неверный ввод параметров валют.\nПример ввода: рубль доллар 100\n/start')

        try:
            amount = float(amount)
        except:
            raise APIExceptions(f"Неверно введено количество - {amount}.\nПример ввода: рубль доллар 100\n/start")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={currency[quote]}&tsyms={currency[base]}')
        total_base = json.loads(r.content)[currency[base]]

        return f"{amount} {currency[base]} = {round(float(total_base) * float(amount), 2)} {currency[quote]}"
