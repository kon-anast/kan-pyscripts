 
import pandas as pd
import numpy as np
import csv
import os
from io import StringIO
from pandas import ExcelWriter
import tkinter.filedialog
from os.path import basename


filepathname = tkinter.filedialog.askopenfilename()


#Open data
in_data = open(filepathname, 'r')
df = pd.read_csv(in_data, sep=',', encoding='utf-8', quoting=csv.QUOTE_NONE, 
                  names = ['ID', 'X', 'Y', 'Z'])

FileName = df.loc[0, 'ID']
print(FileName)

#Remuve 7000000 from x
df['X'] = df['X']-7000000
#print(df[1])

decimals = pd.Series([0, 3, 3, 3], index=['ID', 'X', 'Y', 'Z'])
df = df.round(decimals)

#Filters
dfBases = df[df['ID'].str.contains('^[^0-9]')]
dfPoints = df[df['ID'].str.contains('^[^a-zA-Z]')]


print(df)


#Diferences
#PointDiff = df.loc[1, 'X']
#print(PointDiff)


#mean




## Create a list to store the data
#Diff = []

## For each row in the column,
#for row in dfPoints['X']:
    ## if more than a value,
    #if row > (PointDiff + 5):
        ## Append a letter grade
        #Diff.append('A')
    ## else, if more than a value,
    #elif row > (PointDiff - 5):
        ## Append a letter grade
        #Diff.append('A')
    ## otherwise,
    #else:
        ## Append a failing grade
        #Diff.append('Failed')
        
## Create a column from the list
#dfPoints['Diff'] = Diff

#print(dfPoints['Diff'])


# Save data
#export_bases = open(FileName + '.~ST', 'w')
#dfBases.to_csv(
    #export_bases, encoding='utf-8',
    #quoting=csv.QUOTE_NONE, sep='\t')

filepath = os.path.splitext(filepathname)[0]
	
#filepath = os.path.dirname(filepathname)
	
export_points = open(filepath + '.~TO', 'w')
dfPoints.to_csv(
    export_points, encoding='utf-8',
    quoting=csv.QUOTE_NONE, sep=',', index = None, header= None)


writer = pd.ExcelWriter(filepath + '.xlsx', engine='xlsxwriter')
dfBases.to_excel(writer, sheet_name='Bases')

writer.save()

# Close files
in_data.close()
#export_bases.close()
export_points.close()

