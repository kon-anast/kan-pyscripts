import pandas as pd
import numpy as np
import csv
from pandas import ExcelWriter
import os
import tkinter.filedialog
from os.path import basename
import openpyxl
from tkinter import messagebox

# hide main window
root = tkinter.Tk()
root.withdraw()
 
# message box display
#messagebox.showerror("Error", "Error message")
#messagebox.showwarning("Warning","Warning message")
messagebox.showinfo("XOROSTATMISI", "\n 1. EPILEGOUME TO ARXEIO ME TA RAW DEDOMENA APO TO ORGNO\n\n 2. EPILEGOYME EXCEL ARXEIO (.xlsx) STO OPOIO THELOYME NA APOTHIKEYTOYN TA DEDOMENA\n\n (ta dedomena tha apothikeytoun se kenouria kartela sto arxeio)")

#FolderPath = filedialog.askdirectory()
FilePathName = tkinter.filedialog.askopenfilename()

ExelFilePathName = tkinter.filedialog.askopenfilename()

FileName = os.path.splitext(os.path.basename(FilePathName))[0]
print(FileName)

ExelFileName = os.path.basename(ExelFilePathName)
print(ExelFileName)

Folder = os.path.basename(os.path.dirname(FilePathName))
print(Folder)


in_data = open(FilePathName, 'r')
temp1 = open('temp2', "w")

n = 1
for line in in_data:
    for word in line:
        if word == ' ':
            temp1.write(word.replace(' ', '_'))
            n += 1
        else:
            temp1.write(word)

in_data.close()
temp1.close()

temp1 = open('temp1', "w")
temp2 = open('temp2', 'r')

for i, line in enumerate(temp2):
        if not line.startswith('__') and not line.startswith('*') and line.strip() and not line.startswith('_\n'):
            temp1.write(line)
            
temp1.close()
temp2.close()


temp1 = open('temp1', "r")
temp2 = open('temp2', 'w')

for line in temp1:
    for word in line:
        if word == '_':
            temp2.write(word.replace('_', ' '))
            n += 1
        else:
            temp2.write(word)

temp1.close()
temp2.close()

#temp1 = open('temp1', "w")
temp2 = open('temp2', 'r')

fwidths = [9,10,10,13,12,9,13,12]

columns_num = ['BackSight', 'ForeSight', 'Intermediate', 'InstrHeight', 'Distance', 'GroundHeight']

df = pd.read_fwf(temp2, widths = fwidths,
               )
#names = ['PointNum', 'BackSight', 'ForeSight', 'Intermediate', 'InstrHeight', 'Distance', 'GroundHeight', 'Description']


FirstPoint = df.loc[0, 'PointNum']
LastPoint = df["PointNum"].iloc[-1]

print(FirstPoint)
print(LastPoint)


df = df.set_index('PointNum')

df['BackSight'] = pd.to_numeric(df['BackSight'].str.strip('m'))
df['ForeSight'] = pd.to_numeric(df['ForeSight'].str.strip('m'))
df['Intermediate'] = pd.to_numeric((df['Intermediate'].fillna('')).str.strip('m'))
df['InstrHeight'] = pd.to_numeric(df['InstrHeight'].str.strip('m'))
df['Distance'] = pd.to_numeric(df['Distance'].str.strip('m'))
df['GroundHeight'] = pd.to_numeric(df['GroundHeight'].str.strip('m'))

df['Distance2'] = df['Distance']

df = df[['BackSight', 'Intermediate', 'ForeSight', 'Distance','Distance2']]

BackSight1 = df.loc[FirstPoint, 'BackSight']

df['BackSight'] = df['BackSight'].shift(-1)

df.loc[FirstPoint, 'BackSight'] = BackSight1

df['Distance'] = df['Distance'].shift(-1)

df.loc[FirstPoint, 'Distance'] = df.loc[FirstPoint, 'Distance2']



LastRow = (df.tail(1))

df = df.dropna(subset=['BackSight', 'Intermediate'], how='all')

df = df.append(LastRow)


export_xlsx = pd.ExcelWriter(ExelFilePathName, engine='openpyxl')

#df.to_excel(export_xlsx, sheet_name=FileName)

if os.path.exists(ExelFilePathName):
    book = openpyxl.load_workbook(ExelFilePathName)
    export_xlsx.book = book

df.to_excel(export_xlsx, sheet_name = FirstPoint + ' - ' + LastPoint)

export_xlsx.save()
export_xlsx.close()


temp2.close()

os.remove('temp1')
os.remove('temp2')
