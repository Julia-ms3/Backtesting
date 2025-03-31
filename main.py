from core.data_loader import load_data
from data.sma_cross import sma_cross

if __name__ == '__main__':
    sma_cross(symbol='BTC-USD',  start='2019-01-01 UTC', end='2020-01-01 UTC')
