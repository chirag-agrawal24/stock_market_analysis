import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from data.update_data import refresh_data
import plotly.graph_objects as go
import numpy as np

# Paths to JSON files

CRYPTO_FILE = Path("data/crypto_data.json")
STOCK_FILE = Path("data/stock_data.json")
timezone = ZoneInfo("America/New_York")

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
    cleaned_date_str = "".join(ch for ch in timestamp_str if not ch.isalpha())
    timestamp = datetime.strptime(cleaned_date_str, "%Y-%m-%d %H:%M:%S %z")
    return datetime.now(timezone) - timestamp > timedelta(hours=24)

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
                "Symbol": coin["symbol"],
                "Name": coin["name"],
                "Current price": coin["current_price"],
                "Percent Change": coin["price_change_percentage_24h"]  
            }
            transformed_gainers.append(transformed_coin)
        
        return transformed_gainers
    else:
        data = load_data(STOCK_FILE)
        # Extract and reformat the gainers
        gainers = data["data"]["gainers"]
        
        # Transform each gainers entry
        transformed_gainers = []
        for coin in gainers:
            transformed_coin = {
                "Symbol": coin["symbol"],
                "Name": coin["company_name"],
                "Current price": coin["current_price"],
                "Percent Change": coin["percent_change"]  
            }
            transformed_gainers.append(transformed_coin)
        
        return transformed_gainers
        


def fetch_top_losers(stock_or_crypto):
    if stock_or_crypto == "Crypto":
        data = load_data(CRYPTO_FILE)
        # Extract and reformat the losers
        losers = data["data"]["losers"]
        
        # Transform each loser entry
        transformed_losers = []
        for coin in losers:
            transformed_coin = {
                "Symbol": coin["symbol"],
                "Name": coin["name"],
                "Current price": coin["current_price"],
                "Percent Change": coin["price_change_percentage_24h"]  # Rename price_change_percentage_24h to percent_change
            }
            transformed_losers.append(transformed_coin)
        
        return transformed_losers
    else:
        data = load_data(STOCK_FILE)
        losers = data["data"]["losers"]
        transformed_losers = []
        for coin in losers:
            transformed_coin = {
                "Symbol": coin["symbol"],
                "Name": coin["company_name"],
                "Current price": coin["current_price"],
                "Percent Change": coin["percent_change"]  
            }
            transformed_losers.append(transformed_coin)
        
        return transformed_losers
        


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


    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title,"font":{"size":30}},
        number={
            "valueformat": "",  # This ensures no decimal places
            "prefix": "",
            "suffix": "",
            "font": {"size": 30, "color":"#2E86C1", "family": "Arial"},
        },
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "rgba(255, 255, 255, 0.7)",'thickness': 0.4},

            'steps': [
                {'range': [0, max_value * 0.2], 'color': "#00c853"},
                {'range': [max_value * 0.2, max_value * 0.4], 'color': "#76ff03"},
                {'range': [max_value * 0.4, max_value * 0.6], 'color': "#ffeb3b"},
                {'range': [max_value * 0.6, max_value * 0.8], 'color': "#ff9800"},
                {'range': [max_value * 0.8, max_value], "color": "#b60000"},
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }

    ))



    return fig


def create_fear_greed_index(value, title="Greed Index", max_value=100):
    """
    Creates a Plotly speedometer gauge chart with mood text inside the meter.
    """
    value = int(value)
    mood = "Error"
    color = "#2E86C1"  # default color
    
    # Define mood and colors based on value ranges
    if 0 <= value < 20:
        mood = "Extreme Fear"
        color = "#00c853"
    elif 20 <= value < 40:
        mood = "Fear"
        color = "#76ff03"
    elif 40 <= value < 60:
        mood = "Neutral"
        color = "#ffeb3b"
    elif 60 <= value < 80:
        mood = "Greed"
        color = "#ff9800"
    elif 80 <= value <= 100:
        mood = "Extreme Greed"
        color = "#b60000"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title,"font":{"size":30}},
        number={
            "valueformat": "",  # This ensures no decimal places
            "prefix": "",
            "suffix": "",
            "font": {"size": 30, "color": color, "family": "Arial"},
        },
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "rgba(255, 255, 255, 0.7)",'thickness': 0.4},

            'steps': [
                {'range': [0, max_value * 0.2], 'color': "#00c853"},
                {'range': [max_value * 0.2, max_value * 0.4], 'color': "#76ff03"},
                {'range': [max_value * 0.4, max_value * 0.6], 'color': "#ffeb3b"},
                {'range': [max_value * 0.6, max_value * 0.8], 'color': "#ff9800"},
                {'range': [max_value * 0.8, max_value], "color": "#b60000"},
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    # Add the mood text annotation in the center of the gauge
    fig.add_annotation(
        text=mood,
        x=0.5,
        y=0.25,  # Positioned slightly above center
        showarrow=False,
        font=dict(size=24, color=color),
        xref='paper',
        yref='paper'
    )
    

    
    return fig
