import ccxt
import pprint  # for better formatting on printing
import time # for sleeping
import schedule

# Load evironment variables from .env file
import os
from dotenv import load_dotenv
load_dotenv()

PUBLIC_KEY = os.getenv("PHEMEX_PUBLIC_KEY")
PRIVATE_KEY = os.getenv("PHEMEX_PRIVATE_KEY")


# Connect to Phemex


phemex = ccxt.phemex(
    {
        "enableRateLimit": True,
        "apiKey": PUBLIC_KEY,
        "secret": PRIVATE_KEY,
        # "uid": False,
        # "login": False,
        # "password": False,
        # "twofa": False,
        # "privateKey": False,
        # "walletAddress": False,
        # "token": False,
    }
)

USDT_bal = phemex.fetch_balance()['USDT']
pprint.pprint(USDT_bal)


# Making A Buy Order
def buy():
    symbol = 'uBTCUSD'
    size = 1
    bid = 10000
    params = {
        'timeInForce': 'PostOnly'
    }
    order = phemex.create_limit_buy_order(symbol, size, bid, params)
    
    # Sleep for 10 seconds
    time.sleep(5)
    
    # Cancel The Order
    phemex.cancel_all_orders(symbol)
