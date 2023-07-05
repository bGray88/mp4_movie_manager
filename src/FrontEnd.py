'''
Created on November 12, 2016

@author: bgray
'''

import tkinter as tk    #Python 3
#import Tkinter as tk    #Python 2

import App
import Window
import StatusBar
import os
import FileProcessor
import threading
import PIL

from tkinter.constants import DISABLED, NORMAL

# DO NOT DELETE
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from os.path import normpath
from PIL import Image
from PIL import ImageTk
from PIL import PngImagePlugin

class FrontEnd(App.App):

    def __init__(self):
        super().__init__()

        #self.fileProcessor = FileProcessor.FileProcessor()
        #self.savedFilePaths = self.fileProcessor.getDataSavedPaths()
        self.initialize()

    def initialize(self):
        self.container.setFrameIcon('mp4movieman.ico')
        self.contGridConfig = [[0,20,None,None], [1,10,0,1]]
        self.container.configContainers(self.container, self.contGridConfig)
        try:
            del self.listProcessFiles[:]
        except:
            pass
        self.listProcessFiles = []
        self.mpgFileSelected = ''
        try:
            self.bgdWindow.destroy()
        except:
            pass
        try:
            self.stpWindow.destroy()
        except:
            pass
        try:
            self.chcWindow.destroy()
        except:
            pass
        try:
            self.btnWindow.destroy()
        except:
            pass
        try:
            self.statusBar.destroy()
        except:
            pass
        self.setBgdWindow()
        self.setStpWindow()
        self.setProcChcWindow()
        self.setBtnWindow()
        self.setStatusBarWindow()

    def startProcess(self):
        self.initialize()

    def setEntryText(self, entryObject, start, msgContents, disable=True):
        entryObject.config(state=NORMAL)
        try:
            entryObject.delete(0, tk.END)
        except:
            pass
        entryObject.insert(start, msgContents)
        if disable == True:
            entryObject.config(state=DISABLED)

    def setFocusEntry(self, event):
        event.widget.delete(0, tk.END)

    def createTopLevel(self):
        self.container.withdraw()
        self.top = tk.Toplevel()
        self.top.protocol("WM_DELETE_WINDOW", self.disableEvent)
        self.top.resizable(0,0)
        self.top.lift()
        self.top.attributes('-topmost', True)

    def removeTopLevel(self):
        self.top.destroy()
        self.container.deiconify()

    def browseForFile(self, title, initialdir):
        return tk.filedialog.askopenfilename(title=title,
                                          initialdir=initialdir)

    def browseForFolder(self, title, mustexist, initialdir):
        return tk.filedialog.askdirectory(title=title,
                                          mustexist=mustexist,
                                          initialdir=initialdir)

    def getRootDir(self):
        rootDir = os.path.expanduser("~")
        rootIdx = rootDir.find(os.path.normpath('/'))
        while rootDir.find(os.path.normpath('/'), (rootIdx + 1)) is not -1:
            rootDir = os.path.dirname(rootDir)
        return (os.path.dirname(rootDir))

    def getFileName(self, filepath):
        return normpath(os.path.basename(filepath))

    def disableEvent(self):
        pass

    def setSubsProc(self):
        self.removeTopLevel()
        self.entryMpgMedia = tk.Entry(self.stpWindow, width=70)
        self.entryMpgMedia.config(state=DISABLED)
        self.setEntryText(self.entryMpgMedia, tk.END, 'Select a File')
        ADD_MPG_CMD = lambda: self.setProcMedWindow('ADD')
        self.addMedButton = self.stpWindow.createButton('+', 'BLACK',
                                                   'WHITE', ADD_MPG_CMD, '1', '4')
        REM_MPG_CMD = lambda: self.setProcMedWindow('REMOVE')
        self.remMedButton = self.stpWindow.createButton('-', 'BLACK',
                                                   'WHITE', REM_MPG_CMD, '1', '4')
        self.textProcessFiles = tk.Text(self.stpWindow, wrap=None, height=10, width=70, state=DISABLED)
        ADD_SUBS_CMD = lambda: self.setProcSubsWindow()
        self.addSubsButton = self.stpWindow.createButton('+', 'BLACK',
                                                   'WHITE', ADD_SUBS_CMD, '1', '4')
        REM_SUBS_CMD = lambda: self.setProcSubsWindow()
        self.remSubsButton = self.stpWindow.createButton('-', 'BLACK',
                                                   'WHITE', REM_SUBS_CMD, '1', '4')
        self.msgGridConfig = [[0,1,0,3], [1,1,1,1],
                              [2,1,2,2], [3,1,3,1],
                              [4,1,4,3], [5,1,None,None],
                              [6,1,None,None], [7,1,None,None]]
        self.stpWindow.configWindows(self.stpWindow, self.msgGridConfig)
        self.stpWindow.windowCustomize(1, tk.RAISED)
        self.stpWindow.addWindow(self.entryMpgMedia, 1, 1, '', 3)
        self.stpWindow.placeButton(self.addMedButton, 3, 1, 'we')
        self.stpWindow.placeButton(self.remMedButton, 3, 3, 'we')
        self.stpWindow.addWindow(self.textProcessFiles, 5, 1, '', 3)
        self.stpWindow.placeButton(self.addSubsButton, 7, 1, 'we')
        self.stpWindow.placeButton(self.remSubsButton, 7, 3, 'we')
        self.bgdWindow.addWindow(self.stpWindow, 0, 0, 'nsew', 5)

    def setProcMedWindow(self, action):
        if action == 'REMOVE':
            self.mpgFileSelected = ''
            self.setEntryText(self.entryMpgMedia, tk.END, 'Select a File')
        if action == 'ADD':
            self.setMpgFile()

    def setMpgFile(self):
        rootDir = self.getRootDir()
        self.container.withdraw()
        self.mpgFileSelected = self.browseForFile('Select the File',
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entryMpgMedia, tk.INSERT, self.getFileName(self.mpgFileSelected))
        self.container.deiconify()

    def setProcSubsWindow(self):
        self.createTopLevel()
        self.entrySubsMedia = tk.Entry(self.top)
        self.entrySubsMedia.config(state=DISABLED)
        self.setEntryText(self.entrySubsMedia, tk.END, 'Select a File')
        self.subsIdx = tk.IntVar()
        self.entrySubsIdx = tk.Entry(self.top, textvariable=self.subsIdx)
        self.setEntryText(self.entrySubsIdx, tk.INSERT, 'Index Placement', False)
        self.entrySubsIdx.bind("<Button-1>", self.setFocusEntry)
        browseButton = tk.Button(self.top, text="...", command=self.setSubsFile,
                                 background='LIGHTGRAY')
        exitButton = tk.Button(self.top, text="Select", command=self.setListContents,
                                 background='LIGHTGRAY')
        self.entrySubsMedia.pack(side='left', anchor='w', fill='both')
        browseButton.pack(side='left', anchor='w', fill='both')
        self.entrySubsIdx.pack(side='left', anchor='w', fill='both')
        exitButton.pack(side='left', anchor='w', fill='both')

    def setSubsFile(self):
        rootDir = self.getRootDir()
        self.top.withdraw()
        self.subsFileSelected = self.browseForFile('Select the File',
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entrySubsMedia, tk.INSERT, self.subsFileSelected)
        self.top.deiconify()

    def setListContents(self):
        self.subsIdx.set(self.subsIdx.get()+1)
        if str(self.subsIdx.get()).isnumeric():
            for file in self.listProcessFiles:
                if self.subsFileSelected == file:
                    self.listProcessFiles.remove(file)
            self.listProcessFiles.insert((self.subsIdx.get()-1), self.subsFileSelected)
            self.textProcessFiles.config(state=NORMAL)
            self.textProcessFiles.delete(0.0, tk.END)
            for file in self.listProcessFiles:
                self.textProcessFiles.mark_set('insert', "" + str(self.listProcessFiles.index(file)+1) +
                                               ".0" + "")
                self.textProcessFiles.insert(tk.INSERT, str(self.listProcessFiles.index(file)+1) +
                                             " " + self.getFileName(file) + '\n')
            self.textProcessFiles.config(state=DISABLED)
            self.removeTopLevel()

    def setBgdWindow(self):
        self.bgdWindow = Window.Window(self.container, bgColor='BLACK')
        self.bgdGridConfig = [[None, None, 0, 1],
                              [0, 1, 1, 20]]
        self.bgdWindow.configWindows(self.bgdWindow, self.bgdGridConfig)
        self.container.addWindow(self.bgdWindow, 0, 0, 'nsew')

    def setProcChcWindow(self):
        self.createTopLevel()
        subsButton = tk.Button(self.top, text="Subtitles", command=self.setSubsProc,
                                 background='LIGHTGRAY')
        '''
        audButton = tk.Button(self.top, text="Audio", command=self.setAudProc,
                                 background='LIGHTGRAY')
        avButton = tk.Button(self.top, text="Audio & Video", command=self.setAvProc,
                                 background='LIGHTGRAY')
        convButton = tk.Button(self.top, text="Convert", command=self.setConvProc,
                                 background='LIGHTGRAY')
        '''
        self.top.title('...')
        subsButton.pack(anchor='n', fill='both')
        '''
        audButton.pack(anchor='n', fill='both')
        avButton.pack(anchor='n', fill='both')
        convButton.pack(anchor='n', fill='both')
        '''

    def setStpWindow(self):
        self.stpWindow = Window.Window(self.bgdWindow, bgColor='GOLDENROD')
        self.labelFont = ('bodoni', 14, 'bold')

    def setBtnWindow(self):
        self.btnWindow = Window.Window(self.container, bgColor='BLACK')
        PROCESS_COMMAND = self.startProcess
        self.processButton = self.btnWindow.createButton('Process', 'GRAY',
                                                 'WHITE', PROCESS_COMMAND, '2', '15')
        RESTART_COMMAND = self.initialize
        self.restartButton = self.btnWindow.createButton('Restart', 'GRAY',
                                                 'WHITE', RESTART_COMMAND, '2', '15')
        EXIT_COMMAND = self.endApp
        self.exitButton = self.btnWindow.createButton('Exit', 'GRAY',
                                                 'WHITE', EXIT_COMMAND, '2', '15')
        self.btnGridConfig = [[0,5,None,None], [1,0,None,None],
                              [2,0,0,5], [3,0,1,1],
                              [4,5,2,5]]
        self.processButton.config(state=NORMAL)
        self.exitButton.config(state=NORMAL)
        self.btnWindow.configWindows(self.btnWindow, self.btnGridConfig)
        self.btnWindow.windowCustomize(1, tk.RAISED)
        self.btnWindow.placeButton(self.processButton, 1, 1, 'nsew')
        self.btnWindow.placeButton(self.restartButton, 2, 1, 'nsew')
        self.btnWindow.placeButton(self.exitButton, 3, 1, 'nsew')
        self.container.addWindow(self.btnWindow, 1, 0, 'nsew', 2)

    def setStatusBarWindow(self):
        self.statusBar = StatusBar.StatusBar(self.container, '', '')
        self.statusBar.setTitle('MP4 Movie Manager')
        self.statusBar.setScreen('Menu')
        self.statusBar.padConfig(1, 1)
        self.statGridConfig = [[None,None,0,5], [None,None,1,5],
                              [None,None,2,5], [None,None,3,5],
                              [0,1,4,3]]
        self.bgdWindow.configWindows(self.statusBar, self.statGridConfig)
        self.container.addWindow(self.statusBar, 2, 0, 'nsew', 2)

    '''
    Not Used

    if self.savedFilePaths is not -1 and len(self.savedFilePaths) > 0:
        self.mediaDirSelected = self.savedFilePaths[0].rstrip('\r\n')
        self.titleDirSelected = self.savedFilePaths[1].rstrip('\r\n')
        self.themeDirSelected = self.savedFilePaths[2].rstrip('\r\n')
        self.saveDirSelected = self.savedFilePaths[3].rstrip('\r\n')
    else:
        self.mediaDirSelected = 'Media Path'
        self.titleDirSelected = 'Titles Path'
        self.themeDirSelected = 'Themes Path'
        self.saveDirSelected = 'Save Path'
    self.checkMediaSet = tk.IntVar()
    self.checkTitleSet = tk.IntVar()
    self.checkThemeSet = tk.IntVar()
    self.checkPlaylistSet = tk.IntVar()
    self.checkDatabaseSet = tk.IntVar()
    self.startTimeSelected = '-1'
    self.durationTimeSelected = '-1'
    self.returnMsg = None

    def checkProcessThread(self):
        if self.processThread.is_alive():
            self.container.after(1, self.checkProcessThread)
        else:
            self.completeProcess()
            self.progressBar.stop()

    def runFileProcess(self):
        self.returnMsg = self.fileProcessor.processFiles()

    def startProcess(self):
        if self.saveDirSelected != 'Save Path' and self.saveDirSelected != '':
            startProcessClear = False
            if self.checkMediaSet.get() or self.checkTitleSet.get() or self.checkThemeSet.get() or self.checkPlaylistSet.get() or self.checkDatabaseSet.get():
                if self.checkMediaSet.get() and (self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if self.checkTitleSet.get() and (self.titleDirSelected != 'Titles Path' and self.titleDirSelected != '' and
                                                self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if self.checkThemeSet.get() and (self.themeDirSelected != 'Themes Path' and self.themeDirSelected != '' and
                                                self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if self.checkPlaylistSet.get() and (self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if self.checkDatabaseSet.get() and (self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if startProcessClear:
                    self.prepareProcess()
                    self.setProcWindow()
                    self.progressBar.start()
                    self.fileProcessor.setTaskProcess(self.checkMediaSet.get(),
                                                      self.checkTitleSet.get(),
                                                      self.checkThemeSet.get(),
                                                      self.checkPlaylistSet.get(),
                                                      self.checkDatabaseSet.get(),
                                                      self.startTimeSelected,
                                                      self.durationTimeSelected)
                    self.fileProcessor.setFilePaths(self.mediaDirSelected,
                                                    self.titleDirSelected,
                                                    self.themeDirSelected,
                                                    self.saveDirSelected)
                    self.processThread = threading.Thread(target=self.runFileProcess)
                    self.processThread.daemon = True
                    self.processThread.start()
                    self.container.after(1, self.checkProcessThread)
                else:
                    tk.messagebox.showwarning('Open file',
                                              'Please select a valid task and directory')
            else:
                tk.messagebox.showwarning('Open file',
                                          'Please select a task to process before starting')
        else:
            tk.messagebox.showwarning('Open file',
                                      'Please select a valid save directory')

    def prepareProcess(self):
        self.checkMedia.config(state=DISABLED)
        self.checkTitle.config(state=DISABLED)
        self.checkTheme.config(state=DISABLED)
        self.browseMediaButton.config(state=DISABLED)
        self.browseTitleButton.config(state=DISABLED)
        self.browseThemeButton.config(state=DISABLED)
        self.browseSaveButton.config(state=DISABLED)
        self.processButton.config(state=DISABLED)
        self.exitButton.config(state=DISABLED)

    def completeProcess(self):
        self.exitButton.config(state=NORMAL)
        unsuccessfulMsg = ('The process has finished unsuccessfully\n')
        successfulMsg = ('The process has finished successfully\n')
        suffixUnMsg = ('Please check your setup and attempt the process again\n')
        suffixMsg = ('Enjoy all of the newly created media\n')

        if self.returnMsg is 'EMPTY':
            completeMsg = (unsuccessfulMsg + 'NO_MESSAGE\n' + suffixUnMsg)
        elif self.returnMsg is 'EMPTY':
            completeMsg = (unsuccessfulMsg + 'NO_MESSAGE\n' + suffixUnMsg)
        else:
            completeMsg = (successfulMsg + suffixMsg)
        self.procMessage.config(text=completeMsg)

    def setMediaDir(self):
        rootDir = self.getRootDir()
        self.container.withdraw()
        self.mediaDirSelected = self.browseForFolder('Select the Media Directory', True,
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entryMedia, tk.INSERT, self.mediaDirSelected)
        self.container.deiconify()

    def setTitleDir(self):
        rootDir = self.getRootDir()
        self.container.withdraw()
        self.titleDirSelected = self.browseForFolder('Select the Titles Directory', True,
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entryTitle, tk.INSERT, self.titleDirSelected)
        self.container.deiconify()

    def setThemeDir(self):
        rootDir = self.getRootDir()
        self.container.withdraw()
        self.themeDirSelected = self.browseForFolder('Select the Theme Directory', True,
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entryTheme, tk.INSERT, self.themeDirSelected)
        self.container.deiconify()

    def setSaveDir(self):
        rootDir = self.getRootDir()
        self.container.withdraw()
        self.saveDirSelected = self.browseForFolder('Select the File Save Directory', True,
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entrySave, tk.INSERT, self.saveDirSelected)
        self.container.deiconify()

    def selectMediaTime(self):
        if self.checkMediaSet.get():
            self.labelFont = ('sans', 12, 'bold')
            self.createTopLevel()
            selectButton = tk.Button(self.top, text="Finish", command=self.processMediaTime,
                                     background='GRAY')
            self.top.title('Input Time for Conversion')
            self.startTimeLabel = tk.Label(self.top, width=0, height=0, padx=12, pady=12,
                                       background='GRAY', foreground='WHITE', font=self.labelFont,
                                       text='\nInput Start Time In Seconds\n')
            self.startTime = tk.StringVar()
            entryStartBox = tk.Entry(self.top, textvariable=self.startTime, background='WHITE')
            self.endTimeLabel = tk.Label(self.top, width=0, height=0, padx=12, pady=12,
                                       background='GRAY', foreground='WHITE', font=self.labelFont,
                                       text='\nInput Duration In Seconds\n')
            self.durationTime = tk.StringVar()
            entryDurBox = tk.Entry(self.top, textvariable=self.durationTime, background='WHITE')

            self.startTimeLabel.pack()
            entryStartBox.pack(anchor='center')
            self.endTimeLabel.pack()
            entryDurBox.pack(anchor='center')
            selectButton.pack(anchor='n', fill='both')

    def processMediaTime(self):
        self.setMediaTime()
        self.removeTopLevel()

    def setMediaTime(self):
        if self.startTime.get() == '' or self.startTime.get() == '-1':
            self.startTimeSelected = '300'
        else:
            self.startTimeSelected = self.startTime.get()
        if self.durationTime.get() == '' or self.startTime.get() == '-1':
            self.durationTimeSelected = '30'
        else:
            self.durationTimeSelected = self.durationTime.get()

    def setProcWindow(self):
        self.procWindow = Window.Window(self.bgdWindow, bgColor='RED')
        self.labelFont = ('sans', 12, 'bold')
        self.procMessage = tk.Label(self.procWindow, width=0, height=0,
                                   background='RED', foreground='WHITE', font=self.labelFont,
                                   text='\nThe program will now copy media based\n'
                                   'on the paths selected\n')
        self.progressBar = tk.ttk.Progressbar(self.procWindow, orient="horizontal",
                                        length=(int(self.windowedWidth / 2)),
                                        mode="indeterminate")
        self.procGridConfig = [[0,1,None,None], [1,1,None,None],
                              [2,1,None,None], [3,1,None,None],
                              [4,1,0,1]]
        self.checkMedia.deselect()
        self.checkTitle.deselect()
        self.checkTheme.deselect()
        self.checkMedia.config(state=NORMAL)
        self.checkTitle.config(state=NORMAL)
        self.checkTheme.config(state=NORMAL)
        self.browseMediaButton.config(state=NORMAL)
        self.browseTitleButton.config(state=NORMAL)
        self.browseThemeButton.config(state=NORMAL)
        self.browseSaveButton.config(state=NORMAL)
        self.procWindow.configWindows(self.procWindow, self.procGridConfig)
        self.procWindow.windowCustomize(1, tk.RAISED)
        self.procWindow.addWindow(self.procMessage, 1, 0, 'nsew')
        self.procWindow.addWindow(self.progressBar, 3, 0)
        self.bgdWindow.addWindow(self.procWindow, 0, 0, 'nsew', 2)

    def setAudProcWindow(self):
        self.removeTopLevel()
        self.checkMedia = tk.Checkbutton(self.stpWindow, bg='GOLDENROD', activebackground='GOLDENROD',
                                         variable=self.checkMediaSet, command=self.selectMediaTime)
        self.entryAudioMedia = tk.Entry(self.stpWindow)
        self.entryAudioMedia.config(state=DISABLED)
        self.setEntryText(self.entryAudioMedia, tk.INSERT, self.mediaDirSelected)
        BROWSE_MEDIA_CMD = self.setMediaDir
        self.browseMediaButton = self.stpWindow.createButton('...', 'BLACK',
                                                   'WHITE', BROWSE_MEDIA_CMD, '1', '4')
        self.msgGridConfig = [[0,1,0,1], [1,1,1,1],
                              [2,1,2,1], [3,1,3,5],
                              [4,1,4,1], [5,1,5,1],
                              [5,1,6,1]]
        self.stpWindow.configWindows(self.stpWindow, self.msgGridConfig)
        self.stpWindow.windowCustomize(1, tk.RAISED)
        self.stpWindow.addWindow(self.checkMedia, 1, 1, '')
        self.stpWindow.addWindow(self.entryAudioMedia, 1, 3, 'ew')
        self.stpWindow.placeButton(self.browseMediaButton, 1, 5, '')
        self.bgdWindow.addWindow(self.stpWindow, 0, 0, 'nsew', 5)

    def setAvProcWindow(self):
        self.removeTopLevel()
        self.checkMedia = tk.Checkbutton(self.stpWindow, bg='GOLDENROD', activebackground='GOLDENROD',
                                         variable=self.checkMediaSet, command=self.selectMediaTime)
        self.entryAvMedia = tk.Entry(self.stpWindow)
        self.entryAvMedia.config(state=DISABLED)
        self.setEntryText(self.entryAvMedia, tk.INSERT, self.mediaDirSelected)
        BROWSE_MEDIA_CMD = self.setMediaDir
        self.browseMediaButton = self.stpWindow.createButton('...', 'BLACK',
                                                   'WHITE', BROWSE_MEDIA_CMD, '1', '4')
        self.msgGridConfig = [[0,1,0,1], [1,1,1,1],
                              [2,1,2,1], [3,1,3,5],
                              [4,1,4,1], [5,1,5,1],
                              [5,1,6,1]]
        self.stpWindow.configWindows(self.stpWindow, self.msgGridConfig)
        self.stpWindow.windowCustomize(1, tk.RAISED)
        self.stpWindow.addWindow(self.checkMedia, 1, 1, '')
        self.stpWindow.addWindow(self.entryAvMedia, 1, 3, 'ew')
        self.stpWindow.placeButton(self.browseMediaButton, 1, 5, '')
        self.bgdWindow.addWindow(self.stpWindow, 0, 0, 'nsew', 5)

    def setConvProcWindow(self):
        self.removeTopLevel()
        self.checkMedia = tk.Checkbutton(self.stpWindow, bg='GOLDENROD', activebackground='GOLDENROD',
                                         variable=self.checkMediaSet, command=self.selectMediaTime)
        self.entryConvMedia = tk.Entry(self.stpWindow)
        self.entryConvMedia.config(state=DISABLED)
        self.setEntryText(self.entryConvMedia, tk.INSERT, self.mediaDirSelected)
        BROWSE_MEDIA_CMD = self.setMediaDir
        self.browseMediaButton = self.stpWindow.createButton('...', 'BLACK',
                                                   'WHITE', BROWSE_MEDIA_CMD, '1', '4')
        self.msgGridConfig = [[0,1,0,1], [1,1,1,1],
                              [2,1,2,1], [3,1,3,5],
                              [4,1,4,1], [5,1,5,1],
                              [5,1,6,1]]
        self.stpWindow.configWindows(self.stpWindow, self.msgGridConfig)
        self.stpWindow.windowCustomize(1, tk.RAISED)
        self.stpWindow.addWindow(self.checkMedia, 1, 1, '')
        self.stpWindow.addWindow(self.entryConvMedia, 1, 3, 'ew')
        self.stpWindow.placeButton(self.browseMediaButton, 1, 5, '')
        self.bgdWindow.addWindow(self.stpWindow, 0, 0, 'nsew', 5)

    def getFolderSelected(self):
        return self.fileDirSelected
    '''
