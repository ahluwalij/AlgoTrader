
import ccxt
import pprint  # for better formatting on printing
import time  # for sleeping
import schedule

# Load evironment variables from .env file
import os
from dotenv import load_dotenv
load_dotenv()

PUBLIC_KEY = os.getenv("PHEMEX_PUBLIC_KEY")
PRIVATE_KEY = os.getenv("PHEMEX_PRIVATE_KEY")
SYMBOL = os.getenv("SYMBOL")
TICKER = os.getenv("TICKER")
sl_percent = .2  # percent to take loss on trades
tp_percent = .25  # percent to take profit on trades

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
def long():
    position, in_position, long = get_position(phemex, SYMBOL)
    if in_position:
        # get your current position information (position is a dict of position information)
        close_position(phemex, SYMBOL)
    if not in_position:
        size = 600
        bid = ask_bid(SYMBOL)[1]
        params = {
            'timeInForce': 'PostOnly',
            'stopLoss': bid * (1-(sl_percent/100)),
            'takeProfit': bid * (1+(tp_percent/100)),
        }
        order = phemex.create_limit_buy_order(SYMBOL, size, bid, params)

    # Sleep for 30 seconds
    # time.sleep(30)

    # Cancel The Order
    # phemex.cancel_all_orders(SYMBOL)

# Making A Sell Order


def short():
    close_position(phemex, SYMBOL)
    # get your current position information (position is a dict of position information)
    position, in_position, long = get_position(phemex, SYMBOL)
    if not in_position:
        size = 600
        ask = ask_bid(SYMBOL)[0]
        params = {
            'timeInForce': 'PostOnly',
            'stopLoss': ask * (1-(sl_percent/100)),
            'takeProfit': ask * (1+(tp_percent/100))
        }
        order = phemex.create_limit_sell_order(SYMBOL, size, ask, params)

    # Sleep for 30 seconds
    # time.sleep(30)

    # Cancel The Order
    # phemex.cancel_all_orders(SYMBOL)


def ask_bid(symbol=SYMBOL):
    ob = phemex.fetch_order_book(SYMBOL)

    bid = ob['bids'][0][0]
    ask = ob['asks'][0][0]

    print(f'This is the ask for {SYMBOL}: {ask}')
    print(f'This is the bid for {SYMBOL}: {bid}')

    # ask_bid[0] = ask ask_bid[1] = bid
    return ask, bid


def fetch_markets():
    markets = phemex.fetch_markets()

    for a in markets:
        print(a['id'])


def get_position(phemex, symbol):
    '''
    get the info of your position for the given symbol.
    '''
    params = {'type': 'swap', 'code': 'USD'}
    phe_bal = phemex.fetch_balance(params=params)
    # get your position for the provided symbol
    position_info = [pos for pos in phe_bal['info']['data']
                     ['positions'] if pos['symbol'] == symbol][0]

    # if there is a position (side is none when no current position)
    if position_info['side'] != 'None':
        in_position = True
        long = True if position_info['side'] == 'Buy' else False

    # if not in position currently
    else:
        in_position = False
        long = None

    return position_info, in_position, long


def close_position(phemex, symbol):
    '''
    close your position for the given symbol
    '''

    # close all pending orders
    phemex.cancel_all_orders(symbol)

    # get your current position information (position is a dict of position information)
    position, in_position, long = get_position(phemex, symbol)

    # keep trying to close position every 30 seconds until sucessfully closed
    while in_position:

        # if position is a long create an equal size short to close.
        # use reduceOnly to make sure you dont create a trade in the opposite direction
        # sleep for 30 seconds to give order a chance to fill
        if long:
            bid = phemex.fetch_ticker(symbol)['bid']  # get current bid price
            order = phemex.create_limit_sell_order(symbol, position['size'], bid, {
                                                   'timeInForce': 'PostOnly', 'reduceOnly': True})
            print(
                f'just made a BUY to CLOSE order of {position["size"]} {symbol} at ${bid}')
            time.sleep(30)

        # if position is a short create an equal size long to close.
            # use reduceOnly to make sure you dont create a trade in the opposite direction
            # sleep for 30 seconds to give order a chance to fill
        else:
            ask = phemex.fetch_ticker(symbol)['ask']  # get current ask price
            order = phemex.create_limit_buy_order(symbol, position['size'], ask, {
                                                  'timeInForce': 'PostOnly', 'reduceOnly': True})
            print(
                f'just made a SELL to CLOSE order of {position["size"]} {symbol} at ${ask}')
            time.sleep(30)

        position, in_position, long = get_position(phemex, symbol)

    # cancel all outstanding orders
    phemex.cancel_all_orders(symbol)

    # sleep for a minute to avoid running twice
    time.sleep(60)
