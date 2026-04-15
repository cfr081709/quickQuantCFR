import sys
import numpy as np
from queue import Queue

sys.path.insert(0, r"E:\quickQuantCFR\src")

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
    blackScholesPricing,
    calculateGreeks,
    volatilityARCH
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
    n_simulations = 1000
    n_steps = 50

    mc_call, mc_put, mc_putPayoffs, mc_callPayoffs = monteCarloSimulations.priceOptions(
        S0, K, r, sigma, T, n_simulations, n_steps, verbose=False, plot=True
    )

    print("\nMonte Carlo Call Price:", mc_call)
    print("Monte Carlo Put Price:", mc_put)
    print("Monte Carlo Call Payoff:", mc_callPayoffs)
    print("Monte Carlo Put Payoff:", mc_putPayoffs)

    mc_call, mc_put, mc_AntiCall, mc_AntiPut, mc_AntiCallPayoff, mc_AntiPutPayoff, mc_putPayoffs, mc_callPayoffs = monteCarloSimulations.priceOptionsAntiVariate(
        S0, K, r, sigma, T, n_simulations, n_steps, verbose=False, plot=True
    )

    print("\nMonte Carlo Call Price:", mc_call)
    print("Monte Carlo Put Price:", mc_put)
    print("Anti-Variate Monte Carlo Call Price:", mc_AntiCall)
    print("Anti-Variate Monte Carlo Put Price:", mc_AntiPut)
    print("Monte Carlo Call Payoff:", mc_callPayoffs)
    print("Monte Carlo Put Payoff:", mc_putPayoffs)
    print("Anti-Variate Monte Carlo Call Payoff:", mc_AntiCallPayoff)
    print("Anti-Variate Monte Carlo Call Payoff:", mc_AntiPutPayoff)


    print("\n=== 5. BLACK-SCHOLES TEST ===")

    bs_call = blackScholesPricing.blackScholesCall(S0, K, r, sigma, T, verbose=True)
    bs_put = blackScholesPricing.blackScholesPut(S0, K, r, sigma, T, verbose=True)

    print("\nBlack-Scholes Call:", bs_call)
    print("Black-Scholes Put:", bs_put)

    print("\n==== 6. CALCULATE GREEK'S TEST ====")
    
    deltaCall = calculateGreeks.deltaCall(S0, K, r, sigma, T, verbose=False)
    deltaPut = calculateGreeks.deltaPut(S0, K, r, sigma, T, verbose=False)
    gamma = calculateGreeks.gamma(S0, K, r, sigma, T, verbose=False)
    vega = calculateGreeks.vega(S0, K, r, sigma, T, verbose=False)
    thetaCall = calculateGreeks.thetaCall(S0, K, r, sigma, T, verbose=False)
    thetaPut = calculateGreeks.thetaPut(S0, K, r, sigma, T, verbose=False)
    rhoCall = thetaCall = calculateGreeks.rhoCall(S0, K, r, sigma, T, verbose=False)
    rhoPut = calculateGreeks.rhoPut(S0, K, r, sigma, T, verbose=False)

    print(f"\n Delta Call: {deltaCall}")
    print(f"Delta Put: {deltaPut}")
    print(f"Gamma: {gamma}")
    print(f"Vega: {vega}")
    print(f"Theta Call: {thetaCall}")
    print(f"Theta Put: {thetaPut}")
    print(f"Rho Call: {rhoCall}")
    print(f"Rho Put: {rhoPut}")

    calculateGreeks.computeAllGreeks(S0, K, r, sigma, T, verbose=True)

    print("\n ==== 7. VOLATILITY FORECAST TEST ===")

    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2024-01-01"


    weightedMovingAverageVolatility = volatilityARCH.weightedMovingAverageVolatilityForecasting(ticker, start_date, end_date, decayFactor=0.94, verbose=False, plot=True)

    print(f"\n Forecasted Volatility: {weightedMovingAverageVolatility}")
    
    print("\n === 8. BACKTEST ENGINE TEST ===")

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