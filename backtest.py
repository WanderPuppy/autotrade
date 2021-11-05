import pyupbit
import time
import numpy as np

day = 1
ticker = "KRW-BTC"

min_interv = 5


def get_delta(ticker):
    # OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
    df = pyupbit.get_ohlcv(ticker, count = day * 3600, interval = "minute1")
    
    
    # delta라는 칼럼 만듦
    df['delta'] = (df['close'] - df['open'].shift(5)) / df['open'].shift(5) * 100
    
    time.sleep(0.1)
    return df['delta']

print(get_delta(ticker))
