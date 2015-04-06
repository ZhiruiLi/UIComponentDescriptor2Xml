#coding=utf-8
from UIComponentDescriptor import uiComponentDescripter2XML
from UIComponentDescriptor import UIComponentDescriptor
from StringProcessor import StringProcessor
import ASModule
import codecs
import FileProcessor
def fromFileToFile(readPath, typePrefixDict = {}, defaultPrefix = '', writePath = ''):
    '''
    read file descriptor from readPath, and write XML to writePath
    '''
    if writePath == '':
        writePath = readPath + '.xml'
    s = FileProcessor.readAllFromFile(readPath)
    s = ASModule.removeComments(s)
    uicd = UIComponentDescriptor.parserDescriptorFromString(s)
    doc = uiComponentDescripter2XML(uicd, typePrefixDict, defaultPrefix)
    FileProcessor.writeAllToFile(doc.toprettyxml('    '), writePath)

def configParser(configPath = './config.cfg'):
    '''
    read config.cfg in the dir of this script
    return (readWriteDict:dict, typePrefixDict:dict, defaultPrefix:str)
    '''
    readWriteDict = {}
    typePrefixDict = {}
    defaultPrefix = ''
    config = open(configPath, 'rb')
    lines = FileProcessor.readAllFromFile(configPath).splitlines()
    for line in lines:
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
            if not (line.isspace() or line == ''):
                raise RuntimeError('illegal config head')
    return (readWriteDict, typePrefixDict, defaultPrefix)

if __name__ == '__main__':
    (readWriteDict, tagPrefixDict, defPrefix) = configParser()
    for (k, v) in readWriteDict.items():
        fromFileToFile(k, tagPrefixDict, defPrefix, v)