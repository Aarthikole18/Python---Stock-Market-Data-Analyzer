import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

from ta.momentum import RSIIndicator

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Stock Market Data Analyzer",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("📈 Stock Market Data Analyzer")

st.write("Analyze stock market trends, RSI, returns, and moving averages.")

# -----------------------------------
# USER INPUT
# -----------------------------------
ticker = st.text_input(
    "Enter Stock Ticker (Example: AAPL, TSLA, INFY.NS)",
    "AAPL"
)

# -----------------------------------
# FETCH DATA
# -----------------------------------
@st.cache_data
def load_data(ticker):

    data = yf.download(
        ticker,
        start="2020-01-01",
        end="2025-01-01",
        auto_adjust=False
    )

    data.reset_index(inplace=True)

    # Fix multi-level columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


# -----------------------------------
# PROCESS DATA
# -----------------------------------
if st.button("Analyze Stock"):

    data = load_data(ticker)

    if data.empty:
        st.error("No stock data found.")
    else:

        # Moving averages
        data['SMA_20'] = data['Close'].rolling(window=20).mean()

        data['SMA_50'] = data['Close'].rolling(window=50).mean()

        # Daily returns
        data['Daily_Return'] = data['Close'].pct_change()

        # RSI
        rsi = RSIIndicator(close=data['Close'], window=14)

        data['RSI'] = rsi.rsi()

        # -----------------------------------
        # SUMMARY
        # -----------------------------------
        highest_price = float(data['High'].max())

        lowest_price = float(data['Low'].min())

        average_close = float(data['Close'].mean())

        volatility = float(data['Daily_Return'].std())

        latest_rsi = float(data['RSI'].iloc[-1])

        # Signal logic
        if latest_rsi < 30:
            signal = "BUY"

        elif latest_rsi > 70:
            signal = "SELL"

        else:
            signal = "HOLD"

        # -----------------------------------
        # DISPLAY METRICS
        # -----------------------------------
        st.subheader("📊 Stock Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Highest Price", f"{highest_price:.2f}")

        col2.metric("Lowest Price", f"{lowest_price:.2f}")

        col3.metric("Average Close", f"{average_close:.2f}")

        st.write(f"### Volatility: {volatility:.4f}")

        st.write(f"### Latest RSI: {latest_rsi:.2f}")

        st.write(f"### Trading Signal: {signal}")

        # -----------------------------------
        # DATA PREVIEW
        # -----------------------------------
        st.subheader("📄 Dataset Preview")

        st.dataframe(data.head())

        # -----------------------------------
        # STOCK PRICE CHART
        # -----------------------------------
        st.subheader("📈 Stock Price Analysis")

        fig1, ax1 = plt.subplots(figsize=(14, 6))

        ax1.plot(data['Close'], label='Close Price')

        ax1.plot(data['SMA_20'], label='SMA 20')

        ax1.plot(data['SMA_50'], label='SMA 50')

        ax1.legend()

        ax1.grid()

        st.pyplot(fig1)

        # -----------------------------------
        # DAILY RETURNS CHART
        # -----------------------------------
        st.subheader("📉 Daily Returns")

        fig2, ax2 = plt.subplots(figsize=(14, 6))

        ax2.plot(data['Daily_Return'], color='orange')

        ax2.grid()

        st.pyplot(fig2)

        # -----------------------------------
        # RSI CHART
        # -----------------------------------
        st.subheader("📊 RSI Analysis")

        fig3, ax3 = plt.subplots(figsize=(14, 6))

        ax3.plot(data['RSI'], label='RSI')

        ax3.axhline(70, linestyle='--')

        ax3.axhline(30, linestyle='--')

        ax3.legend()

        ax3.grid()

        st.pyplot(fig3)

        st.success("Stock Analysis Completed Successfully")