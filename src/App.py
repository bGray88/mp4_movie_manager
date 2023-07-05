'''
Created on November 12, 2016

@author: bgray
'''

import tkinter as tk    #Python 3
#import Tkinter as tk    #Python 2

import Container
import ctypes

appid = u'mp4movieman.version00'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

class App():
    
    def __init__(self):
        self.container = Container.Container()
        self.container.wm_title('MP4 Movie Manager')
        
        self.screenSize = self.container.getScreenDimensions()
        self.windowedWidth = self.screenSize[0]/2
        self.windowedHeight = self.screenSize[1]/2
        self.container.setMinSize(self.windowedWidth, self.windowedHeight)
        
        self.container.focus_set()
        self.container.bind('<Key>', self.keyBind)
        
    def startApp(self):
        self.container.startLoop()
        
    def endApp(self):
        self.container.endLoop()
        
    def keyBind(self, event):
        self.inputProcess(event.keysym)
    
    def inputProcess(self, event):
        if event=='Escape':
            self.container.endLoop()
        if event=='F11':
            self.container.toggleFullScreen()
    