import requests
import json
from datetime import datetime, timedelta
import schedule
import time
import yfinance as yf
import numpy as np
from zoneinfo import ZoneInfo
from newspaper import Article, Config
import nltk
from typing import List, Dict

import streamlit as st


timezone = ZoneInfo("America/New_York")

# Load API key and URLs from JSON config
with open("data/config.json", "r") as config_file:
    config = json.load(config_file)

NEWSAPI_KEY = st.secrets["general"]["NEWSAPI_KEY"]
urls = config["urls"]
TOP_30_STOCKS = [ stock["ticker"] for stock in config["US30"]]

ticker_to_name = {stock["ticker"]: stock["name"] for stock in config["US30"]}

# Keywords for both stocks and crypto
stock_keywords = config['stock_keywords']
crypto_keywords = config['crypto_keywords']


# Download required NLTK data for article summarization
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')




# Fetch stock data using yfinance
def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="5d")  # Fetch the last 2 days of data
        
        if not hist.empty and len(hist) > 1:
            prev_close = hist['Close'].iloc[-2]
            current_price = hist['Close'].iloc[-1]
            percent_change = ((current_price - prev_close) / prev_close) * 100
            return {
                "symbol": symbol,
                "current_price": current_price,
                "percent_change": percent_change
            }
        return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


# Fetch top 5 gainers and losers from top US30 stocks
def fetch_market_gainers_and_losers():
    all_stocks = []
    try:
        for symbol in TOP_30_STOCKS:
            stock_data = fetch_stock_data(symbol)
            if stock_data and stock_data['percent_change'] is not None:
                # Add the company name from the US30 mapping
                stock_data["company_name"] = ticker_to_name.get(symbol, "Unknown")
                
                # Reorder keys to match the required format
                reordered_stock_data = {
                    "symbol": stock_data["symbol"],
                    "company_name": stock_data["company_name"],
                    "current_price": stock_data["current_price"],
                    "percent_change": stock_data["percent_change"]
                }

                all_stocks.append(reordered_stock_data)
        
        # Sort the stocks based on percentage change
        sorted_stocks = sorted(all_stocks, key=lambda x: x['percent_change'], reverse=True)
        
        # Get top gainers and losers
        top_gainers = [x for x in sorted_stocks[:5] if x['percent_change'] > 0]
        top_losers = [x for x in sorted_stocks[-1:-6:-1] if x['percent_change'] < 0]
        
        return top_gainers, top_losers
    
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return [], []



# Fetch cryptocurrency top gainers and losers using CoinGecko
def fetch_crypto_gainers_and_losers():
    try:
        response = requests.get(urls["crypto_gainers_losers"], params={
            "vs_currency": "usd",
            "order": "market_cap_desc"
        }, timeout=10)
        response.raise_for_status()
        crypto_data = response.json()

        top_gainers, top_losers=[],[]
        for x in sorted(crypto_data, key=lambda x: x['price_change_percentage_24h'], reverse=True)[:5]:
            if x['price_change_percentage_24h']>0:
                top_gainers.append(x)
        for x in sorted(crypto_data, key=lambda x: x['price_change_percentage_24h'])[:5]:
            if x['price_change_percentage_24h']<0:
                top_losers.append(x)

        return top_gainers, top_losers
    except Exception as e:
        print(f"Error fetching crypto gainers/losers: {e}")
        return [], []


# Fetch VIX for stocks
def fetch_stock_volatility():
    try:
        vix = yf.Ticker("^VIX")
        vix_history = vix.history(period="1d")
        if not vix_history.empty:
            return {"vix_level": vix_history['Close'].iloc[-1]}
        return {"vix_level": "N/A"}
    except Exception as e:
        print(f"Error fetching stock VIX: {e}")
        return {"vix_level": "N/A"}

def fetch_bitcoin_volatility():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart", params={
            "vs_currency": "usd",
            "days": "30",
            "interval": "daily"
        }, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract daily prices
        prices = [price[1] for price in data["prices"]]
        daily_returns = np.diff(prices) / prices[:-1]
        volatility = np.std(daily_returns) * 100  # Convert to percentage

        return round(volatility, 2)
    except Exception as e:
        print(f"Error fetching Bitcoin volatility: {e}")
        return "N/A"

# Fetch Greed Index for stocks
def fetch_stock_greed_index():
    try:
        response = requests.get(urls["greed_index_stocks"], timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [{}])[0]
    except Exception as e:
        print(f"Error fetching stock Greed Index: {e}")
        return None


# Fetch Greed Index for crypto
def fetch_crypto_greed_index():
    try:
        response = requests.get(urls["greed_index_crypto"], timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [{}])[0]
    except Exception as e:
        print(f"Error fetching crypto Greed Index: {e}")
        return None

def fetch_news(keywords):
    articles = fetch_and_enrich_news(keywords)
    if articles:
        formatted_articles=[]

        for idx,article in enumerate(articles,1):
            # Clean and format the article
            new_article = clean_and_format_article(article)
            formatted_articles.append(new_article)
        return formatted_articles
    
    return []
        

def fetch_and_enrich_news(keywords: List[str]) -> List[Dict]:
    """
    Fetch news articles and enrich them with full content and summaries.
    
    Args:
        keywords (List[str]): List of keywords to search for
        
    Returns:
        List[Dict]: List of enriched news articles
    """
    try:
        # Combine keywords
        query = " OR ".join(keywords)
        
        # Get news from the last 24 hours
        yesterday = (datetime.now(timezone) - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        
        params = {
            'q': query,
            'apiKey': NEWSAPI_KEY,
            'language': 'en',
            'sortBy': 'popularity',
            'from': yesterday,
        }
        
        response = requests.get(urls["news_data"], params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            print("API response not OK:", data.get("message", "Unknown error"))
            return []

        # Configure newspaper
        config = Config()
        config.browser_user_agent = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Brave/1.0.0.0 Safari/537.36'
)

        config.request_timeout = 10

        enriched_articles = []
        
        for article_data in data.get("articles", []):
            if len(enriched_articles)>=5:
                break
            try:
                if article_data.get('title', '')=='' or article_data.get('title', '').lower()=='[removed]':
                    continue

                
                # Basic article info from News API
                article_info = {
                    'title': article_data.get('title', ''),
                    'description': article_data.get('description', ''),
                    'url': article_data.get('url', ''),
                    'source': article_data.get('source', {}).get('name', ''),
                    'published_at': article_data.get('publishedAt', ''),
                    'api_content': article_data.get('content', '')
                }
                

                # Fetch full content using newspaper3k
                article = Article(article_info['url'], config=config)
                article.download()
                time.sleep(1)  # Be nice to servers
                article.parse()
                article.nlp()  # This generates summary and keywords
                
                # Only store a preview of the full text (first 1000 characters)
                full_text = article.text[:1000] + '...' if len(article.text) > 1000 else article.text

                # Enrich with full content and NLP features
                article_info.update({
                    'summary': article.summary,
                    'keywords': article.keywords,
                    'authors': article.authors,
                    'top_image': article.top_image,
                    'movies': article.movies,  # Video URLs if available
                    'text_preview': full_text 
                })

                enriched_articles.append(article_info)

                
            except Exception as e:
                print(f"Error processing article {article_data.get('url')}: {str(e)}")
                # Add the article with basic info even if enrichment fails
                continue

        return enriched_articles

    except Exception as e:
        print(f"Error fetching news data: {e}")
        return []

def clean_and_format_article(article: Dict) -> Dict:
    """
    Clean and format article content.
    """
    # Remove extra whitespace and normalize text
    if article.get('full_text'):
        article['full_text'] = ' '.join(article['full_text'].split())
    
    # Create a shorter summary if the article summary is too long
    if article.get('summary') and len(article['summary']) > 500:
        sentences = article['summary'].split('. ')
        article['short_summary'] = '. '.join(sentences[:3]) + '.'
    
    return article





def save_data_to_json(data, file_name):
    # Ensure file_name is a string
    if not isinstance(file_name, str):
        raise TypeError(f"file_name should be a string, got {type(file_name)}")
    
    timestamp = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S %Z%z")
    data_with_time = {"timestamp": timestamp, "data": data}
    file_path="data/"+file_name+".json"
    # Ensure the directory exists before trying to save the file
    try:
        with open(file_path, "w") as json_file:
            json.dump(data_with_time, json_file, indent=4)
        print(f"{file_path} saved successfully at {timestamp}")
    except Exception as e:
        print(f"Error saving data: {e}")






# Automate data refresh
def refresh_data():
    print("Refreshing data")
    start=time.time()


    # Stocks data
    top_stock_gainers, top_stock_losers = fetch_market_gainers_and_losers()
    stock_volatility = fetch_stock_volatility()
    stock_greed_index = fetch_stock_greed_index()
    stock_news = fetch_news(stock_keywords)

    # Save stock data without Fear & Greed Index
    save_data_to_json({
        "gainers": top_stock_gainers,
        "losers": top_stock_losers,
        "volatility": stock_volatility,
        "greed_index": stock_greed_index,
        "news": stock_news
    }, "stock_data")

    

    bitcoin_volatility = fetch_bitcoin_volatility()
    top_crypto_gainers, top_crypto_losers = fetch_crypto_gainers_and_losers()
    crypto_greed_index = fetch_crypto_greed_index()
    crypto_news = fetch_news(crypto_keywords)

    # Save crypto data
    save_data_to_json({
        "gainers": top_crypto_gainers,
        "losers": top_crypto_losers,
        "volatility": {"volatility_index": bitcoin_volatility},
        "greed_index": crypto_greed_index,
        "news": crypto_news
    }, "crypto_data")   

    end=time.time()

    print("Time taken to refresh Data:",round(end-start,2),"seconds")

    print("Data refresh completed.")




# Main loop for scheduling
if __name__ == "__main__":
    pass
    # Schedule daily updates
    schedule.every(24).hours.do(refresh_data)
    print("Scheduler started. Data will be refreshed every 24 hours.")
    refresh_data()  # Initial run
    while True:
        schedule.run_pending()
        time.sleep(1)
