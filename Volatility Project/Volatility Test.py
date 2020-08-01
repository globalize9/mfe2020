# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 10:47:41 2020
Volatility Testing
  CBOE S&P 500 Volatility Index (VIX)	
  CBOE S&P 100 Volatility Index (VXO)	
  CBOE NASDAQ Volatility Index (VXN)	
  CBOE DJIA Volatility Index (VXD)

@author: yushi
"""
import os # to set wd
import pandas as pd
import numpy as np
import matplotlib as plt
import datetime
from plotnine import *
from plotnine.data import mpg

ggplot(mpg) + aes(x='class', color = 'class') + geom_bar(size=8) + ggtitle("mpg")


start = datetime.datetime.now()

a = 32

duration = datetime.datetime.now() - start
print ("time elapsed is: {} good".format(str(duration)[5:13])) # subsets to only the seconds 

os.getcwd()
# os.chdir("Documents\GitHub\mfe2020\Volatility Project")
vol = pd.read_csv("Documents\GitHub\mfe2020\Volatility Project\lalaland.csv")
# vol.index = vol.date
sp500 = pd.read_csv("Documents\GitHub\mfe2020\Volatility Project\sp500vwretd.csv")
datetime.datetime.strptime("2013-1-25", '%Y-%m-%d').strftime('%m/%d/%y')
vix = vol['vix'].dropna()
vol.columns
# ggplot(vol) + aes(x = list(range(1,7535,1)), y = 'vix') + geom_line() 


"""
Individual stocks testing along with pandas and numpy
"""
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf, acf
from statsmodels.graphics.tsaplots import *
import investpy
from datetime import *

stock_symbols = ['BP', 'CVX']

from_date = '01/01/2002' ## dd/mm/yyyy
end_date = '14/07/2020'
end_date = datetime.strftime(datetime.date(datetime.today()), format = '%d/%m/%Y')

stocks = {}
closing = {}

for stock_symbol in stock_symbols:
    df = investpy.get_stock_historical_data(stock = stock_symbol, country = 'united states', from_date = '01/01/2015', to_date = '20/03/2020')
    stocks[stock_symbol] = df
    closing[stock_symbol] = df['Close']

df_close = pd.DataFrame(closing)
close_ret = df_close.pct_change()
close_ret.plot(kind = 'line')

df_close_lag1 = df_close.shift(1)
df_ret = (df_close - df_close_lag1)/df_close_lag1
df_ret = df_ret.dropna()
# we can see that this is same as using pct_change

# let's see what happens if we apply an AR(1) model to this
plot_acf(df_ret['CVX'])
plot_pacf(df_ret['CVX'])
acf(df_ret['CVX'])

wti = pd.DataFrame(investpy.get_commodity_historical_data(commodity = 'Crude Oil Wti', from_date = from_date, to_date = end_date))
ng = pd.DataFrame(investpy.get_commodity_historical_data(commodity = 'Natural Gas', from_date = from_date, to_date = end_date))

# summary statistics can be achieved with .describe
wti[wti.columns.difference(['Volume'])] # removes the volume column
wti_close = wti["Close"]
wti_ret = wti_close.pct_change()

ng_close = ng["Close"]
ng_ret = ng_close.pct_change()

joint_df = pd.concat([wti_ret, ng_ret], axis = 1, join = 'inner')
joint_df.columns = ["wti", "ng"]
joint_df['Dates'] = joint_df.index
ggplot(joint_df, aes(x = 'Dates', y = 'wti')) + geom_line(color = 'r', alpha = 0.5)
ggplot(joint_df, aes(x = 'Dates', y = 'ng')) + geom_line(color = 'g', alpha = 0.5)

print("Standard deviation of WTI return is %.5f and NG return is %.5f"%(np.std(wti_ret), np.std(ng_ret)))

# checking how this changes over time
start_dt = '2015-01-01'
end_dt = "2020-03-01"
# volatility of oil as of 3/23 is much higher than anything...strat: short vol???
joint_sub = joint_df[start_dt:end_dt]
del joint_sub['Dates']
joint_sub.plot(kind = "line", alpha = 0.4, color = ['r', 'k'])


all_indices = investpy.indices.get_indices()

vix = investpy.indices.get_index_historical_data(index='S&P 500 VIX', country='united states', from_date = from_date, to_date = end_date)

df_vix = investpy.get_index_recent_data(index='S&P 500 VIX', country='united states')
df_vix

from fbprophet import Prophet
from fbprophet.plot import plot_plotly

def prophet_model(vix):
    vix = vix['Close']
    vix = pd.DataFrame(vix)
    vix.columns = ['y']
    vix['ds'] = vix.index.to_pydatetime()
    # preping the data for analysis
    train_df = vix[:len(vix)-20]
    
    prophet_basic = Prophet()
    prophet_basic.fit(train_df)
    
    future = prophet_basic.make_future_dataframe(periods=100)
    future.tail(2)
    
    forecast = prophet_basic.predict(future)
    fig1 = prophet_basic.plot(forecast)
    fig1 = prophet_basic.plot_components(forecast)
    
    forecast['actual_y'] = np.NaN
    forecast.loc[:len(vix.index)-1,'actual_y'] = vix['y'].values
    forecast['MAPE'] = abs(forecast['actual_y'] - forecast['yhat']) / forecast['actual_y']
    print(forecast['MAPE'].plot(title='MAPE'))
    return forecast

vix_forecast = prophet_model(vix)

stock_df = investpy.get_stock_historical_data(stock = 'PSX', country = 'united states', from_date = from_date, to_date = end_date)
psx_forecast = prophet_model(stock_df)


# adding change points
from fbprophet.plot import add_changepoints_to_plot

fig = prophet_basic.plot(forecast)
a = add_changepoints_to_plot(fig.gca(), prophet_basic, forecast)

prophet_basic.changepoints

# change the inferred changepoint range by setting the changepoint_range
pro_change= Prophet(changepoint_range=0.9, changepoint_prior_scale=0.08)
forecast = pro_change.fit(train_vix).predict(future)
fig= pro_change.plot(forecast);
a = add_changepoints_to_plot(fig.gca(), pro_change, forecast)


