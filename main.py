# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:37:07 2019

@author: franc
"""
import mysql.connector
import SQL
import BayesianNet

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
                    print("Last symptom inserted is wrong. Insert a valid one.")
                    value = input()
            list.append(value)
        else:
            break
    return list

        
def mergeList(diagn):
    #funzione che unisce le liste delle diagnosi associate ai sintomi
    mergedList = []
    for i in range (0,len(diagn)):
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
    
def sortDictDiagn(dictDiagn):
    #funzione che ordina i valori del dizionario con le diagnosi
    return sorted(dictDiagn.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)

    
def findNameDiagn(conn, listDiagn):
    finalDict = {}
    cursor = conn.cursor()
    for i in listDiagn:
        finalDict[SQL.checkDiagnName(cursor, i[0])] = i[1]
    return finalDict

def tabulateDictionary(finalDict):
    import pandas as pd
    diagn = list(finalDict.keys())
    prob = list(str(v)+" %" for v in finalDict.values())
    d = {'DIAGNOSIS': diagn, 'PROBABILITY': prob }
    df = pd.DataFrame(data = d)
    pd.set_option('display.max_rows', None)
    return df
    

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
    listDiagn = sortDictDiagn(dictDiagn)        #La funzione di sorting restituisce una lista di tuple
    finalDict = findNameDiagn(conn, listDiagn)
    
    df = tabulateDictionary(finalDict)
    print(df)
    
    