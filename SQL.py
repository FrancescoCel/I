import mysql.connector



def executeQueries(filename,tablename,conn):
    import pymysql as sql    
    sql.install_as_MySQLdb()
    import MySQLdb as mysql
    import openpyxl as xl
    
    cursor = conn.cursor()  
    
    queryDrop = """DROP TABLE IF EXISTS """+ tablename
    
    if filename == 'diagn_title':
        
        #Caricamento del worksheet
        sheet = xl.load_workbook("C:/Users/utente/ICon/Dataset_xlsx/" + filename +".xlsx")
        #sheet = xl.load_workbook("C:/Users/franc/ICon/Dataset_xlsx/" + filename +".xlsx")
        table = sheet['id']
    
        #Query per la creazione della tabella del file diagn_title.xlsx
        queryCreate = """CREATE TABLE """+ tablename + """(
                    id VARCHAR(30),
                    title text);"""
 
       #Query per l'inserimento dei dati nella tabella
        insertQuery = """INSERT INTO """+ tablename +"""(
                     id,title) VALUES(%s,%s);"""
        
    elif filename == 'diffsydiw':
        
        #Caricamento del worksheet
        sheet = xl.load_workbook("C:/Users/utente/Desktop/Progetto ICon/Dataset/Dataset_xlsx/" + filename +".xlsx")
        #sheet = xl.load_workbook("C:/Users/franc/ICon/Dataset_xlsx/" + filename +".xlsx")
        table = sheet['syd']
        
        #Query per la creazione della tabella del file diffsydiw.xlsx
        queryCreate = """CREATE TABLE """+ tablename + """(
                    syd VARCHAR(10),
                    did VARCHAR(20));"""
        
        #Query per l'inserimento dei dati nella tabella
        insertQuery = """INSERT INTO """+ tablename +"""(
                     syd,did) VALUES(%s,%s);"""
        
    elif filename == 'symptoms2':    
        
        #Caricamento del worksheet
        sheet = xl.load_workbook("C:/Users/utente/Desktop/Progetto ICon/Dataset/Dataset_xlsx/" + filename +".xlsx")
        #sheet = xl.load_workbook("C:/Users/franc/ICon/Dataset_xlsx/" + filename +".xlsx")
        table = sheet['_id']
        
        #Query per la creazione della tabella del file symptoms2.xlsx
        queryCreate = """CREATE TABLE """+ tablename + """(
                    _id VARCHAR(40),
                    name text);"""
        
        #Query per l'inserimento dei dati nella tabella
        insertQuery = """INSERT INTO """+ tablename +"""(
                     _id ,name) VALUES(%s,%s);"""
    
    try:
        cursor.execute(queryDrop)
        cursor.execute(queryCreate)
        conn.commit()
    except sql.ProgrammingError:
        pass
    
    for row in table.rows:
        
        if filename == 'symptoms2':
             _id = row[0].value
             name = row[3].value
             values = (_id,name)
             #Esecuzione query
             cursor.execute(insertQuery,values)
        elif filename == 'diffsydiw':
            syd = row[0].value
            did = row[1].value
            values = (syd,did)
            #Esecuzione query
            cursor.execute(insertQuery,values)
        elif filename == 'diagn_title':
            id = row[0].value
            title = row[1].value
            values = (id,title)
            #Esecuzione query
            cursor.execute(insertQuery,values)
    cursor.close()      
    #Commit della transazione
    conn.commit()
    
def createDb(conn):
    import pymysql as sql    
    sql.install_as_MySQLdb()
    import MySQLdb as mysql
    
    cursor = conn.cursor()
    query1 = """DROP DATABASE IF EXISTS medical;"""
    query2 = """CREATE DATABASE medical; """
    query3 = """USE medical; """
    
    try:
         cursor.execute(query1)
         cursor.execute(query2)
         cursor.execute(query3)
         conn.commit()
    except sql.ProgrammingError:
         pass
    
    cursor.close()
    
def SQLConnect():
    
    
    conn = mysql.connector.connect(host = "localhost",
                                   user = "root",
                                   password = "checco")
    
    #conn = mysql.connector.connect(host = "localhost", user = "root", password = "password")
    
    createDb(conn)
    executeQueries('diagn_title', 'diagn',conn)
    executeQueries('diffsydiw', 'diff',conn)
    executeQueries('symptoms2', 'sym',conn)
    
    
    
    return conn

def closeConn(conn):
    conn.close()
    
def searchDiagn(conn,list):
    import numpy as np
    
    cursor = conn.cursor(buffered = True)
    idSymptoms = []
    idDiseases = []
    
    for i in list:
        #Query che preleva l'id corrispondenti ai sintomi
        querySym = """SELECT _id from sym where name='""" + i +"""';""" 
        cursor.execute(querySym)
        idSymptoms.append(cursor.fetchall()) 

    
    for i in idSymptoms:
        i = np.asarray(i)
        #Query che restituisce l'id delle malattie collegate all'id dei sintomi(colonna did nella tabella)
        queryDid = """SELECT did from diff where syd='"""+ i[0][0] +"""';"""
        cursor.execute(queryDid)
        idDiseases.append(cursor.fetchall())
        
    print(idDiseases)   
        



      
