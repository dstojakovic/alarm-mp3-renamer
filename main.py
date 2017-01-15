#!/usr/bin/env python
def main():
  '''TODO: program description '''
  # TODO: ubacivanje config fajla
  # TODO: GUI
  
  import os
  import pdb
  import logging
  
  # variables setup; TODO config
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  directoryMaster = 'd:\mp3\podcast\Alarm'
  # directoryMonth = '201701-test'
  directoryMonth = '201701'
  directoryWork = directoryMaster + os.sep + directoryMonth
  directoryCurrent = os.path.dirname(os.path.realpath(__file__))
  weekdays = ['ponedeljak', 'utorak', 'sreda', 'cetvrtak', 'petak']


  def readMp3Filenames(dirWorking):
    '''Scans given absolute path for mp3 files and returns them as list'''
    fileNamesAll = os.listdir(dirWorking)
    fileNamesMp3 = []
    for fileName in fileNamesAll:
      fileNameLower = fileName.lower()
      if fileNameLower[-3:] == 'mp3':
        logger.debug('{0} added to mp3 list'.format(fileName))
        fileNamesMp3.append(fileName)
      else:
        logger.debug('{0} is not mp3'.format(fileName))
    return fileNamesMp3


  def renameMp3Filenames(inputMp3Filenames, inputDirectory):
    '''Renames list of mp3 files in given directory, returns nothing.
    {weekday}_{DD}.{MM}.{YYYY}1.mp3 -> {YYYY}.{MM}.{DD}_{weekday}.mp3
    '''
    # hardcoded, there will be trouble latter
    # there can be problem if there is weekday somewhere else than at begging
    # TODO: test for relative path, works with absolute path only
    logger.debug('input Filename, new Filename')
    for fileName in inputMp3Filenames:
      targetFilename = ''
      counterDays = 0
      for day in weekdays:
        weekdayTest = fileName.find(day)
        if weekdayTest > 0:
          logger.warn('{0} already renamed to target format.'.format(fileName))
        elif weekdayTest == 0:
          logger.debug('{0} proccessing started.'.format(fileName))
          logger.debug(fileName, day)
          fileNameTemp = fileName[(len(day) + 1):]
          fileNameTempList = fileNameTemp.split('.')
          # remove unneccessery figure at end YYYY string
          if len(fileNameTempList[2]) > 4:
            logger.debug('Additional figure present in year (YYYYx)')
            fileNameTempList[2] = fileNameTempList[2][0:-1]
          else:
            logger.debug('Correct number of figures in year (YYYY)')
          logger.debug('Rearanging timestamp in filename started.')
          tempString = '_'.join([fileNameTempList[0], day])
          fileNameTempList[0] = tempString
          fileNameTempListOrder = [fileNameTempList[2], fileNameTempList[1],
                                   fileNameTempList[0], fileNameTempList[3]]
          targetFilename = '.'.join(fileNameTempListOrder)
          logger.debug('Rearanging timestamp in filename finished.')
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
  
  logging.info('Start')
  mp3Files = readMp3Filenames(directoryWork)
  renameMp3Filenames(mp3Files, directoryWork)
  logging.info('Finished')


if __name__ == '__main__':
    main()