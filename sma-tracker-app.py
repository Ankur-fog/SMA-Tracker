import streamlit as st
import yfinance as yf
import pandas as pd

# Config
CONSOLIDATION_THRESHOLD = 0.5  # percent

# Stock lists (Nifty50, BankNifty, MidcapNifty)
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

# SMA calculation and consolidation check
def check_consolidation(df, threshold=CONSOLIDATION_THRESHOLD):
    df['SMA14'] = df['Close'].rolling(window=14).mean()
    df['SMA21'] = df['Close'].rolling(window=21).mean()
    df['SMA35'] = df['Close'].rolling(window=35).mean()

    if df[['SMA14', 'SMA21', 'SMA35']].dropna().empty:
        return False

    latest = df[['SMA14', 'SMA21', 'SMA35']].dropna().iloc[-1]
    sma_values = [latest['SMA14'], latest['SMA21'], latest['SMA35']]
    range_pct = ((max(sma_values) - min(sma_values)) / max(sma_values)) * 100

    return range_pct < threshold

# Function to scan a list of tickers and return those in consolidation
def scan_tickers(tickers):
    consolidating = []
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if df.empty:
                continue
            if check_consolidation(df):
                consolidating.append(ticker)
        except Exception as e:
            st.write(f"Error fetching {ticker}: {e}")
    return consolidating

# Streamlit UI
st.title("SMA Consolidation Tracker")

st.write("This app scans stocks for 14, 21, 35 SMA consolidation.")

option = st.selectbox(
    "Choose Index to Scan",
    ("Nifty 50", "Bank Nifty", "Midcap Nifty")
)

if st.button("Scan Now"):
    with st.spinner('Scanning stocks, please wait...'):
        if option == "Nifty 50":
            results = scan_tickers(nifty50_tickers)
        elif option == "Bank Nifty":
            results = scan_tickers(banknifty_tickers)
        else:
            results = scan_tickers(midcap_tickers)

    if results:
        st.success(f"Stocks in consolidation:\n{', '.join(results)}")
    else:
        st.info("No stocks currently consolidating.")
