'''
KostisLab - KonAnast
http://
Python Script for Crypto data management
Version 0.1
02/2018
'''


import pandas as pd
import csv

# Open data files
in_mycoins = open(
    'mycoins', 'r')
mycoins = pd.read_csv(
    in_mycoins, sep='\t', encoding='utf-8')

in_coins_prices = open(
    '20180216', 'r')
coins_prices = pd.read_csv(
    in_coins_prices, sep='\t', encoding='utf-8')

#Summation of coins from diferent exchanges
mycoins = mycoins.groupby('Symbol')['Balance'].sum()

# Connection of data
#results = pd.merge(
    #mycoins, coins_prices, on='Symbol')

results = coins_prices.merge(
    mycoins.to_frame(), left_on='Symbol', right_index=True)


#Cleaning data
results['Price'].value_counts()
results['Market Cap'].value_counts()
results['Circulating Supply'].value_counts()
results['Price'] = results['Price'].str.replace('$', '')
results['Price'] = results['Price'].str.replace('?', '0')
results['Price'] = results['Price'].str.replace(',', '')
results['Market Cap'] = results['Market Cap'].str.replace('$', '')
results['Market Cap'] = results['Market Cap'].str.replace('?', '0')
results['Market Cap'] = results['Market Cap'].str.replace(',', '')
results['Circulating Supply'] = results['Circulating Supply'].str.replace('$', '')
results['Circulating Supply'] = results['Circulating Supply'].str.replace('?', '0')
results['Circulating Supply'] = results['Circulating Supply'].str.replace(',', '')

results['Price'] = results['Price'].astype(float)
results['Balance'] = results['Balance'].astype(float)

#Calculating Total
results['Total'] = results['Balance'] * results['Price']

results.columns = pd.Series(results.columns).str.replace('Name_y', 'Name')
columns = [
   'Name', 'Symbol', 'Price', 'Balance', 'Total', 'Market Cap']


#Count totals
SumUSD = results['Total'].sum()

#Print on screen
results = results[columns]
print(results)
print('\n')

print('!!!ALERT THESE ARE COINS WITH SAME SYMBOLS!!!')
ids = results[results.duplicated(['Symbol'], keep=False)]
print(ids)

print('\n')
print('Sum in $ = ', SumUSD, 'without removing the fees (0.1)') # noqa
print('Sum in $ = ', SumUSD * 0.9, 'net and conversion fees removed (*0.9)')
SumEU = SumUSD * 0.8
print('Sum in € = ', SumEU, '*0.8 (USD to EURO)')
print('Sum in € = ', SumEU * 0.9, 'net and conversion fees removed (*0.9)')
print('Sum in € = ', SumEU * 0.9 - 3100, 'profit (-3100 first investment)')


# Save data
export_data = open('export_data3.txt', 'w')
results.to_csv(
    export_data, encoding='utf-8',
    quoting=csv.QUOTE_NONE, sep='\t')

# Close files
in_mycoins.close()
in_coins_prices.close()
export_data.close()

