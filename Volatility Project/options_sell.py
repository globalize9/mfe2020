import pandas as pd
import numpy as np
import scipy.stats as si
from datetime import datetime, date
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

def intrinsic(optiondf, underlyingdf, option_type):
    # todaystock = underlyingdf.loc[date.today().strftime('%Y-%m-%d'),'Close']
    todaystock = underlyingdf.iloc[-1]['Close'] # grab the most recent closing price
    if option_type == 'call':
        optiondf['intrinsic'] = [max(todaystock - strikeprice,0) for strikeprice in optiondf['strike']]
    else:
        optiondf['intrinsic'] = [max(strikeprice - todaystock,0) for strikeprice in optiondf['strike']]
    optiondf['mid'] = (optiondf['bid'] + optiondf['ask'])/2
    optiondf['timevalue'] = np.maximum(optiondf['mid'] - optiondf['intrinsic'],0)
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
    if option_type == 'call': return(si.norm.cdf(d2))
    else: return(si.norm.cdf(-d2))

def ImpliedMove(S0, calldf, putdf):
    put_idx = np.abs(putdf['strike'] - S0).argmin() # find nearest strike
    call_idx = np.abs(S0 - calldf['strike']).argmin()
    return round(putdf.loc[put_idx, 'mid'] + calldf.loc[call_idx, 'mid'],2)


# still need to think about how to define the Expected Payout
def ExpPayout(S0, df, option_type):
    return df['timevalue'] * (1-df['ProbITM'])
    # if option_type == 'call':
    #     if S0 > df['strike']:
    #         return df['mid']
    #     else:            
    #         return (df['strike'] - S0) * df['ProbITM']


def CleanDF(df, stockdf, time_to_expiry, opt_type, bs_filter = True): 
    todaystock = round(stockdf.iloc[-1]['Close'],2) # take the px_last of the underlying
    bs_filter_cutoff = 0.5 # if BS estimate is off by 0.5, drop the contracts
    temp_df = df.copy()
    # converting to datetime format
    temp_df['lastTradeDate'] = pd.to_datetime(temp_df['lastTradeDate']).dt.date
    
    # filter to drop trades that are more than 2 days old
    # temp_df = temp_df[temp_df['lastTradeDate'] > stockdf.index[-2].date()].reset_index(drop=True)
    

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

if __name__ == "__main__":
    
    ## inputs
    ticker = input('Enter a ticker: ')
    
    # obtains the available options expiry dates for a particular underlying
    stock = yf.Ticker(ticker)
    exp_dates = stock.options 
    opt_exp_date = exp_dates[0] # temp use of the first exp date
    
    implied_move_df = pd.DataFrame(None, index = exp_dates, columns = ['Implied_Move'])
    
    calldf, putdf, stockdf = getdata(ticker,opt_exp_date, save = False)
    initial_price = round(stockdf.iloc[-1]['Close'],2) # obtain the relevant strikes around this value
    strike_mid = 1 * round(initial_price/1)
    strike_width = 5
    strike_col = range((strike_mid - strike_width)*10, (strike_mid + strike_width)*10, 5)
    strike_col = [x/10 for x in strike_col]
    
    puts_df = pd.DataFrame(None, index = exp_dates, columns = strike_col)
    puts_tv_df = pd.DataFrame(None, index = exp_dates, columns = strike_col)
    
    
    for opt_exp_date in exp_dates:
        print(opt_exp_date)
        calldf, putdf, stockdf = getdata(ticker,opt_exp_date, save = False)
        
        # focusing on put df for now, works equally for call
        # assuming sell short call or put
        putdf = intrinsic(putdf, stockdf, 'put')
        calldf = intrinsic(calldf, stockdf, 'call')
        todaystock = round(stockdf.iloc[-1]['Close'],2)
        time_to_expiry = np.busday_count(date.today(), datetime.strptime(opt_exp_date,'%Y-%m-%d').date())
        cleaned_df = CleanDF(putdf, stockdf, time_to_expiry, 'put')
        
        cleaned_df['ProbITM'] = None
        # cleaned_df['Exp_Payout'] = None # assuming no price movement until maturity (very unlikely)
        
        for i in range(len(cleaned_df)):
            temp_line = cleaned_df.iloc[i,:]
            cleaned_df.loc[i,'ProbITM'] = ProbITM(todaystock, 0, temp_line['impliedVolatility'], time_to_expiry/252, temp_line['strike'], 'put')
            if temp_line['strike'] in strike_col:
                puts_df.loc[opt_exp_date, temp_line['strike']] = cleaned_df.loc[i,'ProbITM']
                puts_tv_df.loc[opt_exp_date, temp_line['strike']] = cleaned_df.loc[i,'timevalue']
                
        implied_move_df.loc[opt_exp_date, 'Implied_Move'] = ImpliedMove(todaystock, calldf, putdf)
    
    implied_move_df['Percentage'] = implied_move_df['Implied_Move'] / initial_price
    implied_move_df['Lower'] = initial_price - implied_move_df['Implied_Move']
    implied_move_df['Upper'] = initial_price + implied_move_df['Implied_Move']

    print('{} options implied moves generated'.format(ticker))
    
    with pd.ExcelWriter('{}_{}22.xlsx'.format(ticker,date.today().strftime('%Y-%m-%d'))) as writer:
        puts_df.to_excel(writer, sheet_name = 'ProbITM')
        puts_tv_df.to_excel(writer, sheet_name = 'TimeValue')
        implied_move_df.to_excel(writer, sheet_name = 'ImpliedMove')
        
    
    
