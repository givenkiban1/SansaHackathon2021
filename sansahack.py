# -*- coding: utf-8 -*-
"code needs to be sorted properly... everything was all over the place in google collab ,,,"
"""SansaHack.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AjDoF4OMc1whOl2Mw8nF2jHx8lHAvVgi

Importing all important libraries
"""

import firebase_admin
from firebase_admin import credentials
import requests as r
from firebase_admin import db
import json
import pandas as pd

databaseURL = "https://sansahack2-default-rtdb.firebaseio.com/"
x_ray_flux = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
solar_flare_ace = "https://services.swpc.noaa.gov/json/ace/swepam/ace_swepam_1h.json"

cred = credentials.Certificate("serviceConfig.json")
if not firebase_admin._apps:
  firebase_admin.initialize_app(cred, {
      "app"
      "databaseURL": databaseURL
  })

# Get a database reference to our posts
ref1 = db.reference('realtime/x_ray_flux')
ref2 = db.reference('realtime/solar_wind')
ref3 = db.reference('alerts/solar_flare')

#request
x_ray_req = r.get(x_ray_flux)
solar_flare_req = r.get(solar_flare_ace)

#response
x_ray_resp = x_ray_req.json()

solar_flare_resp = solar_flare_req.json()

with open('x_ray.json', 'w') as json_file:
    json.dump(x_ray_resp, json_file)

with open('solar_wind.json', 'w') as json_file:
    json.dump(solar_flare_resp, json_file)

print("Done")

#determining if there's a solar flare

#find an average over past 24 hours
#find average over past 6 hours

#if current flare > average flare (24 hours)
#check if average over 6 hours>average over 24 hours, flares have definitely occured

df = pd.read_json("x_ray.json")

print(df)

df2 = pd.read_json("solar_wind.json")
print(df2)

#last item in dataset
print(df.last_valid_index())
last = df.tail(1)

print(df2.last_valid_index())
first = df2.head(1)

last_t = last["time_tag"].to_string()
last_t = last_t.split("    ")
last_t = last_t[1]

first = first["time_tag"].to_string()
first = first.split("    ")
first = first[1]

import datetime
from datetime import datetime, timedelta

format = "%Y-%m-%dT%H:%M:%SZ"
t = datetime.strptime(last_t, format)

yt = datetime.strftime(t - timedelta(1), format)

print(last_t2)

print(yt)

last24 = df.loc[(df['time_tag'] >= yt) & (df['time_tag'] <= last_t)]

#slaps face when sees that this is data for last 24hours...

#avg over 24 hours
print(last24["flux"].mean())

#avg over last 6 hours
last6HoursDateTime = t - timedelta(hours = 6)
l6 = datetime.strftime(last6HoursDateTime, format)

print(l6)
print(type(l6))

last6 = df.loc[(df['time_tag'] >= l6) & (df['time_tag'] <= last_t)]

#avg over last 6 hours
print(last6["flux"].mean())

last6mean = last6["flux"].mean()
last24mean = last24["flux"].mean()

bMax = 1e-6
cMax = 1e-5
mMax = 1e-4

def classify(mean):
  if (mean<bMax):
    return "B"
  elif (mean<cMax and mean>=bMax):
    return "C"
  elif (mean<mMax and mean>=cMax):
    return "M"
  elif (mean>=mMax):
    return "X"

print(last6mean>last24mean)

classify(last6mean)

classify(last24mean)

(last["flux"]>last24mean).bool() and classify(last6mean)>classify(last24mean)

classify(float((last["flux"].to_string()).split("    ")[1]))

timeStamp = datetime.strftime(datetime.now(), format)
print(timeStamp)

ref3.child(timeStamp).update({
    'solarFlareClass': classify(float((last["flux"].to_string()).split("    ")[1])),
    'last6HoursClass':  classify(last6mean),
    'last24HoursClass': classify(last24mean),
    'solarFlareDetected': (last["flux"]>last24mean).bool() and classify(last6mean)>classify(last24mean),
    'timeStamp': timeStamp,
})

print(df2)

print(first)

speedMean = df2["speed"].mean()
print(speedMean)

densityMean = df2["dens"].mean()
print(densityMean)

"""https://umbra.nascom.nasa.gov/spartan/the_solar_wind.html

average solar wind speed = 400
when there's solar wind of high class, wind speed between 600 and 1000
"""

#look at most recent alert from firebase db
#if class of solar flare is C7 --- X
#check if there's an increase/spike in solar wind speed + density
print(first)
print(last)

(first["dens"]>densityMean).bool() and (first["dens"]>5).bool()

(first["speed"]>speedMean).bool() and (first["speed"]>600).bool()