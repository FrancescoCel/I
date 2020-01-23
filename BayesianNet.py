# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 10:45:33 2019

@author: utente
"""

def probDiagnose(percList):
    import pomegranate as pg
    sym = pg.DiscreteDistribution({'gen': 192./389, 'sup': 125./389, 'inf': 72./389})
    diagn = pg.ConditionalProbabilityTable(
            [['gen','gen',0.5],
             ['gen','sup',0.25],
             ['gen','inf',0.25],
             ['sup','gen',0.20],
             ['sup','sup',0.75],   
             ['sup','inf',0.05],
             ['inf','gen',0.2],
             ['inf','sup',0.05],
             ['inf','inf',0.75]],[sym])
    
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
           temp['inf'] = (condProbList[cont])['inf'] * val
           temp['sup'] = (condProbList[cont])['sup'] * val
           temp['gen'] = (condProbList[cont])['gen'] * val
           lista.append(temp)
           cont += 1
           
       return lista
   
def defProbCat(weightProb):
    #funzione che restituisce le probabilità definitive delle categorie
    i = 0
    defList = {'inf':0,'sup':0,'gen':0}
    string = 'inf'
    while i < 3:
        for t in weightProb:
            defList[string] = defList[string]+t[string]
        if i == 0:
            string = 'sup'
        elif i == 1:
            string = 'gen'
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
        if i == "inf":
            infCont += 1
        elif i == "gen":
            genCont += 1
        else:
            supCont += 1
           
    if genCont != 0:
        percList.append((genCont/len(categories), "gen"))
    if infCont != 0:
        percList.append((infCont/len(categories), "inf"))
    if supCont != 0:
        percList.append((supCont/len(categories), "sup"))
           
    return percList
        
def finalProbDiagn(conn,defListCat, dictDiagn, mergedList):
    #funzione che restituisce un dizionario con diagnosi e la corrispettiva probabilità finale
    import SQL
    for i in dictDiagn.keys():
        categoria = SQL.searchCatDiagn(conn,i[0])
        dictDiagn[i] = dictDiagn[i]*defListCat[categoria[0]]
     
    corr = (1 - sum(dictDiagn.values())) / len(dictDiagn)
    for i in dictDiagn.keys():
        dictDiagn[i] += corr
        dictDiagn[i] = dictDiagn[i]*100
        dictDiagn[i] = round(dictDiagn[i], 4)
    
        
    return dictDiagn         
            
            
            
            
            
            
            
            