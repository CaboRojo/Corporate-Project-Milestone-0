# Investment Portfolio App

This is a Flask-based web application that displays an investment portfolio. It provides an overview of the portfolio and detailed information about each stock, including price data for the last 12 months.

## Features

- View a summary of the investment portfolio, including company names, symbols, percentage of the portfolio, and dollar values.
- View detailed information about each stock, including historical price data for the last 12 months.

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/yourrepository.git

2. Navigate to the project directory:
   ```sh
   cd yourrepository
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt

## Usage

1. Replace the `api_key` in `get_stock_data_for_last_12_months()` function with your own API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

2. Run the Flask application:
   ```sh
   python app.py

3. Open your web browser and go to:
   ```
   http://127.0.0.1:5000/

## Important Note on API Key Security

- The current implementation uses an API key for Alpha Vantage directly in the code. **Do not expose your API key in public repositories**.
- Consider using environment variables to store your API key securely:
  ```python
  import os
  api_key = os.getenv('ALPHAVANTAGE_API_KEY')
  ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application is for demonstration purposes only and should not be used for actual financial decisions. Always consult with a financial advisor before making investment decisions.
