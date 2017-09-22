'''
Artemis - Aerosurvey
http://aerosurvey.eu
Python Script for flight data management
Version 0.3
09/2017
'''


import pandas as pd
import csv
from datetime import timedelta


# Anigma arxeion
in_camera_data1 = open(
    'OBLIGUE_2_SHOOTINGDATA.txt', 'r')
camera_data1 = pd.read_csv(
    in_camera_data1, sep='\t', encoding='utf-8')

in_camera_data2 = open(
    'OBLIGUEShootingdata_AEREA_3.txt', 'r')
camera_data2 = pd.read_csv(
    in_camera_data2, sep='\t', encoding='utf-8')


in_aircraft_data = open(
    'FLIGHTDATA_1.tab', 'r')
aircraft_data = pd.read_csv(
    in_aircraft_data, sep='\t', encoding='utf-8', skiprows=[0, 2])


# Sindesi dedomenon camers
camera_data = pd.concat([camera_data1, camera_data2])

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


# Diamorfosi xronou
camera_data['Date Shot'] = pd.to_datetime(
    camera_data['Date Shot'])

camera_data['DateTime'] = camera_data['Date Shot'] - timedelta(
    hours=3, minutes=0, seconds=9) # noqa

# camera_data['Date'] = camera_data['DateTime'].dt.date
camera_data['Time Milis'] = camera_data['DateTime'].dt.time

camera_data['Time'] = camera_data['Time Milis'].map(
    lambda t: t.strftime('%H:%M:%S')) # noqa


# Sindesi dedomenon
results = pd.merge(
    camera_data, aircraft_data, on='Time')

columns = [
    'File', 'Date', 'Time', 'Lat', 'Lon', 'Alt GPS', 'Roll', 'Pitch', 'Yaw', '#GPS sat'] # noqa

results = results[columns]
# print(camera_data)
# print(aircraft_data)
print(results)


# Apothikeysi tou apotelesmatos
export_data = open('export_data1.txt', 'w')
results.to_csv(
    export_data, encoding='utf-8',
    quoting=csv.QUOTE_NONE, sep='\t')

# Kleisimo arxeion
in_camera_data1.close()
in_camera_data2.close()
in_aircraft_data.close()
export_data.close()
