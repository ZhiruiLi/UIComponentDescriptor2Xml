from UIComponentDescriptor2XML import uiComponentDescripter2XML
from UIComponentDescriptor2XML import UIComponentDescriptor
from StringProcessor import StringProcessor
import codecs
def fromFileToFile(readPath, typePrefixDict = {}, defaultPrefix = '', writePath = ''):
    '''
    read file descriptor from readPath, and write XML to writePath
    '''
    if writePath == '':
        writePath = readPath + '.xml'
    readFile = file = open(readPath, 'rb')
    len = readFile.seek(0, 2) + 1
    readFile.seek(0, 0)
    bytes = readFile.read(len)
    readFile.close()
    if bytes[:3] == codecs.BOM_UTF8:
        bytes = bytes[3:]
    s = bytes.decode()
    uicd = UIComponentDescriptor.parserDescriptorFromString(s)
    doc = uiComponentDescripter2XML(uicd, typePrefixDict, defaultPrefix)
    writeFile = open(writePath, 'wb')
    bytes = doc.toprettyxml('    ').encode('utf-8')
    writeFile.write(bytes)
    writeFile.close()

def configParser(configPath = './config.cfg'):
    '''
    read config.cfg in the dir of this script
    return (readWriteDict:dict, typePrefixDict:dict, defaultPrefix:str)
    '''
    readWriteDict = {}
    typePrefixDict = {}
    defaultPrefix = ''
    config = open(configPath, 'rb')
    for bytesLine in config.readlines():
        if bytesLine[:3] == codecs.BOM_UTF8:
            bytesLine = bytesLine[3:]
        line = bytesLine.decode('utf-8')
        processor = StringProcessor(line)
        tempChar = processor.skipSpace().readChar()
        tempKey = processor.skipSpace().readStringWithSameLayerBracket('<')
        tempKey = StringProcessor.cutHeadAndTail(tempKey)
        tempVal = processor.skipSpace().readStringWithSameLayerBracket('<')
        tempVal = StringProcessor.cutHeadAndTail(tempVal)
        if tempChar == '#':
            continue
        elif tempChar == '@':
           readWriteDict[tempKey] = tempVal
        elif tempChar == '$':
            typePrefixDict[tempKey] = tempVal
        elif tempChar == '&':
            defaultPrefix = tempKey
        else:
            if not line.isspace():
                raise RuntimeError('illegal config head')
    return (readWriteDict, typePrefixDict, defaultPrefix)

if __name__ == '__main__':
    (readWriteDict, tagPrefixDict, defPrefix) = configParser()
    for (k, v) in readWriteDict.items():
        fromFileToFile(k, tagPrefixDict, defPrefix, v)