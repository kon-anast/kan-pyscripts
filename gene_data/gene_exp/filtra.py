import pandas as pd
import numpy as np
import csv
import os
#Open data
in_data = open('gene_exp.diff', 'r')
df = pd.read_csv(in_data, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE)

#Replace characters with tabs
df['locus'] = df['locus'].str.replace(':','\t')
df['locus'] = df['locus'].str.replace('-','\t')

#Split column "locus"
locus = df['locus'].apply(lambda x: x.split('\t'))
df['chr'] = locus.apply(lambda x: x[0])
df['start'] = locus.apply(lambda x: x[1])
df['end'] = locus.apply(lambda x: x[2])

#Replace "locus" title
df.columns = pd.Series(df.columns).str.replace('locus', 'chr\tstart\tend')
#Define data type
cols = ['start', 'end']
df[cols] = df[cols].applymap(np.int64)

##Filters##
df = df[df['status'].str.contains("OK")]    #Select from status teh rows that contain OK
df = df[df['gene'].str.contains("MYH") == False]    #Exloud rows from column "gene"
df = df[(df['value_1'] > 2) & (df['value_2'] > 2)]
df = df[df['end'] - df['start'] > 500]

#Delete the extra columns
df.drop(df.columns[[-1, -2, -3]], axis=1, inplace=True)


dfsum = len(df.index)
print(df)


full_path = os.getcwd()
path, filename = os.path.split(full_path)

print("\n" + "Full path: " + full_path + "\n")
print("Exported data file name: " + filename + "_new.diff" + "\n")

out_data = open(filename + '_new.diff', 'w')
df.to_csv(out_data, sep='\t', encoding='utf-8', escapechar=' ', quoting=csv.QUOTE_NONE, index = False)
in_data.close()
out_data.close()
