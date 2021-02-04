#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 15:17:57 2021

@author: minayuan
"""
import pandas as pd
import numpy as np
import investpy
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



    
        


    