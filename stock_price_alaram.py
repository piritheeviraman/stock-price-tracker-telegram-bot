# import the required libraries
import telegram.ext #This line imports the telegram.ext module. This module contains the classes and functions needed to create and manage Telegram bots.
import pandas_datareader as pdr  #This line imports the pandas_datareader library, which allows us to access financial data from various sources.We will use this library to get stock data from Yahoo Finance.
import time
import pandas as pd

updater = telegram.ext.Updater('5624094353:AAEiyRgPpAPStBJ0Ao5vL-RoI7AcLYhl4ig', use_context=True) # create an object of class Updater 
dispatcher=updater.dispatcher # create a dispatcher object

def start(update,context): # define a function for the start command
     update.message.reply_text("""welcome to stock price bot 
for any help --> /help""")

def help(update,context): # define a function for the help command
     update.message.reply_text("""
/getstockprice --> To cheak the company price
Eg:/getstockprice [company symbol]
'/getstockprice AAPL'
/setreminder --> To get notification of company price
Eg:/setreminder [company symbol] [highest price value] [lowest price value]
'/setreminder AAPL 140 140
/findticker --> To find ticker symbol of company
Eg:/findticker [company name]
/findticker APPLE""")

def findticker(update,context): # define a function for the companyticker command
     company_name = context.args[0]
     data = pd.read_html(f'https://finance.yahoo.com/quote/{company_name}')[1]
     ticker = data.at[1,'Ticker']
     tickers = ticker(company_name)
     update.message.reply_text(f"The {company_name} company ticker symbol{tickers}")

def getprice(update,context): # define a function for the getstockprice command
     ticker=context.args[0]
     msg=f'https://finance.yahoo.com/quote/{ticker}'
     last_price=[pdr.DataReader(ticker,'yahoo')["Adj Close"][-1]]
     update.message.reply_text(f"The current price of {ticker} is {last_price} {msg}")
#This code uses the pdr.DataReader function from the pandas_datareader library to pull the adjusted close price for the given ticker from Yahoo! Finance. The adjusted close price is the closing price of a stock that has been adjusted to account for any corporate actions that have occurred since the stock last traded.
def setreminder(update,context): # define a function for the setreminder command
     ticker=context.args[0]
     upper=context.args[1]
     lower=context.args[2]
     upper_limits=int(upper)
     lower_limits=int(lower)
     msg=f'https://finance.yahoo.com/quote/{ticker}'
     price=[pdr.DataReader(ticker,'yahoo')["Adj Close"][-1]]
     last_price=int(price[0])   

     if upper_limits < last_price:
          update.message.reply_text(f"{ticker} has reached a price of {last_price}. You might want to sell {msg}")
          time.sleep(0) #pause for 0 seconds
     elif lower_limits > last_price:
          update.message.reply_text(f"{ticker} has reached a price of {last_price}. You might want to buy {msg}")
          time.sleep(60) # pause for 60 seconds.

dispatcher.add_handler(telegram.ext.CommandHandler("start",start)) # handlers for the start commands
dispatcher.add_handler(telegram.ext.CommandHandler("help",help)) # handlers for the help commands
dispatcher.add_handler(telegram.ext.CommandHandler("setreminder",setreminder)) # handlers for the setreminder commands
dispatcher.add_handler(telegram.ext.CommandHandler("getprice",getprice)) # handlers for the getstockprice commands
dispatcher.add_handler(telegram.ext.CommandHandler("findticker",findticker))
updater.start_polling() # start the bot
updater.idle() # wait for the bot to stop

'''This is a python function that takes in three arguments - ticker, upper, and lower. The function then sets the upper and lower limits for the stock price. If the stock price goes above the upper limit, the function will send a message to the user telling them to sell the stock. If the stock price goes below the lower limit, the function will send a message to the user telling them to buy the stock.'''
'''
The code is adding handlers for different commands that the user can enter. The commands are "start", "help", "setreminder", "getprice", and "findticker". The code is also setting up a polling mechanism so that the bot can listen for incoming messages from the user.'''
'''The fifth line adds a handler for the findticker command. This means that when the bot receives a message with the text '/findticker', the 'findticker' function will be called.'''