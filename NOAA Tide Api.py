import requests, json
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# https://tidesandcurrents.noaa.gov/api/

'200: Everything went okay, and the result has been returned (if any).'
'301: The server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint name is changed.'
'400: The server thinks you made a bad request. This can happen when you don’t send along the right data, among other things.'
'401: The server thinks you’re not authenticated. Many APIs require login ccredentials, so this happens when you don’t send the right credentials to access an API.'
'403: The resource you’re trying to access is forbidden: you don’t have the right permissions to see it.'
'404: The resource you tried to access wasn’t found on the server.'
'503: The server is not ready to handle the request.'

'water_level	Preliminary or verified water levels, depending on availability.'
'air_temperature	Air temperature as measured at the station.'
'water_temperature	Water temperature as measured at the station.'
'wind	Wind speed, direction, and gusts as measured at the station.'
'air_pressure	Barometric pressure as measured at the station.'
"air_gap	Air Gap (distance between a bridge and the water's surface) at the station."
"conductivity	The water's conductivity as measured at the station."
"visibility	Visibility from the station's visibility sensor. A measure of atmospheric clarity."
'humidity	Relative humidity as measured at the station.'
'salinity	Salinity and specific gravity data for the station.'
'hourly_height	Verified hourly height water level data for the station.'
'high_low	Verified high/low water level data for the station.'
'daily_mean	Verified daily mean water level data for the station.'
'monthly_mean	Verified monthly mean water level data for the station.'
'one_minute_water_level	One minute water level data for the station.'
'predictions	6 minute predictions water level data for the station.'
'datums	                  datums data for the stations.'
'currents	Currents data for currents stations.'
'currents_predictions	Currents predictions data for currents predictions stations.'

now = datetime.now()
current_day = now.strftime('%Y%m%d')
current_time = now.strftime("%H:%M")

interval = 12
later = datetime.now() + timedelta(hours=interval)
later_day = later.strftime('%Y%m%d')
later_time = later.strftime("%H:%M")

'Request future tide predictions for an interval from NOAA API'
response = requests.get("https://tidesandcurrents.noaa.gov/api/datagetter?begin_date=" + current_day + " " + current_time + "&end_date=" + later_day + " " + later_time + "&station=9410230&product=predictions&datum=mllw&units=english&time_zone=lst&application =ports_screen&format=json")
#print(response.headers.get("content-type"))
j = response.json()
tide_heights = []
tide_times = []

for i in range(0,len(j['predictions'])):
    tide_heights.append(float(j['predictions'][i]['v']))
    t = j['predictions'][i]['t']
    tide_times.append(str(t[-5:]))

'Retrieve low and high tide info, this works for ranges < 20 hours'
try:
    lowIndex = ((np.diff(np.sign(np.diff(tide_heights))) > 0).nonzero()[0] + 1)[0] # local min
    if len(lowIndex) > 1:
        lowIndex = lowIndex[0]
except: low = 'No low tides'
try:
    highIndex = ((np.diff(np.sign(np.diff(tide_heights))) < 0).nonzero()[0] + 1)[0] # local max
    if len(highIndex) > 1:
        highIndex = highIndex[0]
except: high = 'No high tides'

low = str(tide_heights[lowIndex])
lowTime = str(tide_times[lowIndex])
high =  str(tide_heights[highIndex])
highTime = str(tide_times[highIndex])

def detDay(time):
    global day
    if int(time[:2]) < 12: day = 'am'
    else: day = 'pm'

response = requests.get("https://tidesandcurrents.noaa.gov/api/datagetter?date=latest&station=9410230&product=water_level&datum=mllw&units=english&time_zone=lst&application =ports_screen&format=json")
#print(response.headers.get("content-type"))
j = response.json()
latest = str(j['data'][0]['v'])
latestTime = str(j['data'][0]['t'])

detDay(latestTime)
print("Latest Tide: " + latest + ' ft at ' +  str(np.mod(int(latestTime[11:13]), 12)) + ":" + latestTime[-2:] + " " + day)
detDay(lowTime)
print('Low Tide: ' + low + ' ft at ' +  str(np.mod(int(lowTime[:2]), 12)) + ":" + lowTime[-2:] + " " + day)
detDay(highTime)
print('High Tide: ' + high + ' ft at ' +  str(np.mod(int(highTime[:2]), 12)) + ":" + highTime[-2:] + " " + day)

min_t, max_t = 0, 12 * interval
fig = plt.figure(figsize=(5,5))
ax = plt.subplot(111)
ax.set_xticks(np.linspace(min_t, max_t, 6, endpoint=False))

plt.plot(tide_times, tide_heights, linewidth=.5)

plt.show()
