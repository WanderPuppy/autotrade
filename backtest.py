import pyupbit
import time
import datetime
import numpy as np
import pandas as pd
import openpyxl

tickers = pyupbit.get_tickers(fiat="KRW")
tickers_count = len(tickers)
tickers_delta = pd.DataFrame()
df = pd.DataFrame()
money = 10000

min_interv = 5


def get_delta(ticker, now):
    # OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
    df = pyupbit.get_ohlcv(ticker, count = 200, interval = "minute1", to = now)
    
    # delta라는 칼럼 만듦
    df[ticker] = (df['close'] - df['open'].shift(min_interv)) / df['open'].shift(min_interv) * 100
    
    time.sleep(0.1)
    return df[ticker]

def get_ticker_delta_data(tickers):
    print("Getting ticker data")
    now = datetime.datetime.now()

    
    for i in range(0, tickers_count):
        ticker = tickers[i]
        tickers_delta[ticker] = get_delta(ticker, now)
        print("Data Loading ({0} / {1})".format(i, tickers_count-1))
        time.sleep(0.1)
    tickers_delta.to_excel("test.xlsx")
    return tickers_delta

def get_most_crypto(i):
    stickers_delta = tickers_delta.iloc[i]
    # stickers_delta = tickers_delta.loc[]
    name = tickers_delta.iloc[i].index[0]
    
    stickers_delta.sort_values(axis = 1)
    most_crypto = stickers_delta.iloc[0, 0]
    
    
    # stickers_delta = pd.DataFrame()
    # most_crypto = pd.DataFrame()
    # for i in range(0, 200):
    #     stickers_delta = tickers_delta.sort_values(by=tickers_delta.index[i], axis = 1, ascending = False)
    #     print(stickers_delta)
    #     print(stickers_delta[i,0])
    #     most_crypto.append(stickers_delta[i, 0])
    #     print(most_crypto)
    # for i in range(0, 200):
    #     stickers_delta = tickers_delta.iloc[i]
    #     print(stickers_delta)
    #     most_crypto = most_crypto.append(sorted(stickers_delta.items(), key=lambda x: x[1], reverse=True)[:1], ignore_index = True)
    #     print("Sorting ticker data ({0} / {1})".format(i, 200))
    #     # print(most_crypto)
    #     time.sleep(0.1)
    # # print(len(most_crypto.index), len(tickers_delta.index))
    # # print(most_crypto.index)
    # print(most_crypto)
    # most_crypto.set_index(keys = tickers_delta.index, inplace = False)
    return most_crypto

tickers_data = get_ticker_delta_data(tickers)
for i in (0, 200):
    most_crypto = get_most_crypto(i)
    print(most_crypto)
    
print(tickers_data)
tickers_data.to_excel("data.xlsx")
