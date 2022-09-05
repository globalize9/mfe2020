import pandas as pd
import numpy as np
import scipy.stats as si
from datetime import datetime, timedelta, date
import yfinance as yf

def getdata(ticker, expiry, save = False, savepath = '/Users/minayuan/Documents/data science project/option trading/data/'):
    stock = yf.Ticker(ticker)
    call_chain = stock.option_chain(date=expiry).calls
    put_chain = stock.option_chain(date=expiry).puts
    stock_chain = stock.history(period="max")
    if save:
        call_chain.to_csv(savepath + '{}_call_{}_{}'.format(ticker,expiry,date.today()))
        put_chain.to_csv(savepath + '{}_put_{}_{}'.format(ticker,expiry,date.today()))
        stock_chain.to_csv(savepath + '{}_history_{}'.format(ticker,date.today()))
    return([call_chain,put_chain,stock_chain])

def intrinsic (optiondf, underlyingdf, call = True):
    # todaystock = underlyingdf.loc[date.today().strftime('%Y-%m-%d'),'Close']
    todaystock = underlyingdf.iloc[-1]['Close'] # grab the most recent closing price
    if call:
        optiondf['intrinsic'] = [max(todaystock - strikeprice,0) for strikeprice in optiondf['strike']]
    else:
        optiondf['intrinsic'] = [max(strikeprice - todaystock,0) for strikeprice in optiondf['strike']]
    optiondf['mid'] = (optiondf['bid'] + optiondf['ask'])/2
    optiondf['timevalue'] = optiondf['mid'] - optiondf['intrinsic']
    return(optiondf)

def BSMOptions(S0, r, sigma, T, X, option_type = 'call'):
    d1 = (np.log(S0 / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S0 / X) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        option_price = (S0 * si.norm.cdf(d1) - X * np.exp(-r * T) * si.norm.cdf(d2))
    if option_type == 'put':
        option_price = -S0 * si.norm.cdf(-d1) + X * np.exp(-r * T) * si.norm.cdf(-d2)
    if option_type != 'call' and option_type != 'put':
        option_price = 'invalid selection'
    return(option_price)

def ProbITM(S0, r, sigma, T, X, option_type = 'call'):
    d2 = (np.log(S0 / X) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return(si.norm.cdf(d2))
    

def CleanDF(df, stockdf, time_to_expiry, opt_type, bs_filter = True): 
    todaystock = round(stockdf.iloc[-1]['Close'],2) # take the px_last of the underlying
    bs_filter_cutoff = 0.5 # if BS estimate is off by 0.5, drop the contracts
    temp_df = df.copy()
    # converting to datetime format
    temp_df['lastTradeDate'] = pd.to_datetime(temp_df['lastTradeDate']).dt.date
    
    # filter for trades that are more than 2 days old
    temp_df = temp_df[temp_df['lastTradeDate'] > stockdf.index[-2].date()].reset_index(drop=True)
    

    # check listed IV against BS calculated option price
    # no need to calc IV again, its already calculated with BS using MID price
    temp_df['Calc_OptP'] = None
    for i in range(len(temp_df)):
        temp_line = temp_df.iloc[i,:]
        temp_df.loc[i,'Calc_OptP'] = BSMOptions(todaystock, 0, temp_line['impliedVolatility'], time_to_expiry/252, temp_line['strike'], opt_type) 
    temp_df['Diff'] = abs(temp_df['Calc_OptP'] - temp_df['mid'])
    
    if bs_filter:
        temp_df = temp_df[temp_df['Diff'] < bs_filter_cutoff].reset_index(drop=True)

    return temp_df

## inputs
ticker = 'KWEB'
opt_exp_date = '2022-09-16' # typically the third Friday of every month



calldf, putdf, stockdf = getdata(ticker,opt_exp_date, save = False)

# focusing on put df for now, works equally for call
putdf = intrinsic(putdf, stockdf, call = True)
todaystock = round(stockdf.iloc[-1]['Close'],2)
time_to_expiry = np.busday_count(date.today(), datetime.strptime(opt_exp_date,'%Y-%m-%d').date())
cleaned_df = CleanDF(putdf, stockdf, time_to_expiry, 'put')ß


cleaned_df['ProbITM'] = None
for i in range(len(cleaned_df)):
    temp_line = temp_df.iloc[i,:]
    (todaystock, 0, temp_line['impliedVolatility'], time_to_expiry/252, temp_line['strike'], 'call')




print(intrinsic(calldf,stockdf,call = True).head())
temp = intrinsic(calldf, stockdf, call=True)
