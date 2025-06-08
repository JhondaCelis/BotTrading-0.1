import requests
import pandas as pd

def get_ohlc(symbol="BTC-USDT", interval="1m", limit=200):
    endpoints = [
        "https://open-api.bingx.com/openApi/swap/market/kline",
        "https://open-api.bingx.com/openApi/spot/v1/market/kline"
    ]
    last_error = None

    for url in endpoints:
        try:
            params = {"symbol": symbol, "interval": interval, "limit": limit}
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            
            if data.get("code") == 0:
                kline_data = data["data"]
                
                # Muestra un ejemplo del contenido real (8 columnas)
                if isinstance(kline_data, list) and len(kline_data) > 0:
                    print(">> Ejemplo de fila:", kline_data[0])

                # Usa solo las primeras 6 columnas: timestamp, open, high, low, close, volume
                df = pd.DataFrame(kline_data)[[0, 1, 2, 3, 4, 5]]
                df.columns = ["timestamp", "open", "high", "low", "close", "volume"]

                df[["open","high","low","close","volume"]] = df[["open","high","low","close","volume"]].astype(float)
                df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms")
                return df
            else:
                last_error = data
        except Exception as e:
            last_error = {"error": str(e)}

    raise Exception(f"No se pudo obtener datos de ningún endpoint. Último error: {last_error}")
