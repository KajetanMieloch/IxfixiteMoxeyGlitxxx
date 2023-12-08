from binance import Client
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from binance.enums import *
import matplotlib.animation as animation
from datetime import datetime, timedelta
from matplotlib.animation import FuncAnimation
import sys
import collections
import numpy as np
import time

load_dotenv()

api_key = os.getenv('KEY')
api_secret = os.getenv('SECRET')

client = Client(api_key, api_secret, testnet=False)

klines = []

def nextDay(startingDate):
    startingDate = datetime.strptime(startingDate, "%d %B, %Y, %H:%M:%S")
    endingLocalDate = startingDate + timedelta(days=1)
    return endingLocalDate.strftime("%d %B, %Y, %H:%M:%S")

def nextXHours(startingDate, hours):
    startingDate = datetime.strptime(startingDate, "%d %B, %Y, %H:%M:%S")
    endingLocalDate = startingDate + timedelta(hours=hours)
    return endingLocalDate.strftime("%d %B, %Y, %H:%M:%S")

def nextXMinutes(startingDate, minutes):
    startingDate = datetime.strptime(startingDate, "%d %B, %Y, %H:%M:%S")
    endingLocalDate = startingDate + timedelta(minutes=minutes)
    return endingLocalDate.strftime("%d %B, %Y, %H:%M:%S")


startingDate = "5 November, 2023, 00:00:00"
endingLocalDate = startingDate
endingDate = "11 November, 2023, 00:00:00"


#Input range (low and high)
lowRange = 34150
highRange = 35950

openPosition = False

def getKlines():
    for kline in client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, startingDate, endingDate):
        klines.append(kline)


#Sredni wolumen 15 minutowy w tym przedziale czasowym pokazywany pod wykresem 

#Range of 15 minutes

#Breakout strategy
#If the price breaks the range, buy/sell
# Define the plot function

fig, ax = plt.subplots()
getKlines()
klinesInTimeRange = collections.deque(maxlen=96)

def plot(klinesInTimeRange):
    global openPosition
    #Now i need to get the data in range from startingDate to endingDate from the klines and without connecting to the API
    endingLocalDateTimestamp = datetime.strptime(endingLocalDate, "%d %B, %Y, %H:%M:%S").timestamp() * 1000
    for kline in klines:
        if endingLocalDateTimestamp <= kline[0] < endingLocalDateTimestamp + 60*60*1000:  # Check if the kline is within the next hour
            klinesInTimeRange.append(kline)
 
    # Pre-allocate memory for lists
    timestamps = np.empty(len(klinesInTimeRange))
    open_prices = np.empty(len(klinesInTimeRange))
    high_prices = np.empty(len(klinesInTimeRange))
    low_prices = np.empty(len(klinesInTimeRange))
    close_prices = np.empty(len(klinesInTimeRange))

    # Extracting relevant data from the klines
    for i, kline in enumerate(klinesInTimeRange):
        timestamps[i] = kline[0]
        open_prices[i] = float(kline[1])
        high_prices[i] = float(kline[2])
        low_prices[i] = float(kline[3])
        close_prices[i] = float(kline[4])

    # Convert timestamps to datetime objects for better x-axis formatting
    dates = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in timestamps]

    ax.clear()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.HourLocator())

    if open_prices[-1] > highRange and openPosition == False:
        openPosition = True
        #On the plot, show the position as as big green dot with text "Long" and price of the position
        ax.plot(dates[-1], open_prices[-1], marker='o', linestyle='', color='green', label='Open', markersize=12)
        ax.text(dates[-1], open_prices[-1], "Long", fontsize=12, color='green')
        print("Long")
    elif open_prices[-1] < lowRange and openPosition == False:
        openPosition = True
        print("Short")

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

def update(i):
    global endingLocalDate
    endingLocalDate = nextXHours(endingLocalDate, 1)
    plot(klinesInTimeRange)  # Plot the new data
    print(endingLocalDate)
    if endingLocalDate == endingDate:
        sys.exit()
        quit()

ani = animation.FuncAnimation(fig, update, interval=10, cache_frame_data=False)
ani.save('BTCUSDT.gif', writer='pillow')


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
