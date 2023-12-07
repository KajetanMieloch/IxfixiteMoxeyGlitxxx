from binance import Client
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

load_dotenv()

api_key = os.getenv('KEY')
api_secret = os.getenv('SECRET')

client = Client(api_key, api_secret, testnet=False)

klines = []

for kline in client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
    klines.append(kline)

# Extracting relevant data from the klines
timestamps = [kline[0] for kline in klines]
open_prices = [float(kline[1]) for kline in klines]
high_prices = [float(kline[2]) for kline in klines]
low_prices = [float(kline[3]) for kline in klines]
close_prices = [float(kline[4]) for kline in klines]

# Convert timestamps to datetime objects for better x-axis formatting
dates = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in timestamps]

# Create a candlestick plot
fig, ax = plt.subplots()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
ax.xaxis.set_major_locator(mdates.HourLocator())

candlestick_data = list(zip(dates, open_prices, close_prices, low_prices, high_prices))
ax.plot(dates, open_prices, marker='o', linestyle='', color='green', label='Open')
ax.plot(dates, close_prices, marker='o', linestyle='', color='red', label='Close')
ax.vlines(dates, low_prices, high_prices, color='black', linewidth=2, label='Low/High')

plt.title('BNBBTC Candlestick Chart')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()