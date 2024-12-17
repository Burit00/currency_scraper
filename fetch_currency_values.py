import time
from datetime import datetime, timedelta

import database
from currency_endpoints import get_historical_currency_values
from currency_model import CurrencyValue
from database import get_currency_value_last_date


if __name__ == '__main__':
    date_start = get_currency_value_last_date() + timedelta(days=1)
    date_end = datetime.now()

    error_counter = 0
    mapped_currency_values: list[CurrencyValue] = []
    date_subtract = date_end - date_start

    for day in range(date_subtract.days):
        date = date_start + timedelta(days=day)
        currency_values_from_api = None

        while currency_values_from_api is None:
            try:
                currency_values_from_api = get_historical_currency_values(date)

            except Exception as error:
                error_counter += 1
                print(f"{error_counter}. {error}")
                for i in range(3):
                    print(f"{60 - i * 20}s", end=', ')
                    time.sleep(20)
                print('', end='\n')

        date_string = str(date).split(' ')[0]
        currency_values_for_date = currency_values_from_api[date_string]
        for currency_code in currency_values_for_date:
            currency_value = currency_values_for_date[currency_code]
            mapped_currency_values.append(CurrencyValue(currency_code=currency_code,
                                                        value=currency_value,
                                                        date=date))

        if day % 10 == 0 or day == date_subtract.days - 1:
            database.add_currency_values(mapped_currency_values)
