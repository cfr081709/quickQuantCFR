import yfinance as yf
import pandas as pd
import numpy as np

def collectAndCheckData(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.index = pd.to_datetime(data.index)
    if data.isnull().values.any():
        data = data.ffill().bfill()
    elif data.empty:
        raise ValueError("No data found for the given ticker and date range.")
    data = data[~data.index.duplicated(keep='first')]
    data['returns'] = data['Adj Close'].pct_change().fillna(0)
    data['log_returns'] = np.log(data['Adj Close'] / data['Adj Close'].shift(1)).fillna(0)
    data = data.sort_index()
    return data


