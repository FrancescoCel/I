# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:37:07 2019

@author: franc
"""
def read_symptoms():
    list = []
    stop = "/"
    while True:
        value = input()
        if value == stop:
            break
        list.append(value)
    
    return list

        

def main():
    print("Insert your symptoms. Type '/' to stop insertion.")
    list = read_symptoms()
    print(list)

    