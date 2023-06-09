# Stock Price Telegram Bot

This Telegram bot allows users to get real-time stock prices, set price alerts, and manage their reminders. It interacts with Yahoo Finance API to fetch stock data and utilizes the Telegram Bot API for user interactions.

## Features

- Get the current price of a stock by providing the stock symbol.
- Set price alerts for specific stocks with upper and lower price limits.
- Remove price alerts for individual stocks.
- List all active price alerts for a user.

## Requirements

- Python 3.7 or higher
- Required libraries: telebot, time, re, yfinance

## Usage

1. Create a new bot on the Telegram Bot API and obtain the bot token.
2. Install the required libraries using pip: `pip install telebot pandas_datareader yfinance`.
3. Replace the `bot_token` variable in the code with your bot token.
4. Run the script using `python bot.py`.
5. Interact with the bot on Telegram using the available commands.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
