import yfinance as yf
import matplotlib.pyplot as plt

# Define functions
def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y')['Close'].iloc[-1])


def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y')['Close']
    return str(data.rolling(window=window).mean().iloc[-1])


def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y')['Close']
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])


def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period='1y')['Close']
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return str(rsi.iloc[-1])


def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period='1y')['Close']

    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data, label=f'{ticker} Stock Price')
    plt.title('Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    plt.legend()
    return plt  # Return the plot instead of directly displaying it


def get_crypto_price(crypto_symbol):
    crypto_ticker = yf.Ticker(crypto_symbol + "-USD")
    data = crypto_ticker.history(period='1d')
    current_price = data['Close'].iloc[-1]
    return str(current_price)


def plot_crypto_price_graph(crypto_symbol):
    crypto_ticker = yf.Ticker(crypto_symbol + "-USD")
    data = crypto_ticker.history(period='1y')['Close']

    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data, label=f'{crypto_symbol} Price')
    plt.title(f'{crypto_symbol} Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()
    return plt  # Return the plot instead of directly displaying it


# Define available functions
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
        'name': 'calculate_SMA',
        'description': 'Calculates the Simple Moving Average (SMA) for a given stock ticker over a specified window.',
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
        'name': 'calculate_EMA',
        'description': 'Calculates the Exponential Moving Average (EMA) for a given stock ticker over a specified window.',
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
        'description': 'Plots the price graph and, graph of a specified cryptocurrency over the last year.',
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

available_functions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI': calculate_RSI,
    'plot_stock_price': plot_stock_price,
    'get_crypto_price': get_crypto_price,
    'plot_crypto_price_graph': plot_crypto_price_graph
}
