# Placeholder for financial data retrieval (since yfinance is unavailable)
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- CONFIGURATION ---
CONSOLIDATION_THRESHOLD = 0.5  # SMA spread threshold in %
SIMULATED_DAYS = 60

# --- TICKERS ---
nifty50_tickers = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
    'LT.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'ITC.NS', 'BHARTIARTL.NS'
]

banknifty_tickers = [
    'HDFCBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'SBIN.NS',
    'PNB.NS', 'BANKBARODA.NS', 'FEDERALBNK.NS', 'IDFCFIRSTB.NS', 'INDUSINDBK.NS'
]

midcap_tickers = [
    'GUJGASLTD.NS', 'TRENT.NS', 'BALKRISIND.NS', 'CROMPTON.NS', 'COFORGE.NS',
    'AUBANK.NS', 'ZYDUSLIFE.NS', 'MAXHEALTH.NS', 'INDHOTEL.NS', 'TATAELXSI.NS'
]

# --- SIMULATED STOCK DATA ---
def simulate_price_data(days=SIMULATED_DAYS):
    np.random.seed(42)
    base = np.cumsum(np.random.randn(days) * 2 + 100)
    dates = pd.date_range(end=datetime.today(), periods=days)
    return pd.DataFrame({'Date': dates, 'Close': base}).set_index('Date')

# --- CONSOLIDATION LOGIC ---
def check_consolidation(df, threshold=CONSOLIDATION_THRESHOLD):
    df['SMA14'] = df['Close'].rolling(14).mean()
    df['SMA21'] = df['Close'].rolling(21).mean()
    df['SMA35'] = df['Close'].rolling(35).mean()

    if df[['SMA14', 'SMA21', 'SMA35']].dropna().empty:
        return False

    latest = df[['SMA14', 'SMA21', 'SMA35']].dropna().iloc[-1]
    sma_values = [latest['SMA14'], latest['SMA21'], latest['SMA35']]
    sma_range_pct = ((max(sma_values) - min(sma_values)) / max(sma_values)) * 100

    return sma_range_pct < threshold

# --- SCREEN FUNCTION ---
def screen_stocks(ticker_list):
    results = []
    for ticker in ticker_list:
        try:
            df = simulate_price_data()
            if check_consolidation(df):
                results.append(ticker)
        except Exception as e:
            print(f"{ticker} - error: {e}")
    return results

# --- CLI EXECUTION ---
if __name__ == "__main__":
    print("Scanning for SMA Consolidation using simulated data...")
    print("\nNifty 50:")
    print(screen_stocks(nifty50_tickers))

    print("\nBank Nifty:")
    print(screen_stocks(banknifty_tickers))

    print("\nMidcap Nifty:")
    print(screen_stocks(midcap_tickers))
