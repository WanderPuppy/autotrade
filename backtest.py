import pyupbit
import time
import datetime
import numpy as np
import pandas as pd
import openpyxl

day = 1
t = day * 3600
tickers = pyupbit.get_tickers(fiat="KRW")
tickers_count = len(tickers)
tickers_delta = pd.DataFrame()
df = pd.DataFrame()
crypto = "KRW-BTC"
money = 10000

min_interv = 5


def get_delta(ticker):
    # OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
    df = pyupbit.get_ohlcv(ticker, count = t, interval = "minute1")
    
    # delta라는 칼럼 만듦
    df[ticker] = (df['close'] - df['open'].shift(min_interv)) / df['open'].shift(min_interv) * 100
    
    time.sleep(0.1)
    return df[ticker]

def get_ticker_data(tickers):
    print("Getting ticker data")
    for i in range(0, tickers_count):
        tickers_delta[tickers[i]] = get_delta(tickers[i])
        print(tickers_delta)
        time.sleep(0.1)
    print(tickers_delta)
    tickers_delta.to_excel("test.xlsx")
    stickers_delta = {}
    most_crypto = {}
    print("Sorting ticker data")
    for i in range(min_interv, t):
        stickers_delta = tickers_delta.iloc[i]
        print(stickers_delta)
        most_crypto[i] = sorted(stickers_delta.items(), key=lambda x: x[1], reverse=True)
        print(most_crypto[i])
        
    return most_crypto

print(get_ticker_data(tickers))
