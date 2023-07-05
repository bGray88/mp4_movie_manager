'''
Created on November 12, 2016

@author: bgray
'''

import tkinter as tk    #Python 3
#import Tkinter as tk    #Python 2

import Window
import datetime
import threading

class StatusBar(Window.Window):
    
    def __init__(self, container, title=None, screen=None):
        super().__init__(container)
        self.titlevariable = tk.StringVar() 
        self.screenvariable = tk.StringVar() 
        self.progressvariable = tk.StringVar() 
        self.datevariable = tk.StringVar()
        
        self.titleLabel = tk.Label(self, foreground='GRAY', relief=tk.SUNKEN, 
                                   anchor='w', textvariable=self.titlevariable,
                                   font=('arial', 10, 'normal'))
        self.middleLabel = tk.Label(self, foreground='GRAY', relief=tk.SUNKEN, 
                                   anchor='w', textvariable=self.screenvariable,
                                   font=('arial', 10, 'normal'))
        self.endLabel = tk.Label(self, foreground='GRAY', relief=tk.SUNKEN, 
                                   anchor='w', textvariable=self.progressvariable,
                                   font=('arial', 10, 'normal'))
        self.progressLabel = tk.Label(self, foreground='GRAY', relief=tk.SUNKEN, 
                                   anchor='w', textvariable=self.datevariable,
                                   font=('arial', 10, 'normal'))
        self.runLabel = tk.Label(self, background='LIGHTGREEN', relief=tk.SUNKEN,
                                 padx=5, anchor='center')
        
        self.titlevariable.set(title)
        self.screenvariable.set(screen)
        
        self.timeThread = threading.Thread(target=self.updateTime)
        self.timeThread.daemon = True
        self.timeThread.start()
        
        self.addWindow(self.titleLabel, 0, 0, 'nsew')
        self.addWindow(self.middleLabel, 0, 1, 'nsew')
        self.addWindow(self.endLabel, 0, 2, 'nsew')
        self.addWindow(self.progressLabel, 0, 3, 'nsew')
        self.addWindow(self.runLabel, 0, 4, 'nsew')
        
    def destroyBar(self):
        super(Window, self).destroy()
    
    def setTitle(self, txtTitle):
        self.titlevariable.set(txtTitle)
        
    def setScreen(self,txtScreen):
        self.screenvariable.set(txtScreen)
        
    def setProgress(self, txtProgress):
        self.progressvariable.set(txtProgress)
        
    def setRunStatus(self, background):
        self.runLabel.config(background=background)
        
    def updateTime(self):
        self.currentTime = datetime.datetime.now().ctime()
        if self.currentTime is not self.datevariable:
            self.datevariable.set(datetime.datetime.now().ctime())
        self.after(200, self.updateTime)
                