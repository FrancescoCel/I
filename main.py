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
    goodVal = False
    while goodVal is False:
        diseaseName = input()
        goodVal = SQL.checkDiseaseWithErr(conn, diseaseName)
        if not goodVal:
            print("You entered a wrong value. Please insert a valid one.")
    return goodVal.lower()

def mergeList(diagn):
    #funzione che unisce le liste delle diagnosi associate ai sintomi
    mergedList = []
    for i in range (0, len(diagn)):
        mergedList += diagn[i]   
    return mergedList

def countOcc(mergedList):
    #funzione che restituisce un dizionario con diagnosi e numero delle occorrenze
    occDict = {}
    
    for i in mergedList:
        if i not in occDict.keys():
            occDict[i] = mergedList.count(i)
   
    return occDict

def percOfDiagn(listSize,occDict):
    #funzione che restituisce un dizionario con le percentuali delle diagnosi
    for i in occDict.keys():
        occDict[i] = occDict[i]/listSize    
    return occDict
    
def sortDict(dictionary, rev):
    #funzione che ordina i valori del dizionario con le diagnosi
    return sorted(dictionary.items(), key = lambda kv:(kv[1], kv[0]), reverse = rev)

    
def findNameDiagn(conn, listDiagn):
    finalDict = {}
    cursor = conn.cursor()
    for i in listDiagn:
        finalDict[SQL.checkDiagnName(cursor, i[0])] = i[1]
    return finalDict

def tabulateDictionary(dictionary, nameCol1, nameCol2, unitOfMeasure):
    import pandas as pd
    col1 = list(dictionary.keys())
    col2 = list(str(v)+ unitOfMeasure for v in dictionary.values())
    d = {nameCol1: col1, nameCol2: col2 }
    df = pd.DataFrame(data = d)
    pd.set_option('display.max_rows', None)
    return df

def toDict(list):
    d = {}
    for i in list:
        d[i[0]] = i[1]
    return d



def main():
    
    conn = SQL.SQLConnect()
    print("Insert your symptoms. Type '/' to stop insertion.")
    list = read_symptoms(conn)
    
    diagn = SQL.searchDiagn(conn,list)
    mergedList = mergeList(diagn)
    categories = SQL.searchSymCategories(conn,list)
    percList = BayesianNet.percentSymCat(categories)
    condProbList = BayesianNet.probDiagnose(percList)
    weightProb = BayesianNet.weightedProbCat(percList,condProbList)
    defListCat = BayesianNet.defProbCat(weightProb)
    
    occDict = countOcc(mergedList)
    dictDiagn = percOfDiagn(len(mergedList),occDict)
    dictDiagn = BayesianNet.finalProbDiagn(conn, defListCat, dictDiagn, mergedList)
    listDiagn = sortDict(dictDiagn, True)        #La funzione di sorting restituisce una lista di tuple
    finalDict = findNameDiagn(conn, listDiagn)
    df = tabulateDictionary(finalDict, 'DIAGNOSIS', 'PROBABILITY', '%')
    print(df)
    
    print("\nWhich disease would you like to test or cure?")
    diseaseID = getDiseaseName(conn)
    print("\nInsert your city name. Add your address for a better localization.")
    city = input()
    places = GeoLocation.findBestPlaces(conn, diseaseID, city)
    places = sortDict(places, False)
    places = toDict(places)
    print("\n\n Here are the closest hospitals that can help you:")
    tab = tabulateDictionary(places, 'HOSPITALS', 'DISTANCE', 'km')
    print(tab)
    
    
    