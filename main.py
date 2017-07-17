#!/usr/bin/env python
"""TODO: program description """
# TODO: ubacivanje config fajla
# TODO: GUI config, radni direktorijum
# TODO: GUI rename checkbox


import os
import sys
import pdb
import logging
import Tkinter
from xml.etree import ElementTree as ET

# variables setup; TODO config
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
# else:
    # logging.basicConfig(level=logging.FATAL)
# logger = logging.getLogger(__name__)
# logger.info(sys.prefix)
# logger.debug(' Config started.')
# configFile = 'config.xml'
# directory = 'd:\mp3\podcast\Alarm'
# directoryMonth = '201707'
# directoryWork = directory + os.sep + directoryMonth
# directoryCurrent = os.path.dirname(os.path.realpath(__file__))
# logger.debug(' Config finished.')



class AppConfig():
    """
    Creates configuratin data structure
    input: string, config file name in same directory
    """
    def __init__(self, configFile):
        logger.info(' Initial config started.')
        self.configuration = {}
        self.configFile = configFile
        self.absFilePath = os.path.abspath(os.path.join(self.configFile)) 
        self.dom = ET.parse(self.absFilePath)
        self.configtree = self.dom.findall('config/')
        for c in self.configtree:
            logger.debug('config item object'.format(c))
            logger.debug('tag {0}, text {1}, attribute {2}'.format(c.tag, c.text, c.attrib))
            self.configuration[c.tag] = c.text
        self.directoryWork = self.configuration['directory'] + os.sep + self.configuration['directoryMonth']
        self.configuration['weekdays'] = []
        self.weekdays = self.dom.findall('config/weekdays/')
        for day in self.weekdays:
            self.configuration['weekdays'].append(day.text)
            logger.debug(day.text)
        
        logger.info(' Initial config finished.')
    def __str__(self):
        return 'Configuration loaded from {0}'.format(self.configFile)
    def __repr__(self):
        return str('{0}({1})'.format(self.__class__.__name__, self.configFile))
    def printConfig(self):
        """
        Print configuration
        """
        for c in self.configuration:
            print('{0}: {1}'.format(c, self.configuration[c]))
    def getConfig(self):
        """
        output: list, configuration
        """
        return self.configuration
    def defaultConfig():
        """
        Default setup if needed
        """
        self.configuration['weekdays'] = ['ponedeljak', 'utorak', 'sreda', 'cetvrtak', 'petak']
        self.configuration['loglevel'] = 'INFO'
        self.configuration['directory'] = 'd:\mp3\podcast\Alarm'
        self.configuration['directoryMonth'] = '201707'

class filenameOldNew():
    """keeps old and newfile name"""
    def __init__(self, old):
        self.old = old
        self.path = ''
        self.new = ''
    def __repr__(self):
        return str('{0}({1})'.format(self.__class__.__name__, self.old))
    def __str__(self):
        return str(self.old) + ' ---> '+ str(self.old)
    def getOld(self):
        return self.old
    def getNew(self):
        return self.new
    def setOld(self, text):
        self.old = text
    def setNew(self, text):
        self.new = text

def configLoad():
    """
    Loads configuration from configName and returns as list configuration
    
    input: string, configName
    """
    logger.info(' TODO: configLoad()')

def configWrite():
    """
    Writes configuration; configList into configOutputFile
    
    input: string, configList, configOutputFile=configFile
    """
    logger.info(' TODO: configWrite()')

def configApply():
    """
    Applies configuration from configList
    
    input: string, configList
    """
    logger.info(' TODO: configApply()')

def readMp3Filenames(directory):
    """Scans given absolute path for mp3 files and returns them as list of filenameOldNew objects
    
    input: string, absolute path on filesystem
    output: list of strings, mp3 filenames
    """
    logger.info(' readMp3Filenames() started')
    fileNamesAll = os.listdir(directory)
    fileNamesMp3 = []
    for fileName in fileNamesAll:
        fileNameLower = fileName.lower()
        if fileNameLower[-3:] == 'mp3':
            fileObject = filenameOldNew(fileName)
            fileNamesMp3.append(fileObject)
            logger.debug(' {0} added to mp3 list'.format(fileObject))
        else:
            logger.debug(' {0} is not mp3'.format(fileName))
    processed = len(fileNamesAll)
    discarded = len(fileNamesAll)-len(fileNamesMp3)
    logger.info(' readMp3Filenames(): {0} filename(s) processed, {1} discarded'.format(processed, discarded))
    return fileNamesMp3

def newMp3Filename(fileNameObject):
    """Create new string filename from input file name in format YYYY.MM.DD_weekday*bm.mp3"""
    fileName = fileNameObject.getOld()
    logger.debug(' newMp3Filename() started: {0}'.format(fileName))
    targetFilename = ''
    counterDays = 0
    weekdays = ['ponedeljak', 'utorak', 'sreda', 'cetvrtak', 'petak']
    for day in weekdays:
        weekdayTest = fileName.find(day)
        if weekdayTest > 0:
            logger.debug(' {0} already renamed to target format.'.format(fileName))
            targetFilename = fileName
        elif weekdayTest == 0:
            logger.debug(' {0} proccessing started.'.format(fileName))
            logger.debug(' filename: {0}  weekday: {1}'.format(fileName, day))
            fileNameTemp = fileName[(len(day) + 1):]
            tempDD, tempMM, tempYYYY, tempExtension = fileNameTemp.split('.')
            # add . at between YYYY and 'bm' string
            if len(tempYYYY) > 4:
                logger.debug(' Additional string present in year: {0}'.format(tempYYYY))
                tempYYYY, tempAdditional = tempYYYY[0:-2], tempYYYY[-2:]
            else:
                logger.debug(' Correct number of figures in year: {0}'.format(tempYYYY))
            logger.debug(' Rearanging timestamp in filename started: {0}.'.format(fileName))
            tempString = '_'.join([tempDD, day])
            tempDD = tempString
            fileNameTempListOrder = [tempYYYY, tempMM, tempDD, tempAdditional, tempExtension]
            targetFilename = '.'.join(fileNameTempListOrder)
            logger.debug(' Rearanging timestamp in filename finished: {0}.'.format(targetFilename))
        elif weekdayTest == -1:
            logger.debug(' day {0} not found in filename'.format(day))
        else:
            logger.error(' TODO: unknown case for weekday in {0}'.format(fileName))
    fileNameObject.setNew(targetFilename)

def newMp3Filenames(fileNameObjects):
    """Execute method for creating new filenames for each filenameOldNew object
    
    input: list of filenameOldNew objects
    """
    logger.info(' newMp3Filenames(): started')
    for filename in fileNameObjects:
        newMp3Filename(filename)
        logger.debug(' New filename: {0}'.format(filename.getNew()))
    logger.info(' newMp3Filenames(): {0} filename(s) processed'.format(len(fileNameObjects)))
    return None

def renameMp3Filenames(mp3Files, inputDirectory):
    """Renames list of mp3 files in given directory, returns nothing.
    {weekday}_{DD}.{MM}.{YYYY}bm.mp3 -> {YYYY}.{MM}.{DD}_{weekday}.mp3
    """
    # asumed filename format, there can be problem later
    # if there is weekday somewhere else than at beggining, but wrong filename format
    # TODO: test for relative path, works with absolute path only
    counter = len(mp3Files)
    logger.info(' renameMp3Filenames() started.')
    logger.debug(inputDirectory)
    for fileNameObject in mp3Files:
        old = fileNameObject.getOld()
        new = fileNameObject.getNew()
        if not os.path.isfile(inputDirectory + os.sep + new):
            logger.debug(' Target filename {0} not found, go for rename.'.format(new))
            logger.debug(' {0}, {1}'.format(old, new))
            #rename file
            os.rename(inputDirectory + os.sep + old, inputDirectory + os.sep + new)
            logger.debug(' {0} renamed to {1}.'.format(old, new))
        else:
            logger.warn(' {0} skipped, already exists.'.format(old))
            counter -= 1
    logger.info(' renameMp3Filenames(): {0} processed'.format(counter))

class simpleapp_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parrent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        columnUI = 0
        rowUI = 0
        # Label: original filenames column
        self.labelOldName = Tkinter.StringVar()
        self.labelOldName.set('Old mp3 filenames')
        labelOldNames = Tkinter.Label(self,textvariable=self.labelOldName,anchor="w")
        labelOldNames.grid(column=columnUI,row=rowUI,sticky='EW')
        # Label: new filenames column
        self.labelNewName = Tkinter.StringVar()
        self.labelNewName.set('New mp3 filenames')
        labelNewNames = Tkinter.Label(self,textvariable=self.labelNewName,
                                      anchor="w",fg="white",bg="blue")
        labelNewNames.grid(column=columnUI + 1,row=rowUI,sticky='EW')
        rowUI = 1
        self.mp3FileObjects = readMp3Filenames(config.directoryWork)
        newMp3Filenames(self.mp3FileObjects)
        # populate columns for old and new filenames
        for mp3FileObject in self.mp3FileObjects:
            logger.debug(' GUI: mp3 file old name: {0}'.format(mp3FileObject.getOld()))
            self.labelOldmp3FileName = Tkinter.StringVar()
            self.labelOldmp3FileName.set(mp3FileObject.getOld())
            labelOldmp3FileName = Tkinter.Label(self,textvariable=self.labelOldmp3FileName,anchor="w")
            labelOldmp3FileName.grid(column=columnUI,row=rowUI,sticky='EW')
            logger.debug(' GUI: mp3 file new name: {0}'.format(mp3FileObject.getNew()))
            # self.varCheck = Tkinter.IntVar()
            if mp3FileObject.getNew() == mp3FileObject.getOld():
                # use default colors if there is no need to rename files
                fgColor = 'black'
                bgColor = 'SystemMenu'
                # self.varCheck.set(0)
            else:
                # use special colors to mark files that need to be renamed
                fgColor = 'white'
                bgColor = 'blue'
            self.labelNewmp3FileName = Tkinter.StringVar()
            self.labelNewmp3FileName.set(mp3FileObject.getNew())
            labelNewmp3FileName = Tkinter.Label(self,textvariable=self.labelNewmp3FileName,anchor="w",fg=fgColor,bg=bgColor)
            labelNewmp3FileName.grid(column=columnUI + 1,row=rowUI,sticky='EW')
            rowUI = rowUI + 1
        # Command buttons on bottom
        columnUI = 0
        buttonRefresh = Tkinter.Button(self,text=u"Refresh",command=self.OnButtonRefreshClick)
        buttonRefresh.grid(column=columnUI,row=rowUI)
        buttonRename = Tkinter.Button(self,text=u"Rename",command=self.OnButtonRenameClick)
        buttonRename.grid(column=columnUI + 1,row=rowUI)
        buttonExit = Tkinter.Button(self,text=u"Exit",command=self.OnButtonExitClick)
        buttonExit.grid(column=columnUI + 2,row=rowUI)
        # UI Grid configuration
        self.grid_columnconfigure(0,weight=1)
   
    def OnButtonRefreshClick(self):
        """Calls for repopulation of columns"""
        logger.info(' GUI: refresh GUI and mp3 files list')
        self.initialize()

    def OnButtonRenameClick(self):
        """Calls execution of rename function"""
        logger.info(' GUI: Rename mp3 files')
        renameMp3Filenames(self.mp3FileObjects, config.directoryWork)
        self.OnButtonRefreshClick()
    
    def OnButtonExitClick(self):
        """Calls End program"""
        logger.info(' GUI: Exiting program')
        exit()
    
def mainGUI():
    app = simpleapp_tk(None)
    app.title('Alarm mp3 files renamer')
    app.mainloop()

def mainConsole():
    logging.info(' Start')
    mp3Files = readMp3Filenames(config.directoryWork)
    newMp3Filenames(mp3Files)
    renameMp3Filenames(mp3Files, config.directoryWork)
    logging.info(' Finished')

def main(*args):
    configFile = 'config.xml'
    global config
    config = AppConfig(configFile)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-c':
            mainConsole()
    else:
        mainGUI()

if __name__ == '__main__':
    sys.exit(main(sys.argv))

