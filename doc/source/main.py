# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:37:07 2019

@author: franc
"""
import mysql.connector
import SQL
import BayesianNet
import GeoLocation

def read_symptoms(conn):
    """
    Funzione utilizzata per prendere in input i sintomi che un utente ha
    Parameters
    ----------
    conn: connection
        connessione al database. Serve per verificare che il nome di un
        sintomo inserito sia corretto
    
    Returns
    -------
    list: list
        Lista di sintomi inseriti dall'utente
    """
    list = []
    stop = "/"
    while True:
        value = input()
        if value != stop:
            goodVal = False
            while goodVal is False:
                goodVal = SQL.checkSymWithErr(conn, value)
                if goodVal is False:
                    print("Last symptom inserted is wrong. Please insert a valid one.")
                    value = input()
                    if value==stop:
                        if not list:
                            continue
                        else:
                            return list
            list.append(value.lower())
        else:
            if not list:
                print("You have to insert at least one symptom!")
            else:
                break
    return list


def getDiseaseName(conn):
    """
    Funzione utilizzata per acquisire dall'utente il nome di una malattia che 
    vuole curare.
    
    Parameters
    ----------
    conn: connection
        Connessione al database. Server per interrogare il database in modo da 
        verificare che il nome di
        una malattia inserita dall'utente sia corretto
        
    Returns
    -------
    goodVal: str
        Nome della malattia inserito dall'utente e formattato tutto in 
        caratteri minuscoli
    """
    goodVal = False
    while goodVal is False:
        diseaseName = input()
        goodVal = SQL.checkDiseaseWithErr(conn, diseaseName)
        if not goodVal:
            print("You entered a wrong value. Please insert a valid one.")
    return goodVal.lower()

def getLocation():
    goodLoc = False
    while goodLoc is False:
        city = input()
        goodLoc = GeoLocation.checkLocation(city)
        if not goodLoc:
            goodLoc = False
            print("You entered an unknown location. Please retry.")
    return goodLoc


def mergeList(listOfLists):
    """
    Funzione che riceve in input una lista di liste e le unisce in una lista
    unica
    
    Parameters
    ----------
    listOfLists: list
        Lista di liste
    
    Returns
    -------
    mergedList: list
        Lista unica
    """
    mergedList = []
    for i in range (0, len(listOfLists)):
        mergedList += listOfLists[i]   
    return mergedList


def countOcc(mergedList):
    """
    Funzione che restituisce un dizionario in cui le chiavi sono i nomi delle 
    diagnosi e i corrispondenti valori sono il numero di occorrenze di una 
    diagnosi nella lista
    
    Parameters
    ----------
    mergedList: list
        Lista di
        
    Returns
    -------
    occDict: dict
        Dizionario finale
    """
    occDict = {}
    
    for i in mergedList:
        if i not in occDict.keys():
            occDict[i] = mergedList.count(i)
   
    return occDict

def percOfDiagn(listSize,occDict):
    """
    Funzione che restituisce un dizionario in cui le chiavi sono le varie 
    diagnosi e i corrispondenti valori indicano il rapporto tra le occorrenze 
    di una diagnosi e il numero totale di diagnosi
    
    Parameters
    ----------
    listSize: int
        Dimensione della lista delle diagnosi predette
    occDict: dict
        Dizionario in cui le chiavi sono gli id delle diagnosi e i valori sono 
        il numero di occorrenze di ogni diagnosi all'interno della lita di 
        diagnosi predette
    
    Returns
    -------
    occDict: dict
        Lo stesso dizionario ricevuto in input, in cui cambiano solo i valori,
        che ora esprimono un rapporto
    """
    #funzione che restituisce un dizionario con le percentuali delle diagnosi
    for i in occDict.keys():
        occDict[i] = occDict[i]/listSize    
    return occDict
    
def sortDict(dictionary, rev):
    """
    Funzione che ordina le tupkle di un dizionario in base ai valori
    
    Parameters
    ----------
    dictionary: dict
        Dizionario da ordinare
    rev: boolean
        Vale True se si vuole orinare in maniera decrescente, False altrimenti
    
    Returns
    -------
    list
        Lista di tuple ordinate
    """
    return sorted(dictionary.items(), key = lambda kv:(kv[1], kv[0]), reverse = rev)


def toDict(list):
    """
    Funzione che converte una lista di tuple in un dizionario
    
    Parameters
    ----------
    list: list
        lista da convertire
    
    Returns
    -------
    d: dict
        Dizionario finale
    """
    d = {}
    for i in list:
        d[i[0]] = i[1]
    return d

    
def findNameDiagn(conn, listDiagn):
    """
    Funzione che ad ogni id di una diagnosi associa il corrispondente nome
    
    Parameters
    ----------
    conn: connection
        Connessione al database
    listDiagn: list
        Lista di id delle diagnosi
    
    Returns
    -------
    finalDict: dict
        Dizionario in cui le chiavi sono i nomi delle diagnosi e i valori sono 
        le rispettive percentuali
    """
    finalDict = {}
    cursor = conn.cursor()
    for i in listDiagn:
        finalDict[SQL.findDiagnName(cursor, i[0])] = i[1]
    return finalDict


def tabulateDictionary(dictionary, nameCol1, nameCol2, unitOfMeasure):
    """
    Funzione che mette in una tabella i valori di un dizionario
    
    Parameters
    ----------
    dictionary: dict
        Dizionario da tabulare
    nameCol1: str
        Nome della prima colonna
    nameCol2: str
        Nome della seconda colonna
    unitOfMeasure: str
        Stringa o carattere da affiancare ai dati riportati nella seconda 
        colonna. Può valere 'km' o '%'
    
    Returns
    -------
    df: DataFrame
        Tabella finale
    """
    import pandas as pd
    col1 = list(dictionary.keys())
    col2 = list(str(v)+ unitOfMeasure for v in dictionary.values())
    d = {nameCol1: col1, nameCol2: col2 }
    df = pd.DataFrame(data = d)
    pd.set_option('display.max_rows', None)
    return df


def main():
    
    conn = SQL.SQLConnect()
    print("Insert your symptoms. Enter '/' to stop insertion.")
    list = read_symptoms(conn)
    
    diagn = SQL.searchDiagn(conn,list)
    mergedList = mergeList(diagn)
    #print(("Merged list:", mergedList))
    categories = SQL.searchSymCategories(conn,list)
    percList = BayesianNet.probSymCat(categories)
    condProbList = BayesianNet.probDiagnose(percList)
    weightProb = BayesianNet.weightedProbCat(percList,condProbList)
    defListCat = BayesianNet.defProbCat(weightProb)
    
    occDict = countOcc(mergedList)
    dictDiagn = percOfDiagn(len(mergedList),occDict)
    dictDiagn = BayesianNet.finalProbDiagn(conn, defListCat, dictDiagn)
    listDiagn = sortDict(dictDiagn, True)        #La funzione di sorting restituisce una lista di tuple
    finalDict = findNameDiagn(conn, listDiagn)
    df = tabulateDictionary(finalDict, 'DIAGNOSIS', 'PROBABILITY', '%')
    print(df)
    
    print("\nWhich disease would you like to test or cure?")
    diseaseID = getDiseaseName(conn)
    print("\nInsert your city name. Add your address for a better localization.")
    city = getLocation()
    places = GeoLocation.findBestPlaces(conn, diseaseID, city)
    places = sortDict(places, False)
    places = toDict(places)
    print("\n\n Here are the closest hospitals that can help you:")
    tab = tabulateDictionary(places, 'HOSPITALS', 'DISTANCE', 'km')
    print(tab)
    
    
    SQL.closeConn(conn)
    
    
    