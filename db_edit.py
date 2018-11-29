import sqlite3   #enable control of an sqlite database

DB_FILE="smapify.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#info is a list of fieldValues in order without primary key
def insert(tableName, info):
    '''inserts data into certain table, taking info as a list of parameters'''
    # collect Column Data Names in strings
    # c.execute('PRAGMA TABLE_INFO({})'.format(tableName))
    c.execute('PRAGMA TABLE_INFO({})'.format(tableName))
    colNames = ''
    i = 0
    tbl = c.fetchall()
    for cols in tbl:
        if tableName == 'users':
            if i != len(tbl) - 1:
                colNames += "'" + cols[1] + "'"+ ','
                i += 1
        else:
            if i == 0:
                i += 1 # primary key will update itself
            else:
                colNames += "'" + cols[1] + "'"+ ','
    colNames = colNames[:-1]
    print ('column names')
    print (colNames)
    values = ''
    for val in info:
        values += "'" + str(val) + "'" + ","
    values = values[:-1]
    print("INSERT INTO {0}({1}) VALUES ({2})".format(tableName,
                                                          colNames ,
                                                          values  ))
    c.execute("INSERT INTO {0}({1}) VALUES ({2})".format(tableName,
                                                          colNames ,
                                                          values  ))
    db.commit()

def findInfo(tableName,filterValue,colToFilt, sortCol = None, notEqual = None, fetchOne = None, asSubstring= False):
    '''returns entire record with specific value at specific column from specified db table'''
    if notEqual:
        boolEqual = '!'
    else:
        boolEqual = ''

    if sortCol:
        sortQuery = 'ORDER BY {}'.format(sortCol)
    else:
        sortQuery = ''

    if asSubstring:
        filterValue = '%' + filterValue + '%'
        eq = 'LIKE'
    else:
        eq = '='

    command = "SELECT * FROM  '{0}'  WHERE {1} {3}{4} '{2}'".format(tableName,colToFilt,filterValue, boolEqual, eq)
    command += sortQuery
    c.execute(command)

    listInfo = []
    if fetchOne:
        info = c.fetchone()
    else:
        info = c.fetchall()

    if info:
        for col in info:
            #print(col)-
            listInfo.append(col)
    return listInfo

def modify(tableName, colToMod, newVal, filterIndex, filterValue):
    print(("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'").format(tableName, colToMod, newVal, filterIndex, filterValue))
    c.execute(("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'").format(tableName, colToMod, newVal, filterIndex, filterValue))
    db.commit()

def delete(tableName, filterIndex, filterValue):
    print(("DELETE FROM {0} WHERE {1} = '{2}'").format(tableName, filterIndex, filterValue))
    c.execute(("DELETE FROM {0} WHERE {1} = '{2}'").format(tableName, filterIndex, filterValue))
    db.commit()

def checkApos(string):
    '''Fixes strings with apostrophers'''
    i = -1
    aposIndexes = []
    while True:
        i = string.find("'", i + 1)
        if i == -1: break
        aposIndexes.append(i)
    j = 0
    for index in aposIndexes:
        string = string[:index +j ] + "'" + string[index+ j:]
        j += 1
    return string
