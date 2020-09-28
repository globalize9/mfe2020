# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 18:44:44 2020

@author: yushi
"""


# In[]

import socketio

sio = socketio.Client()

@sio.on('connect', namespace='/all-filings')
def on_connect():
    print("Connected to https://api.sec-api.io:3334/all-filings")

@sio.on('filing', namespace='/all-filings')
def on_filings(filing):
    print(filing)

sio.connect('https://api.sec-api.io:3334?apiKey=f7830ea3c6d031e359eff4502fd31584011cc3bc9c541948c7f173a8962bc79b', namespaces=['/all-filings'])
sio.wait()




# In[]

import edgar
#install Python Edgar library
import pandas as pd

edgar.download_index('/Users/jos/Desktop/Desktop/Desktop', 2018,skip_all_present_except_last=False)

selectedcompany = 'Facebook'
selectedreport = '10-Q'

csv = pd.read_csv('2019-QTR4.tsv', sep='\t',  lineterminator='\n', names=None) 

csv.columns.values[0] = 'Item'

companyreport = csv[(csv['Item'].str.contains(selectedcompany)) & (csv['Item'].str.contains(selectedreport))]

Filing = companyreport['Item'].str.split('|')
Filing = Filing.to_list()

for item in Filing[0]:
    
    if 'html' in item:
        report = item
        
url = 'https://www.sec.gov/Archives/' + report
#https://www.sec.gov/ix?doc=/Archives/edgar/data/1652044/000165204419000032/goog10-qq32019.htm

df = pd.read_html(url)
document_index = df[0]
document_index = document_index.dropna()

document_name = document_index[document_index['Description'].str.contains(selectedreport)]
document_name = document_name['Document'].str.split(' ')
document_name = document_name[0][0]

report_formatted = report.replace('-','').replace('index.html','')
url = 'https://www.sec.gov/Archives/' + report_formatted + '/' + document_name


df = pd.read_html(url)

for item in df:
    BS = (item[0].str.contains('Retained') | item[0].str.contains('Total Assets'))
    if BS.any():
        Balance_Sheet = item
        

Balance_Sheet = Balance_Sheet.iloc[2:,[0,2,6]]

header = Balance_Sheet.iloc[0]
Balance_Sheet = Balance_Sheet[1:]

Balance_Sheet.columns = header


Balance_Sheet.columns.values[0] = 'Item'
Balance_Sheet = Balance_Sheet[Balance_Sheet['Item'].notna()]

Balance_Sheet[Balance_Sheet.columns[1:]] = Balance_Sheet[Balance_Sheet.columns[1:]].astype(str)
Balance_Sheet[Balance_Sheet.columns[1]] = Balance_Sheet[Balance_Sheet.columns[1]].map(lambda x: x.replace('(','-'))
Balance_Sheet[Balance_Sheet.columns[2]] = Balance_Sheet[Balance_Sheet.columns[2]].map(lambda x: x.replace('(','-'))

Balance_Sheet[Balance_Sheet.columns[1]] = Balance_Sheet[Balance_Sheet.columns[1]].map(lambda x: x.replace(',',''))
Balance_Sheet[Balance_Sheet.columns[2]] = Balance_Sheet[Balance_Sheet.columns[2]].map(lambda x: x.replace(',',''))

Balance_Sheet[Balance_Sheet.columns[1]] = Balance_Sheet[Balance_Sheet.columns[1]].map(lambda x: x.replace('—','0'))
Balance_Sheet[Balance_Sheet.columns[2]] = Balance_Sheet[Balance_Sheet.columns[2]].map(lambda x: x.replace('—','0'))



Balance_Sheet[Balance_Sheet.columns[1:]] = Balance_Sheet[Balance_Sheet.columns[1:]].astype(float)

Balance_Sheet





# In[]
# https://pypi.org/project/sec-edgar-downloader/

from sec_edgar_downloader import Downloader

# Initialize a downloader instance.
# If no argument is passed to the constructor, the package
# will attempt to locate the user's downloads folder.
dl = Downloader("C:/Users/yushi/Documents/edgar_filings")

# Note: before_date and after_date strings must be in the form "YYYYMMDD"
dl.get("10-K", "0000102909", include_amends = True, after_date="20170101", before_date="20180325")
dl.get("DEF 14A", "882796", include_amends = True, after_date="20140630", before_date="20150630")


# In[]
import re

import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.sec.gov/Archives/edgar/data/36405/000093247115006447/indexfunds_final.htm")
soup = BeautifulSoup(response.content)

futures = soup.find_all(text=re.compile('C. Futures Contract'))
for future in futures:
    for row in future.find_next("table").find_all("tr"):
        print [cell.get_text(strip=True) for cell in row.find_all("td")]





# In[]



# Get all 8-K filings for Apple (ticker: AAPL)
dl.get("8-K", "AAPL")

# Get all 8-K filings for Apple, including filing amends (8-K/A)
dl.get("8-K", "AAPL", include_amends=True)

# Get all 8-K filings for Apple after January 1, 2017 and before March 25, 2017
# Note: before_date and after_date strings must be in the form "YYYYMMDD"
dl.get("10-K", "0000102909", include_amends = True, after_date="20170101", before_date="20180325")

# Get the five most recent 8-K filings for Apple
dl.get("8-K", "AAPL", 5)

# Get all 10-K filings for Microsoft (ticker: MSFT)
dl.get("10-K", "MSFT")

# Get the latest 10-K filing for Microsoft
dl.get("10-K", "MSFT", 1)

# Get the latest 10KSB filing for Ubiquitech Software
dl.get("10KSB", "0001411460", 1)

# Get all 10-Q filings for Visa (ticker: V)
dl.get("10-Q", "V")

# Get all 13F-NT filings for the Vanguard Group (CIK: 0000102909)
dl.get("13F-NT", "0000102909")

# Get all 13F-HR filings for the Vanguard Group
dl.get("13F-HR", "0000102909")

# Get all SC 13G filings for Apple
dl.get("SC 13G", "AAPL")

# Get all SD filings for Apple
dl.get("SD", "AAPL")

# Get the latest supported filings, if available, for Apple
for filing_type in dl.supported_filings:
    dl.get(filing_type, "AAPL", 1)

# Get the latest supported filings, if available, for a
# specified list of tickers and CIKs
symbols = ["AAPL", "MSFT", "0000102909", "V", "FB"]
for s in symbols:
    for filing_type in dl.supported_filings:
        dl.get(filing_type, s, 1)










