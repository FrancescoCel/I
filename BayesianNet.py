# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 10:45:33 2019

@author: utente
"""

def probDiagnose(percList):
    import pomegranate as pg
    print()
    sym = pg.DiscreteDistribution({'Gen': 1./3, 'Sup': 1./3, 'Inf': 1./3})
    diagn = pg.ConditionalProbabilityTable(
            [['Gen','Gen',1],
             ['Gen','Sup',0.5],
             ['Gen','Inf',0.5],
             ['Sup','Gen',0.5],
             ['Sup','Sup',1],
             ['Sup','Inf',0],
             ['Inf','Gen',0.5],
             ['Inf','Sup',0.25],
             ['Inf','Inf',1]],[sym])
    
    s1 = pg.State(sym, name = "sym")
    s2 = pg.State(diagn, name = "diagn")
    
    model = pg.BayesianNetwork("Diagnose finder")
    model.add_states(s1, s2)
    model.add_edge(s1, s2)
    model.bake()
    condProbList = []
    
    for i in percList:
        beliefs1 = model.predict_proba({'sym' : i[1]})
        condProbList.append(beliefs1[1].parameters[0])
        
    
    return condProbList    
            
def weightedProbCat(percList, condProbList):
       #funzione che restituisce le probabilità pesate
       lista = []
       cont = 0
       for i in percList:
           val = i[0]
           temp = {}
           temp['Inf'] = (condProbList[cont])['Inf'] * val
           temp['Sup'] = (condProbList[cont])['Sup'] * val
           temp['Gen'] = (condProbList[cont])['Gen'] * val
           lista.append(temp)
           cont += 1
           
       return lista
   
def defProbCat(weightProb):
    #funzione che restituisce le probabilità definitive delle categorie
    i = 0
    defList = {'Inf':0,'Sup':0,'Gen':0}
    string = 'Inf'
    while i < 3:
        for t in weightProb:
            defList[string] = defList[string]+t[string]
        if i == 0:
            string = 'Sup'
        elif i == 1:
            string = 'Gen'
        i += 1
    return defList
    
    
def percentSymCat(categories):
    #Funzione che restituisce la percentuale della categoria piu' frequente nei sintomi  
    import numpy as np
    infCont = 0
    supCont = 0
    genCont = 0
    percList = []
    categories = np.asarray(categories)
    for i in categories:
        if i == "Inferiore":
            infCont += 1
        elif i == "Generale":
            genCont += 1
        else:
            supCont += 1
           
    if genCont != 0:
        percList.append((genCont/len(categories), "Gen"))
    if infCont != 0:
        percList.append((infCont/len(categories), "Inf"))
    if supCont != 0:
        percList.append((supCont/len(categories), "Sup"))
           
    return percList
        
            
            
            
            
            
            
            
            
            
            
            
            