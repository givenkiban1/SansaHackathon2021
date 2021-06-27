import firebase_admin
from firebase_admin import credentials
import requests as r
from firebase_admin import db

import pandas as pd

databaseURL = "https://sansahack2-default-rtdb.firebaseio.com/"
x_ray_flux = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
solar_flare_ace = "https://services.swpc.noaa.gov/json/ace/swepam/ace_swepam_1h.json"

cred = credentials.Certificate("serviceConfig.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": databaseURL
})

# Get a database reference to our posts
ref1 = db.reference('realtime/x_ray_flux')
ref2 = db.reference('realtime/solar_wind')

#request
x_ray_req = r.get(x_ray_flux)
solar_flare_req = r.get(solar_flare_ace)

#response
x_ray_resp = x_ray_req.json()

solar_flare_resp = solar_flare_req.json()

import json
with open('x_ray.json', 'w') as json_file:
    json.dump(x_ray_resp, json_file)

with open('solar_wind.json', 'w') as json_file:
    json.dump(x_ray_resp, json_file)

print("Done")

#determining if there's a solar flare

#find an average over past 24 hours
#find average over past 6 hours

#if current flare > average flare (24 hours)
#check if average over 6 hours>average over 24 hours, flares have definitely occured

df = pd.read_json("x_ray.json")

print(df)