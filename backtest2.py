import pyupbit
import time
import datetime
import numpy as np
import pandas as pd
import openpyxl
from matplotlib import pyplot as plt



def get_delta(ticker, now):
    # OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
    df = pyupbit.get_ohlcv(ticker, count = 200, interval = min_interval, to = now, period = 0.2)
    
    # delta라는 칼럼 만듦
    df[ticker] = (df['close'] - df['open'].shift(min_interv)) / df['open'].shift(min_interv) * 100
    
    time.sleep(0.1)
    return df[ticker]

def get_ticker_delta_data(tickers): #tickers_delta 데이터 불러오기 
    print("Getting tickers data")

    
    for i in range(0, tickers_count): # get_delta를 이용해 delta값을 계산해 저장
        ticker = tickers[i]
        tickers_delta[ticker] = get_delta(ticker, now)
        print("Data Loading ({0} / {1})".format(i + 1, tickers_count))
        time.sleep(0.1)
    tickers_delta.fillna(0, inplace = True)
    tickers_delta.to_excel("test.xlsx")
    
    print("Sorting tickers data")
    s_tickers_delta = tickers_delta.to_dict('index') #각 row를 기준으로 index에 따라 딕셔너리 변환 ex) {t1: {'A': '~~'}}
    print("Sorting tickers data ( 1 / 4)")
    s1_tickers_delta = s_tickers_delta
    for i in tickers_delta.index:
        s1_tickers_delta[i] = sorted(s_tickers_delta[i].items(), key=lambda x : x[1], reverse=True) #정렬해서 리스트로 저장
    print("Sorting tickers data ( 2 / 4)")
    s2_tickers_delta = pd.DataFrame(s1_tickers_delta) # 데이터 프레임으로 재변환
    print("Sorting tickers data ( 3 / 4)")
    s3_tickers_delta = pd.DataFrame(s2_tickers_delta.transpose()) #행과 열을 바꾸어 재정렬
    print("Sorting tickers data ( 4 / 4)")

    return s3_tickers_delta

def get_ror(time1, time2, ticker, now): #수익률 계산 함수
    df = pyupbit.get_ohlcv(ticker, count = 200, interval = min_interval, to = now, period = 0.2)
    
    c_close = df.loc[time2, 'close']
    c_open = df.loc[time1, 'open']
    
    c_ror = (c_close / c_open) - (fee * 2)
    
    return c_ror



tickers_delta = pd.DataFrame()
df = pd.DataFrame()
now = datetime.datetime.now()
result_f = {}

min_intervs = [1, 5, 10, 30, 50, 100]
min_intervals = [ "day", "minute1", "minute3", "minute5", "minute10", "minute15", "minute30", "minute60", "minute240", "week", "month"]

min_interv = 10
min_interval = "minute1"

try: 
        
    print(min_interv, min_interval)
        
    tickers = pyupbit.get_tickers(fiat="KRW") 
    tickers_count = len(tickers)
        
    tickers_data = get_ticker_delta_data(tickers) #tickers_data에 데이터 저장

    print("Successful getting tickers data")
    tickers_data.to_excel("data.xlsx")
    crypto_price1 = 0
    crypto_prine2 = 0
    crypto_name1 = "KRW-BTC"
    crypto_time1 = tickers_data.index[0]
    crypto_time2 = tickers_data.index[0]
    print(crypto_time1)
    result = {}
    ror = 1
    s_ror = 1
    fee = 0.0005


    # 함수 제작
    for i in tickers_data.index[min_interv:]: #tickers_data.index[min_interv:]는 시간
            
        try:
            crypto_name2 = crypto_name1
            crypto_price2 = crypto_price1

            most_crypto = tickers_data.loc[i, 0] # 가장 상승률이 큰 데이터 불어옴

            crypto_name1 = most_crypto[0] #이름을 저장
            crypto_price1 = most_crypto[1] #가격을 저장

            if crypto_price2 != 0:
                # if crypto_price1 > crypto_price2: #변동성이 더 큰 코인이 나타났을 때
                    if crypto_name1 != crypto_name2: #코인의 이름이 다르면
                        
                        crypto_time2 = crypto_time1
                        crypto_time1 = i

                        ror = get_ror(crypto_time2, crypto_time1, crypto_name2, now) # 수익률 계산

                        s_ror *= ror #누적 수익률 계산
                
            time.sleep(1)
            
        except Exception as e:
            print(e)
            time.sleep(1)


        result[i] = s_ror # result 딕셔너리에 누적 수익률 저장

        time.sleep(0.1)

    result1 = pd.DataFrame(result, index = [0])
    result2 = pd.DataFrame(result1.transpose())
    result2.to_excel('result.xlsx')
        
    print(result[tickers_data.index[-1]], ':', tickers_data.index[min_interv], '->', tickers_data.index[-1])
    print(min_interv, '+', min_interval, ':', result[tickers_data.index[-1]])
    
        
except Exception as e:
    print(e)
    time.sleep(1)

a = input("Backtest Successful Complete!")
