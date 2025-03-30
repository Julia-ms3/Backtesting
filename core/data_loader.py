import os
import zipfile

import ccxt
import pandas as pd
import requests


def load_historical_data(symbol="BTCUSDT", interval='1m', year='2025', month='02'):
    BASE_URL = "https://data.binance.vision/data/spot/monthly/klines"
    url = f"{BASE_URL}/{symbol}/{interval}/{symbol}-{interval}-{year}-{month}.zip"

    zip_filename = "data.zip"
    parquet_filename = f"results/{symbol}_1m_feb25.parquet"
    csv_filename = f"extracted_data/{symbol}-{interval}-{year}-{month}.csv"

    if os.path.exists(parquet_filename):
        print(f"{symbol} already exists")
        return parquet_filename

    response = requests.get(url)
    if response.status_code != 200:
        print(f'Loading error - {response.status_code}')
    with open(zip_filename, 'wb') as file:
        file.write(response.content)

    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_file:
            zip_file.extractall('extracted_data')
    except zipfile.BadZipFile:
        print(f"Corrupt ZIP file for {symbol}, skipping...")
        os.remove(zip_filename)
        return None

    os.remove(zip_filename)
    df = pd.read_csv(csv_filename, header=None)
    df = df.iloc[:, 1:6]
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    df.to_parquet(parquet_filename, engine='pyarrow', compression='snappy')

    print(f"Data saved to {parquet_filename}")
    os.remove(csv_filename)


def get_hundred_pair():
    exchange = ccxt.binance()
    market = exchange.load_markets()

    btc_pairs = [pair for pair in market if pair.endswith('/BTC')]

    quote_volume = []
    tickers = exchange.fetch_tickers(btc_pairs)

    for symbol, data in tickers.items():
        if 'quoteVolume' in data and data['quoteVolume'] is not None and data['quoteVolume'] > 0.0:
            quote_volume.append((symbol, data['quoteVolume']))

    sorted_volume = sorted(quote_volume, key=lambda x: x[1], reverse=True)

    return sorted_volume[:100]


def load_data():
    pairs = get_hundred_pair()

    for symbol in pairs:
        load_historical_data(symbol=symbol[0].replace('/', ''))
