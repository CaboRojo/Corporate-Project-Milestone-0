from flask import Flask, render_template, render_template_string
import requests
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)

# The portfolio data you provided
portfolio_display_dict = {
    "MSFT": {
        "name": "Microsoft",
        "percentage_of_portfolio": "20%",
        "dollar_amount": 20000.0
    },
    "VERA": {
        "name": "Vera Therapeutics Inc.",
        "percentage_of_portfolio": "10%",
        "dollar_amount": 10000.0
    },
    "NU": {
        "name": "Nu Bank",
        "percentage_of_portfolio": "15%",
        "dollar_amount": 15000.0
    },
    "NVO": {
        "name": "Novo Nordisk",
        "percentage_of_portfolio": "25%",
        "dollar_amount": 25000.0
    },
    "LMT": {
        "name": "Lockheed Martin",
        "percentage_of_portfolio": "10%",
        "dollar_amount": 10000.0
    },
    "JPM": {
        "name": "Chase (JPMorgan Chase & Co.)",
        "percentage_of_portfolio": "20%",
        "dollar_amount": 20000.0
    }
}

def get_stock_data_for_last_12_months(symbol):
    base_url = "https://www.alphavantage.co/query?"
    function = "TIME_SERIES_DAILY"
    api_key = "OKRP7XRTHZE2LCWM"  # Replace YOUR_API_KEY with your actual API key
    url = f"{base_url}function={function}&symbol={symbol}&apikey={api_key}&outputsize=full"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            time_series = data["Time Series (Daily)"]
            # Sort the dates in descending order
            sorted_dates = sorted(time_series.keys())
            # Filter for the first entry of each month
            monthly_data = defaultdict(list)
            for date in sorted_dates:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                month_key = (date_obj.year, date_obj.month)
                monthly_data[month_key].append((date, time_series[date]["4. close"]))
            
            # Get the last entry for each month
            last_12_months_data = [monthly_data[month_key][-1] for month_key in sorted(monthly_data.keys(), reverse=True)[:12]]
            return last_12_months_data
        else:
            return "Data not available"
    else:
        return None

# HTML for the home page
home_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Investment Portfolio</title>
</head>
<body>
    <h1>Total Investment: 100,000€</h1>
    <table>
        <tr>
            <th>Company Name</th>
            <th>Symbol</th>
            <th>% of Portfolio</th>
            <th>Value</th>
        </tr>
        {% for symbol, stock in portfolio.items() %}
        <tr>
            <td>{{ stock.name }}</td>
            <td><a href="/details/{{ symbol }}">{{ symbol }}</a></td>
            <td>{{ stock.percentage_of_portfolio }}</td>
            <td>{{ stock.dollar_amount }}€</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# HTML for the details page
details_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Details for {{ stock.name }}</title>
</head>
<body>
    <h3>{{ stock.name }} ({{ symbol }})</h3>
    <h1>Details for {{ stock.name }}</h1>
    <table>
        <tr>
            <th>Symbol</th>
            <td>{{ symbol }}</td>
        </tr>
        <tr>
            <th>% of Portfolio</th>
            <td>{{ stock.percentage_of_portfolio }}</td>
        </tr>
        <tr>
            <th>Value</th>
            <td>{{ stock.dollar_amount }}€</td>
        </tr>
    </table>

    <!-- Price Data Table -->
    <h2>Price Data for the Last 12 Months</h2>
    <table>
        <tr>
            <th>Date</th>
            <th>Closing Price</th>
        </tr>
        {% for date, price in stock_data %}
        <tr>
            <td>{{ date }}</td>
            <td>{{ price }}</td>
        </tr>
        {% endfor %}
    </table>

    <a href="/">Back to Home</a>
</body>
</html>
"""

@app.route('/')
def home():
    # Use render_template_string to render the HTML with the portfolio data
    return render_template_string(home_html, portfolio=portfolio_display_dict)

@app.route('/details/<symbol>')
def details(symbol):
    stock_data = get_stock_data_for_last_12_months(symbol)
    if stock_data:
        # Use render_template_string to render the HTML with the stock data
        return render_template_string(details_html, stock=portfolio_display_dict[symbol], symbol=symbol, stock_data=stock_data)
    else:
        return "Stock data not found", 404


if __name__ == '__main__':
    app.run(debug=True)
