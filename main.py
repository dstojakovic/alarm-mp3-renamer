#!/usr/bin/env python
'''TODO: program description '''
# TODO: ubacivanje config fajla
# TODO: GUI config, radni direktorijum
# TODO: GUI rename checkbox


import os
import sys
import pdb
import logging
import Tkinter

# variables setup; TODO config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(sys.prefix)
logger.debug('Config started.')
configFile = 'config.xml'
directoryMaster = 'd:\mp3\podcast\Alarm'
# directoryMonth = '201705-test'
directoryMonth = '201705'
directoryWork = directoryMaster + os.sep + directoryMonth
directoryCurrent = os.path.dirname(os.path.realpath(__file__))
weekdays = ['ponedeljak', 'utorak', 'sreda', 'cetvrtak', 'petak']
logger.debug('Config finished.')

def configLoad(configName):
  '''Loads configuration from configName and returns as list configuration'''
  pass

def configWrite(configList, configOutputFile=configFile)  :
  '''Writes configuration; configList into configOutputFIle'''
  pass

def configApply(configList)  :
  '''Applies configuration from configList'''
  pass

def readMp3Filenames(dirWorking):
  '''Scans given absolute path for mp3 files and returns them as list'''
  logger.info('readMp3Filenames() started')
  fileNamesAll = os.listdir(dirWorking)
  fileNamesMp3 = []
  for fileName in fileNamesAll:
    fileNameLower = fileName.lower()
    if fileNameLower[-3:] == 'mp3':
      logger.debug('{0} added to mp3 list'.format(fileName))
      fileNamesMp3.append(fileName)
    else:
      logger.debug('{0} is not mp3'.format(fileName))
  logger.info('readMp3Filenames() finished')
  return fileNamesMp3

def newMp3Filename(inputMp3Filename):
  '''Create new string filename from input file name in format YYYY.MM.DD_weekday*bm.mp3'''
  logger.debug('newMp3Filename() started: {0}'.format(inputMp3Filename))
  targetFilename = ''
  counterDays = 0
  fileName = inputMp3Filename
  for day in weekdays:
    weekdayTest = fileName.find(day)
    if weekdayTest > 0:
      logger.debug('{0} already renamed to target format.'.format(fileName))
      targetFilename = fileName
    elif weekdayTest == 0:
      logger.debug('{0} proccessing started.'.format(fileName))
      logger.debug('filename: {0}  weekday: {1}'.format(fileName, day))
      fileNameTemp = fileName[(len(day) + 1):]
      tempDD, tempMM, tempYYYY, tempExtension = fileNameTemp.split('.')
      # add . at between YYYY and 'bm' string
      if len(tempYYYY) > 4:
        logger.debug('Additional string present in year: {0}'.format(tempYYYY))
        tempYYYY, tempAdditional = tempYYYY[0:-2], tempYYYY[-2:]
      else:
        logger.debug('Correct number of figures in year: {0}'.format(tempYYYY))
      logger.debug('Rearanging timestamp in filename started: {0}.'.format(fileName))
      tempString = '_'.join([tempDD, day])
      tempDD = tempString
      fileNameTempListOrder = [tempYYYY, tempMM, tempDD, tempAdditional, tempExtension]
      targetFilename = '.'.join(fileNameTempListOrder)
      logger.debug('Rearanging timestamp in filename finished: {0}.'.format(targetFilename))
    elif weekdayTest == -1:
      logger.debug('day {0} not found in filename'.format(day))
    else:
      logger.error('TODO: unknown case for weekday in {0}'.format(fileName))
  return targetFilename

def newMp3Filenames(inputMp3Filenames):
  '''Create list of new filenames from list of old filenames'''
  finalList = []
  logger.debug('newMp3Filenames() started')
  for filename in inputMp3Filenames:
    finalList.append(newMp3Filename(filename))
  return finalList

def renameMp3Filenames(oldMp3Filenames, newMp3Filenmes, inputDirectory=directoryWork):
  '''Renames list of mp3 files in given directory, returns nothing.
  {weekday}_{DD}.{MM}.{YYYY}bm.mp3 -> {YYYY}.{MM}.{DD}_{weekday}.mp3
  '''
  # hardcoded, there will be trouble latter
  # there can be problem if there is weekday somewhere else than at begging, but wrong filename format
  # TODO: test for relative path, works with absolute path only
  logger.debug('renameMp3Filenames() started.')
  logger.debug(inputDirectory)
  for oldMp3Filename, newMp3Filename in zip(oldMp3Filenames, newMp3Filenmes):
    if not os.path.isfile(inputDirectory + os.sep + newMp3Filename):
      logger.debug('Target filename {0} not found, go for rename.'.format(newMp3Filename))
      logger.debug('{0}, {1}'.format(oldMp3Filename, newMp3Filename))
      #rename file
      os.rename(inputDirectory + os.sep + oldMp3Filename,
                      inputDirectory + os.sep + newMp3Filename)
      logger.info('{0} renamed to {1}.'.format(oldMp3Filename, newMp3Filename))
    else:
      logger.warn('{0} skipped, already exists.'.format(oldMp3Filename))

class simpleapp_tk(Tkinter.Tk):
  def __init__(self, parent):
    Tkinter.Tk.__init__(self, parent)
    self.parrent = parent
    self.initialize()
  def initialize(self):
    self.grid()
    columnUI = 0
    rowUI = 0
    # Labels: original and new filename
    self.labelOldName = Tkinter.StringVar()
    self.labelOldName.set('Old mp3 filenames')
    labelOldNames = Tkinter.Label(self,textvariable=self.labelOldName,anchor="w")
    labelOldNames.grid(column=columnUI,row=rowUI,sticky='EW')
    self.labelNewName = Tkinter.StringVar()
    self.labelNewName.set('New mp3 filenames')
    labelNewNames = Tkinter.Label(self,textvariable=self.labelNewName,anchor="w",fg="white",bg="blue")
    labelNewNames.grid(column=columnUI + 1,row=rowUI,sticky='EW')
    rowUI = 1
    self.mp3FilesOld = readMp3Filenames(directoryWork)
    self.mp3FilesNew = []
    # populate columns for old and new file name
    for mp3FileOld in self.mp3FilesOld:
      logger.debug(' GUI: mp3 file old name: {0}'.format(mp3FileOld))
      self.labelOldmp3FileName = Tkinter.StringVar()
      self.labelOldmp3FileName.set(mp3FileOld)
      labelOldmp3FileName = Tkinter.Label(self,textvariable=self.labelOldmp3FileName,anchor="w")
      labelOldmp3FileName.grid(column=columnUI,row=rowUI,sticky='EW')
      mp3FileNew = newMp3Filename(mp3FileOld)
      logger.debug(' GUI: mp3 file new name: {0}'.format(mp3FileNew))
      # self.varCheck = Tkinter.IntVar()
      self.mp3FilesNew.append(mp3FileNew)
      if mp3FileNew == mp3FileOld:
        # use default colors if there is no need to rename files
        fgColor = 'black'
        bgColor = 'SystemMenu'
        # self.varCheck.set(0)
      else:
        # use special colors to mark files that need to be renamed
        fgColor = 'white'
        bgColor = 'blue'
      self.labelNewmp3FileName = Tkinter.StringVar()
      self.labelNewmp3FileName.set(mp3FileNew)
      labelNewmp3FileName = Tkinter.Label(self,textvariable=self.labelNewmp3FileName,anchor="w",fg=fgColor,bg=bgColor)
      labelNewmp3FileName.grid(column=columnUI + 1,row=rowUI,sticky='EW')
      rowUI = rowUI + 1
    #Buttons
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
    logger.info(' GUI: refresh GUI and mp3 files list')
    self.initialize()
  def OnButtonRenameClick(self):
    logger.info(' GUI: Rename mp3 files')
    renameMp3Filenames(self.mp3FilesOld, self.mp3FilesNew)
    self.OnButtonRefreshClick()
  def OnButtonExitClick(self):
    logger.info(' GUI: Exiting program')
    exit()
    
def mainGUI():
  app = simpleapp_tk(None)
  app.title('Alarm mp3 files renamer')
  app.mainloop()

def mainConsole():
  logging.info('Start')
  mp3Files = readMp3Filenames(directoryWork)
  newMp3FilenamesList = newMp3Filenames(mp3Files)
  renameMp3Filenames(mp3Files, newMp3FilenamesList, directoryWork)
  logging.info('Finished')


if __name__ == '__main__':
    if len(sys.argv) > 1:
      if sys.argv[1] == '-c':
        mainConsole()
    else:
      mainGUI()