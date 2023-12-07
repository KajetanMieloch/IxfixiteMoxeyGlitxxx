from binance import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('KEY')
api_secret = os.getenv('SECRET')

client = Client(api_key, api_secret, testnet=True)

status = client.get_system_status()
info = client.get_symbol_info('BTCUSDT')

print(status)
print(info)