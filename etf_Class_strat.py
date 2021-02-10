#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 15:17:57 2021

@author: minayuan
"""
import pandas as pd
import numpy as np
import investpy
import yfinance as yf
from datetime import *

class ETF:
    def __init__(self, ticker, country, start_date, end_date):
        """
        Parameters
        ----------
        ticker : str
            ticker name
        start_date : str
            "DD/MM/YYYY"
        end_date : str
            "DD/MM/YYYY"
        """
        self.ticker = ticker 
        self.country = country
        self.start = start_date
        self.end = end_date
        
    def getdata(self):
        ########## need refinement here ##########
        df = investpy.get_stock_historical_data(stock = self.ticker, country = self.country, from_date = self.start, to_date = self.end)
        stocks[stock_symbol] = df
        closing[stock_symbol] = df['Close'] 
        return closing
        
    def GetDataFund(self):
        # df = investpy.get_fund_historical_data(fund='Vanguard 500 Index Fund Investor Shares', country='united states', from_date='01/01/2018', to_date='01/01/2019')
        stocks = {}
        df = investpy.get_fund_historical_data(fund=self.ticker, country=self.country, from_date =self.start, to_date=self.end)
        stocks[self.ticker] = df['Close']
        return stocks[self.ticker]
    
    def BollingerBand(self, window=21, no_of_std=2):
        stocks = self.GetDataFund() # so beautiful!
        
        # initiate a dataframe
        data = pd.DataFrame(stocks, columns = ['Close'])
        
        rolling_mean = data['Close'].rolling(window).mean()
        rolling_std = data['Close'].rolling(window).std()
        
        data['Rolling_Mean'] = rolling_mean
        data['Bollinger_Upper'] = data['Rolling_Mean'] + rolling_std * no_of_std
        data['Bolling_Lower'] = data['Rolling_Mean'] - rolling_std * no_of_std
        
        data.plot(color=['black','red','green','green'], title = self.ticker)
        return data
        

test = ETF('Vanguard 500 Index Fund Investor Shares', 'united states', '01/01/2018','01/01/2019')

test.BollingerBand()



data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = ['SPY', 'AAPL', 'MSFT'], # or "SPY AAPL MSFT"

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "5y",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1d",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = False,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )


stock_close = data.xs('Close', axis = 1, level = 1, drop_level = True)

def BollingerBand(stocks, window=21, no_of_std=2):
        
        # initiate a dataframe
        data = pd.DataFrame(stocks.values, columns = ['Close'])
        
        rolling_mean = data['Close'].rolling(window).mean()
        rolling_std = data['Close'].rolling(window).std()
        
        data['Rolling_Mean'] = rolling_mean
        data['Bollinger_Upper'] = data['Rolling_Mean'] + rolling_std * no_of_std
        data['Bolling_Lower'] = data['Rolling_Mean'] - rolling_std * no_of_std
        
        data.plot(color=['black','red','green','green'], title = 'BB')
        return data
    
tt = BollingerBand(stock_close['MSFT'])


# testing trading strat based on BB





    