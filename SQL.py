def executeQueries(filename,tablename,conn):
    import pymysql as sql
    sql.install_as_MySQLdb()
    import MySQLdb as mysql
    import openpyxl as xl
    
    cursor = conn.cursor()  
    
    queryDrop = """DROP TABLE IF EXISTS """+ tablename
    
    if filename == 'diagn_title':
        
        #Caricamento del worksheet
        sheet = xl.load_workbook("C:/Users/utente/Desktop/Progetto ICon/Dataset/Dataset_xlsx/" + filename +".xlsx")
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
        table = sheet['chief_complaint_id']
        
        #Query per la creazione della tabella del file symptoms2.xlsx
        queryCreate = """CREATE TABLE """+ tablename + """(
                    chief_complaint_id VARCHAR(40),
                    name text);"""
        
        #Query per l'inserimento dei dati nella tabella
        insertQuery = """INSERT INTO """+ tablename +"""(
                     chief_complaint_id ,name) VALUES(%s,%s);"""
    
    try:
        cursor.execute(queryDrop)
        cursor.execute(queryCreate)
        conn.commit()
    except sql.ProgrammingError:
        pass
    
    for row in table.rows:
        
        if filename == 'symptoms2':
             chief_complaint_id = row[1].value
             name = row[3].value
             values = (chief_complaint_id,name)
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
             
    #Commit della transazione
    conn.commit()
    
    
    
def SQLConnect():
    import pymysql as sql
    sql.install_as_MySQLdb()
    import MySQLdb as mysql
    #import openpyxl as xl

    """
    sheet = xl.load_workbook("C:/Users/utente/Desktop/Progetto ICon/Dataset/dia_3.xlsx")
    table = sheet['_id']
    """
    
    server = 'localhost'
    db = 'medical'
    pword = 'checco'
    user = 'root'
    conn = mysql.connect(server,user,pword,db)
    
    executeQueries('diagn_title', 'diagn',conn)
    executeQueries('diffsydiw', 'diff',conn)
    executeQueries('symptoms2', 'sym',conn)
    
    
   # cursor = conn.cursor()
    
   # queryDrop = """DROP TABLE IF EXISTS sym  """
   # queryCreate = """CREATE TABLE sym(
   #             _id VARCHAR(30),
   #             diagnose text);"""
   # insertQuery = """INSERT INTO sym(
   #                  _id,diagnose) VALUES(%s,%s);"""
   # 
   # try:
   #     cursor.execute(queryDrop)
   #     cursor.execute(queryCreate)
   #     conn.commit()
   # except sql.ProgrammingError:
   #     pass
   # 
   # for row in table.rows:
   #      _id = row[0].value
   #      diagnose = row[1].value
   #      values = (_id,diagnose)
   #      #Esecuzione query
   #      cursor.execute(insertQuery,values)
   # 
    #Commit della transazione
   # conn.commit()
    
    
    #Chiusura databse
    conn.close()







      