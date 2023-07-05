'''
Created on November 12, 2016

@author: bgray
'''

import os
import shutil
import site
import sys
import subprocess
import LogFile
import Database

from os.path import normpath
from os.path import join
from os.path import isfile

class FileProcessor():

    def __init__(self):
        self.logFile = LogFile.LogFile(self.getDataFile(filename='_Movie_Log'), '_Movie_Log')
        self.dbFile = Database.Database(self.getDataFile(filename='_Movie_Data'), '_Movie_Data')
        self.conversionProgramPath = (normpath(join(self.getDataFile(filename='prgms'), 
                                                    'ffmpeg\\bin', 'ffmpeg.exe')))

    def setTaskProcess(self, mProcess, tiProcess, thProcess, plProcess, dbProcess, mTimeStart, mTimeDuration):
        self.taskProcessSet = [mProcess, tiProcess, thProcess, plProcess, dbProcess]
        self.mediaConvertTime = [mTimeStart, mTimeDuration]

    def setFilePaths(self, mDirectory, tiDirectory, thDirectory, sDirectory):
        self.dataFilePaths = [mDirectory, tiDirectory, thDirectory, sDirectory]
        self.processDirectory = normpath(join(self.dataFilePaths[3] + '\\HyperSpin - Video\\Media\\' +
                                           os.path.basename(self.dataFilePaths[0])))

        self.dbFile.dataClearFile()

        # File paths to Write to Database
        for app in self.dataFilePaths:
            self.dbFile.dataEntryAppend(app + '\n')

    def processFiles(self):
        self.logFile.logMsg('\n-----------------\n'
                            'Created Media for ' + os.path.basename(self.dataFilePaths[0]) + '\n'
                            '-----------------\n')

        if self.taskProcessSet[0]:
            self.processClipCapture()
            self.logFile.logMsg('\n' +
                                'Videos' +
                                '\n')
        if self.taskProcessSet[1]:
            self.processTitleCreate()
            self.logFile.logMsg('\n' +
                                'Wheel Images' +
                                '\n')
        if self.taskProcessSet[2]:
            self.processThemeCreate()
            self.logFile.logMsg('\n' +
                                'Themes' +
                                '\n')
        if self.taskProcessSet[3]:
            self.processPlaylistCreate()
            self.logFile.logMsg('\n' +
                                'Playlists' +
                                '\n')
        if self.taskProcessSet[4]:
            self.processDatabaseCreate()
            self.logFile.logMsg('\n' +
                                'Databases' +
                                '\n')

        return 0

    def processClipCapture(self):
        self.createDirectory(normpath(join(self.processDirectory + '\\' + 'Video')))
        if os.path.exists(self.dataFilePaths[0]):
            listMovies = os.listdir(self.dataFilePaths[0])
            for movieTitle in listMovies:
                subprocess.call(self.doubleQuotes(self.conversionProgramPath) + ' ' + '-loglevel quiet -y -i' +
                                        ' ' + self.doubleQuotes(normpath(join(self.dataFilePaths[0] + '\\' + movieTitle))) +
                                        ' ' + '-ss ' + str(self.mediaConvertTime[0]) +
                                        ' -c:v libx264 -profile:v baseline -crf 23 -t ' + str(self.mediaConvertTime[1]) +
                                        ' ' + self.doubleQuotes(normpath(join(self.processDirectory + '\\' + 'Video\\' +
                                                                              self.getFileName(movieTitle)))))

    def processTitleCreate(self):
        self.createDirectory(normpath(join(self.processDirectory + '\\' + 'Images\\Wheel')))
        if os.path.exists(self.dataFilePaths[0]):
            listMovies = os.listdir(self.dataFilePaths[0])
            listTitles = os.listdir(self.dataFilePaths[1])
            for movie in listMovies:
                try:
                    editMovie = movie.split('-')
                    editMovie = (editMovie[0] + '-' + editMovie[1]).strip(' ')
                except:
                    editMovie = movie
                editMovie = editMovie.rsplit('.', 1)[0]
                for title in listTitles:
                    editTitle = title.split('.')[0]
                    if editMovie == editTitle:
                        shutil.copyfile(normpath(join(self.dataFilePaths[1] + '\\' + title)),
                                        normpath(join(self.processDirectory + '\\' + 'Images\\Wheel\\' + movie.rsplit('.', 1)[0] + '.png')))

    def processThemeCreate(self):
        self.createDirectory(normpath(join(self.processDirectory + '\\' + 'Themes')))
        if os.path.exists(self.dataFilePaths[0]):
            listMovies = os.listdir(self.dataFilePaths[0])
            listThemes = os.listdir(self.dataFilePaths[2])
            for movie in listMovies:
                themeExists = False
                for theme in listThemes:
                    if movie.replace(self.getExtension(movie), '') == theme.replace(self.getExtension(theme), ''):
                        themeExists = True
                        break
                try:
                    if themeExists:
                        shutil.copyfile(normpath(join(self.dataFilePaths[2] + '\\' + theme)),
                                        normpath(join(self.processDirectory + '\\' + 'Themes\\' +
                                                      movie.replace(self.getExtension(movie), '') + '.zip')))
                    else:
                        shutil.copyfile(normpath(join(self.dataFilePaths[2] + '\\Default.zip')),
                                        normpath(join(self.processDirectory + '\\' + 'Themes\\' +
                                                      movie.replace(self.getExtension(movie), '') + '.zip')))
                except:
                    pass

    def processPlaylistCreate(self):
        self.playlistPath = normpath(join(self.dataFilePaths[3] + '\\TV Series\\' + os.path.basename(self.dataFilePaths[0])))
        self.createDirectory(self.playlistPath)
        self.playlistExt = '.xspf'
        if os.path.exists(self.dataFilePaths[0]):
            self.playlistMovies = os.listdir(self.dataFilePaths[0])
            playlists = ['*']
            for movie in self.playlistMovies:
                curPrefix = str(movie[:2])
                if curPrefix in playlists:
                    pass
                else:
                    playlists.append(curPrefix)
            for playlist in playlists:
                if playlist == '*':
                    self.writePlaylistDetails(self.playlistPath + '\\_Play All' + self.playlistExt, 'w', playlist)
                else:
                    fileNameVersion = playlist
                    if playlist[:1] == '0':
                        fileNameVersion = playlist.replace('0', '', 1)
                    if fileNameVersion.isnumeric():
                        self.writePlaylistDetails(self.playlistPath + '\\_Season ' + fileNameVersion + self.playlistExt, 'w', playlist)

    def writePlaylistDetails(self, fileName, writable, version):
        idCount = 0
        sortList = []
        playlist = open(fileName, writable)
        playlist.write('<?xml version="1.0" encoding="UTF-8"?>\n' +
                            '<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">\n' +
                            '\t<title>Playlist</title>\n' +
                            '\t<trackList>\n')
        for movie in self.playlistMovies:
            if self.getExtension(movie) == '.mp4' and (version == '*' or version == str(movie[:2])):
                filePath = '///' + self.dataFilePaths[0] + '//' + movie
                filePath = filePath.replace(' ', '%20')
                filePath = filePath.replace('\'', '%27')
                filePath = filePath.replace('&', '%26')
                sortList.append(filePath)
        if len(sortList) > 1:
            sortList.sort()
        for filePathName in sortList:
            playlist.write('\t\t<track>\n' +
                            '\t\t\t<location>file:' + filePathName + '</location>\n' +
                            '\t\t\t<extension application="http://www.videolan.org/vlc/playlist/0">\n' +
                            '\t\t\t\t<vlc:id>' + str(idCount) + '</vlc:id>\n' +
                            '\t\t\t</extension>\n' +
                            '\t\t</track>\n')
            idCount = idCount + 1
        playlist.write('\t</trackList>\n' +
                            '\t<extension application="http://www.videolan.org/vlc/playlist/0">\n')
        for idx in range(0, (idCount)):
            playlist.write('\t\t\t<vlc:item tid="' + str(idx) + '"/>\n')
        playlist.write('\t</extension>\n</playlist>')
        playlist.close()

    def processDatabaseCreate(self):
        self.databasePath = normpath(join(self.dataFilePaths[3] + '\\HyperSpin - Video\\Databases'))
        self.createDirectory(self.databasePath)
        self.databaseExt = '.xml'
        if os.path.exists(self.dataFilePaths[0]):
            databaseFolderPath = self.dataFilePaths[0].replace(os.path.basename('\\' + self.dataFilePaths[0]), '')
            self.databaseFolders = os.listdir(databaseFolderPath)
            for directory in self.databaseFolders:
                if os.path.isdir(databaseFolderPath + directory):
                    self.databaseMovies = os.listdir(databaseFolderPath + directory)
                    self.createDirectory(self.databasePath + '\\' + directory)
                    self.writeDatabaseDetails(self.databasePath + '\\' + directory +
                                              '\\' + directory + self.databaseExt, 'w', list)

    def writeDatabaseDetails(self, fileName, writable, version):
        sortList = []
        database = open(fileName, writable)
        database.write('<?xml version="1.0"?>\n' +
                            '<menu>\n')
        for movie in self.databaseMovies:
            filePath = movie.replace(str(self.getExtension(movie)), '')
            filePath = filePath.replace('&', '&amp;')
            sortList.append(filePath)
        if len(sortList) > 1:
            sortList.sort()
        for fileName in sortList:
            database.write('\t<game name="' + fileName + '" index="" image="">\n' +
                        '\t\t<description>' + fileName + '</description>\n' +
                        '\t\t<cloneof></cloneof>\n' +
                        '\t\t<crc></crc>\n' +
                        '\t\t<manufacturer></manufacturer>\n' +
                        '\t\t<year></year>\n' +
                        '\t\t<genre></genre>\n' +
                        '\t</game>\n')
        database.write('</menu>')
        database.close()

    def createDirectory(self, filepath):
        os.makedirs(filepath, exist_ok=True)

    def getDataFile(self, path='', filename=''):
        if getattr(sys, 'frozen', False):
            datadir = os.path.dirname(sys.executable)
        else:
            datadir = os.path.join(site.getsitepackages()[0], path)
        return (normpath(join(datadir, filename)))

    def getDataSavedPaths(self):
        if isfile(self.getDataFile(filename='_Hyper_Data') + '.db'):
            return self.dbFile.readLines()
        else:
            return -1

    def getFileName(self, filepath):
        return normpath(os.path.basename(filepath))

    def getExtension(self, filename):
        i = 0
        strIndex = 0
        fileExt = filename
        if fileExt.find('.', i) is not -1:
            while i is not len(fileExt):
                if fileExt.find('.', i) is not -1:
                    strIndex = fileExt.find('.', i)
                if strIndex > i:
                    i = strIndex
                else:
                    i = i + 1
            fileExt = fileExt[strIndex:len(fileExt)]
        else:
            fileExt = None
        return fileExt

    def doubleQuotes(self, strQuotes):
        return ('\"' + strQuotes + '\"')

    def logError(self, failtag):
        self.logFile.logMsg('\n\n**************************************\n'
                            '-THE PROCESS HAS FAILED-' + failtag + '\n'
                            '**************************************\n')
