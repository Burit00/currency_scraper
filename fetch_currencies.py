import database
from currency_endpoints import get_currencies
from currency_model import Currency

if __name__ == '__main__':
    currencies = get_currencies()

    mapped_currencies: list[Currency] = []
    for currency_key in currencies:
        currency = currencies[currency_key]
        mapped_currencies.append(Currency(code=currency['code'], symbol=currency['symbol'], name=currency['name']))

    database.add_currencies(mapped_currencies)



