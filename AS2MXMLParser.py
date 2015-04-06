#coding=utf-8
import ASModule
import codecs
import FileProcessor
from ASParserState import ASPaserState
from ASParserState import StartState
from UIComponentDescriptor import uiComponentDescripter2XML
from UIComponentDescriptor import UIComponentDescriptor
from StringProcessor import StringProcessor

def fromFileToFile(readPath, typePrefixDict = {}, defaultPrefix = '', writePath = ''):
    '''
    read file descriptor from readPath, and write XML to writePath
    '''
    if writePath == '':
        writePath = readPath + '.xml'
    s = FileProcessor.readAllFromFile(readPath)
    s = ASModule.removeComments(s)
    '''
    uicd = UIComponentDescriptor.parserDescriptorFromString(s)
    doc = uiComponentDescripter2XML(uicd, typePrefixDict, defaultPrefix)
    '''
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

def parseASString(s):
    processor = StringProcessor(s)
    state = StartState
    words = ['', '', '', '', '']
    while not state.isEnd():
        tempWord = processor.skipSpace().readWord()
        words = words[1:]
        words.append(tempWord)
        state = state.nextPaser(tempWord)
    if state.isError():
        ws = ''
        for w in words:
            ws += w
        raise RuntimeError('error state, last 5 words are ' + ws)
    return ASPaserState._currentClass

def parseConstructor(asClass):
    pass

def fromASToMXML(asClass):
    asClass.getFunctionsIter()

if __name__ == '__main__':
    '''
    (readWriteDict, tagPrefixDict, defPrefix) = configParser()
    for (k, v) in readWriteDict.items():
        fromFileToFile(k, tagPrefixDict, defPrefix, v)
    '''
    asString = FileProcessor.readAllFromFile('D:\\teststate.as')
    asString = ASModule.removeComments(s)
    asClass = parseASString(s)
    doc = fromASToMXML(asClass)