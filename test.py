import pyupbit
import time
import datetime 

print("LOADING...")
tickers = pyupbit.get_tickers(fiat="KRW")
tickers_count = len(tickers)
tickers_price = {}
crypto_name = "KRW-BTC"

def get_tickers(): #코인의 정보 수집
    tickers = pyupbit.get_tickers(fiat="KRW")
    tickers_cout = len(tickers) #코인의 개수 세기
    return tickers

def upload_tickers(tickers): # ticker의 이름과 가격 저장
    for i in range(0, tickers_count-1):
        tickers_price[tickers[i]] = tickers_tangent(tickers[i])
        time.sleep(0.1)
    print("Successful data upload")
    return tickers_price
    
def tickers_tangent(ticker): # ticker의 5분 구간의 차이 구함 (5분후 가격 - 5분전 가격) / 5분전 가격 
    df = pyupbit.get_ohlcv(ticker, count = 5, interval = "minute1")
    delta = (df.iloc[-1]['close'] - df.iloc[0]['open']) / df.iloc[0]['open'] * 100
    time.sleep(0.1)
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
    
# for i in range(0, tickers_count - 1):
#     ticker = tickers[i]
#     delta = tickers_tangent(ticker)
#     # print(ticker, ':' , delta)
#     time.sleep(0.05)

# print(pyupbit.get_tickers(fiat="KRW"))
# print(pyupbit.get_current_price("KRW-BTC"))


# for i in range(0, tickers_count-1):
#     print(tickers[i], pyupbit.get_current_price(tickers[i]))
#     time.sleep(0.1)

#로그인
access = "YqSsA9cIqwPfMbVO0BcRxqeD0dVxDYxbACJVZxIG"
secret = "jUl1rn9L9xG8ro2uxxea41wDiDSlv3B3nz5iPeIB"
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# target_crypto = get_target_crypto(tickers)
# print(target_crypto)
# print(target_crypto[0][0])
# crypto_name = ""
# print(crypto_name)
# target_crypto_name = target_crypto[0][0]
# if crypto_name != target_crypto_name: #다시 불러와도 상승률이 가장 큰 코인 변동있을 때
#     crypto_name = target_crypto_name
# print(crypto_name)


while True:
    try:
        #상승률이 가장 큰 코인 갱신하기
        target_crypto = get_target_crypto(tickers)
        target_crypto_name = target_crypto[0][0]
        if crypto_name != target_crypto_name: #상승률이 가장 큰 코인 변동있을 때
            print("Change no.1 crypto {1}! ({0} -> {1})".format(crypto_name, target_crypto_name))
            crypto_name = target_crypto_name
            
            #Sell Crypto
            sell_crypto = get_balance(crypto_name)
            upbit.sell_market_order(crypto_name, sell_crypto)
            print("Successful Sell-trade")
            
            #Buy Crypto
            krw = get_balance("KRW")
            
            if krw > 5000:
                upbit.buy_market_order(crypto_name, krw*0.9995)
                print("Successful Buy-trade")
            

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

