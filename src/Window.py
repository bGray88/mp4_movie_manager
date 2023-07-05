'''
Created on November 12, 2016

@author: bgray
'''

import tkinter as tk    #Python 3
#import Tkinter as tk    #Python 2

class Window(tk.Frame):
    
    def __init__(self, container, winWidth=None, winHeight=None, bgColor=None):
        tk.Frame.__init__(self, container, width=winWidth, height=winHeight, background=bgColor)
        self.container = container
        
        self.numButtons = 0
        self.buttons = []
        self.numWindows = 0
        self.windows = []
        self.numInWindows = 0
        self.inWindows = []
        
    def gridConfig(self, rowIdx=None, rowWeight=None, colIdx=None, colWeight=None):
        if rowIdx is not None:
            self.grid_rowconfigure(index=rowIdx, weight=rowWeight)
        if colIdx is not None:
            self.grid_columnconfigure(index=colIdx, weight=colWeight)
            
    def configWindows(self, window, *args):
        for coords in args:
            for rx, rw, cx, cw in coords:    
                window.gridConfig(rx, rw, cx, cw)
                
    def padConfig(self, padX=None, padY=None):
        if padX is not None:
            self.grid_configure(padx=padX, pady=padY)
            
    def windowCustomize(self, borderwidth=None, relief=None, cursor=None):
        if borderwidth is not None:     
            self.config(borderwidth=borderwidth)
        if relief is not None:     
            self.config(relief=relief)
        if relief is not None:     
            self.config(cursor=cursor)
        
    def createInnerFrame(self):
        self.numInWindows = self.numInWindows + 1
        inner = tk.Toplevel()
        self.inWindows.append(inner)
        
    def addWindow(self, window, rowNum, colNum, sticky=None, cSpan=None, rSpan=None):
        self.numWindows = self.numWindows + 1
        window.grid(row=rowNum, column=colNum, sticky=sticky, rowspan=rSpan,
                    columnspan=cSpan)
        self.windows.append(window)
        
    def createButton(self, text, bg, fg, cmnd, height, width):
        self.numButtons = self.numButtons + 1
        return (tk.Button(self,
                           text=text,
                           bg=bg,
                           fg=fg,
                           command=cmnd, 
                           height=height,
                           width=width)
                           )
        
    def placeButton(self, button, rowNum, colNum, sticky=None):
        self.numButtons = self.numButtons + 1
        self.buttons.append(button)
        button.grid(row=rowNum, column=colNum, sticky=sticky)
