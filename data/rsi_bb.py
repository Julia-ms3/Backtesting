import vectorbt as vbt
import matplotlib.pyplot as plt
import os

def download_price_data(symbol, start, end):
    """Upload data."""
    return vbt.YFData.download(symbol, start=start, end=end).get('Close')


def calculate_rsi(price_data, window=14):
    """Calculating the RSI"""
    return vbt.RSI.run(price_data, window=window)


def calculate_bb(price_data, window=20):
    """Calculating the Bollinger Bands"""
    return vbt.BBANDS.run(price_data, window=window)


def find_entry_signals(rsi, bb, price_data):
    """Знаходження точок входу: RSI < 30 та ціна біля нижньої межі BB."""
    return (rsi.rsi < 30) & (price_data <= bb.lower)


def plot_signals(price_data, rsi, bb, entry_signals,symbol):
    """"""
    file_name = f'{symbol}_strategy_equity.png'
    file_path = os.path.join('results/screenshots', file_name)

    plt.figure(figsize=(12, 6))

    plt.plot(price_data, label='Price', color='black', alpha=0.6)

    plt.plot(bb.upper, color='red', linestyle='dashed')
    plt.plot(bb.middle, color='blue', linestyle='dashed')
    plt.plot(bb.lower, color='green', linestyle='dashed')

    plt.plot(rsi.rsi, color='purple')
    plt.scatter(price_data.index[entry_signals], price_data[entry_signals],
                color='black', marker='^', s=100)

    plt.title('RSI and Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.savefig(file_path)
    plt.show()


def rsi_bb(symbol, start='01.02.2025', end='28.02.2025', ):
    """MAIN FUNCTION"""

    price_data = download_price_data(symbol, start, end)
    rsi = calculate_rsi(price_data)
    bb = calculate_bb(price_data)
    entry_signals = find_entry_signals(rsi, bb, price_data)

    plot_signals(price_data, rsi, bb, entry_signals, symbol)
