# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 13:14:14 2020

@author: Francesco
"""

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def checkLocation(loc):
    """
    Funzione che restituisce una variabile contenente un luogo
    
    Parameters
    ----------
    loc: str
        Nome della locazione
    
    Returns
    -------
    geopy.location.Location
        Se lil luogo inserito dall'utente esiste, questa variabile contiene
        un oggetto della classe geolocation.location.Location. In caso 
        contrario la variabile è vuota
    """
    geolocator = Nominatim(user_agent="specify_your_app_name_here",timeout=15)
    return geolocator.geocode(loc)

def findBestPlaces(conn, diagnName, location):
    """
    Funzione che trova gli ospedali che curano una determinata malattia e ne 
    calcola la distanza da un punto inserito dall'utente
    
    Parameters
    ----------
    conn: connection
        Connessione al database
    diagnName: str
        Nome della diagnosi che l'utente vuole curare
    location: geopy.location.Location
        Luogo di cui deve essere calcolata la distanza dagli ospedali
    
    Returns
    -------
    hospitalsDict: dict
        Dizionario le cui chiavi sono i nomi degli ospedali che curano la
        malattia, e i cui valori indicano la distanza in km degli ospedali
        dal punto indicato dal parametro city
    """
    import SQL
    hospitals = SQL.findHospitals(conn, diagnName)
    hospitalsDict = {}
    latitude = location.latitude
    longitude = location.longitude
    home = latitude, longitude
    for i in hospitals:
        hospital = i[1], i[2]
        distance = round(geodesic(home, hospital).km, 3)
        hospitalName = i[0]
        hospitalsDict[hospitalName] = distance
        
    return hospitalsDict
