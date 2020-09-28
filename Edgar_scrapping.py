# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 18:44:44 2020

@author: yushi
"""

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