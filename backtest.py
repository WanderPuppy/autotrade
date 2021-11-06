import pyupbit
import time
import numpy as np

day = 1
t = day * 3600
tickers = pyupbit.get_tickers(fiat="KRW")
tickers_count = len(tickers)
tickers_delta = {}
df = {}
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
        time.sleep(0.1)
    stickers_delta = {}
    most_crypto = {}
    print("Sorting ticker data")
    for i in range(min_interv, t):
        stickers_delta = tickers_delta.iloc[i]
        most_crypto[i] = sorted(tickers_delta.items(), key=lambda x: x[1], reverse=True)
    return most_crypto

print(get_ticker_data(tickers))
