import os
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )
#set dsx dir

os.system('cd ' + os.getcwd())

def isFileNeedEncytp(fileName):
    if fileName.find('.mp3') > -1 :
        return False
    if fileName.find('.wav') > -1 :
        return False
    if fileName.find('.ogg') > -1 :
        return False
    if fileName.find('.Ogg') > -1 :
        return False
    if fileName.find('.mp4') > -1 :
        return False
    if fileName.find('.svn') > -1 :
        return False
    if fileName.find('.ttf') > -1 :
        return False
    if fileName.find('.TTF') > -1 :
        return False
    if fileName.find('.Ttf') > -1 :
        return False
    if fileName.find('.xml') > -1 :
        return False
    if fileName.find('.plist') > -1 :
        return False
    if fileName.find('.py') > -1 :
        return False
    return True

def folderEncytp(folderPath):
	if isFileNeedEncytp(folderPath):
		for file in os.listdir(folderPath):
			if os.path.isdir(folderPath + file + '/'):
				folderEncytp(folderPath + file + '/')
			else:
				if isFileNeedEncytp(file):
					fileName = file
					isEncytp = "0"
					os.system('./cryptobin' + " " + folderPath + " " + fileName + " " + isEncytp)
		return

folderEncytp(os.getcwd() + '/res/')
folderEncytp(os.getcwd() + '/scripts/')

os.system("pause")
