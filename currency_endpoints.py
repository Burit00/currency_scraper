from requests import HTTPError

import env
import requests
from datetime import datetime

access_key = env.ACCESS_KEY
base_url = env.BASE_API_URL
currencies_string = ','.join(env.CURRENCIES_LIST)


def get_historical_currency_values(date: datetime) -> dict:
    date = date.isoformat()

    url = f"{base_url}historical?apikey={access_key}&currencies={currencies_string}&date={date}"
    response = requests.get(url)
    response_data = response.json()

    if response.ok is not True:
        raise Exception(response.json()['message'])

    currency_values = response_data['data']
    return currency_values


def get_currencies() -> dict:
    url = f"{base_url}currencies?apikey={access_key}&currencies={currencies_string}"
    response = requests.get(url)

    response_data = response.json()
    currencies = response_data['data']

    return currencies