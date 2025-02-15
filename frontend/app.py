import streamlit as st
import sys
from pathlib import Path

# Add the parent directory to sys.path
PARENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT_DIR))

from chatbot.chat import process_user_input
import data_read as read


# --- Streamlit App Layout ---
st.set_page_config(page_title="Stock Market Analysis", layout="wide")

# --- Navigation Bar ---
st.markdown("""
<style>
    nav {
        background: linear-gradient(90deg, #34495E, #2E86C1);
        padding: 15px 0;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    nav a {
        text-decoration: none;
        font-size: 18px;
        color: white;
        margin-right: 25px;
        font-weight: bold;
        padding: 8px 15px;
        border-radius: 5px;
    }
    nav a:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
</style>
<nav>
    <center>
        <a href="#chat-section">💬 Chat Section</a>
        <a href="#top-gainers-losers">📊 Gainers & Losers</a>
        <a href="#market-indicators">📈 Market Indicators</a>
        <a href="#market-news">📰 Market News</a>
    </center>
</nav>
""", unsafe_allow_html=True)

st.title("📈 Stock Market Analysis & AI Assistant")

# --- Chat Section ---
st.subheader("💬 AI Chat Assistant", anchor="chat-section")

AI_welcome_message = "Hi! How can I assist you with the Financial market today?"

# Display only the latest AI response
def on_input_change():
    st.session_state.trigger_send = True  # Set a flag to simulate the "Send" button press

# Initialize session state variables
if "trigger_send" not in st.session_state:
    st.session_state.trigger_send = False
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

# Display text area with on_change callback
user_input = st.text_area(
    "Type your message (Shift+Enter for new line, Ctrl+Enter to send)",
    key="chat_input",
    height=100,
    on_change=on_input_change,
)

# Button to process user input
if st.button("Send") or st.session_state.trigger_send :
    st.session_state.trigger_send = False
    if user_input.strip():
        # Call the process_user_input function and get the result
        result = process_user_input(user_input.strip())

        # Handle the result based on the returned data
        if "text" in result:
            st.write(result["text"])  # Display the text response from the model
        elif "plot" in result:
            st.pyplot(result["plot"])  # Display the plot (matplotlib figure)
        elif "error" in result:
            st.error(result["error"])  # Display error message
# --- Adding Space Between Sections ---
st.markdown("<br><br>", unsafe_allow_html=True)

# --- Dropdown to choose Stock or Crypto ---
market_type = st.selectbox(
    "Choose the market type:",
    ["Stock", "Crypto"],
    help="Select Stock or Crypto to view respective market data.",
    index=0,  # Default to 'Stock'
    format_func=lambda x: f"{x.capitalize()} Market"  # Capitalize option text for better UI
)

# Adding space between sections
st.markdown("<br><br>", unsafe_allow_html=True)

# --- Main Content ---
st.header(f"📊 {market_type} Market Insights")

# --- Last Updated Section ---
last_updated = read.get_last_updated_time(f"{market_type.lower()}_data")  # Replace with actual file name
st.markdown(f"**Last updated:** {last_updated}")

# --- Top Gainers and Losers Side by Side ---
st.subheader(f"📊 Gainers & Losers ({market_type})", anchor="top-gainers-losers")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Top Gainers")
    gainers = read.fetch_top_gainers(market_type)
    st.table(gainers)

with col2:
    st.markdown("### 📉 Top Losers")
    losers = read.fetch_top_losers(market_type)
    st.table(losers)

# --- Adding Space Between Sections ---
st.markdown("<br><br>", unsafe_allow_html=True)

# --- Market Volatility and Greed Meter Side by Side ---
st.subheader(f"📈 Market Indicators ({market_type})", anchor="market-indicators")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌪️ Market Volatility")
    volatility = read.fetch_market_volatility(market_type)
    volatility_fig = read.create_speedometer(volatility, "Volatility Index", 100)
    st.plotly_chart(volatility_fig)

with col2:
    st.markdown("### 😈 Market Greed Meter")
    greed = read.fetch_market_greed_meter(market_type)
    greed_fig = read.create_fear_greed_index(greed)
    st.plotly_chart(greed_fig)

# --- Adding Space Between Sections ---
st.markdown("<br><br>", unsafe_allow_html=True)

# --- Market News with Expandable Headlines ---
st.subheader(f"📰 Top News of the Day ({market_type})", anchor="market-news")
news = read.fetch_market_news(market_type)

for article in news:
    with st.expander(article["title"]):
        st.write(article.get("summary","Summary is Not Available"))
        url=article.get('url'," No link Available")
        st.write(f"For more info : {url}")
