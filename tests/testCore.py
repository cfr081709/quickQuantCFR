import numpy as np
from queue import Queue

from quickQuantCFR.backtestingEngine import (
    Event,
    marketEvent,
    signalEvent,
    orderEvent,
    fillEvent,
    dataHandler,
    historicalCSVDataHandler
)

from quickQuantCFR.core import (
    dataCollectionAndModification,
    stockStandardSignalRetrieval,
    evaluationOfSignals,
    monteCarloSimulations,
    blackScholesPricing
)

def run_full_test():
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2024-01-01"

    print("\n=== 1. DATA DOWNLOAD TEST ===")
    data = dataCollectionAndModification.collectData(ticker, start_date, end_date, verbose=True)

    print("\n=== 2. INDICATORS TEST ===")

    ema = stockStandardSignalRetrieval.getEMA(ticker, start_date, end_date)
    sma = stockStandardSignalRetrieval.getSMA(ticker, start_date, end_date)
    macd = stockStandardSignalRetrieval.getMACD(ticker, start_date, end_date)
    rsi = stockStandardSignalRetrieval.getRSI(ticker, start_date, end_date)
    obv = stockStandardSignalRetrieval.getOBV(ticker, start_date, end_date)
    adx = stockStandardSignalRetrieval.getADX(ticker, start_date, end_date)

    print("EMA OK")
    print("SMA OK")
    print("MACD OK")
    print("RSI OK")
    print("OBV OK")
    print("ADX OK")

    print("\n=== 3. SIGNAL EVALUATION TEST ===")

    ema_signal = evaluationOfSignals.evaluateEMA(
        ema['EMA_12'], ema['EMA_26'], ema['EMA_50'], ema['EMA_200']
    )

    sma_signal = evaluationOfSignals.evaluateSMA(
        sma['SMA_20'], sma['SMA_50'], sma['SMA_100'], sma['SMA_200']
    )

    macd_signal = evaluationOfSignals.evaluateMACD(macd)
    rsi_signal = evaluationOfSignals.evaluateRSI(rsi)
    obv_signal = evaluationOfSignals.evaluateOBV(obv)
    adx_signal = evaluationOfSignals.evaluateADX(adx)

    print("EMA Signal:", ema_signal)
    print("SMA Signal:", sma_signal)
    print("MACD Signal:", macd_signal)
    print("RSI Signal:", rsi_signal)
    print("OBV Signal:", obv_signal)
    print("ADX Signal:", adx_signal)

    print("\n=== 4. MONTE CARLO TEST ===")

    S0 = 150
    K = 200
    r = 0.05
    sigma = 0.2
    T = 1
    n_simulations = 10
    n_steps = 5

    mc_call, mc_put = monteCarloSimulations.priceOptions(
        S0, K, r, sigma, T, n_simulations, n_steps, verbose=True, plot=False
    )

    print("\nMonte Carlo Call:", mc_call)
    print("Monte Carlo Put:", mc_put)

    print("\n=== 5. BLACK-SCHOLES TEST ===")

    bs_call = blackScholesPricing.blackScholesCall(S0, K, r, sigma, T, verbose=True)
    bs_put = blackScholesPricing.blackScholesPut(S0, K, r, sigma, T, verbose=True)

    print("\nBlack-Scholes Call:", bs_call)
    print("Black-Scholes Put:", bs_put)

    print("\n === Backtest Engine Tests ===")

    events = Queue()
    csv_dir = r'C:\Users\Owner\Documents\quickQuantCFR\tests'
    symbols = ['AAPL']
    handler = historicalCSVDataHandler(events, csv_dir, symbols)

    print("\nHistorical Data Test:")
    for s in symbols:
        print(handler.symbolData[s])

    # Test getNewBars (generator → must iterate)
    print("\nGet New Bars:")
    bars = handler.getNewBars(symbols[0])
    for i, bar in enumerate(bars):
        print(bar)
        if i > 5: break   # limit output

    # Test updateBars
    print("\nUpdate Bars Test:")
    handler.updateBars()

    # Test getLatestBars
    print("\nGet Latest Bars:")
    print(handler.getLatestBars(symbols[0], N=5))
    
    print("\n=== ALL TESTS COMPLETE AND FUNCTIONAL ===")


if __name__ == "__main__":
    run_full_test()