# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 20:46:51 2019

@author: Francesco
"""

from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import SQL
import numpy as np


def numberOfSons(conn, symIdList):
    mat = np.zeros((len(symIdList), 2))
    for i in range (0, len(symIdList)):
        mat[i][0] = symIdList[i][0]         
        mat[i][1] = SQL.numOfRelatedDiseases(conn, symIdList[i][0])
    return mat
   
    
def buildNet(data, conn):
    model = BayesianModel(data)
    checkedSymp = list()    #Lista dei sintomi già visitati ed aggiunti alla rete
    checkedDis = list()     #Lista delle malattie già aggiunte alla rete
    
    
    #Costruzione dei nodi parents della rete
    for t in data:
        if t[0] not in checkedSymp:
            cpd = TabularCPD(variable = t[0],variable_card = 2,values=[[0.5, 0.5]])
            checkedSymp.append(t[0])
        model.add_cpds(cpd)
    #Costruzione dei nodi figli, collegandoli ai rispettivi parent
    for t in data:
        if t[1] not in checkedDis:
            sym_list = SQL.symList(conn, t[1])      #Ricavo la lista di sintomi collegati alla malattia
            sym_list_length = len(sym_list)
            mat = numberOfSons(conn, sym_list)
            arr = []
            for i in range(0, len(mat)):
                arr.append(mat[i][1])
            print(arr)
            cpd = TabularCPD(variable = t[1],
                             variable_card = sym_list_length,
                             values = np.full((1, sym_list_length), 1/sym_list_length),
                             evidence = sym_list,
                             evidence_card = arr
                             )
            break
            checkedDis.append(t[1])
        model.add_cpds(cpd)
    return model

def check_model(model):
    return model.check_model()
