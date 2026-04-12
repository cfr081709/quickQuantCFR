import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm
import matplotlib.pyplot as plt

class dataCollectionAndModification:
    @staticmethod
    def collectData(ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data
    @staticmethod
    def collectAndStoreData(ticker, start_date, end_date, filename):
        data= yf.download(ticker, start=start_date, end=end_date)
        data.to_csv(filename)
        print(f"Data stored in file {filename}")
        return
    @staticmethod
    def readData(filename, should_print):
        data = pd.read_csv(filename, index_col='Date', parse_dates=True)
        if should_print:
            print(data)
        return data
    @staticmethod
    def clearDataFile(filename):
        open(filename, 'w').close()
        return

class stockStandardSignalRetrieval:
    @staticmethod
    def getEMA(ticker, start_date, end_date, verbose=False):
        data = yf.download(ticker, start=start_date, end=end_date)
        data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
        data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
        data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
        data['EMA_200'] = data['Close'].ewm(span=200, adjust=False).mean()
        if verbose:
            print(data[['EMA_12','EMA_26','EMA_50','EMA_200']])
        return data[['EMA_12','EMA_26','EMA_50','EMA_200']]
    @staticmethod
    def getSMA(ticker, start_date, end_date, verbose=False):
        simpleMovingAverages = []
        data = yf.download(ticker, start=start_date, end=end_date)
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['SMA_100'] = data['Close'].rolling(window=100).mean()
        data['SMA_200'] = data['Close'].rolling(window=200).mean()
        if verbose:
            print(data[['SMA_20','SMA_50','SMA_100','SMA_200']])
        return data[['SMA_20','SMA_50','SMA_100','SMA_200']]
    @staticmethod
    def getMACD(ticker, start_date, end_date, verbose=False):
        data = yf.download(ticker, start=start_date, end=end_date)
        data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
        data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = data['EMA_12'] - data['EMA_26']
        if verbose:
            print(data['MACD'])
        return data['MACD']
    @staticmethod
    def getADX(ticker, start_date, end_date, period=14, verbose=False):
        data = yf.download(ticker, start=start_date, end=end_date)
        high = data['High']
        low = data['Low']
        close = data['Close']
        tr1 = high - low
        tr2 = np.abs(high - close.shift(1))
        tr3 = np.abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        up_move = high.diff().to_numpy().flatten()
        down_move = (-low.diff()).to_numpy().flatten()
        plus_dm = np.where(
            (up_move > down_move) & (up_move > 0),
            up_move,
            0.0
        )
        minus_dm = np.where(
            (down_move > up_move) & (down_move > 0),
            down_move,
            0.0
        )
        plus_dm = pd.Series(plus_dm, index=data.index)
        minus_dm = pd.Series(minus_dm, index=data.index)
        tr_smooth = tr.ewm(alpha=1/period, adjust=False).mean()
        plus_dm_smooth = plus_dm.ewm(alpha=1/period, adjust=False).mean()
        minus_dm_smooth = minus_dm.ewm(alpha=1/period, adjust=False).mean()
        plus_di = 100 * (plus_dm_smooth / tr_smooth)
        minus_di = 100 * (minus_dm_smooth / tr_smooth)
        dx = 100 * (np.abs(plus_di - minus_di) / (plus_di + minus_di))
        adx = dx.ewm(alpha=1/period, adjust=False).mean()
        if verbose:
            print(adx.tail())
        return adx
    @staticmethod
    def getRSI(ticker, start_date, end_date, verbose=False):
        data = yf.download(ticker, start=start_date, end=end_date)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        if verbose:
            print(data['RSI'])
        return data['RSI']
    @staticmethod
    def getOBV(ticker, start_date, end_date, verbose=False):
        data = yf.download(ticker, start=start_date, end=end_date)
        data['OBV'] = (np.sign(data['Close'].diff()) * data['Volume']).fillna(0).cumsum()
        if verbose:
            print(data['OBV'])
        return data['OBV']

class evaluationOfSignals:
    @staticmethod
    def evaluateEMA(ema_12, ema_26, ema_50, ema_200, verbose=False):
        if ema_12.iloc[-1] > ema_26.iloc[-1] and ema_12.iloc[-1] > ema_50.iloc[-1] and ema_12.iloc[-1] > ema_200.iloc[-1]:
            signal = "Buy"
        elif ema_12.iloc[-1] < ema_26.iloc[-1] and ema_12.iloc[-1] < ema_50.iloc[-1] and ema_12.iloc[-1] < ema_200.iloc[-1]:
            signal = "Sell"
        else:
            signal = "Hold"
        if verbose:
            print(signal)
        return signal
    @staticmethod
    def evaluateSMA(sma_20, sma_50, sma_100, sma_200, verbose=False):
        if sma_20.iloc[-1] > sma_50.iloc[-1] and sma_20.iloc[-1] > sma_100.iloc[-1] and sma_20.iloc[-1] > sma_200.iloc[-1]:
            signal = "Buy"
        elif sma_20.iloc[-1] < sma_50.iloc[-1] and sma_20.iloc[-1] < sma_100.iloc[-1] and sma_20.iloc[-1] < sma_200.iloc[-1]:
            signal = "Sell"
        else:
            signal = "Hold"
        if verbose:
            print(signal)
        return signal
    @staticmethod
    def evaluateMACD(macd, verbose=False):
        if macd.iloc[-1] > 0:
            signal = "Buy"
        elif macd.iloc[-1] < 0:
            signal = "Sell"
        else:
            signal = "Hold"
        if verbose:
            print(signal)
        return signal
    @staticmethod
    def evaluateADX(adx, verbose=False):
        if adx.iloc[-1] > 25:
            signal = "Strong Trend"
        elif adx.iloc[-1] < 20:
            signal = "Weak Trend"
        else:
            signal = "Neutral Trend"
        if verbose:
            print(signal)
        return signal
    @staticmethod
    def evaluateRSI(rsi, verbose=False):
        if rsi.iloc[-1] > 70:
            signal = "Overbought - Sell Signal"
        elif rsi.iloc[-1] < 30:
            signal = "Oversold - Buy Signal"
        else:
            signal = "Neutral - Hold Signal"
        if verbose:
            print(signal)
        return signal
    @staticmethod
    def evaluateOBV(obv, verbose=False):
        if obv.diff().iloc[-1] > 0:
            signal = "Buying Pressure - Buy Signal"
        elif obv.diff().iloc[-1] < 0:
            signal = "Selling Pressure - Sell Signal"
        else:
            signal = "Neutral - Hold Signal"
        if verbose:
            print(signal)
        return signal

class monteCarloSimulations:
    @staticmethod
    def callPayoff(S, K):
        return np.maximum(S - K, 0)
    @staticmethod
    def putPayoff(S, K):
        return np.maximum(K - S, 0)
    @staticmethod
    def generateRandomNumbers(mean, std, n):
        return np.random.normal(mean, std, n)
    @staticmethod
    def priceOptions(S0, K, r, sigma, T, n_simulations, n_steps, verbose=False, plot=False):
        S0 = float(S0)
        K = float(K)
        r = float(r)
        sigma = float(sigma)
        T = float(T)
        dt = T / n_steps
        all_paths = []
        for i in range(n_simulations):
            Z = monteCarloSimulations.generateRandomNumbers(0, 1, n_steps)
            S_path = np.zeros(n_steps + 1)
            S_path[0] = S0
            for t in range(n_steps):
                S_path[t+1] = S_path[t] * np.exp(
                    (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[t]
                )
            all_paths.append(S_path)
        all_paths = np.array(all_paths)
        ST = all_paths[:, -1]
        callPayoffs = monteCarloSimulations.callPayoff(ST, K)
        putPayoffs = monteCarloSimulations.putPayoff(ST, K)
        discountFactor = np.exp(-r * T)
        callPrice = discountFactor * np.mean(callPayoffs)
        putPrice = discountFactor * np.mean(putPayoffs)
        if verbose:
            print(f"Estimated Call Option Price: {callPrice}")
            print(f"Estimated Put Option Price: {putPrice}")
        if plot:
            time_grid = np.linspace(0, T, n_steps + 1)
            for i in range(min(50, n_simulations)):
                plt.plot(time_grid, all_paths[i])
            plt.xlabel("Time")
            plt.ylabel("Stock Price")
            plt.title("Monte Carlo Simulated Paths")
            plt.show()

        return callPrice, putPrice

class blackScholesPricing:
    @staticmethod
    def blackScholesCall(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        if verbose:
            print(f"Black-Scholes Call Option Price: {call_price}")
        return call_price
    @staticmethod
    def blackScholesPut(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        if verbose:
            print(f"Black-Scholes Put Option Price: {put_price}")
        return put_price
    @staticmethod
    def blackScholes(S, K, r, sigma, T, verbose=False):
        call_price = blackScholesPricing.blackScholesCall(S, K, r, sigma, T)
        put_price = blackScholesPricing.blackScholesPut(S, K, r, sigma, T)
        if verbose:
            print(f"Black-Scholes Call Option Price: {call_price}")
            print(f"Black-Scholes Put Option Price: {put_price}")
        return call_price, put_price

class calculateGreeks:
    @staticmethod
    def deltaCall(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        delta_call = norm.cdf(d1)
        if verbose:
            print(f"Delta of Call Option: {delta_call}")
        return delta_call
    @staticmethod
    def deltaPut(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        delta_put = norm.cdf(d1) - 1
        if verbose:
            print(f"Delta of Put Option: {delta_put}")
        return delta_put   
    @staticmethod
    def gamma(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        if verbose:
            print(f"Gamma: {gamma}")
        return gamma
    @staticmethod
    def vega(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T)
        if verbose:
            print(f"Vega: {vega}")
        return vega
    @staticmethod
    def thetaCall(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - (sigma * np.sqrt(T))
        theta_call = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) - (r * K * np.exp(-r * T) * norm.cdf(d2))
        if verbose:
            print(f"Theta of Call Option: {theta_call}")
        return theta_call
    @staticmethod
    def thetaPut(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - (sigma * np.sqrt(T))
        theta_put = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) + (r * K * np.exp(-r * T) * norm.cdf(-d2))
        if verbose:
            print(f"Theta of Put Option: {theta_put}")
        return theta_put
    @staticmethod
    def rhoCall(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - (sigma * np.sqrt(T))
        rho_call = K * T * np.exp(-r * T) * norm.cdf(d2)
        if verbose:
            print(f"Rho of Call Option: {rho_call}")
        return rho_call
    @staticmethod
    def rhoPut(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - (sigma * np.sqrt(T))
        rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2)
        if verbose:
            print(f"Rho of Put Option: {rho_put}")
        return rho_put
    @staticmethod
    def computeAllGreeks(S, K, r, sigma, T, verbose=False):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - (sigma * np.sqrt(T))
        deltaCall = norm.cdf(d1)
        deltaPut = norm.cdf(d1) - 1
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T)
        thetaCall = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) - (r * K * np.exp(-r * T) * norm.cdf(d2))
        thetaPut = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) + (r * K * np.exp(-r * T) * norm.cdf(-d2))
        rhoCall = K * T * np.exp(-r * T) * norm.cdf(d2)
        rhoPut = -K * T * np.exp(-r * T) * norm.cdf(-d2)
        if verbose:
            print(f"Delta Call: {deltaCall}")
            print(f"Delta Put: {deltaPut}")
            print(f"Gamma: {gamma}")
            print(f"Vega: {vega}")
            print(f"Theta Call: {thetaCall}")
            print(f"Theta Put: {thetaPut}")
            print(f"Rho Call: {rhoCall}")
            print(f"Rho Put: {rhoPut}")
        return deltaCall, deltaPut, gamma, vega, thetaCall, thetaPut, rhoCall, rhoPut

