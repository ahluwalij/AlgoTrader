'''
turtle.py is what runs the bot and then functions.py does funcs
'''

from turtle import position
import pandas as pd
from datetime import datetime, time
from pytz import timezone
import pandas_ta as ta
from time import sleep


def in_timeframe():
    '''
    returns True if the current time is between 9:30am and 4pm EST on Monday-Friday
    '''
    #get current eastern time
    now = datetime.now(timezone('US/Eastern')).time()
    #get day of week as a number (0=monday,6=sunday)
    day = datetime.today().weekday()

    #return true if the current time in the eastern timezone is between 9:30am and 4pm monday-friday
    if (now >= time(9,30) and now < time(16)) and (day < 5 and day >= 0):
        return True
    return False

def get_position(phemex,symbol):
    '''
    get the info of your position for the given symbol.
    '''
    params = {'type':'swap', 'code':'USD'}
    phe_bal = phemex.fetch_balance(params=params)
    #get your position for the provided symbol
    position_info = [pos for pos in phe_bal['info']['data']['positions'] if pos['symbol'] == symbol][0]

    #if there is a position (side is none when no current position)
    # it will only be NOne if if NOT in position.. so we can use NOT here

    if position_info['side'] != 'None':
        in_position = True
        long = True if position_info['side'] == 'Buy' else False

    #if not in position currently
    else:
        in_position = False
        long = None 

    return position_info, in_position, long

def get_candle_df(phemex,symbol,timeframe):
    '''
    returns a pandas dataframe of the last 55 candles
    '''
    # this converts their list of lists into a DF & set index to time
    ohlcv = pd.DataFrame(phemex.fetch_ohlcv(symbol,timeframe,limit=55),columns=['time','open','high','low','close','volume']).set_index('time')
    return ohlcv

def calc_tr(df):
    '''
    calculate and add the sma to the input dataframe. Returns the most recent sma
    '''

    #use pandas_ta to calculate the true range
    df['True_Range'] = df.ta.atr()

    return df['True_Range'].iloc[-1]

def calc_atr(df,length=None):
    '''
    adds a ATR column to the given dataframe. 
    ATR calculated using pandas_ta library
    makes it a column in the df
    '''
    df['ATR'] = df.ta.atr(length=length)



# support and resis, default of 20 
# this gets the minimum value in the last 20 rows of the low
# resis is the highest high in the length
# returns support and resistance
def calc_sup_res(df,length=20):
    '''
    calculate and add the support/resistance levels to the input dataframe
    '''
    df['support'] = df['low'].rolling(window=length).min()
    df['resistance'] = df['high'].rolling(window=length).max()


    return df['support'].iloc[-1], df['resistance'].iloc[-1]




def hit_target(price,tp,sl,long: bool):
    '''
    returns True if a stop loss or a take profit price is reached
    '''
    if long:
        if price >= tp:
            print('TAKE PROFIT REACHED, CLOSING POSITION')
            return True
        elif price <= sl:
            print('STOP LOSS REACHED, CLOSING POSITION')
            return True
        else:
            return False
    else:
        if price <= tp:
            print('TAKE PROFIT REACHED, CLOSING POSITION')
            return True
        elif price >= sl:
            print('STOP LOSS REACHED, CLOSING POSITION')
            return True
        else:
            return False

#CLOSE YOUR POSITION FOR A SYMBOL
# this will go until it fills
def close_position(phemex,symbol):
    '''
    close your position for the given symbol
    '''

    #close all pending orders
    phemex.cancel_all_orders(symbol)

    #get your current position information (position is a dict of position information)
    position,in_position,long = get_position(phemex,symbol)
    

    #keep trying to close position every 30 seconds until sucessfully closed
    while in_position:

        #if position is a long create an equal size short to close. 
            #use reduceOnly to make sure you dont create a trade in the opposite direction
            #sleep for 30 seconds to give order a chance to fill
        if long:
            bid = phemex.fetch_ticker(symbol)['bid'] #get current bid price
            order = phemex.create_limit_sell_order(symbol, position['size'], bid, {'timeInForce': 'PostOnly', 'reduceOnly':True})
            print(f'just made a BUY to CLOSE order of {position["size"]} {symbol} at ${bid}')
            sleep(30)

        #if position is a short create an equal size long to close. 
            #use reduceOnly to make sure you dont create a trade in the opposite direction
            #sleep for 30 seconds to give order a chance to fill
        else:
            ask = phemex.fetch_ticker(symbol)['ask'] #get current ask price
            order = phemex.create_limit_buy_order(symbol, position['size'], ask, {'timeInForce': 'PostOnly', 'reduceOnly':True})
            print(f'just made a SELL to CLOSE order of {position["size"]} {symbol} at ${ask}')
            sleep(30)

        position,in_position,long = get_position(phemex,symbol)


    #cancel all outstanding orders
    phemex.cancel_all_orders(symbol)

    #sleep for a minute to avoid running twice
    sleep(60)

def end_of_trading_week():
    '''
    returns True if it is Friday at 4pm EST
    '''
    #get current eastern time
    now = datetime.now(timezone('US/Eastern')).time()
    #get day of week as a number (0=monday,6=sunday)
    day = datetime.today().weekday()
    if day == 4 and now >= time(16) and now < time(16,1):
        return True
    return False

def get_extreme_of_consolidation(df,percent):
    '''
    return the lowest low of the current consolidation period
    '''
    #loop through df in reverse, newest values first
    for index,row in df.iloc[::-1].iterrows():
        # this essentially looks to see if its in consolidation or not or starting.. 
        # if the percent difference in tr from close value is greater than our wanted percent deviance (broke consolidation) 
        # return lowest low in the period and highest high
        if (row['True_Range']/row['close'])*100 > percent:
            return df[df.index > index].low.min(),df[df.index > index].low.max()
    return df.low.min(),df.high.max()
