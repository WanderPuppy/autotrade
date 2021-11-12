import pyupbit
import time
import datetime
import numpy as np
import pandas as pd
import openpyxl
from matplotlib import pyplot as plt

#함수

def get_settings(): #코인의 정보 수집
    tickers = pyupbit.get_tickers(fiat="KRW")
    tickers_count = len(tickers) #코인의 개수 세기
    now = datetime.datetime.now()

def upload_tickers(tickers): # ticker의 이름과 가격 저장
    for i in range(0, tickers_count):
        tickers_price[tickers[i]] = tickers_tangent(tickers[i])
        time.sleep(0.1)
    print("Successful data upload")
    return tickers_price
    
def tickers_tangent(ticker): # ticker의 구간의 차이 구함
    df = pyupbit.get_ohlcv(ticker, count = 6, interval = "minute5", to = now, period = 0.2)
    delta = (df.iloc[-1]['close'] - df.iloc[0]['open']) / df.iloc[0]['open'] * 100
    return delta

def get_balance(ticker): #잔고 조회
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker): #현재가 조회
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def get_start_time(ticker): #시작시간 조회
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_target_crypto(tickers): #상승률이 가장 큰 코인 조회
    data = upload_tickers(tickers)
    sdata = sorted(data.items(), key=lambda x: x[1], reverse=True) #sdata에 상승률이 높은 순대로 저장
    most_crypto = sdata[:1] #상승률이 가장 높은 코인 저장
    print("{0} : {1}".format(most_crypto[0][0], most_crypto[0][1]))
    return most_crypto

#본문

access = "YqSsA9cIqwPfMbVO0BcRxqeD0dVxDYxbACJVZxIG"
secret = "jUl1rn9L9xG8ro2uxxea41wDiDSlv3B3nz5iPeIB"
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

print("LOADING...")
tickers = pyupbit.get_tickers(fiat="KRW")
tickers_count = len(tickers)
tickers_price = {}
crypto_name = "KRW-BTC"
crypto_price = 0
now = datetime.datetime.now()

while True:
    try:
        #세팅 주기적으로 하기
        get_settings()
        
        #상승률이 가장 큰 코인 갱신하기
        target_crypto = get_target_crypto(tickers)
        target_crypto_name = target_crypto[0][0]
        target_crypto_price = target_crypto[0][1] #target_crypto는 현재 시점에서 가장 상승률이 큰 코인
        
        if crypto_name != target_crypto_name: #상승률이 가장 큰 코인 변동있을 때
            print("Change no.1 crypto {1}! ({0} -> {1})".format(crypto_name, target_crypto_name))
            
            #Sell Crypto
            crypto_name1 = crypto_name.split('-')
            crypto_name2 = crypto_name1[-1]
            sell_crypto = get_balance(crypto_name2)
            current_price = get_current_price(crypto_name)
            current_price_f = sell_crypto * current_price
            if current_price_f > 5000: 
                upbit.sell_market_order(crypto_name, sell_crypto)
                print("Successful Sell-trade : {0}, {1}".format(crypto_name, current_price))
            
            crypto_name = target_crypto_name
            
            #Buy Crypto
            if target_crypto_price > 0:
                krw = get_balance("KRW")

                if krw > 5000:
                    upbit.buy_market_order(crypto_name, krw*0.9995)
                    print("Successful Buy-trade : {0}, {1}".format(crypto_name, krw))
            

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
