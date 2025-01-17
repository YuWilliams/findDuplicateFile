import hashlib
import logging
import os
import sys
import logging
logger = logging.getLogger("FINDPY")
logger.setLevel(logging.INFO)
logger1 = logging.StreamHandler()
logger1.setLevel(logging.INFO)
fomatter = logging.Formatter('%(asctime)s-%(module)s:%(message)s')
logger1.setFormatter(fomatter)
logger.addHandler(logger1)
if len(sys.argv) < 2:
    print('find.py <folder> [-log <log_file>]')
    sys.exit(-1)
if len(sys.argv) == 4:
    logger2 = logging.FileHandler(sys.argv[3])
    logger2.setLevel(logging.INFO)
    logger2.setFormatter(fomatter)
    logger.addHandler(logger2)
rootFolder = sys.argv[1]
rootFolder+='\\'
temp = {}
duplicateList = {}


def getMD5List(folder):
    files = os.listdir(folder)
    if len(files) == 0:
        return False
    for file in files:
        filePath = '%s%s' % (folder, file)

        if os.path.isdir(filePath):
            getMD5List('%s/' % filePath)
        else:
            oFile = open(filePath, 'rb')
            value = hashlib.md5()
            value.update(oFile.read())
            oFile.close()
            temp.update({filePath: value.hexdigest()})


def findDuplicateFile(md5List):
    for md5 in md5List:
        try:
            duplicateList[md5List[md5]].append(md5)
        except:
            duplicateList.update({md5List[md5]: [md5]})
            pass


def showDuplicateFile(duplicateArray):
    count = 0
    for one in duplicateArray:
        if len(duplicateArray[one]) > 1:
            count = count + 1
            for two in duplicateArray[one]:
                logger.info(two)
            logger.info('')
    logger.info('总共找到 %s 组文件重复。' % count)


getMD5List(rootFolder)
findDuplicateFile(temp)
showDuplicateFile(duplicateList)
