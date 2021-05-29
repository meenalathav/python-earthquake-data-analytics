#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 12:52:24 2020

@author: Meenalatha Vaithilingam
"""

"""
Downloading and Parsing Earthquake JSON Data
"""

import urllib.request, urllib.parse, urllib.error
import json
import datetime
import time
from pymongo import MongoClient

# Setting the API URL and parameters
earthquakeURL =  "http://earthquake.usgs.gov/fdsnws/event/1/query?"
paramD = dict()
paramD["format"] = "geojson"                 # the format the data will be in
paramD["starttime"] = "1970-01-01T00:00:00"  # the minimum date/time that might be retrieved
paramD["endtime"] = "2020-03-14T23:59:59"    # the maximum date/time that might be retrieved
paramD["minmag"] = 6                         # the smallest earthquake magnitude to return
paramD["limit"] = 500                        # the maximum number of earthquakes to return
                                             # starts with the most recent

# MongoDB Atlas cluster connection setup

client = MongoClient('mongodb+srv://m001-student:m001-mongodb-basics@sandbox-e8oed.mongodb.net/test?retryWrites=true&w=majority')

# Create a database, seismicDB
seismicDB = client.seismicDB
# Create a collection, earthquakes in seismicDB
earthquakes = seismicDB.earthquakes

bypass_validation = False

# Checking for existing data in database to prevent adding of duplicate records

result = seismicDB.earthquakes.find({}, {'properties.time':1, '_id':0}).sort('properties.time', 1).limit(1)

try:
    for record in result:
        earliestTime = record['properties']['time'] 

    dttmeobj = datetime.datetime.fromtimestamp(earliestTime/1000)
    dttme_iso = dttmeobj.isoformat()
    paramD["endtime"] = dttme_iso
    
# Error handling for the case wherein earthquakes collection is empty
except:
    print("Database collection is currently empty.")


iteration = 0
count = paramD["limit"]


while count == paramD["limit"]:
    
    iteration = iteration + 1
    print("While Loop Iteration: ", iteration)

    params = urllib.parse.urlencode(paramD)
    connection = urllib.request.urlopen(earthquakeURL+params)
    data = connection.read().decode()
    
    # Error handling for invalid JSON data
    try:
        jsonDoc = json.loads(data)
    except:
        jsonDoc = None
    
    # If jsonDoc is set to None or 'type' key doesn't exist
    if not jsonDoc or 'type' not in jsonDoc:
        print('==== Failure To Retrieve ====')
        print(data)
        
    count = jsonDoc['metadata']['count'] 
    print("Count: ",count)
    
    # If there are no more records retrieved from the given time period, count will be 0
    if count == 0: break
    
    # Extract features array into a list
    earthquakeSet = jsonDoc['features']
    
    # Insert the set into sesismicDB.earthquakes collection
    insert_result = earthquakes.insert_many(earthquakeSet, bypass_validation)

    # Get the earliest timestamp from the last record in the current set
    lastEarthquake = earthquakeSet[count-1] 
    
    earliestDateTime = int(lastEarthquake['properties']['time'])
    milli_to_sec = earliestDateTime/1000

    timestamp_dttime = datetime.datetime.fromtimestamp(milli_to_sec)
    # Convert to iso format
    endtime = timestamp_dttime.isoformat()
    
    print("Earliest date in the earthquake set:",endtime)

    # Reset the date and time for the next iteration to start downloading data with
    paramD["endtime"] = endtime
    
    # Pause the program so it doesn't overwhelm the network or the USGS API
    time.sleep(7)






