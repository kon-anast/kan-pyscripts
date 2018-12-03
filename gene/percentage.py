#Calculate the percentage per columns

import pandas as pd
import numpy as np
import csv
#import matplotlib.pyplot as plt

#Fortosi dedomenon
in_data = open('data2.txt', 'r')
df = pd.read_csv(in_data, encoding='utf-8', quoting=csv.QUOTE_NONE, header = None)

#Aferesi ton gramon pou ksekinanen me '>' p.x.: >chr12:65775568-65775768(+)
df = (df[~df[0].astype(str).str.contains(r'[>]', na=False)])
#Aferesi ton xaraktiron meta apo keno kai parenthesi ' (' p.x.: (-29.70)
df[0] = df[0].apply(lambda x: x.split(' (')[0])


#replace (.*) with(1*) >40
df_ones = df[0].str.replace('\(.\)','(1)')
df_ones[0] = df_ones.str.replace('\(.\.\)','(11)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\)','(111)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\.\)','(1111)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\.\.\)','(11111)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\.\.\.\)','(111111)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\.\.\.\.\)','(1111111)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\.\.\.\.\.\)','(11111111)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\.\.\.\.\.\.\)','(111111111)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\.\.\.\.\.\.\.\)','(1111111111)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\.\.\.\.\.\.\.\.\)','(11111111111)')
df_ones[0] = df_ones[0].str.replace('\(\.\.\.\.\.\.\.\.\.\.\.\.\)','(111111111111)')
df_ones = df_ones[0].astype(str).apply(lambda x: pd.Series(list(x))).astype(str)


#Diaxorismos kathe xaraktira se diaforetiki stili
df = df[0].astype(str).apply(lambda x: pd.Series(list(x))).astype(str)

#Filtrarisma tou pinaka me vasi ti proti stili [0] gia to an exi telies kai paranthesis h gramata
df_acgu = (df[~df[0].astype(str).str.contains(r'[.()]', na=False)])
df_dots = (df[~df[0].astype(str).str.contains(r'[ACGUacgu]', na=False)])
df_ones = (df_ones[~df_ones[0].astype(str).str.contains(r'[ACGUacgu]', na=False)])

#Ypologismos tou synolou ton gramon
dfsum = len(df.index)
dfsum_acgu = len(df_acgu.index)
dfsum_dots = len(df_dots.index)
dfsum_ones = len(df_ones.index)

#Ypologismos tou arithmoy emfanisis tou kathe xaraktira
dfcount = df.apply(pd.value_counts)
#Ypologismos posostou
dfper_all = df.apply(pd.value_counts) * (100/dfsum)
dfper_acgu = df_acgu.apply(pd.value_counts) * (100/dfsum_acgu)
dfper_dots = df_dots.apply(pd.value_counts) * (100/dfsum_dots)
dfper_ones = df_ones.apply(pd.value_counts) * (100/dfsum_ones)


#eksagogi dedomenon

#Apothikeysi tou arithmoy emfanisis tou kathe xaraktira
out_data_count = open('data_count.txt', 'w')
dfcount.to_csv(out_data_count, sep='\t', encoding='utf-8', escapechar=' ', quoting=csv.QUOTE_NONE)
#Gia paralipsi ton titlon stis grames kai tis stiles bazeis meta to quoting=csv.QUOTE_NONE ta akoloutha: , index=False, index_label=False, header=False

#Apothikeysi tou posostou gia oles tis grames
out_data_all = open('percentage_all.txt', 'w')
dfper_all.to_csv(out_data_all, sep='\t', encoding='utf-8', escapechar=' ', quoting=csv.QUOTE_NONE)

#Apothikeysi tou posostou gia tis grames me gramata
out_data_acgu = open('percentage_acgu.txt', 'w')
dfper_acgu.to_csv(out_data_acgu, sep='\t', encoding='utf-8', escapechar=' ', quoting=csv.QUOTE_NONE)

#Apothikeysi tou posostou gia tis grames me telies kai parenthesis
out_data_dots = open('percentage_dots.txt', 'w')
dfper_dots.to_csv(out_data_dots, sep='\t', encoding='utf-8', escapechar=' ', quoting=csv.QUOTE_NONE)

#Apothikeysi tou posostou gia to 1
out_data_ones = open('percentage_ones.txt', 'w')
dfper_ones.to_csv(out_data_ones, sep='\t', encoding='utf-8', escapechar=' ', quoting=csv.QUOTE_NONE)

print("DataFrame")
print(df)
print("Count DataFrame")
print(dfcount)
print("All Data Pecentage")
print(dfper_all)
print("Sum All")
print(dfsum)
print("acgu Percentage")
print(dfper_acgu)
print("Sum acgu")
print(dfsum_acgu)
print("dots Percentage")
print(dfper_dots)
print("Sum dots")
print(dfsum_dots)
print("ones Percentage")
print(dfper_ones)
print("Sum ones")
print(dfsum_ones)

#>>Gial ti dimiourgia plot
#dfcount[0] = float(dfcount[0])
#dfcount  = dfcount.astype(float)
#plt.plot(dfcount.index, dfcount[0])

in_data.close()
out_data_count.close()
out_data_all.close()
out_data_acgu.close()
out_data_dots.close()
