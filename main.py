# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:37:07 2019

@author: franc
"""
import mysql.connector
import SQL

def read_symptoms(conn):
    list = []
    stop = "/"
    while True:
        value = input()
        if value != stop:
            value = SQL.checkSymWithErr(conn,value)
        if value == stop:
            break
        list.append(value)
    
    return list

        

def main():
    
    conn = SQL.SQLConnect()
    print("Insert your symptoms. Type '/' to stop insertion.")
    list = read_symptoms(conn)
    
    print(list)
    
    SQL.searchDiagn(conn,list)
    
    