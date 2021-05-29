#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python program to run a simple analysis to calculate basic statistics on a sample earthquake data set
Created on Thu Apr  2 14:48:47 2020

@author: Meenalatha Vaithilingam

"""

import numpy as np
import sqlite3

while(True):
    try:
        howmany = int( input("How many earthquake locations to display? Enter a number between 1 and 20:") )
        if howmany < 1 or howmany > 20: 
            print("Entered number is not between 1 and 20.")
            continue
    
    except KeyboardInterrupt:
        print("\nProgram was interrupted by user.")
        break
    
    except:
        print("Error: Invalid input. Please enter a number between 1 and 20.")
        continue
    
    # connect to the index.sqlite database
    conn = sqlite3.connect("index.sqlite")
    
    # forces database to return strings for TEXT attributes
    conn.text_factory = str
    
    # get the cursor for the connection
    cur = conn.cursor()
    
    # run Select query on Earthquakes table to get data for statistics
    cur.execute("SELECT place, region, magnitude, felt, tsunami, depth FROM Earthquakes")
    
    # set up variables to hold table data
    # count earthquakes by place/region
    # store data about magnitude, felt, tsunami, depth
    placecounts = dict()
    regioncounts = dict()
    mag = []
    felt = []
    tsunami = []
    depth = []
    
    for quake in cur:
        # Get data from cursor and add to lists or dictionaries
        # Dictionaries will track counts, lists will append value data
        place = quake[0]    
        placecounts[place] = placecounts.get(place, 0) + 1
        
        region = quake[1]
        regioncounts[region] = regioncounts.get(region, 0) + 1
        
        mag.append(quake[2])
        felt.append(quake[3])
        tsunami.append(quake[4])
        depth.append(quake[5])
    
    # Replace None values in felt list with 0
    while None in felt:
        felt[felt.index(None)] = 0
    
    # Print out places with top earthquake counts
    print('\nTop', howmany, 'earthquake places:')
    
    # Sort placecounts dictionary by its values, store dictionary keys in top_places
    top_places = sorted(placecounts, key = placecounts.get, reverse = True)
    # Display places with the highest counts
    for k in top_places[:howmany]:
        print(k, placecounts[k])
        if placecounts[k] < 10: 
            break
        
    
    # Print out regions with top earthquake counts
    print('\nTop', howmany, 'earthquake regions:')
    
    # Sort regioncounts dictionary by its values, store keys in top_regions
    top_regions = sorted(regioncounts, key = regioncounts.get, reverse = True)
    # Display regions with the highest counts
    for k in top_regions[:howmany]:
        print(k, regioncounts[k])
        if regioncounts[k] < 10: break
    
    
    print("\nBasic Statistics:\n")
    print("************* Magnitude ********************")
    # Print out basic statistics like number of earthquakes, mean, median, standard deviation of magnitude
    print("Number of earthquakes: ", len(mag))
    print("Maximum earthquake magnitude:", max(mag))
    print("Mean magnitude of earthquakes:", round(np.mean(mag), 4))
    print("Median magnitude of earthquakes:", np.median(mag))
    print("Standard deviation of earthquake magnitudes:", np.std(mag))
    
    
    print("\nStatistics based on felt attribute: \n")
    print("************* Felt ********************")
    npfelt_filter = np.array(felt)
    # Boolean mask
    felt_filterB = npfelt_filter > 0 
    # Numpy array created by applying Boolean mask to mag list
    magF = np.array(mag)[felt_filterB]
    # Print out basic statistics for felt earthquakes
    print("Number of felt earthquakes: ", len(magF))
    print("Maximum felt earthquake magnitude:", magF.max())
    print("Mean magnitude of felt earthquakes:", round(magF.mean(), 4))
    print("Median magnitude of felt earthquakes:", np.median(magF))
    print("Standard deviation of felt earthquake magnitudes:", round(magF.std(), 4))
 
 
    
    
    
    
















