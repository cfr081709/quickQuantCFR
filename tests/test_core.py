import unittest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from src.quickQuantCFR.core import dataCollectionAndModification, stockStandardSignalRetrieval, evaluationOfSignals

class TestDataCollectionAndModification(unittest.TestCase):

    @patch('src.quickQuantCFR.core.yf.download')
    def test_collectData(self, mock_download):
        # Mock the yfinance download
        mock_data = pd.DataFrame({
            'Open': [100, 101],
            'High': [105, 106],
            'Low': [95, 96],
            'Close': [102, 103],
            'Volume': [1000, 1100]
        })
        mock_download.return_value = mock_data

        result = dataCollectionAndModification.collectData('AAPL', '2020-01-01', '2020-12-31')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        mock_download.assert_called_once_with('AAPL', start='2020-01-01', end='2020-12-31')

    @patch('src.quickQuantCFR.core.yf.download')
    @patch('src.quickQuantCFR.core.pd.DataFrame.to_csv')
    @patch('builtins.print')
    def test_collectAndStoreData(self, mock_print, mock_to_csv, mock_download):
        mock_data = pd.DataFrame({'Close': [100, 101]})
        mock_download.return_value = mock_data

        dataCollectionAndModification.collectAndStoreData('AAPL', '2020-01-01', '2020-12-31', 'test.csv')
        mock_download.assert_called_once_with('AAPL', start='2020-01-01', end='2020-12-31')
        mock_to_csv.assert_called_once_with('test.csv')
        mock_print.assert_called_once_with("Data stored in file {filename}")

    @patch('src.quickQuantCFR.core.pd.read_csv')
    @patch('builtins.print')
    def test_readData_with_print(self, mock_print, mock_read_csv):
        mock_data = pd.DataFrame({'Close': [100, 101]})
        mock_read_csv.return_value = mock_data

        result = dataCollectionAndModification.readData('test.csv', True)
        self.assertIsInstance(result, pd.DataFrame)
        mock_read_csv.assert_called_once_with('test.csv', index_col='Date', parse_dates=True)
        mock_print.assert_called_once_with(mock_data)

    @patch('src.quickQuantCFR.core.pd.read_csv')
    @patch('builtins.print')
    def test_readData_without_print(self, mock_print, mock_read_csv):
        mock_data = pd.DataFrame({'Close': [100, 101]})
        mock_read_csv.return_value = mock_data

        result = dataCollectionAndModification.readData('test.csv', False)
        self.assertIsInstance(result, pd.DataFrame)
        mock_print.assert_not_called()

    @patch('builtins.open')
    def test_clearDataFile(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value = mock_file

        dataCollectionAndModification.clearDataFile('test.csv')
        mock_open.assert_called_once_with('test.csv', 'w')
        mock_file.close.assert_called_once()

class TestStockStandardSignalRetrieval(unittest.TestCase):

    @patch('src.quickQuantCFR.core.yf.download')
    def test_getEMA(self, mock_download):
        mock_data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200]
        })
        mock_download.return_value = mock_data

        result = stockStandardSignalRetrieval.getEMA('AAPL', '2020-01-01', '2020-12-31', Print=False)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)  # EMA_12, EMA_26, EMA_50, EMA_200

    @patch('src.quickQuantCFR.core.yf.download')
    def test_getSMA(self, mock_download):
        mock_data = pd.DataFrame({
            'Close': [100] * 200
        })
        mock_download.return_value = mock_data

        result = stockStandardSignalRetrieval.getSMA('AAPL', '2020-01-01', '2020-12-31', Print=False)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)  # SMA_20, SMA_50, SMA_100, SMA_200

    @patch('src.quickQuantCFR.core.yf.download')
    def test_getMACD(self, mock_download):
        mock_data = pd.DataFrame({
            'Close': [100] * 50
        })
        mock_download.return_value = mock_data

        result = stockStandardSignalRetrieval.getMACD('AAPL', '2020-01-01', '2020-12-31', Print=False)
        self.assertIsInstance(result, pd.Series)

    @patch('src.quickQuantCFR.core.yf.download')
    def test_getADX(self, mock_download):
        mock_data = pd.DataFrame({
            'High': [105] * 10,
            'Low': [95] * 10,
            'Close': [100] * 10
        })
        mock_download.return_value = mock_data

        result = stockStandardSignalRetrieval.getADX('AAPL', '2020-01-01', '2020-12-31', Print=False)
        self.assertIsInstance(result, pd.Series)

    @patch('src.quickQuantCFR.core.yf.download')
    def test_getRSI(self, mock_download):
        mock_data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150]
        })
        mock_download.return_value = mock_data

        result = stockStandardSignalRetrieval.getRSI('AAPL', '2020-01-01', '2020-12-31', Print=False)
        self.assertIsInstance(result, pd.Series)

    @patch('src.quickQuantCFR.core.yf.download')
    def test_getOBV(self, mock_download):
        mock_data = pd.DataFrame({
            'Close': [100, 101, 99, 102],
            'Volume': [1000, 1100, 900, 1200]
        })
        mock_download.return_value = mock_data

        result = stockStandardSignalRetrieval.getOBV('AAPL', '2020-01-01', '2020-12-31', Print=False)
        self.assertIsInstance(result, pd.Series)

class TestEvaluationOfSignals(unittest.TestCase):

    def test_evaluateEMA_buy(self):
        ema_12 = pd.Series([100, 101, 102])
        ema_26 = pd.Series([95, 96, 97])
        ema_50 = pd.Series([90, 91, 92])
        ema_200 = pd.Series([85, 86, 87])

        result = evaluationOfSignals.evaluateEMA(ema_12, ema_26, ema_50, ema_200, Print=False)
        self.assertEqual(result, "Buy")

    def test_evaluateEMA_sell(self):
        ema_12 = pd.Series([85, 86, 87])
        ema_26 = pd.Series([95, 96, 97])
        ema_50 = pd.Series([90, 91, 92])
        ema_200 = pd.Series([100, 101, 102])

        result = evaluationOfSignals.evaluateEMA(ema_12, ema_26, ema_50, ema_200, Print=False)
        self.assertEqual(result, "Sell")

    def test_evaluateEMA_hold(self):
        ema_12 = pd.Series([95, 96, 97])
        ema_26 = pd.Series([95, 96, 97])
        ema_50 = pd.Series([90, 91, 92])
        ema_200 = pd.Series([100, 101, 102])

        result = evaluationOfSignals.evaluateEMA(ema_12, ema_26, ema_50, ema_200, Print=False)
        self.assertEqual(result, "Hold")

    def test_evaluateSMA_buy(self):
        sma_20 = pd.Series([100, 101, 102])
        sma_50 = pd.Series([95, 96, 97])
        sma_100 = pd.Series([90, 91, 92])
        sma_200 = pd.Series([85, 86, 87])

        result = evaluationOfSignals.evaluateSMA(sma_20, sma_50, sma_100, sma_200, Print=False)
        self.assertEqual(result, "Buy")

    def test_evaluateSMA_sell(self):
        sma_20 = pd.Series([85, 86, 87])
        sma_50 = pd.Series([95, 96, 97])
        sma_100 = pd.Series([90, 91, 92])
        sma_200 = pd.Series([100, 101, 102])

        result = evaluationOfSignals.evaluateSMA(sma_20, sma_50, sma_100, sma_200, Print=False)
        self.assertEqual(result, "Sell")

    def test_evaluateSMA_hold(self):
        sma_20 = pd.Series([95, 96, 97])
        sma_50 = pd.Series([95, 96, 97])
        sma_100 = pd.Series([90, 91, 92])
        sma_200 = pd.Series([100, 101, 102])

        result = evaluationOfSignals.evaluateSMA(sma_20, sma_50, sma_100, sma_200, Print=False)
        self.assertEqual(result, "Hold")

    def test_evaluateMACD_buy(self):
        macd = pd.Series([-1, 0, 1])

        result = evaluationOfSignals.evaluateMACD(macd, Print=False)
        self.assertEqual(result, "Buy")

    def test_evaluateMACD_sell(self):
        macd = pd.Series([1, 0, -1])

        result = evaluationOfSignals.evaluateMACD(macd, Print=False)
        self.assertEqual(result, "Sell")

    def test_evaluateMACD_hold(self):
        macd = pd.Series([-1, 0, 0])

        result = evaluationOfSignals.evaluateMACD(macd, Print=False)
        self.assertEqual(result, "Hold")

    def test_evaluateADX_strong_trend(self):
        adx = pd.Series([20, 25, 30])

        result = evaluationOfSignals.evaluateADX(adx, Print=False)
        self.assertEqual(result, "Strong Trend")

    def test_evaluateADX_weak_trend(self):
        adx = pd.Series([25, 20, 15])

        result = evaluationOfSignals.evaluateADX(adx, Print=False)
        self.assertEqual(result, "Weak Trend")

    def test_evaluateADX_neutral_trend(self):
        adx = pd.Series([20, 22, 23])

        result = evaluationOfSignals.evaluateADX(adx, Print=False)
        self.assertEqual(result, "Neutral Trend")

    def test_evaluateRSI_overbought(self):
        rsi = pd.Series([65, 70, 75])

        result = evaluationOfSignals.evaluateRSI(rsi, Print=False)
        self.assertEqual(result, "Overbought - Sell Signal")

    def test_evaluateRSI_oversold(self):
        rsi = pd.Series([35, 30, 25])

        result = evaluationOfSignals.evaluateRSI(rsi, Print=False)
        self.assertEqual(result, "Oversold - Buy Signal")

    def test_evaluateRSI_neutral(self):
        rsi = pd.Series([45, 50, 55])

        result = evaluationOfSignals.evaluateRSI(rsi, Print=False)
        self.assertEqual(result, "Neutral - Hold Signal")

    def test_evaluateOBV_buy(self):
        obv = pd.Series([1000, 1100, 1200])

        result = evaluationOfSignals.evaluateOBV(obv, Print=False)
        self.assertEqual(result, "Buying Pressure - Buy Signal")

    def test_evaluateOBV_sell(self):
        obv = pd.Series([1200, 1100, 1000])

        result = evaluationOfSignals.evaluateOBV(obv, Print=False)
        self.assertEqual(result, "Selling Pressure - Sell Signal")

    def test_evaluateOBV_hold(self):
        obv = pd.Series([1000, 1000, 1000])

        result = evaluationOfSignals.evaluateOBV(obv, Print=False)
        self.assertEqual(result, "Neutral - Hold Signal")

if __name__ == '__main__':
    unittest.main()