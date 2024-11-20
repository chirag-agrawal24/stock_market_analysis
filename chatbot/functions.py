import yfinance as yf
import matplotlib.pyplot as plt


def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y')['Close'].iloc[-1])


def get_indian_stock_price(ticker, exchange='NS'):
    """
    Gets the latest Indian stock price given the ticker symbol and exchange.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'RELIANCE' for Reliance Industries)
        exchange (str): Exchange code - 'NS' for NSE or 'BO' for BSE
    """
    modified_ticker = f"{ticker}.{exchange}"
    return str(yf.Ticker(modified_ticker).history(period='1y')['Close'].iloc[-1])


def plot_indian_stock_price(ticker, exchange='NS', window=None, period='1y'):
    """
    Plots the Indian stock price over specified period.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'RELIANCE' for Reliance Industries)
        exchange (str): Exchange code - 'NS' for NSE or 'BO' for BSE
        window (int): Optional window size for moving average
        period (str): Time period for data
    """
    modified_ticker = f"{ticker}.{exchange}"
    data = yf.Ticker(modified_ticker).history(period=period)
    close_prices = data['Close']

    plt.figure(figsize=(10, 5))
    plt.plot(close_prices.index, close_prices, label=f'{ticker} Stock Price')

    if window:
        ma = close_prices.rolling(window=window, min_periods=1).mean()
        plt.plot(ma.index, ma, label=f'MA ({window} days)', linestyle='--')

    plt.title(f'{ticker} Stock Price Over {period}')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (₹)')
    plt.grid(True)
    plt.legend()
    return plt


def plot_SMA(ticker, window=20, period='1y'):
    # Get stock data
    data = yf.Ticker(ticker).history(period=period)
    close_prices = data['Close']

    # Calculate SMA
    sma = close_prices.rolling(window=window, min_periods=1).mean()  # Added min_periods=1

    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.plot(close_prices.index, close_prices, label=f'{ticker} Stock Price', alpha=0.7)
    plt.plot(sma.index, sma, label=f'SMA ({window} days)', linewidth=2)
    plt.title(f'{ticker} Stock Price and {window}-Day SMA')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.grid(True)
    plt.legend()
    return plt


def plot_EMA(ticker, window=20, period='1y'):
    # Get stock data
    data = yf.Ticker(ticker).history(period=period)
    close_prices = data['Close']

    # Calculate EMA
    ema = close_prices.ewm(span=window, adjust=False).mean()

    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.plot(close_prices.index, close_prices, label=f'{ticker} Stock Price', alpha=0.7)
    plt.plot(ema.index, ema, label=f'EMA ({window} days)', linewidth=2, color='red')
    plt.title(f'{ticker} Stock Price and {window}-Day EMA')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.grid(True)
    plt.legend()
    return plt


def calculate_RSI(ticker, period='1y'):
    data = yf.Ticker(ticker).history(period=period)['Close']
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return str(rsi.iloc[-1])


def plot_stock_price(ticker, window=None, period='1y'):
    data = yf.Ticker(ticker).history(period=period)
    close_prices = data['Close']

    plt.figure(figsize=(10, 5))
    plt.plot(close_prices.index, close_prices, label=f'{ticker} Stock Price')

    if window:
        # Add moving average if window is specified
        ma = close_prices.rolling(window=window, min_periods=1).mean()  # Added min_periods=1
        plt.plot(ma.index, ma, label=f'MA ({window} days)', linestyle='--')

    plt.title(f'{ticker} Stock Price Over {period}')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    plt.legend()
    return plt


def get_crypto_price(crypto_symbol):
    crypto_ticker = yf.Ticker(crypto_symbol + "-USD")
    data = crypto_ticker.history(period='1d')
    current_price = data['Close'].iloc[-1]
    return str(current_price)


def plot_crypto_price_graph(crypto_symbol, window=None, period='1y'):
    crypto_ticker = yf.Ticker(crypto_symbol + "-USD")
    data = crypto_ticker.history(period=period)
    close_prices = data['Close']

    plt.figure(figsize=(10, 5))
    plt.plot(close_prices.index, close_prices, label=f'{crypto_symbol} Price')

    if window:
        # Add moving average if window is specified
        ma = close_prices.rolling(window=window, min_periods=1).mean()  # Added min_periods=1
        plt.plot(ma.index, ma, label=f'MA ({window} days)', linestyle='--')

    plt.title(f'{crypto_symbol} Price Over {period}')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()
    return plt


# Update the functions list to include the new Indian stock functions
functions = [
    {
        'name': 'get_stock_price',
        'description': 'Gets the latest stock price given the ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., MSFT for Microsoft).'
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'get_indian_stock_price',
        'description': 'Gets the latest Indian stock price given the ticker symbol and exchange.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol (e.g., RELIANCE for Reliance Industries).'
                },
                'exchange': {
                    'type': 'string',
                    'description': 'The exchange code - NS for NSE or BO for BSE.',
                    'default': 'NS'
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'plot_indian_stock_price',
        'description': 'Plots the Indian stock price over specified period.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol (e.g., RELIANCE for Reliance Industries).'
                },
                'exchange': {
                    'type': 'string',
                    'description': 'The exchange code - NS for NSE or BO for BSE.',
                    'default': 'NS'
                },
                'window': {
                    'type': 'integer',
                    'description': 'Optional window size for moving average.'
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'plot_SMA',
        'description': 'Plots the stock price and Simple Moving Average (SMA) for a given stock ticker over a specified window.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., MSFT for Microsoft).'
                },
                'window': {
                    'type': 'integer',
                    'description': 'The window size for the moving average calculation.'
                }
            },
            'required': ['ticker', 'window']
        }
    },
    {
        'name': 'plot_EMA',
        'description': 'Plots the stock price and Exponential Moving Average (EMA) for a given stock ticker over a specified window.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., MSFT for Microsoft).'
                },
                'window': {
                    'type': 'integer',
                    'description': 'The window size for the moving average calculation.'
                }
            },
            'required': ['ticker', 'window']
        }
    },
    {
        'name': 'calculate_RSI',
        'description': 'Calculates the Relative Strength Index (RSI) for a given stock ticker.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., MSFT for Microsoft).'
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'plot_stock_price',
        'description': 'Plots the stock price over the last year for a given ticker symbol.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., MSFT for Microsoft).'
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'get_crypto_price',
        'description': 'Gets the current price of a specified cryptocurrency.',
        'parameters': {
            'type': 'object',
            'properties': {
                'crypto_symbol': {
                    'type': 'string',
                    'description': 'The cryptocurrency symbol (e.g., BTC for Bitcoin).'
                }
            },
            'required': ['crypto_symbol']
        }
    },
    {
        'name': 'plot_crypto_price_graph',
        'description': 'Plots the price graph of a specified cryptocurrency over the last year.',
        'parameters': {
            'type': 'object',
            'properties': {
                'crypto_symbol': {
                    'type': 'string',
                    'description': 'The cryptocurrency symbol (e.g., BTC for Bitcoin).'
                }
            },
            'required': ['crypto_symbol']
        }
    }
]

# Update the available functions dictionary
available_functions = {
    'get_stock_price': get_stock_price,
    'get_indian_stock_price': get_indian_stock_price,
    'plot_indian_stock_price': plot_indian_stock_price,
    'plot_SMA': plot_SMA,
    'plot_EMA': plot_EMA,
    'calculate_RSI': calculate_RSI,
    'plot_stock_price': plot_stock_price,
    'get_crypto_price': get_crypto_price,
    'plot_crypto_price_graph': plot_crypto_price_graph
}