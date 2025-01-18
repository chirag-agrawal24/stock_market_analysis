# Financial Market Analysis Tool  

## Project Overview  
The **Financial Market Analysis Tool** is a comprehensive platform that provides users with real-time insights into the stock and cryptocurrency markets. With features such as market trends, sentiment analysis, and the latest news, the tool helps users stay informed and make data-driven decisions.  

Additionally, the integration of the **Gemini Chatbot** allows users to query market data interactively, offering a seamless experience for financial market analysis.  


---

## Project Structure  

The project is organized into the following directories and files:

### 1. **[`chatbot/`](chatbot)**
   - **[`functions.py`](chatbot/functions.py)**: Contains utility functions used by the Gemini chatbot to retrieve and process data.  
   - **[`chat.py`](chatbot/chat.py)**: Implements the chatbot's logic and defines how it generates responses.  

### 2. **[`data/`](data)**
   - **[`config.json`](data/config.json)**: Stores URLs , stock tickers (e.g., US30), and relevant keywords.  
   - **[`update_data.py`](data/update_data.py)**: Functions for refreshing and saving market data into JSON files.  
   - **[`stock_data.json`](data/stock_data.json)**: Stores updated stock market data, including top gainers, losers, volatility, and sentiment analysis.  
   - **[`crypto_data.json`](data/crypto_data.json)**: Stores updated cryptocurrency market data with similar attributes.  

### 3. **[`frontend/`](frontend)**
   - **[`app.py`](frontend/app.py)**: Main application file built with Streamlit, which powers the user interface and chatbot integration.  
   - **[`data_read.py`](frontend/data_read.py)**: Reads data from the JSON files and triggers a data refresh if the data is older than 24 hours.  

### 4. **Other Files**
   - **[`requirements.txt`](requirements.txt)**: Lists all the dependencies required to run the project.  
   - **[`README.md`](README.md)**: Documentation for the project, including setup instructions.  
   - **[`.streamlit/secrets.toml`](.streamlit/secrets.toml)** : Secrets to securely save API KEYS


---

## Setup  

Follow these steps to set up and run the **Financial Market Analysis Tool**:  

### Prerequisites  
- Python 3.8+  
- [Streamlit](https://streamlit.io) (used for the web-based frontend)  

### Installation  

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/chirag-agrawal24/stock_market_analysis.git
   cd stock_market_analysis
   ```  

2. **Install dependencies**:  
   Run the following command to install all required Python packages:  
   ```bash
   pip install -r requirements.txt
   ```  

3. **Set up the configuration**:  
   - Open the [`.streamlit/secrets.toml`](.streamlit/secrets.toml) file and input your **API keys**

4. **Run the application**:  
   Start the Streamlit frontend by running:  
   ```bash
   streamlit run frontend/app.py
   ```  

5. **Access the application**:  
   Open your browser and go to `http://localhost:8501` to access the tool.  

---

## Features  

- **Market Insights**: View the top gainers, top losers, market volatility, and sentiment analysis (greed index).  
- **Latest News**: Get up-to-date news about stocks and cryptocurrencies.  
- **Gemini Chatbot**: Interactive chatbot that answers queries about market trends and data.  
- **Automated Data Refresh**: Ensures data is updated regularly by checking timestamps.  

---


## Contributors  

- **Yash Pinjarkar**: Project Lead & Chatbot Development &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              | &nbsp;&nbsp; [LinkedIn Profile](https://www.linkedin.com/in/yash-pinjarkar/) &nbsp;&nbsp;|&nbsp;&nbsp; [GitHub Profile](https://github.com/yashpinjarkar10)  
- **Chirag Agrawal**: News Summarization, Frontend, Deployment &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
| &nbsp;&nbsp; [LinkedIn Profile](https://www.linkedin.com/in/-chirag-agrawal-/) &nbsp;&nbsp;|&nbsp;&nbsp; [GitHub Profile](https://github.com/chirag-agrawal24)  
- **Deepanshu Kesharwani**:  Data Fetching & Analysis &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  | &nbsp;&nbsp; [LinkedIn Profile](https://www.linkedin.com/in/deepanshu-kesharwani-0028b1191/) &nbsp;&nbsp;|&nbsp;&nbsp; [GitHub Profile](https://github.com/Deepanshu-kesharwani)  



---

We’re excited to have you contribute! To get started, fork repository and submit a pull request.  
Feel free to make changes or suggest enhancements to improve the tool. 🚀 

 

---  

