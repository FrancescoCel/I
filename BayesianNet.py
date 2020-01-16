# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 10:45:33 2019

@author: utente
"""

def probDiagnose():
    import pomegranate as pg
    
    sym = pg.DiscreteDistribution({'Gen': 1./3, 'Sup': 1./3, 'Inf': 1./3})
    diagn = pg.ConditionalProbabilityTable(
            [['Gen','Gen',1],
             ['Gen','Sup',0.5],
             ['Gen','Inf',0.5],
             ['Sup','Gen',0.5],
             ['Sup','Sup',1],
             ['Sup','Inf',0],
             ['Inf','Gen',0.5],
             ['Inf','Sup',0],
             ['Inf','Inf',1]],[sym])
    
    s1 = pg.State(sym, name = "sym")
    s2 = pg.State(diagn, name = "diagn")
    
    model = pg.BayesianNetwork("Diagnose finder")
    model.add_states(s1, s2)
    model.add_edge(s1, s2)
    model.bake()
    
    beliefs1 = model.predict_proba({'sym' : 'Gen'})
    
    beliefs1 = map(str,beliefs1)
    
    print("n".join( "{}t{}".format( state.name, belief ) for state, belief in zip( model.states, beliefs1 ) ))
    