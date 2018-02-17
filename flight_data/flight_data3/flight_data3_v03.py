'''
Konstantinos Anastasakis
Python Script for flight data management
Version 0.3 For one camera file
09/2017
'''


import pandas as pd
import csv
from datetime import timedelta


# Open data files
in_camera_data = open(
    'OBLIGUE_3_NIKON.txt', 'r')
camera_data = pd.read_csv(
    in_camera_data, sep='\t', encoding='utf-8')

in_aircraft_data = open(
    'THEMIS05-08-17-A.tab', 'r')
aircraft_data = pd.read_csv(
    in_aircraft_data, sep='\t', encoding='utf-8', skiprows=[0, 2])


# GPG
split_name = camera_data[
    'File'].apply(lambda x: x.split('.'))

camera_data['FileName'] = split_name.apply(lambda x: x[0])
camera_data['FileExt'] = split_name.apply(lambda x: x[1])

camera_data['FileExt'] = 'JPG'
camera_data['File'] = camera_data[
    ['FileName', 'FileExt']].apply(
        lambda x: '.'.join(x), axis=1) # noqa


# Yaw +90
aircraft_data['Yaw'] = aircraft_data['Yaw'] + 90
aircraft_data.loc[aircraft_data[
    'Yaw'] >= 360, 'Yaw'] = aircraft_data['Yaw']-360; aircraft_data # noqa


# Roll +45
aircraft_data['Roll'] = aircraft_data['Roll'] + 45


# Time correction
camera_data['Date Shot'] = pd.to_datetime(
    camera_data['Date Shot'])

camera_data['DateTime'] = camera_data['Date Shot'] - timedelta(
    hours=2, minutes=59, seconds=49) # noqa

# camera_data['Date'] = camera_data['DateTime'].dt.date
camera_data['Time Milis'] = camera_data['DateTime'].dt.time

camera_data['Time'] = camera_data['Time Milis'].map(
    lambda t: t.strftime('%H:%M:%S')) # noqa


# Data connection
results = pd.merge(
    camera_data, aircraft_data, on='Time')

columns = [
    'File', 'Date', 'Time', 'Lat', 'Lon', 'Alt GPS', 'Roll', 'Pitch', 'Yaw', '#GPS sat'] # noqa

results = results[columns]
print(type(camera_data))
# print(aircraft_data)
print(results)


# Save data
export_data = open('metfl2.txt', 'w')
results.to_csv(
    export_data, encoding='utf-8',
    quoting=csv.QUOTE_NONE, sep='\t')

# Close files
in_camera_data.close()
in_aircraft_data.close()
export_data.close()
