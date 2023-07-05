'''
Created on November 12, 2016

@author: bgray
'''

import sys
import os
import site

import tkinter as tk    #Python 3
#import Tkinter as tk    #Python 2

class Container(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.state = False

        self.resizable(width=False, height=False)

        self.numWindows = 0
        self.windows = []

    def gridConfig(self, rowIdx=None, rowWeight=None, colIdx=None, colWeight=None):
        if rowIdx is not None:
            self.grid_rowconfigure(index=rowIdx, weight=rowWeight)
        if colIdx is not None:
            self.grid_columnconfigure(index=colIdx, weight=colWeight)

    def configContainers(self, container, *args):
        for coords in args:
            for rx, rw, cx, cw in coords:
                container.gridConfig(rx, rw, cx, cw)

    def getScreenDimensions(self):
        return [self.winfo_screenwidth(), self.winfo_screenheight()]

    def getContainerDimensions(self):
        return [self.winfo_width(), self.winfo_height()]

    def setMinSize(self, winX, winY):
        self.minsize(width=int(winX), height=int(winY))

    def setResizable(self, winWidth, winheight):
        self.resizable(width=winWidth, height=winheight)

    def setFrameIcon(self, filename):
        if filename.find('\\') is not -1:
            self.iconbitmap(filename)
        else:
            self.iconbitmap(self.getIconFile(filename))

    def addWindow(self, window, rowNum, colNum, sticky=None, cSpan=None, rSpan=None):
        self.numWindows = self.numWindows + 1
        window.grid(row=rowNum, column=colNum, sticky=sticky, rowspan=rSpan,
                    columnspan=cSpan)
        self.windows.append(window)

    def toggleFullScreen(self):
        self.state = not self.state  # Change state boolean
        self.attributes('-fullscreen', self.state)
        return 'break'

    def setFullScreen(self):
        self.state = True  # Change state boolean
        self.attributes('-fullscreen', self.state)

    def getIconFile(self, filename):
        if getattr(sys, 'frozen', False):
            datadir = os.path.join(os.path.dirname(sys.executable), 'icns')
        else:
            datadir = os.path.join(site.getsitepackages()[0], 'icns')
        return os.path.join(datadir, filename)

    def startLoop(self):
        self.mainloop()

    def endLoop(self):
        self.quit()
