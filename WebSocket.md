/ ticker /

type /	타입	/ String / ticker : 현재가

code / 마켓 코드 (ex. KRW-BTC) / String	

opening_price	시가	Double	

high_price	고가	Double	

low_price	저가	Double	

trade_price	현재가	Double

prev_closing_price	전일 종가	Double	

change	c	전일 대비	String	
RISE : 상승 / EVEN : 보합 / FALL : 하락

change_price	부호 없는 전일 대비 값	Double	

signed_change_price	전일 대비 값	Double	

change_rate	부호 없는 전일 대비 등락율	Double	

signed_change_rate	전일 대비 등락율	Double	

trade_volume	가장 최근 거래량	Double	

acc_trade_volume	누적 거래량(UTC 0시 기준)	Double	

acc_trade_volume_24h	24시간 누적 거래량	Double	

acc_trade_price	 누적 거래대금(UTC 0시 기준)	Double	

acc_trade_price_24h	24시간 누적 거래대금	Double	

trade_date	최근 거래 일자(UTC)	String	yyyyMMdd

trade_time	최근 거래 시각(UTC)	String	HHmmss

trade_timestamp	체결 타임스탬프 (milliseconds)	Long	

ask_bid	매수/매도 구분	String
ASK : 매도 BID : 매수

acc_ask_volume	누적 매도량	Double	

acc_bid_volume	누적 매수량	Double	

highest_52_week_price	52주 최고가	Double	

highest_52_week_date	52주 최고가 달성일	String	yyyy-MM-dd

lowest_52_week_price	52주 최저가	Double	

lowest_52_week_date	52주 최저가 달성일	String	yyyy-MM-dd

trade_status	거래상태 *deprecated	String	

market_state	거래상태	String	PREVIEW : 입금지원
ACTIVE : 거래지원가능 DELISTED : 거래지원종료

market_state_for_ios	거래 상태 *deprecated	String	

is_trading_suspended	거래 정지 여부	Boolean	

delisting_date	상장폐지일	Date	

market_warning	유의 종목 여부	String	NONE : 해당없음 CAUTION : 투자유의

timestamp		타임스탬프 (milliseconds)	Long	

stream_type		스트림 타입	String	
SNAPSHOT : 스냅샷 REALTIME : 실시간
