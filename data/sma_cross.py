import matplotlib.pyplot as plt
import vectorbt as vbt


def download_data(symbol, start, end):
    """ Downloading data by currency """

    data = vbt.YFData.download(symbol, start=start, end=end)
    return data.get('High'), data.get('Low'), data.get('Close')


def calculate_sma(close, period):
    """ Calculating the moving average """

    return vbt.MA.run(close, period)


def calculate_atr(high, low, close, period=14):
    """ Calculating ATR """

    return vbt.ATR.run(high, low, close, period).atr


def generate_signals(fast_sma, slow_sma):
    """ Generation of buy/sell signals """

    entries = fast_sma.ma_crossed_above(slow_sma)
    exits = fast_sma.ma_crossed_below(slow_sma)
    return entries, exits


def backtest_portfolio(close, entries, exits):
    """ Calculating the total profit """

    pf = vbt.Portfolio.from_signals(close, entries, exits)
    print(f'Total return: {pf.total_return(): }')
    return pf


def plot_strategy(close, fast_sma, slow_sma, entries, exits, symbol):
    """ Drawing a graph """

    plt.figure(figsize=(11, 5))
    plt.plot(close, label=f'{symbol} Price', color='black', alpha=0.6)
    plt.plot(fast_sma.ma, label=f'Fast MA', linestyle='dashed')
    plt.plot(slow_sma.ma, label=f'Slow MA', linestyle='dashed')

    plt.scatter(close.index[entries], close[entries], color='green', label='Buy', marker='^')
    plt.scatter(close.index[exits], close[exits], color='red', label='Sell', marker='v')

    plt.legend()
    plt.title("SMA Crossover Strategy")
    plt.show()


def sma_cross(symbol, start='01.02.2025', end='28.02.2025', fast_period=10, slow_period=50):
    """ MAIN FUNCTION """

    high, low, close = download_data(symbol, start, end)

    fast_sma = calculate_sma(close, fast_period)
    slow_sma = calculate_sma(close, slow_period)

    atr = calculate_atr(high, low, close)

    entries, exits = generate_signals(fast_sma, slow_sma)

    pf = backtest_portfolio(close, entries, exits)
    plot_strategy(close, fast_sma, slow_sma, entries, exits, symbol)
