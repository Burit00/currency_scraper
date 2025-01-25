from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

from currency_charts import generate_currency_comparison, generate_currency_comparison_for_month
from database import get_currencies, get_currency_value_first_date, get_currency_value_last_date

app = Flask(__name__)

@app.route('/')
def index():
    # Pobierz dostępne waluty z bazy danych
    currencies = get_currencies()
    min_date = get_currency_value_first_date()
    max_date = get_currency_value_last_date()

    return render_template('index.html', currencies=currencies, min_date=min_date.date(), max_date=max_date.date())

@app.route('/monthly')
def monthly():
    # Pobierz dostępne waluty z bazy danych
    currencies = get_currencies()
    min_year = get_currency_value_first_date().year
    max_year = get_currency_value_last_date().year

    return render_template('monthly.html', currencies=currencies, max_year=max_year, min_year=min_year)

@app.route('/plot-monthly', methods=['POST'])
def plot_monthly():
    month = int(request.form.get('month'))
    years = [int(year) for year in request.form.getlist('years')]
    base_currency = request.form.get('base_currency')
    currency_to_conversion = request.form.get('currency_to_conversion')

    generate_currency_comparison_for_month(month, years, converted=currency_to_conversion, base=base_currency)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render_template('monthly-plot.html', plot=image_base64)

@app.route('/plot', methods=['POST'])
def plot():
    # Pobieranie danych z formularza
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    base_currency = request.form.get('base_currency')
    currencies_to_conversion = request.form.getlist('currencies_to_conversion')

    # Konwersja dat na obiekt datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    generate_currency_comparison(date_end=end_date, date_start=start_date, base=base_currency, converted=currencies_to_conversion)
    # Zapisanie wykresu jako obraz
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Przekazanie wykresu jako dane base64 do przeglądarki
    return render_template('plot.html', plot=image_base64)

if __name__ == '__main__':
    app.run(debug=True)
