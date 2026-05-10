import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

from ta.momentum import RSIIndicator

# -----------------------------------
# CREATE FOLDERS
# -----------------------------------
os.makedirs("outputs", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# -----------------------------------
# FETCH STOCK DATA
# -----------------------------------
def get_stock_data(ticker):

    print(f"\nFetching stock data for {ticker}...\n")

    data = yf.download(
        ticker,
        start="2020-01-01",
        end="2025-01-01",
        auto_adjust=False
    )

    if data.empty:
        print("No data found!")
        return None

    data.reset_index(inplace=True)

    # Fix multi-level columns issue
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


# -----------------------------------
# MOVING AVERAGES
# -----------------------------------
def add_moving_averages(data):

    data['SMA_20'] = data['Close'].rolling(window=20).mean()

    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    return data


# -----------------------------------
# DAILY RETURNS
# -----------------------------------
def calculate_daily_returns(data):

    data['Daily_Return'] = data['Close'].pct_change()

    return data


# -----------------------------------
# RSI CALCULATION
# -----------------------------------
def calculate_rsi(data):

    rsi = RSIIndicator(close=data['Close'], window=14)

    data['RSI'] = rsi.rsi()

    return data


# -----------------------------------
# VOLATILITY
# -----------------------------------
def calculate_volatility(data):

    volatility = data['Daily_Return'].std()

    return volatility


# -----------------------------------
# BUY/SELL SIGNALS
# -----------------------------------
def generate_signals(data):

    signals = []

    for rsi in data['RSI']:

        if rsi < 30:
            signals.append("BUY")

        elif rsi > 70:
            signals.append("SELL")

        else:
            signals.append("HOLD")

    data['Signal'] = signals

    return data


# -----------------------------------
# STOCK SUMMARY
# -----------------------------------
def stock_summary(data, ticker):

    highest_price = float(data['High'].max())

    lowest_price = float(data['Low'].min())

    average_close = float(data['Close'].mean())

    volatility = float(calculate_volatility(data))

    latest_signal = data['Signal'].iloc[-1]

    latest_rsi = data['RSI'].iloc[-1]

    print("\n========== STOCK SUMMARY ==========")

    print(f"Ticker: {ticker}")

    print(f"Highest Price: {highest_price:.2f}")

    print(f"Lowest Price: {lowest_price:.2f}")

    print(f"Average Closing Price: {average_close:.2f}")

    print(f"Volatility: {volatility:.4f}")

    print(f"Latest RSI: {latest_rsi:.2f}")

    print(f"Trading Signal: {latest_signal}")

    print("===================================\n")

    report = f"""
STOCK MARKET DATA ANALYSIS REPORT
=================================

Ticker: {ticker}

Highest Price: {highest_price:.2f}
Lowest Price: {lowest_price:.2f}
Average Closing Price: {average_close:.2f}
Volatility: {volatility:.4f}

Latest RSI: {latest_rsi:.2f}

Trading Signal: {latest_signal}

Signal Logic:
BUY  -> RSI below 30
SELL -> RSI above 70
HOLD -> Neutral zone

DISCLAIMER:
This project is for educational purposes only and not financial advice.
"""

    report_path = f"reports/{ticker}_report.txt"

    with open(report_path, "w") as file:
        file.write(report)

    print(f"Report saved: {report_path}")


# -----------------------------------
# STOCK PRICE CHART
# -----------------------------------
def plot_stock_analysis(data, ticker):

    plt.figure(figsize=(14, 7))

    plt.plot(data['Close'], label='Close Price')

    plt.plot(data['SMA_20'], label='SMA 20')

    plt.plot(data['SMA_50'], label='SMA 50')

    plt.title(f"{ticker} Stock Price Analysis")

    plt.xlabel("Days")

    plt.ylabel("Price")

    plt.legend()

    plt.grid()

    image_path = f"images/{ticker}_stock_analysis.png"

    plt.savefig(image_path)

    print(f"Chart saved: {image_path}")

    plt.show()


# -----------------------------------
# DAILY RETURNS CHART
# -----------------------------------
def plot_daily_returns(data, ticker):

    plt.figure(figsize=(14, 7))

    plt.plot(data['Daily_Return'], color='orange')

    plt.title(f"{ticker} Daily Returns")

    plt.xlabel("Days")

    plt.ylabel("Returns")

    plt.grid()

    image_path = f"images/{ticker}_daily_returns.png"

    plt.savefig(image_path)

    print(f"Chart saved: {image_path}")

    plt.show()


# -----------------------------------
# RSI CHART
# -----------------------------------
def plot_rsi(data, ticker):

    plt.figure(figsize=(14, 6))

    plt.plot(data['RSI'], label='RSI')

    plt.axhline(70, linestyle='--')

    plt.axhline(30, linestyle='--')

    plt.title(f"{ticker} RSI Analysis")

    plt.xlabel("Days")

    plt.ylabel("RSI")

    plt.legend()

    plt.grid()

    image_path = f"images/{ticker}_RSI_chart.png"

    plt.savefig(image_path)

    print(f"Chart saved: {image_path}")

    plt.show()


# -----------------------------------
# MAIN FUNCTION
# -----------------------------------
if __name__ == "__main__":

    ticker = input("Enter Stock Ticker (Example: AAPL, TSLA, INFY.NS): ")

    stock_data = get_stock_data(ticker)

    if stock_data is not None:

        # Add moving averages
        stock_data = add_moving_averages(stock_data)

        # Daily returns
        stock_data = calculate_daily_returns(stock_data)

        # RSI
        stock_data = calculate_rsi(stock_data)

        # Signals
        stock_data = generate_signals(stock_data)

        # Save CSV
        csv_path = f"outputs/{ticker}_stock_data.csv"

        stock_data.to_csv(csv_path, index=False)

        print(f"CSV saved: {csv_path}")

        # Summary
        stock_summary(stock_data, ticker)

        # Charts
        plot_stock_analysis(stock_data, ticker)

        plot_daily_returns(stock_data, ticker)

        plot_rsi(stock_data, ticker)

        print("\nPROJECT EXECUTED SUCCESSFULLY")