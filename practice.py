import pprint # for better formatting on printing

# Load evironment variables from .env file
import os
from dotenv import load_dotenv
load_dotenv()

PUBLIC_KEY = os.getenv("PHEMEX_PUBLIC_KEY")
PRIVATE_KEY = os.getenv("PHEMEX_PRIVATE_KEY")


# Connect to Phemex

import ccxt

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

# Making an order


