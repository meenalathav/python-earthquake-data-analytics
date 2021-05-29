#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:06:32 2020

@author: Meenalatha Vaithilingam
"""

import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from wordcloud import WordCloud


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
    regionlist = []
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
        regionlist.append(region)
        mag.append(quake[2])
        felt.append(quake[3])
        tsunami.append(quake[4])
        depth.append(quake[5])
    
    # Replace None values in felt list with 0
    while None in felt:
        felt[felt.index(None)] = 0
    
    topcounts = []
    # Sort regioncounts dictionary by its values, store dictionary keys in top_regions
    top_regions = sorted(regioncounts, key = regioncounts.get, reverse = True)
    # Extract counts for regions with the highest counts
    for k in top_regions[:howmany]:
        topcounts.append(regioncounts[k])

    plt.rcdefaults()
    # Word Cloud
    word_obj = WordCloud(width = 500, height = 500, max_words = howmany,
                         max_font_size = 100, min_font_size = 10, 
                         background_color = 'lightblue').generate_from_frequencies(regioncounts)
    plt.figure(figsize = (10, 10))
    plt.imshow(word_obj, interpolation = 'bilinear')
    plt.axis('off')
    plt.title('Top %s Earthquake Regions' %howmany)
    plt.savefig("../SpyderScripts/wordcloud_A5.png")
    plt.show()
    
    # Bar Graph
    x_pos_lst = top_regions[:howmany]
    plt.figure(figsize = (12, 8))
    plt.bar(x_pos_lst, topcounts, width = 0.7, color = 'r', alpha = 0.5)
    plt.xticks(rotation = 60)
    plt.xlabel("Top %s Regions" %howmany)
    plt.ylabel("Number of Earthquakes")
    plt.title("Top Earthquake-hit Regions and their Quake Count")
    plt.tight_layout()   # keeps x-tick labels and axis labels from running outside the figure canvas
    plt.savefig("../SpyderScripts/bargraph_A5.png")
    plt.show()

    # Histogram to show frequency of earthquakes falling within a magnitude bin
    plt.style.use('classic')
    plt.figure(figsize = (8, 10))
    bin_limits = np.arange(6.0, 9.25, step = 0.2)
    n, bins, patches = plt.hist(mag, bin_limits, alpha = 0.5)
    plt.xticks(bins, rotation = 60)
    plt.xlabel("Magnitude of Earthquakes")
    plt.ylabel("Frequency of Earthquakes")
    plt.title("Histogram of Earthquake Magnitudes between 1970 to 2020")
    plt.savefig("../SpyderScripts/histogram_A5.png")
    plt.show()

    # Construct a Bubble Chart for Region with the most number of earthquakes
    topregion = top_regions[0]
    
    # Convert lists to numpy arrays
    npregionlst = np.array(regionlist)
    npfelt = np.array(felt)
    npdepth = np.array(depth)
    npmag = np.array(mag)
    
    # Boolean mask to focus only on the region with most earthquakes
    region_filterB = npregionlst == topregion
    
    # Filtered arrays for particular region created by applying Boolean mask 
    magR = npmag[region_filterB]
    depthR = npdepth[region_filterB]
    feltR = npfelt[region_filterB]    
    
    plt.figure(figsize = (10, 10))
    plt.scatter(magR, depthR, s = feltR, color = 'yellow', edgecolors = 'black', alpha = 0.6)
    plt.yscale('log')
    plt.axis([5.5, 9.0, 10**0.5, 10**3])
    plt.xlabel("Magnitude of Earthquakes around %s" %topregion)
    plt.ylabel("Depth of Earthquakes around %s" %topregion)
    plt.title("Magnitude by Depth and Felt (bubble size) for %s Earthquakes" %topregion)
    plt.savefig("../SpyderScripts/bubblechart_A5.png")
    plt.show()
    























