#coding=utf-8
import codecs
def readAllFromFile(filePath):
    readBinaryFile = open(filePath, 'rb')
    len = readBinaryFile.seek(0, 2) + 1
    readBinaryFile.seek(0, 0)
    bytes = readBinaryFile.read(len)
    readBinaryFile.close()
    if bytes[:3] == codecs.BOM_UTF8:
        bytes = bytes[3:]
    return bytes.decode()

def writeAllToFile(s, filePath):
    writeFile = open(filePath, 'wb')
    bytes = s.encode('utf-8')
    writeFile.write(bytes)
    writeFile.close()