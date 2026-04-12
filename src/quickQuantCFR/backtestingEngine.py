import os
import numpy as np
import pandas as pd
from abc import ABCMeta, abstractmethod


# =========================
# EVENTS
# =========================

class Event(object):
    pass


class marketEvent(Event):
    def __init__(self):
        self.type = 'MARKET'


class signalEvent(Event):
    def __init__(self, datetime, signalType, symbol):
        self.type = 'SIGNAL'
        self.datetime = datetime
        self.signalType = signalType
        self.symbol = symbol


class orderEvent(Event):
    def __init__(self, ticker, orderType, quantity, direction):
        self.type = 'ORDER'
        self.symbol = ticker
        self.orderType = orderType
        self.quantity = quantity
        self.direction = direction

    def printOrder(self):
        print(f"Order: {self.orderType} of {self.quantity} shares of {self.symbol} in direction {self.direction}")


class fillEvent(Event):
    def __init__(self, timeindex, symbol, exchange, quantity, direction, fillCost, commission=None):
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fillCost = fillCost

        if commission is None:
            self.commission = self.calculateIBCommission()
        else:
            self.commission = commission

    def calculateIBCommission(self):
        fullCost = 1.3

        if self.quantity < 500:
            fullCost = max(1.3, 0.013 * self.quantity)
        else:
            fullCost = max(1.3, 0.008 * self.quantity)

        fullCost = min(fullCost, 0.005 * self.quantity * self.fillCost)
        return fullCost


# =========================
# DATA HANDLER BASE
# =========================

class dataHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getLatestBars(self, symbol, N=1):
        raise NotImplementedError()

    @abstractmethod
    def updateBars(self):
        raise NotImplementedError()


# =========================
# HISTORICAL CSV HANDLER
# =========================

class historicalCSVDataHandler(dataHandler):

    def __init__(self, events, csvDir, symbolList):
        self.events = events
        self.csvDir = csvDir
        self.symbolList = symbolList

        self.symbolData = {}
        self.latestSymbolData = {}
        self.continueBacktest = True

        self.openConvertCSVFiles()

    # -------------------------
    # LOAD DATA
    # -------------------------
    def openConvertCSVFiles(self):

        combIndex = None

        # Load CSVs
        for s in self.symbolList:

            filepath = os.path.join(self.csvDir, f'{s}.csv')
            print("Loading file:", filepath)

            filepath = r"C:\Users\Owner\Documents\quickQuantCFR\tests\AAPL.csv"

            with open(filepath, "r") as f:
                print(f.read())

            df = pd.read_csv(
                filepath,
                header=0,
                index_col=0,
                parse_dates=True
            )

            df.sort_index(inplace=True)

            self.symbolData[s] = df

            if combIndex is None:
                combIndex = df.index
            else:
                combIndex = combIndex.union(df.index)

        # init latest bars container (FIXED)
        self.latestSymbolData = {s: [] for s in self.symbolList}

        # Align data + features
        for s in self.symbolList:

            df = self.symbolData[s].reindex(combIndex, method='pad')

            df['returns'] = df['adj_close'].pct_change()
            df['daily_change'] = df['open'] - df['close']

            df['log_returns'] = np.log(
                df['adj_close'] / df['adj_close'].shift(1)
            )

            self.symbolData[s] = df

            # IMPORTANT FIX: iterator per symbol
            self.symbolData[s] = self.symbolData[s].iterrows()

    # -------------------------
    # GENERATOR
    # -------------------------
    def getNewBars(self, symbol):
        for b in self.symbolData[symbol]:
            yield (
                symbol,
                b[0],
                b[1]['open'],
                b[1]['high'],
                b[1]['low'],
                b[1]['close'],
                b[1]['volume']
            )

    # -------------------------
    # LATEST BARS
    # -------------------------
    def getLatestBars(self, symbol, N=1):
        try:
            bars = self.latestSymbolData[symbol]
            return bars[-N:]
        except KeyError:
            print("Symbol not found in dataset.")
            return []

    # -------------------------
    # STREAM UPDATE
    # -------------------------
    def updateBars(self):

        for s in self.symbolList:

            try:
                bar = next(self.getNewBars(s))   # FIXED
            except StopIteration:
                self.continueBacktest = False
                continue

            if s not in self.latestSymbolData:
                self.latestSymbolData[s] = []

            self.latestSymbolData[s].append(bar)

        self.events.put(marketEvent())