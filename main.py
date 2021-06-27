x_ray_flux = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"

solar_flare_ace = "https://services.swpc.noaa.gov/json/ace/swepam/ace_swepam_1h.json"

import firebase_admin
from firebase_admin import credentials
import requests as r
from firebase_admin import db

databaseURL = "https://sansahack2-default-rtdb.firebaseio.com/"

cred = credentials.Certificate("serviceConfig.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": databaseURL
})

# Get a database reference to our posts
ref1 = db.reference('realtime/x_ray_flux')
ref2 = db.reference('realtime/solar_wind')


#this is the code that runs once per hour

x_ray_req = r.get(x_ray_flux)
solar_flare_req = r.get(solar_flare_ace)

x_ray_resp = x_ray_req.json()

solar_flare_resp = solar_flare_req.json()

#
# print("X-ray")
#
# for item in x_ray_resp[len(x_ray_resp)-210:]:
#     print(x_ray_resp.index(item), '/', len(x_ray_resp))
#     c = item.keys()
#
#     if (ref1.child(item["time_tag"]).get()==None):
#         ref1.child(item["time_tag"]).update(item)


print("Solar flare")

for item in solar_flare_resp[:210]:
    print(solar_flare_resp.index(item), '/', len(solar_flare_resp))
    c = item.keys()
    if c.__contains__("time_tag") and c.__contains__("dens") and c.__contains__("speed"):
        if (ref2.child(item["time_tag"]).get() == None):
            ref2.child(item["time_tag"]).update(item)

print("Done")


