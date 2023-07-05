'''
Created on November 12, 2016

@author: bgray
'''

import os
import datetime

class Database():
    
    def __init__(self, path, dbName):
        self.databasePath = (os.path.normpath(path + '.db'))
        self.databaseName = dbName
            
    def printHeader(self, dbHeader):
        self.database = open(self.databasePath, 'w')
        self.database.write('\n\n' + dbHeader + '\n')
        self.database.write(datetime.datetime.now().ctime() + '\n')
        self.database.write('----------------------------------------\n')
        self.database.close()
                
    def readLines(self):
        self.database = open(self.databasePath, 'r')
        arrData = []
        for line in self.database:
            arrData.append(line)
        self.database.close()
        return arrData
        
    def dataEntryWrite(self, msgContents):
        self.database = open(self.databasePath, 'w')
        self.database.write(msgContents)
        self.database.close()
        
    def dataEntryAppend(self, msgContents):
        self.database = open(self.databasePath, 'a')
        self.database.write(msgContents)
        self.database.close()
        
    def dataClearFile(self):
        self.database = open(self.databasePath, 'w').close()
    