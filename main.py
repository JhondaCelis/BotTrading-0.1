# main.py
from utils.bingx_api import get_ohlc

if __name__ == "__main__":
    df = get_ohlc(symbol="BTC-USDT", interval="1m", limit=100)
    print(df.tail())
