#!/usr/bin/env python
def main():
  '''TODO: program description '''
  # TODO: ubacivanje config fajla
  # TODO: GUI
  
  import os
  import sys
  import pdb
  import logging
  
  # variables setup; TODO config
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  logger.info(sys.prefix)
  logger.debug('Config started.')
  configFile = 'config.xml'
  directoryMaster = 'd:\mp3\podcast\Alarm'
  # directoryMonth = '201701-test'
  directoryMonth = '201704'
  directoryWork = directoryMaster + os.sep + directoryMonth
  directoryCurrent = os.path.dirname(os.path.realpath(__file__))
  weekdays = ['ponedeljak', 'utorak', 'sreda', 'cetvrtak', 'petak']
  logger.debug('Config finished.')
  
  def configLoad(configName):
    '''Loads configuration from configName  and returns as list configuration'''
    pass

  def configWrite(configList, configOutputFile=configFile)  :
    '''Writes configuration; configList into configOutputFIle'''
    pass
  
  def configApply(configList)  :
    '''Applies configuration from configList'''
    pass

  def readMp3Filenames(dirWorking):
    '''Scans given absolute path for mp3 files and returns them as list'''
    logger.debug('readMp3Filenames() started')
    fileNamesAll = os.listdir(dirWorking)
    fileNamesMp3 = []
    for fileName in fileNamesAll:
      fileNameLower = fileName.lower()
      if fileNameLower[-3:] == 'mp3':
        logger.debug('{0} added to mp3 list'.format(fileName))
        fileNamesMp3.append(fileName)
      else:
        logger.debug('{0} is not mp3'.format(fileName))
    logger.debug('readMp3Filenames() finished')
    return fileNamesMp3


  def renameMp3Filenames(inputMp3Filenames, inputDirectory):
    '''Renames list of mp3 files in given directory, returns nothing.
    {weekday}_{DD}.{MM}.{YYYY}bm.mp3 -> {YYYY}.{MM}.{DD}_{weekday}.mp3
    '''
    # hardcoded, there will be trouble latter
    # there can be problem if there is weekday somewhere else than at begging, but wrong filename format
    # TODO: test for relative path, works with absolute path only
    logger.debug('renameMp3Filenames() started.')
    for fileName in inputMp3Filenames:
      targetFilename = ''
      counterDays = 0
      for day in weekdays:
        weekdayTest = fileName.find(day)
        if weekdayTest > 0:
          logger.warn('{0} already renamed to target format.'.format(fileName))
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
          
          if not os.path.isfile(inputDirectory + os.sep + targetFilename):
            logger.debug('OK to rename, target {0} not found.'.format(targetFilename))
            logger.debug(inputDirectory)
            logger.debug('{0}, {1}'.format(fileName, targetFilename))
            os.rename(inputDirectory + os.sep + fileName,
                      inputDirectory + os.sep + targetFilename)
            logger.info('{0} renamed to {1}.'.format(fileName, targetFilename))
          else:
            logger.warn('{0} skipped, already exists.'.format(fileName))
        elif weekdayTest == -1:
          logger.debug('{0} not found in {1}'.format(day, fileName))
          counterDays = counterDays + 1
          if counterDays > 4:
            logger.warn('weekday not found in {0}'.format(fileName))
        else:
          logger.error('TODO: unknown case for weekday in {0}'.format(fileName))
    logger.debug('renameMp3Filenames() finished.')
  
  logging.info('Start')
  mp3Files = readMp3Filenames(directoryWork)
  renameMp3Filenames(mp3Files, directoryWork)
  logging.info('Finished')


if __name__ == '__main__':
    main()