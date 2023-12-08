from binance import Client
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from binance.enums import *
import keyboard
import matplotlib.animation as animation

load_dotenv()

api_key = os.getenv('KEY')
api_secret = os.getenv('SECRET')

client = Client(api_key, api_secret, testnet=False)

klines = []

def nextDay(startingDate):
    startingDate = startingDate.split(" ")
    day = startingDate[0]
    month = startingDate[1]
    year = startingDate[2]
    if day == "31" and month == "December":
        day = "1"
        month = "January"
        year = str(int(year) + 1)
    elif day == "31" and month == "January":
        day = "1"
        month = "February"
    elif day == "28" and month == "February":
        day = "1"
        month = "March"
    elif day == "31" and month == "March":
        day = "1"
        month = "April"
    elif day == "30" and month == "April":
        day = "1"
        month = "May"
    elif day == "31" and month == "May":
        day = "1"
        month = "June"
    elif day == "30" and month == "June":
        day = "1"
        month = "July"
    elif day == "31" and month == "July":
        day = "1"
        month = "August"
    elif day == "31" and month == "August":
        day = "1"
        month = "September"
    elif day == "30" and month == "September":
        day = "1"
        month = "October"
    elif day == "31" and month == "October":
        day = "1"
        month = "November"
    elif day == "30" and month == "November":
        day = "1"
        month = "December"
    elif day == "29" and month == "February":
        day = "1"
        month = "March"
    else:
        day = str(int(day) + 1)
    return day + " " + month + " " + year

startingDate = "1 November, 2023"
endingDate = startingDate

#Input range (low and high)
lowRange = 34150
highRange = 35950

def getKlines():
    for kline in client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, startingDate, endingDate):
        klines.append(kline)


#Sredni wolumen 15 minutowy w tym przedziale czasowym pokazywany pod wykresem 

#Range of 15 minutes

#Breakout strategy
#If the price breaks the range, buy/sell
# Define the plot function
def plot():

    # Extracting relevant data from the klines
    timestamps = [kline[0] for kline in klines]
    open_prices = [float(kline[1]) for kline in klines]
    high_prices = [float(kline[2]) for kline in klines]
    low_prices = [float(kline[3]) for kline in klines]
    close_prices = [float(kline[4]) for kline in klines]

    # Convert timestamps to datetime objects for better x-axis formatting
    dates = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in timestamps]


    fig, ax = plt.subplots()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.HourLocator())

    candlestick_data = list(zip(dates, open_prices, close_prices, low_prices, high_prices))
    ax.plot(dates, open_prices, marker='o', linestyle='', color='green', label='Open')
    ax.plot(dates, close_prices, marker='o', linestyle='', color='red', label='Close')
    ax.vlines(dates, low_prices, high_prices, color='black', linewidth=2, label='Low/High')
    #Hlines of range
    ax.hlines(lowRange, dates[0], dates[-1], color='blue', linewidth=2, label='Low Range')
    ax.hlines(highRange, dates[0], dates[-1], color='blue', linewidth=2, label='High Range')

    plt.title('BTCUSDT Candlestick Chart')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

def update(i):
    global endingDate
    endingDate = nextDay(endingDate)
    getKlines()
    ax.clear()  # Clear the current plot
    plot()  # Plot the new data

fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
plt.show()


# balance = client.get_asset_balance(asset='USDT')
# print("USDT before: ", balance)
# balance = client.get_asset_balance(asset='BTC')
# print("BTC before: ", balance)

# order = client.create_order(
#     symbol='BTCUSDT',
#     side=SIDE_BUY,
#     type=ORDER_TYPE_MARKET,
#     quantity=0.1)

# balance = client.get_asset_balance(asset='USDT')
# print("USDT after: ", balance)
# balance = client.get_asset_balance(asset='BTC')
# print("BTC after: ", balance)

######## ANALYSIS OF THE DATA ########
