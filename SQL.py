import mysql.connector

def SQLConnect():
    conn = mysql.connector.connect(host = "localhost", user = "root",password = "checco")
    #conn = mysql.connector.connect(host = 'localhost', user = 'root', password = 'password')
    #conn = mysql.connector.connect(host = 'localhost', user = 'root', password = 'sole1997')
    
    if checkDb(conn) is True:
        
        createDb(conn)
        queryUse(conn)
        executeQueries('diagn_title', 'diagn',conn)
        executeQueries('diffsydiw', 'diff',conn)
        executeQueries('symptoms2', 'sym',conn)
    else:
        print("Database esistente!")
        queryUse(conn)
    
    return conn



def checkDb(conn):
    
    cursor = conn.cursor()
    
    queryCheck = """SHOW DATABASES LIKE 'medical';"""
    cursor.execute(queryCheck)
    check = cursor.fetchall()
    
    if not check:
        return True
    else:
        return False


def createDb(conn):
    import pymysql as sql    
    sql.install_as_MySQLdb()
    import MySQLdb as mysql
    
    cursor = conn.cursor()
    query1 = """CREATE DATABASE medical; """
    query2 = """USE medical; """
    
    try:
         cursor.execute(query1)
         cursor.execute(query2)
         conn.commit()
    except sql.ProgrammingError:
         pass
    
    cursor.close()
    

def queryUse(conn):
    cursor = conn.cursor()
    query = """USE medical;"""
    cursor.execute(query)
    conn.commit()
    
    
    
def executeQueries(filename,tablename,conn):
    import pymysql as sql    
    sql.install_as_MySQLdb()
    import MySQLdb as mysql
    import openpyxl as xl
    
    cursor = conn.cursor()  
    queryDrop = """DROP TABLE IF EXISTS """+ tablename
    
    if filename == 'diagn_title':
        
        #Caricamento del worksheet
        #sheet = xl.load_workbook("C:/Users/utente/ICon/Dataset_xlsx/" + filename +".xlsx")
        sheet = xl.load_workbook("C:/Users/franc/ICon/Dataset_xlsx/" + filename +".xlsx")
        #sheet = xl.load_workbook("C:/Users/nico9/ICon/Dataset_xlsx/" + filename +".xlsx")
        
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
        #sheet = xl.load_workbook("C:/Users/utente/ICon/Dataset_xlsx/" + filename +".xlsx")
        sheet = xl.load_workbook("C:/Users/franc/ICon/Dataset_xlsx/" + filename +".xlsx")
        #sheet = xl.load_workbook("C:/Users/nico9/ICon/Dataset_xlsx/" + filename +".xlsx")
        
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
        #sheet = xl.load_workbook("C:/Users/utente/ICon/Dataset_xlsx/" + filename +".xlsx")
        sheet = xl.load_workbook("C:/Users/franc/ICon/Dataset_xlsx/" + filename +".xlsx")
        #sheet = xl.load_workbook("C:/Users/nico9/ICon/Dataset_xlsx/" + filename +".xlsx")
        
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
    


def checkSymWithErr(conn,value):
    #Funzione che verifica se un determinato sintomo inserito è corretto
    cursor = conn.cursor(buffered = True)
    querySym = """SELECT _id from sym where name='""" + value +"""';""" 
    cursor.execute(querySym)
    check = cursor.fetchall()
    if not check:
        return False
    else:
        return True
        
    

def searchDiagn(conn,list):
    import numpy as np
    
    cursor = conn.cursor(buffered = True)
    idDiseases = []
    idSymptoms = []
    
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
    checkDiagnName(idDiseases,cursor)
        

def checkDiagnName(idDiseases,cursor):
    #Funzione che restituisce le diagnosi per i vari sintomi
    import numpy as np
    diagnName = []
    
    for i in idDiseases:
        i = np.asarray(i)
        for a in range(0,len(i)):
            #Query che restituisce i nomi delle diagnosi associati all'id
            queryName = """SELECT title from diagn where id ='"""+i[a][0]+"""';"""
            cursor.execute(queryName)
            diagnName.append(cursor.fetchall())
    print(diagnName)  


def closeConn(conn):
    conn.close()
