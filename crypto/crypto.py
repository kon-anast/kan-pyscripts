'''
KostisLab - KonAnast
http://
Python Script for Crypto data management
Version 0.2
04/2018
'''


import pandas as pd
import csv
import tkinter.filedialog
import os
from os.path import basename


# Open data files
filepathname = tkinter.filedialog.askopenfilename()

in_mycoins = open(
    'mycoins', 'r')
mycoins = pd.read_csv(
    in_mycoins, sep='\t', encoding='utf-8')

in_coins_prices = open(
    filepathname, 'r')
coins_prices = pd.read_csv(
    in_coins_prices, sep='\t', encoding='utf-8')

#Summation of same coins from diferent exchanges
mycoins = mycoins.groupby('Symbol')['Balance'].sum()

# Connection of data
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
print(results)
results.columns = pd.Series(results.columns).str.replace('Name_y', 'Name')

columns = [
   'Name', 'Symbol', 'Price', 'Balance', 'Total', 'Market Cap']

results = results[columns]

#Remuve coins
print('!!!ALERT THESE ARE COINS WITH SAME SYMBOLS!!!')
duplicated = results[results.duplicated(['Symbol'], keep=False)]
print(duplicated)

print('These coins are remuved: KingN Coin, BlockCAT, BatCoin, Catcoin')
results = results[results.Name != 'KingN Coin']
results = results[results.Name != 'BlockCAT']
results = results[results.Name != 'BatCoin']
results = results[results.Name != 'Catcoin']

duplicated = results[results.duplicated(['Symbol'], keep=False)]
print(duplicated)
print('Test!: if Index: [] is emty it is OK, \n')

#Print on screen
print(results)
print('\n')

#Count totals
SumUSD = results['Total'].sum()
SumEU = SumUSD * 0.8

#net and conversion fees removed (*0.9)
SumUSDfe = SumUSD * 0.9
SumEUfe = SumEU * 0.9

firstIn = 3100
profit = SumEUfe - firstIn

print('Sum in $ = ', "%.2f" % SumUSD, 'without removing the fees (0.1)') # noqa
print('Sum in $ = ', "%.2f" % SumUSDfe, 'net and conversion fees removed (*0.9)')
print('Sum in € = ', "%.2f" % SumEU, '*0.8 (USD to EURO) without removing the fees (0.1)')
print('Sum in € = ', "%.2f" % SumEUfe, 'net and conversion fees removed (*0.9)')
print('Sum in € = ', "%.2f" % profit, 'profit - ', firstIn, 'first investment)')


# Save data
filepath = os.path.splitext(filepathname)[0]

export_data = open(filepath + '_profits', 'w')
results.to_csv(
    export_data, encoding='utf-8',
    quoting=csv.QUOTE_NONE, sep='\t')
export_data.close()

with open(filepath + '_profits', "a") as myfile:
    myfile.write(
        '\nSum in $ = ' + str("%.2f" % SumUSD) + ' without removing the fees (0.1)'
        '\nSum in $ = ' + str("%.2f" % SumUSDfe) + ' net and conversion fees removed (*0.9)'
        '\nSum in € = ' + str("%.2f" % SumEU) + ' *0.8 (USD to EURO)'
        '\nSum in € = ' + str("%.2f" % SumEUfe) + ' net and conversion fees removed (*0.9)'
        '\nSum in € = ' + str("%.2f" % profit) + ' profit - ' +  str(firstIn) + ' first investment'
        )


# Close files
myfile.close()
in_mycoins.close()
in_coins_prices.close()


