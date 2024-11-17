import json
from datetime import datetime, timedelta
from pathlib import Path
from data.update_data import refresh_data

# Paths to JSON files

CRYPTO_FILE = Path("data/crypto_data.json")
STOCK_FILE = Path("data/stock_data.json")


def get_last_updated_time(file_name):
    try:
        with open(f"data/{file_name}.json", "r") as json_file:
            data = json.load(json_file)
            return data.get("timestamp", "Unknown")
    except Exception as e:
        print(f"Error reading timestamp: {e}")
        return "Unknown"


def is_data_stale(timestamp_str):
    """
    Check if the given timestamp is older than 24 hours.
    """
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return datetime.now() - timestamp > timedelta(hours=24)

def load_data(file_path):
    """
    Load data from the specified JSON file. If the file is stale or missing, refresh the data.
    """
    if not file_path.exists():
        refresh_data()  # Call refresh if the file doesn't exist
    else:
        with open(file_path, "r") as file:
            data = json.load(file)
            if is_data_stale(data["timestamp"]):
                refresh_data()  # Call refresh if data is stale
                with open(file_path, "r") as refreshed_file:
                    data = json.load(refreshed_file)
            return data
    return load_data(file_path)  # Re-read after refresh

# Functions to fetch data for Streamlit
def fetch_top_gainers(stock_or_crypto):
    if stock_or_crypto == "Crypto":
        data = load_data(CRYPTO_FILE)
        # Extract and reformat the gainers
        gainers = data["data"]["gainers"]
        
        # Transform each gainers entry
        transformed_gainers = []
        for coin in gainers:
            transformed_coin = {
                "symbol": coin["symbol"],
                "name": coin["name"],
                "current_price": coin["current_price"],
                "percent_change": coin["price_change_percentage_24h"]  # Rename price_change_percentage_24h to percent_change
            }
            transformed_gainers.append(transformed_coin)
        
        return transformed_gainers
    else:
        data = load_data(STOCK_FILE)
        return data["data"]["gainers"]


def fetch_top_losers(stock_or_crypto):
    if stock_or_crypto == "Crypto":
        data = load_data(CRYPTO_FILE)
        # Extract and reformat the losers
        losers = data["data"]["losers"]
        
        # Transform each loser entry
        transformed_losers = []
        for coin in losers:
            transformed_coin = {
                "symbol": coin["symbol"],
                "name": coin["name"],
                "current_price": coin["current_price"],
                "percent_change": coin["price_change_percentage_24h"]  # Rename price_change_percentage_24h to percent_change
            }
            transformed_losers.append(transformed_coin)
        
        return transformed_losers
    else:
        data = load_data(STOCK_FILE)
        return data["data"]["losers"]


def fetch_market_news(stock_or_crypto):
    data = load_data(CRYPTO_FILE if stock_or_crypto == "Crypto" else STOCK_FILE)
    return data["data"]["news"]

def fetch_market_volatility(stock_or_crypto):
    data = load_data(CRYPTO_FILE if stock_or_crypto == "Crypto" else STOCK_FILE)
    if stock_or_crypto == "Crypto":
        return data["data"]["volatility"]["volatility_index"]
    else:
        return data["data"]["volatility"]["vix_level"]

def fetch_market_greed_meter(stock_or_crypto):
    data = load_data(CRYPTO_FILE if stock_or_crypto == "Crypto" else STOCK_FILE)
    return int(data["data"]["greed_index"]["value"])

def create_speedometer(value, title, max_value):
    """
    Creates a Plotly speedometer gauge chart.
    """
    import plotly.graph_objects as go

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={
            'axis': {'range': [0, max_value]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, max_value * 0.4], 'color': "green"},
                {'range': [max_value * 0.4, max_value * 0.7], 'color': "yellow"},
                {'range': [max_value * 0.7, max_value], 'color': "red"},
            ],
        }
    ))
    return fig
