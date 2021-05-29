#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:06:14 2020

@author: Meenalatha Vaithilingam
"""

import Earthquake
import sqlite3
import pandas as pd

# connect to the index.sqlite database
con = sqlite3.connect("../SqliteDB/index.sqlite")
# force the database to return strings for text attributes
con.text_factory = str
# create a cursor
cur = con.cursor()
# run a SELECT query on the database
cur.execute('SELECT magnitude, time, place, region, felt, tsunami, depth FROM Earthquakes')

earthquakeList = list()

# extract data from the database records 
for record in cur:
    mag = record[0]
    ts = record[1]
    p = record[2]
    r = record[3]
    f = record[4]
    t = record[5]
    d = record[6]
    # instantiate an Earthquake class object for each earthquake record
    e = Earthquake.Earthquake(mag, p, r, f, t, d, ts)
    earthquakeList.append(e)

# create a dataframe of earthquake data and populate it using the list of Earthquake dictionaries  
earthquakeDF = pd.DataFrame( [eObj.dictRepr() for eObj in earthquakeList] )

# adjust the display width in the output console
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

# display the first 5 rows of the dataframe
print("\n", "First 5 earthquakes in the dataframe:")
print(earthquakeDF.head())  

print("\n", "Built-in Statistic Reference for Dataframe Data:")
print(earthquakeDF.describe())

print("\n", " Basic Statistics for Earthquake Magnitudes ".center(80, '*'))
print("Number of Earthquakes: ", earthquakeDF.Magnitude.count())
print("Maximum Magnitude of all Earthquakes:", earthquakeDF.Magnitude.max())
print("Mean Magnitude of all Earthquakes:", round(earthquakeDF.Magnitude.mean(), 4))
print("Median Magnitude of all Earthquakes:", earthquakeDF.Magnitude.median())
print("Standard Deviation of Earthquake Magnitudes:", round(earthquakeDF.Magnitude.std(), 5))


print("\n", " Basic Statistics by Region ".center(80, '*'))

# Number of occurrences in the dataframe for each region with top frequencies at the beginning of the series
print(earthquakeDF["Region"].value_counts()[:6])

# Statistics for one region with more than 200 earthquakes
japanDF = earthquakeDF[earthquakeDF.Region == 'Japan']
print("\n"," Japan ".center(20, '*'))
print("Number of Earthquakes: ", japanDF.Magnitude.count())
print("Maximum Magnitude of Earthquakes:", japanDF.Magnitude.max())
print("Mean Magnitude of Earthquakes:", round(japanDF.Magnitude.mean(), 4))
print("Median Magnitude of Earthquakes:", japanDF.Magnitude.median())
print("Standard Deviation of Earthquake Magnitudes:", round(japanDF.Magnitude.std(), 5))

# Statistics for a second region with more than 200 earthquakes
chileDF = earthquakeDF[earthquakeDF.Region == 'Chile']
print("\n", " Chile ".center(20, '*'))
print("Number of Earthquakes: ", chileDF.Magnitude.count())
print("Maximum Magnitude of Earthquakes:", chileDF.Magnitude.max())
print("Mean Magnitude of Earthquakes:", round(chileDF.Magnitude.mean(), 4))
print("Median Magnitude of Earthquakes:", chileDF.Magnitude.median())
print("Standard Deviation of Earthquake Magnitudes:", round(chileDF.Magnitude.std(), 5))


# Filter dataframe by Depth column values
print("\n", " Statistics for Earthquakes with Depth < 50 ".center(80, '*'))

# subset of dataframe with depth column value < 50
depthDF = earthquakeDF[earthquakeDF.Depth < 50]
print("Number of Earthquakes: ", depthDF.Magnitude.count())
print("Maximum Magnitude of Earthquakes:", depthDF.Magnitude.max())
print("Mean Magnitude of Earthquakes:", round(depthDF.Magnitude.mean(), 4))
print("Median Magnitude of Earthquakes:", depthDF.Magnitude.median())
print("Standard Deviation of Earthquake Magnitudes:", round(depthDF.Magnitude.std(), 5))



















