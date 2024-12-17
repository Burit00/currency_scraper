import database
from datetime import datetime
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
    plt.show()


if __name__ == '__main__':
    generate_currency_comparison(converted=['PLN', 'EUR'], base='USD', date_end=datetime(2020, 2, 1))
    generate_currency_comparison(converted=['EUR', 'USD', 'CHF'], base='PLN', date_end=datetime(2020, 2, 1))