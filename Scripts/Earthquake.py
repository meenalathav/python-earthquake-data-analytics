#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 11:10:24 2020

@author: Meenalatha Vaithilingam
"""

import datetime

class Earthquake:
    
    def __init__(self, mag, p, r, f, t, d, ts):
        self.magnitude = mag
        self.place = p
        self.region = r
        self.felt = f
        self.tsunami = t
        self.depth = d
        self.tstampObj = Time(ts)
    
    # Method to return dictionary containing earthquake attributes
    def dictRepr(self):
        retDict = {'Magnitude':self.magnitude, 'Place':self.place, 'Region':self.region, 'Felt':self.felt,
                   'Tsunami':self.tsunami, 'Depth':self.depth, 'Datetime':str(self.tstampObj)}
        return retDict
    
    # Overriding the __str__ method to return a string representation of the earthquake object
    def __str__(self):
        retStr =  self.place + ", " + self.region + ", " + str(self.magnitude) + ", " + str(self.depth) + "\n" + str(self.tstampObj)
        return retStr
    
    # Property object methods for the magnitude attribute
    @property
    def magnitude(self):
        return self.__magnitude
    
    @magnitude.setter
    def magnitude(self, mag):
        # Check for correct datatype 
        if isinstance(mag, float):
            self.__magnitude = mag
    
    # Property object methods for the felt attribute    
    @property
    def felt(self):
        return self.__felt
    
    @felt.setter
    def felt(self, f):
        # Replace all None values for felt with 0
        if f is None: f = 0
        # Check both datatype and lower limit of felt
        if isinstance(f, int) and f >= 0:
            self.__felt = f
    
    
class Time:
    
    def __init__(self, ts):
        self.timestamp = ts
    
    # Overriding the __str__ method to return a string representation of the Time object      
    def __str__(self):
        # Convert the timestamp to a datetime value
        dttime = datetime.datetime.fromtimestamp(self.timestamp/1000)
        # Format the datetime object into date and time strings
        dateStr = dttime.strftime("%d %b %Y")
        timeStr = dttime.strftime("%I:%M:%S %p")
        
        return dateStr + ", " + timeStr










       
        

      


    
    