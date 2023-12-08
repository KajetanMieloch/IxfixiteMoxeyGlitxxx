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

load_dotenv()

api_key = os.getenv('KEY')
api_secret = os.getenv('SECRET')

client = Client(api_key, api_secret, testnet=False)

klines = []

def nextDay(startingDate):
    startingDate = datetime.strptime(startingDate, "%d %B, %Y, %H:%M:%S")
    endingDate = startingDate + timedelta(days=1)
    return endingDate.strftime("%d %B, %Y, %H:%M:%S")

def nextXHours(startingDate, hours):
    startingDate = datetime.strptime(startingDate, "%d %B, %Y, %H:%M:%S")
    endingDate = startingDate + timedelta(hours=hours)
    return endingDate.strftime("%d %B, %Y, %H:%M:%S")

def nextXMinutes(startingDate, minutes):
    startingDate = datetime.strptime(startingDate, "%d %B, %Y, %H:%M:%S")
    endingDate = startingDate + timedelta(minutes=minutes)
    return endingDate.strftime("%d %B, %Y, %H:%M:%S")


startingDate = "1 November, 2023, 00:00:00"
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

fig, ax = plt.subplots()

def plot():

    # Extracting relevant data from the klines
    timestamps = [kline[0] for kline in klines]
    open_prices = [float(kline[1]) for kline in klines]
    high_prices = [float(kline[2]) for kline in klines]
    low_prices = [float(kline[3]) for kline in klines]
    close_prices = [float(kline[4]) for kline in klines]

    # Convert timestamps to datetime objects for better x-axis formatting
    dates = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in timestamps]


    ax.clear()
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

def update(i):
    global endingDate
    endingDate = nextXHours(endingDate, 1)
    getKlines()
    plot()  # Plot the new data
    print(endingDate)
    if endingDate == "02 November, 2023, 00:00:00":
        sys.exit()

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
