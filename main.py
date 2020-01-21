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
    
    mergedList = []
    for i in range (0,len(diagn)):
        mergedList += diagn[i]
        
    print(mergedList)
    
def main():
    
    conn = SQL.SQLConnect()
    print("Insert your symptoms. Type '/' to stop insertion.")
    list = read_symptoms(conn)
    
    diagn = SQL.searchDiagn(conn,list)
    print(diagn)
    categories = SQL.searchSymCategories(conn,list)
    percList = BayesianNet.percentSymCat(categories)
    condProbList = BayesianNet.probDiagnose(percList)
    weightProb = BayesianNet.weightedProbCat(percList,condProbList)
    defList = BayesianNet.defProbCat(weightProb)
    #print(list)
    
   
    
    