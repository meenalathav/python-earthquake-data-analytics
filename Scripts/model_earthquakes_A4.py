#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:03:13 2020

@author: Meenalatha Vaithilingam
"""

import sqlite3
from pymongo import MongoClient
import re

# list of words to remove when cleaning the place data
stopwords = ['south', 'southern', 'southeast', 'southwest', 'southwestern', 'southeastern', 'north', 'northern',
             'northeast', 'northeastern','ssw', 'nnw', 'se', 'ne', 'km','northwest', 'northwestern', 'east',
             'eastern', 'west', 'western', 'of', 'the', 'and', 'islands', 'island', 'region',  'central',
              'off', 'coast', 'near', 'offshore', 'peninsula', 'gulf', 'earthquake', 'mid']


# dictionary of specific place data mapped to its generalized region data 
loc_dict = {"Ridgecrest Sequence" : "California", "Pacific Rise" : "Pacific Ocean", "Ca" : "California", "Georgia Sandwich" : "Sandwich", 
            "Mauritius Reunion" : "Mauritius", "Federated States Micronesia" : "Micronesia", 
            "Mx" : "Mexico", "Baja California" : "California", "Georgia Sak'art'velo" : "Georgia",
            "Sea Japan" : "Japan", "Philippine" : "Philippines", "Atlantic Ridge" : "Atlantic Ocean", "Indian Ridge" : "Indian Ocean"} 

# function to clean place data into a larger region data
def clean(place):

    place = place.lower().strip()
    
    # Check for numeric digits in place and remove them
    if re.search("[0-9]+", place):
        toreplace = re.findall("[0-9]\S+", place)[0]
        place = place.replace(toreplace, '')
    
    # Check for punctuation characters and remove them
    punc = ['(', ')', '-']
    for item in punc:
        place = place.replace(item, ' ')
    
    # Search for presence of data following the final occurrence of ',' in place
    if re.search(",.\w+", place):
            # Greedy search for last comma, extract region data following it
            region = re.findall(".+,(.+)", place)[0]
            terms = region.split()
    
    # Else to address cases of a place with either no commas or with any commas that don't have region data following them  
    else: 
        terms = place.replace(',','').split()
    
    # Remove any stopwords and create a new list 
    terms = [word.capitalize() for word in terms if word not in stopwords]

    # Concatenate terms into a single string with words separated by a space
    region = ' '.join(terms)
    
    # Match the region to keys in the dictionary and replace with its associated value.  
        # Regular expression with word boundaries ensures substrings such as the 'Ca' substring in 'Canada', 'Caledonia' 
            # are not mapped to 'California'
    for key in loc_dict:
        regex = r'\b'+key+r'\b'
        if re.search(regex, region):
            region = region.replace(key, loc_dict[key])
    
    # Trim whitespaces 
    region = region.strip()

    return(region)


# Connect to index.sqlite and create Earthquakes table
con = sqlite3.connect("../SqliteDB/index.sqlite")
cur = con.cursor()

# Drop table and create it fresh
cur.executescript('''
        DROP TABLE IF EXISTS Earthquakes;
        CREATE TABLE Earthquakes (
                earthquake_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                magnitude REAL,
                time INTEGER,
                long REAL,
                lat REAL,
                depth REAL,
                place TEXT,
                title text,
                felt INTEGER,
                tsunami INTEGER,
                region TEXT
            );       
        ''')

# Connect to MongoDB and retrieve required fields 
client = MongoClient('mongodb+srv://m001-student:m001-mongodb-basics@sandbox-e8oed.mongodb.net/test?retryWrites=true&w=majority')
coll_handle = client.seismicDB.earthquakes

projection = {"properties.mag":1, "properties.time":1, "geometry":1, "properties.place":1, 
              "properties.title":1, "properties.felt":1,"properties.tsunami":1, "_id":0}

result = coll_handle.find({}, projection)

count = 0

# Extract values from the raw data set and insert into Sqlite DB
for rec in result:
    
    mag = rec['properties']['mag']
    time = rec['properties']['time']
    long = rec['geometry']['coordinates'][0]
    lat = rec['geometry']['coordinates'][1]
    depth = rec['geometry']['coordinates'][2]
    place = rec['properties']['place']
    title = rec['properties']['title']
    felt = rec['properties']['felt']
    tsunami = rec['properties']['tsunami']
    
    # Invoke function to clean place data and map it to a more general region 
    region = clean(place)
    
    cur.execute(''' INSERT INTO Earthquakes 
                (magnitude, time, long, lat, depth, place, title, felt, tsunami, region)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (mag, time, long, lat, depth, place, title, felt, tsunami, region)
                )
    
    if count % 500 == 0:
        print("Count:", count)
        con.commit()

    count += 1

# Retrieve distinct regions and number of times they occur in the table    
sqlstr = '''SELECT region, count() FROM Earthquakes GROUP BY region ORDER BY count() DESC'''

print("Distinct Regions and their counts in Earthquakes table:")
for row in cur.execute(sqlstr):
    print(row)

# Commit all the records written to index.sqlite    
con.commit()

cur.close()
con.close()










































