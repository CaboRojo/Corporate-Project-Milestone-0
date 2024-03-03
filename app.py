from flask import Flask, jsonify 
import requests
import json
from flask_cors import CORS
import datetime

with open("stock_portfolio.json", "r") as file:
    portfolio = json.load(file)

with open("stock_portfolio_details.json", "r") as file:
    portfolio_details = json.load(file)

app = Flask(__name__)
CORS(app)
    
def get_stock_final_price(symbol):
    base_url = "https://www.alphavantage.co/query?"
    function = "TIME_SERIES_DAILY"
    api_key = "OKRP7XRTHZE2LCWM"  # Replace YOUR_API_KEY with your actual API key
    url = f"{base_url}function={function}&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Check if the expected data is in the response
        if "Time Series (Daily)" in data:
            latest_date = max(data["Time Series (Daily)"].keys())
            final_price = data["Time Series (Daily)"][latest_date]["4. close"]
            return final_price
        else:
            # Handle cases where "Time Series (Daily)" is not present
            return "Data not available"
    else:
        return None

def portfolio_graph_landing_page(symbol):
    base_url = "https://www.alphavantage.co/query?"
    function = "TIME_SERIES_MONTHLY"
    api_key = "OKRP7XRTHZE2LCWM"
    url = f"{base_url}function={function}&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        if "Monthly Time Series" in data:
            dates = list(data["Monthly Time Series"].keys())
            dates.sort()
            prices = [data["Monthly Time Series"][date]["4. close"] for date in dates]
            return {"dates": dates, "prices": prices}
        
def calculate_portfolio_original(portfolio_details):
    original_value = 0
    # Iterate over each stock in the investments list
    for stock in portfolio_details["investments"]:
        # For each stock, sum up the amounts from each investment
        for investment in stock["investments"]:
            original_value += investment["amount"]
    return original_value

def calculate_portfolio_current(portfolio):
    current_value = 0
    for stock in portfolio["stocks"]:
        symbol = stock["symbol"]
        final_price = get_stock_final_price(symbol)
        if final_price:
            current_value += final_price * stock["quantity"]
    return current_value
    
    
@app.route('/portfolio/final_price')
def portfolio_final_price():
    prices = []
    for stock in portfolio["stocks"]:
        symbol = stock["symbol"]
        final_price = get_stock_final_price(symbol)
        if final_price:
            prices.append({"Symbol": symbol, "Final Price": final_price})
        else:
            prices.append({"Symbol": symbol, "Error": "Failed to fetch data"})
    return jsonify(prices)

@app.route('/portfolio/graph')
def portfolio_graph():
    graph_data = {}
    for stock in portfolio["stocks"]:
        symbol = stock["symbol"]
        data = portfolio_graph_landing_page(symbol)
        if data:
            last_12_months = data["dates"][-12:]
            prices = data["prices"][-12:]
            graph_data[symbol] = {"dates": last_12_months, "prices": prices}
        else:
            graph_data[symbol] = {"Error": "Failed to fetch data"}
    return jsonify(graph_data)

if __name__ == "__main__":
    app.run(debug=True)