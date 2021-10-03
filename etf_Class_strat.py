#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 15:17:57 2021

"""
import pandas as pd
import numpy as np
import investpy
import yfinance as yf
from datetime import *
import matplotlib.pyplot as plt

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
        

test = ETF('Vanguard 500 Index Fund Investor Shares', 'united states', '01/01/2020','01/01/2021')

test.BollingerBand()



data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = ['SPY', 'AAPL', 'MSFT'], # or "SPY AAPL MSFT"

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "10y",

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

def BollingerBand(stocks, window=21, no_of_std=2, start_date = date(2017,1,1), end_date = date(2020,12,31)):
        
        # initiate a dataframe
        data = pd.DataFrame(stocks.values, index = stocks.index, columns = ['Close'])
        
        rolling_mean = data['Close'].rolling(window).mean()
        rolling_std = data['Close'].rolling(window).std()
        
        data['Rolling_Mean'] = rolling_mean
        data['Bollinger_Upper'] = data['Rolling_Mean'] + rolling_std * no_of_std
        data['Bollinger_Lower'] = data['Rolling_Mean'] - rolling_std * no_of_std
        
        data.plot(color=['black','red','green','green'], title = 'BB', xlim = [start_date, end_date])
        return data
    
tt = BollingerBand(stock_close['MSFT'])


# testing trading strat based on BB
df = tt.copy()

#Create an "empty" column as placeholder for our /position signals
df['Position'] = None

#Fill our newly created position column - set to sell (-1) when the price hits the upper band, and set to buy (1) when it hits the lower band
for row in range(len(df)):
    if (df['Close'].iloc[row] > df['Bollinger_Upper'].iloc[row]) and (df['Close'].iloc[row-1] < df['Bollinger_Upper'].iloc[row-1]):
        df['Position'].iloc[row] = -1
        
    if (df['Close'].iloc[row] < df['Bollinger_Lower'].iloc[row]) and (df['Close'].iloc[row-1] > df['Bollinger_Lower'].iloc[row-1]):
        df['Position'].iloc[row] = 1 


    # think about how to close a long position
    # if df['Position'].iloc[row] == 1:
    if (df['Close'].iloc[row] < df['Rolling_Mean'].iloc[row]) and (df['Close'].iloc[row-1] > df['Rolling_Mean'].iloc[row-1]):
        df.loc[df.index[row],'Position'] = 0
    
    # how to close a short position
    # if df['Position'].iloc[row] == -1:
    if (df['Close'].iloc[row] > df['Rolling_Mean'].iloc[row]) and (df['Close'].iloc[row-1] < df['Rolling_Mean'].iloc[row-1]):
        df.loc[df.index[row],'Position'] = 0

# the last 2 criterias essentially says that do NOT trade under certain conditions

             

# Naive case where position switches between the two extremes
#Fill our newly created position column - set to sell (-1) when the price hits the upper band, and set to buy (1) when it hits the lower band
for row in range(len(df)):
    if (df['Close'].iloc[row] > df['Bollinger_Upper'].iloc[row]) and (df['Close'].iloc[row-1] < df['Bollinger_Upper'].iloc[row-1]):
        df['Position'].iloc[row] = -1
        
    if (df['Close'].iloc[row] < df['Bollinger_Lower'].iloc[row]) and (df['Close'].iloc[row-1] > df['Bollinger_Lower'].iloc[row-1]):
        df['Position'].iloc[row] = 1 



#Forward fill our position column to replace the "None" values with the correct long/short positions to represent the "holding" of our position
#forward through time
df['Position'].fillna(method='ffill',inplace=True)

#Calculate the daily market return and multiply that by the position to determine strategy returns
df['Market Return'] = df['Close'] / df['Close'].shift(1) 
df['Strategy Return'] = df['Market Return'] * df['Position'].shift(1)

#Plot the strategy returns
plt.figure()
# this ignores the zero return for strategy return when there isn't a position
df['Strategy Return'][df['Strategy Return']>0].cumprod().plot(title = 'Cumulative Return').legend()
df['Market Return'].cumprod().plot(color = 'blue').legend()





# In[]: let's try the dollar cost average basis
# do NOT use log returns here, as log return is time additive, i.e. log return from t -> t + 1 and t + 1 -> t + 2 is the same as
# t -> t + 2, but once portfolio weights are introduced, this statement no longer holds
# DCA investment hits the return on the day it is invested using prior day's closing price
# but your return is calculated using the closing price of today

ds = tt.copy()
ds['Daily_Return'] = ds['Close'].pct_change()
ds['DCA_Position'] = 0


def IsFirstWed(data):
    # 0 is Monday, 4 is Friday
    date_form = datetime.strptime(str(data).split(" ")[0], "%Y-%m-%d")

    return date_form.weekday() == 2 and 2 <= date_form.day <= 8 

# assign DCA average allocation 
dca_allocation_amt = 1000
init_allocation_amt = dca_allocation_amt

ds['FirstWed'] = list(map(lambda x: IsFirstWed(x), ds.index))

rebal_dates = ds.index[ds['FirstWed'] == True]
ds.loc[rebal_dates, 'DCA_Add_On'] = dca_allocation_amt
ds['DCA_Add_On'] = ds['DCA_Add_On'].fillna(0)

#Calculate the daily market return and multiply that by the position to determine strategy returns

ds['Market Return'] = np.NaN
ds['DCA_Ret'] = np.NaN

#Adjust the returns so that it omits the data before the first Add_On date
start_date = ds.index[np.where(ds['FirstWed'] == True)[0][0]]
start_index = np.where(ds.index == start_date)[0][0] + 1
# ds.iloc[:np.where(ds.index == start_date)[0][0], -2:] = np.NaN
ds.loc[ds.index[start_index - 1],'DCA_Position'] = init_allocation_amt

# assuming the Add_On investment kicks in the same day (adds to the index at today's close)
for i in range(start_index,len(ds)):
    ds.loc[ds.index[i],'DCA_Position'] = ds.loc[ds.index[i-1],'DCA_Position'] * (1+ds.loc[ds.index[i],'Daily_Return']) 
    ds.loc[ds.index[i],'DCA_Ret'] = np.log(ds.loc[ds.index[i], 'DCA_Position'] / ds.loc[ds.index[i-1], 'DCA_Position'])
    ds.loc[ds.index[i],'Market Return'] = np.log(ds.loc[ds.index[i],'Close'] / ds.loc[ds.index[i-1],'Close'] )
    # if date is rebal_date, account for the extra DCA allocation 
    if ds.index[i] in rebal_dates:
        # ds.loc[ds.index[i],'DCA_Ret'] = np.log((ds.loc[ds.index[i], 'DCA_Position'] - dca_allocation_amt) / ds.loc[ds.index[i-1], 'DCA_Position'])
        ds.loc[ds.index[i],'DCA_Position'] += ds.loc[ds.index[i],'DCA_Add_On']

# ds.loc[ds.index[start_index], 'DCA_Ret'] = ds.loc[ds.index[start_index], 'Market Return']

ds['DCA_cum_ret'] = ds['DCA_Ret'].cumsum()
ds['Mkt_cum_ret'] = ds['Market Return'].cumsum()


# it makes more sense to specify dates in the initial data cut, as the cum return would not be accurate otherwise
end_date = date(2020,12,31)

ds_trunc = ds[:end_date].copy()
total_invested = ds_trunc.DCA_Add_On.sum()
ds_trunc['Mkt_Position'] = np.NaN
# assume 3% simple interest rate
pv_total = total_invested / np.power((1+0.03), ((ds_trunc.index[-1] - ds_trunc.index[0]).days/float(365.25)))
ds_trunc.loc[ds_trunc.index[start_index - 1],'Mkt_Position'] = pv_total
# let's calculate the market position over this time span vs DCA
for i in range(start_index, len(ds_trunc)):
    ds_trunc.loc[ds_trunc.index[i],'Mkt_Position'] = ds_trunc.loc[ds_trunc.index[i-1],'Mkt_Position'] * (1+ds_trunc.loc[ds_trunc.index[i],'Daily_Return']) 

#Plot the strategy returns
plt.figure()
ds.loc[:end_date,'DCA_cum_ret'].plot(title = 'Cumulative Return', alpha = 0.8).legend()
ds.loc[:end_date,'Mkt_cum_ret'].plot(color = 'black', alpha = 0.8).legend()
# ds.to_excel('DCA_test.xlsx')


    