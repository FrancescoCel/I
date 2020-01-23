# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 13:14:14 2020

@author: Francesco
"""

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def findBestPlaces(conn, diagnName, city):
    import SQL
    hospitals = SQL.findHospitals(conn, diagnName)
    hospitalsList = {}
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(city)
    latitude = location.latitude
    longitude = location.longitude
    home = latitude, longitude
    for i in hospitals:
        hospital = i[1], i[2]
        distance = round(geodesic(home, hospital).km, 3)
        hospitalName = i[0]
        hospitalsList[hospitalName] = distance
        
    return hospitalsList
