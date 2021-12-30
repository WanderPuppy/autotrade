import pyupbit
import pandas
import numpy as np

class Data_Setting: #데이터 세팅 클래스
    pass

class RT_Data: #실시간 데이터 클래스
    def tickers_name_load(self): #코인 이름을 모두 불러옵니다
        tickers_name = pyupbit.get_tickers(fiat="KRW")
        return tickers_name
    def tickers_print(self):
        print(RT_Data.tickers_name_load(self))

class Boss_Strategy: #상승률 기반 전략 판단 클래스
    pass

class Feedback: #피드백을 통한 변수 조정 클래스
    pass

# data = RT_Data()
# data.tickers_print()

def getting_MA(ticker, time, n, m, cut): #ticker: 코인, time: 시간, n: 기간, m: 최대기간, cut= 0이면 원본, 1이면 맨 뒤 데이터만, 2면 원본에서 결측값 제거
    MA = pyupbit.get_ohlcv(ticker, interval = time, count = m) # time은 문자열
    if cut == 0:
        MA_n = MA['close'].rolling(n).mean()
        MA_n = MA_n.fillna(0)
    elif cut == 1:
        MA_n = MA['close'].rolling(n).mean().iloc[-1]
    elif cut == 2:
        MA_n = MA['close'].rolling(n).mean()
        MA_n = MA_n.dropna()
    return MA_n

def scoring_MA1(ticker, time, short_n, long_n): #short_n : 단기 MA 기간, long_n : 장기 MA 기간
    short_MA = getting_MA(ticker, time, short_n, short_n, 1)
    long_MA = getting_MA(ticker, time, long_n, long_n, 1)
    MA_x = short_MA / long_MA # 1보다 크면 상승세
    MA_score = MA_x / (1 + MA_x) * 100 #점수 평가(0~100) MA_score가 높을 수록 상승세에 있음
    
    return MA_score

def scoring_MA2(ticker, time, short_n, long_n):
    short_MA = getting_MA(ticker, time, short_n, short_n + 3, 2)
    long_MA = getting_MA(ticker, time, long_n, long_n + 3, 2)
    
    grad_MA = (short_MA - long_MA) / (short_MA + long_MA) #0보다 크면 상승
    r_grad_MA = (grad_MA - grad_MA.shift(1)).iloc[1] #0보다 크면 기울기가 상승하는 방향으로 커짐
    score = (1 / (1 + np.exp(- r_grad_MA))) * 100
    
    return score
    
    

# print(getting_MA("KRW-BTC", "minute60", 5, 10, 2))
print(scoring_MA1("KRW-BTC", "minute60", 5, 60))
print(scoring_MA2("KRW-BTC", "minute60", 5, 60))



