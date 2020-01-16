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

        

def main():
    
    conn = SQL.SQLConnect()
    print("Insert your symptoms. Type '/' to stop insertion.")
    list = read_symptoms(conn)
    
    categories = SQL.searchSymCategories(conn,list)
    percList = BayesianNet.percentSymCat(categories)
    BayesianNet.probDiagnose(percList)
    
    #print(list)
    
    SQL.searchDiagn(conn,list)
    
    