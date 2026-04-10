import numpy as np
import pandas as pd
import yfinance as yf

exponentialMovingAverages = []
simpleMovingAverages = []

class dataCollectionAndModification:
    def collectData(ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data
    def collectAndStoreData(ticker, start_date, end_date, filename):
        data= yf.download(ticker, start=start_date, end=end_date)
        data.to_csv(filename)
        print("Data stored in file {filename}")
        return
    def readData(filename, should_print):
        data = pd.read_csv(filename, index_col='Date', parse_dates=True)
        if should_print:
            print(data)
        return data
    def clearDataFile(filename):
        open(filename, 'w').close()
        return

class stockStandardSignalRetrieval:
    def getEMA(ticker, start_date, end_date, Print=False):
        exponentialMovingAverages = []
        data = yf.download(ticker, start=start_date, end=end_date)
        data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
        data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
        data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
        data['EMA_200'] = data['Close'].ewm(span=200, adjust=False).mean()
        exponentialMovingAverages.append(data['EMA_12'])
        exponentialMovingAverages.append(data['EMA_26'])
        exponentialMovingAverages.append(data['EMA_50'])
        exponentialMovingAverages.append(data['EMA_200'])
        if Print:
            print(exponentialMovingAverages)
        return exponentialMovingAverages
    def getSMA(ticker, start_date, end_date, Print=False):
        simpleMovingAverages = []
        data = yf.download(ticker, start=start_date, end=end_date)
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['SMA_100'] = data['Close'].rolling(window=100).mean()
        data['SMA_200'] = data['Close'].rolling(window=200).mean()
        simpleMovingAverages.append(data['SMA_20'])
        simpleMovingAverages.append(data['SMA_50'])
        simpleMovingAverages.append(data['SMA_100'])
        simpleMovingAverages.append(data['SMA_200'])
        if Print:
            print(simpleMovingAverages)
        return simpleMovingAverages
    def getMACD(ticker, start_date, end_date, Print=False):
        data = yf.download(ticker, start=start_date, end=end_date)
        data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
        data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = data['EMA_12'] - data['EMA_26']
        if Print:
            print(data['MACD'])
        return data['MACD']
    def getADX(ticker, start_date, end_date, Print=False):
        data = yf.download(ticker, start=start_date, end=end_date)
        data['ADX'] = (data['High'] - data['Low']) / data['Close']
        if Print:
            print(data['ADX'])
        return data['ADX']
    def getRSI(ticker, start_date, end_date, Print=False):
        data = yf.download(ticker, start=start_date, end=end_date)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        if Print:
            print(data['RSI'])
        return data['RSI']
    def getOBV(ticker, start_date, end_date, Print=False):
        data = yf.download(ticker, start=start_date, end=end_date)
        data['OBV'] = (np.sign(data['Close'].diff()) * data['Volume']).fillna(0).cumsum()
        if Print:
            print(data['OBV'])
        return data['OBV']

class evaluationOfSignals:
    def evaluateEMA(ema_12, ema_26, ema_50, ema_200, Print=False):
        if ema_12.iloc[-1] > ema_26.iloc[-1] and ema_12.iloc[-1] > ema_50.iloc[-1] and ema_12.iloc[-1] > ema_200.iloc[-1]:
            signal = "Buy"
        elif ema_12.iloc[-1] < ema_26.iloc[-1] and ema_12.iloc[-1] < ema_50.iloc[-1] and ema_12.iloc[-1] < ema_200.iloc[-1]:
            signal = "Sell"
        else:
            signal = "Hold"
        if Print:
            print(signal)
        return signal
    def evaluateSMA(sma_20, sma_50, sma_100, sma_200, Print=False):
        if sma_20.iloc[-1] > sma_50.iloc[-1] and sma_20.iloc[-1] > sma_100.iloc[-1] and sma_20.iloc[-1] > sma_200.iloc[-1]:
            signal = "Buy"
        elif sma_20.iloc[-1] < sma_50.iloc[-1] and sma_20.iloc[-1] < sma_100.iloc[-1] and sma_20.iloc[-1] < sma_200.iloc[-1]:
            signal = "Sell"
        else:
            signal = "Hold"
        if Print:
            print(signal)
        return signal
    def evaluateMACD(macd, Print=False):
        if macd.iloc[-1] > 0:
            signal = "Buy"
        elif macd.iloc[-1] < 0:
            signal = "Sell"
        else:
            signal = "Hold"
        if Print:
            print(signal)
        return signal
    def evaluateADX(adx, Print=False):
        if adx.iloc[-1] > 25:
            signal = "Strong Trend"
        elif adx.iloc[-1] < 20:
            signal = "Weak Trend"
        else:
            signal = "Neutral Trend"
        if Print:
            print(signal)
        return signal
    def evaluateRSI(rsi, Print=False):
        if rsi.iloc[-1] > 70:
            signal = "Overbought - Sell Signal"
        elif rsi.iloc[-1] < 30:
            signal = "Oversold - Buy Signal"
        else:
            signal = "Neutral - Hold Signal"
        if Print:
            print(signal)
        return signal
    def evaluateOBV(obv, Print=False):
        if obv.diff().iloc[-1] > 0:
            signal = "Buying Pressure - Buy Signal"
        elif obv.diff().iloc[-1] < 0:
            signal = "Selling Pressure - Sell Signal"
        else:
            signal = "Neutral - Hold Signal"
        if Print:
            print(signal)
        return signal