import calendar

import database
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def generate_currency_comparison(converted: list[str] = ['PLN'], base: str = 'USD', date_start: datetime = None, date_end: datetime = None):
    plt.figure(figsize=(12,6))
    plt.title(f'Wartości walut: {', '.join(converted)} w odniesieniu do wartości waluty ' + base)

    base_currency_values = database.get_currency_values(date_start, date_end, [base])

    for converted_currency in converted:
        currency_values = database.get_currency_values(date_start, date_end, [converted_currency])

        dates = []
        values = []

        for currency_value in currency_values:
            base_currency_value = next(base_cv for base_cv in base_currency_values if base_cv.date == currency_value.date)

            dates.append(currency_value.date)
            values.append(currency_value.value / base_currency_value.value)

        plt.plot(dates, values, label=converted_currency)
    plt.legend()


def generate_currency_comparison_for_month(month: int, years: list[int], converted: str = 'PLN', base: str = 'USD'):
    plt.figure(figsize=(12,6))
    plt.title(f'Wartości waluty: {converted} w odniesieniu do wartości waluty {base}')

    for year in years:
        date_start = datetime(year, month, 1)
        date_end = datetime(year, month, calendar.monthrange(year, month)[1])

        base_currency_values = database.get_currency_values(date_start, date_end, [base])
        currency_values = database.get_currency_values(date_start, date_end, [converted])

        days = []
        values = []

        for currency_value in currency_values:
            base_currency_value = next(base_cv for base_cv in base_currency_values if base_cv.date == currency_value.date)

            days.append(currency_value.date.day)
            values.append(currency_value.value / base_currency_value.value)

        plt.plot(days, values, label=year)
    plt.legend()
