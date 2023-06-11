import telebot
import time
import pandas_datareader as pdr
import re
import yfinance as yf

# Create an instance of the bot
bot_token = '<YOUR_BOT_TOKEN>'
bot = telebot.TeleBot(bot_token)


# Dictionary to store user price reminders
REMINDERS = {}

# Define the /start command handler
@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.reply_to(message, "Welcome to the Stock Price Bot! To get started, type /help for a list of available commands.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Define the /help command handler
@bot.message_handler(commands=['help'])
def help(message):
    try:
        bot.reply_to(message, "Here's a list of available commands:\n/getprice [symbol] - Get the current price of a stock\n/setreminder [symbol] [high_price] [low_price] - Set a price alert for a stock\n/removereminder [symbol] - Remove a price alert for a stock\n/listreminders - List all your active price alerts")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Define the /getprice command handler
@bot.message_handler(commands=['getprice'])
def getprice(update):
    try:
        message_text = update.text
        match = re.search(r"\/getprice\s+(\S+)", message_text)
        if match:
            ticker = match.group(1)
            msg = f'https://finance.yahoo.com/quote/{ticker}'
            data = yf.download(tickers=ticker, period='1d', interval='1d')
            if data.empty:
                bot.send_message(update.chat.id, f"No data available for {ticker}.")
            else:
                last_price = data["Adj Close"].iloc[-1]
                bot.send_message(update.chat.id, f"The current price of {ticker} is {last_price:.2f} {msg}")
        else:
            bot.send_message(update.chat.id, "Invalid command format. Please use /getprice [symbol] to get the current price of a stock.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Define the /setreminder command handler
@bot.message_handler(commands=['setreminder'])
def setreminder(update):
    try:
        message_text = update.text
        match = re.search(r"\/setreminder\s+(\S+)\s+(\d+)\s+(\d+)", message_text)
        if match:
            user_id = update.chat.id
            ticker = match.group(1)
            upper_limit = float(match.group(2))
            lower_limit = float(match.group(3))
            msg = f'https://finance.yahoo.com/quote/{ticker}'
            data = yf.download(tickers=ticker, period='1d', interval='1d')
            if data.empty:
                bot.send_message(update.chat.id, f"No data available for {ticker}.")
            else:
                last_price = data["Adj Close"].iloc[-1]
                # Store the reminder data in the dictionary
                if user_id not in REMINDERS:
                    REMINDERS[user_id] = {}
                REMINDERS[user_id][ticker] = {"upper_limit": upper_limit, "lower_limit": lower_limit}

                if upper_limit < last_price:
                    bot.send_message(update.chat.id, f"{ticker} has reached a price of {last_price:.2f}. You might want to sell {msg}")
                    time.sleep(30)
                elif lower_limit > last_price:
                    bot.send_message(update.chat.id, f"{ticker} has reached a price of {last_price:.2f}. You might want to buy {msg}")
                    time.sleep(30)
                else:
                    bot.send_message(update.chat.id, f"A price alert has been set for {ticker}. You will be notified when the price reaches {upper_limit:.2f} or {lower_limit:.2f}.")
        else:
            bot.send_message(update.chat.id, "Invalid command format. Please use /setreminder [symbol] [high_price] [low_price] to set a price alert for a stock.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



# Define the /removereminder command handler
@bot.message_handler(commands=['removereminder'])
def removereminder(update):
    try:
        message_text = update.text
        match = re.search(r"\/removereminder\s+(\S+)", message_text)
        if match:
            user_id = update.chat.id
            ticker = match.group(1)

            if user_id in REMINDERS and ticker in REMINDERS[user_id]:
                del REMINDERS[user_id][ticker]
                bot.send_message(update.chat.id, f"A price alert has been removed for {ticker}.")
            else:
                bot.send_message(update.chat.id, f"No price alert was found for {ticker}.")
        else:
            bot.send_message(update.chat.id, "Invalid command format. Please use /removereminder [symbol] to remove a price alert for a stock.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Define the /listreminders command handler
@bot.message_handler(commands=['listreminders'])
def listreminders(update):
    try:
        user_id = update.chat.id

        if user_id in REMINDERS:
            reminders = REMINDERS[user_id]
            if len(reminders) == 0:
                bot.send_message(update.chat.id, "You don't have any active price alerts.")
            else:
                msg = "Here are your active price alerts:\n"
                for ticker, data in reminders.items():
                    msg += f"{ticker}: upper limit = {data['upper_limit']}, lower limit = {data['lower_limit']}\n"
                bot.send_message(update.chat.id, msg)
        else:
            bot.send_message(update.chat.id, "You don't have any active price alerts.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Start the bot
try:
    bot.polling()
except Exception as e:
    print(f"An error occurred while running the bot: {str(e)}")
