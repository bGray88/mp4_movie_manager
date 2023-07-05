'''
Created on November 12, 2016

@author: bgray
'''

import os
import datetime

class LogFile():
    
    def __init__(self, path, logName):
        self.logPath = (os.path.normpath(path + '.log'))
        self.logName = logName
        self.printHeader(self.logName)
        
    def printHeader(self, logHeader):
        self.logTxt = open(self.logPath, 'a')
        self.logTxt.write('\n\n' + logHeader + '\n')
        self.logTxt.write(datetime.datetime.now().ctime() + '\n')
        self.logTxt.write('----------------------------------------\n')
        self.logTxt.close()
        
    def logMsg(self, msgContents):
        self.logTxt = open(self.logPath, 'a')
        self.logTxt.write(msgContents)
        self.logTxt.close()
        