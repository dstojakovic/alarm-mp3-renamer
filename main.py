#!/usr/bin/env python
def main():
  # TODO: ubacivanje config fajla
  # TODO: GUI
  
  # import modules
  import os
  import pdb
  import logging
  
  # variables setup; TODO config
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  directoryMaster = 'd:\mp3\podcast\Alarm'
  directoryMonth = '201701-test'
  directoryWork = directoryMaster + os.sep + directoryMonth
  directoryCurrent = os.path.dirname(os.path.realpath(__file__))
  weekdays = ['ponedeljak',
          'utorak',
          'sreda',
          'cetvrtak',
          'petak'
          ]


  def readMp3Filenames(dirWorking):
    '''
    TODO:opis funkcije
    '''
    fileNamesAll = os.listdir(dirWorking)
    fileNamesMp3 = []
    for fileName in fileNamesAll:
      fileNameLower = fileName.lower()
      if fileNameLower[-3:] == 'mp3':
        fileNamesMp3.append(fileName)
      else:
        logger.debug('{} is not mp3'.format(fileName))
    return fileNamesMp3


  def renameMp3Filenames(inputMp3Filenames, inputDirectory):
    '''
    TODO:opis funkcije
    '''
    # hardkodovanje, obice se o glavu
    # cetvrtak_05.01.20171.mp3  {dan}_{DD}.{MM}.{YYYY}1.mp3
    # 2017.01.05_{dan}.mp3      {YYYY}.{MM}.{DD}_{dan}.mp3
    # moze biti problem ako ima dan negde u toku fajla, a ne napocetku
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
          # skidanje suvisnog broja na kraju YYYY
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
          logger.debug('{0} not present in {1}'.format(day, fileName))
          counterDays = counterDays + 1
          if counterDays > 4:
            logger.warn('Not any weekday in {0}'.format(inputFilename=fileName))
        else:
          logger.error(' TODO unknown case for weekday in filename')
  
  logging.info('Start')
  mp3Files = readMp3Filenames(directoryWork)
  renameMp3Filenames(mp3Files, directoryWork)
  logging.info('Finished')

if __name__ == '__main__':
    main()