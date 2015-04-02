#coding=utf-8
from xml.dom.minidom import Document
from os import path
import codecs
class UIComponentDescriptor:
    '''
    this class repersent the UIComponentDescripter in ActionScript
    '''
    def __init__(self, isSimpleDescriptor = False):
        self.__id = ''
        self.__type = ''
        self.__attributes = {}
        self.__events = {}
        self.__children = []
        self.__isSimple = isSimpleDescriptor
    def __str__(self):
        resultString = ''
        if self.getType() != '':
            resultString += ('type : ' + self.getType() + '\n')
        if self.getID() != '':
            resultString += ('id : ' + self.getID() + '\n')
        for (k, v) in self.getAttributeIter():
            resultString += ('attribute : ' + k + ' --- ' + v + '\n')
        for (k, v) in self.getEventIter():
            resultString += ('event : ' + k + ' --- ' + v + '\n')
        for child in self.getChildrenIter():
            resultString += ('\n' + str(child) + '\n')
        if self.__isSimple:
            print('is simple descriptor') 
        return resultString
    def setID(self, id):
        '''
        set ID of self
        '''
        self.__id = id
        return self
    def getID(self):
        '''
        get ID if self has one, or return '' 
        '''
        return self.__id
    def setType(self, type):
        '''
        set type of self
        '''
        self.__type = type
        return self
    def getType(self):
        '''
        get ID if self has one, or return ''
        '''
        return self.__type
    def addAttribute(self, attrKey, attrVal):
        '''
        add attribute key-value pair to self
        '''
        self.__attributes[attrKey] = attrVal
        return self
    def removeAttribute(self, attrKey):
        '''
        remove a attribute of self
        '''
        if self.__attributes.has(attrKey):
            del self.__attributes[attrKey]
        return self
    def getAttributeIter(self):
        '''
        get the attribute iterator of self
        '''
        return self.__attributes.items()
    def addEvent(self, eventKey, eventVal):
        '''
        add event key-value pair to self
        '''
        self.__events[eventKey] = eventVal
        return self
    def removeEvent(self, eventKey):
        '''
        remove a event of self
        '''
        if self.__events.has(eventKey):
            del self.__events[eventKey]
        return self
    def getEventIter(self):
        '''
        get the event iterator of self
        '''
        return self.__events.items()
    def addChild(self, uiComDescriptor):
        '''
        add a child UIComponentDescriptor to self
        '''
        self.__children.append(uiComDescriptor)
        return self
    def getChildrenIter(self):
        '''
        get the children iterator of self
        '''
        return iter(self.__children)
    def isSimple(self):
        '''
        return if self is a simple descriptor
        '''
        if self.__isSimple:
            return True
        else:
            return False
    @staticmethod
    def __skipFunctionDeclaration(processor, type):
        '''
        skip sentence like 'function ():type'
        '''
        if processor.skipSpace().readWord() != 'function':
            raise RuntimeError('illegal syntax')
        if processor.skipSpace().readChar() != '(':
            raise RuntimeError('illegal syntax')
        if processor.skipSpace().readChar() != ')':
            raise RuntimeError('illegal syntax')
        tempChar = processor.skipSpace().readChar()
        if tempChar == ':':
            if processor.skipSpace().readWord() != type:
                raise RuntimeError('illegal syntax')
        elif tempChar == '':
            raise RuntimeError('illegal syntax')
        else:
            processor.unRead(1)
    @staticmethod
    def parserDescriptorFromString(inputString):
        '''
        input: 'new UIComponentDescriptor({...});'
        output: result UIComponentDescriptor
        '''
        resultDescriptor = UIComponentDescriptor()
        mainProcessor = StringProcessor(inputString)
        tempWord = mainProcessor.skipSpace().readWord()
        if tempWord != 'new':
            raise RuntimeError('illegal syntax')
        tempWord = mainProcessor.skipSpace().readWord()
        if tempWord != 'UIComponentDescriptor':
            raise RuntimeError('illegal syntax')
        tempHeadBracket = mainProcessor.skipSpace().readChar()
        if tempHeadBracket != '(':
            raise RuntimeError('illegal syntax')
        tempHeadBracket = mainProcessor.skipSpace().readChar()
        if tempHeadBracket != '{':
            raise RuntimeError('illegal syntax')
        mainProcessor.unRead(1)
        inputObjectProcessor = StringProcessor(mainProcessor.readStringWithSameLayerBracket('{'))
        inputObjectProcessor.readChar()
        while True:
            tempKey = inputObjectProcessor.skipSpace().skipString(',').skipSpace().readStringWithWrapper('"')
            if tempKey == '':
                if inputObjectProcessor.readChar() == '}':
                    break
                else:
                    raise RuntimeError('illegal syntax')
            tempKey = StringProcessor.cutHeadAndTail(tempKey)
            if inputObjectProcessor.skipSpace().readChar() != ':':
                raise RuntimeError('illegal syntax')
            if tempKey == 'type':
                tempType = inputObjectProcessor.skipSpace().readWord()
                if tempType == '':
                    raise RuntimeError('illegal syntax')
                resultDescriptor.setType(tempType)
                continue
            elif tempKey == 'id':
                tempID = inputObjectProcessor.skipSpace().readStringWithWrapper('"')
                if tempID == '':
                    raise RuntimeError('illegal syntax')
                resultDescriptor.setID(StringProcessor.cutHeadAndTail(tempID))
                continue
            elif tempKey == 'events':
                if inputObjectProcessor.skipSpace().readChar() != '{':
                    raise RuntimeError('illegal syntax')
                eventsDict = UIComponentDescriptor.eventsParser(\
                    inputObjectProcessor.unRead(1).readStringWithSameLayerBracket('{'))
                for (k, v) in eventsDict.items():
                    resultDescriptor.addEvent(k, v)
                continue
            elif tempKey == 'stylesFactory':
                UIComponentDescriptor.__skipFunctionDeclaration(inputObjectProcessor, 'void')
                if inputObjectProcessor.skipSpace().readChar() != '{':
                    raise RuntimeError('illegal syntax')
                stylesDict = UIComponentDescriptor.stylesFactoryParser(\
                    inputObjectProcessor.unRead(1).readStringWithSameLayerBracket('{'))
                for (k, v) in stylesDict.items():
                    resultDescriptor.addAttribute(k, v)
                continue
            elif tempKey == 'propertiesFactory':
                UIComponentDescriptor.__skipFunctionDeclaration(inputObjectProcessor, 'Object')
                if inputObjectProcessor.skipSpace().readChar() != '{':
                    raise RuntimeError('illegal syntax')
                (attrsDict, childrenList) = UIComponentDescriptor.propertiesFactoryParser(\
                    inputObjectProcessor.unRead(1).readStringWithSameLayerBracket('{'))
                for (k, v) in attrsDict.items():
                    resultDescriptor.addAttribute(k, v)
                for child in iter(childrenList):
                    resultDescriptor.addChild(child)
                continue
        return resultDescriptor
    @staticmethod
    def eventsParser(eventsString):
        '''
        parse event string to dictionry
        input: '{"change":"onChange"}'
        output: {"change":"onChange"}
        '''
        resultDict = {}
        processor = StringProcessor(eventsString)
        if processor.skipSpace().readChar() != '{':
            raise RuntimeError('illegal syntax')
        while True:
            tempKey = processor.skipSpace().skipString(',').skipSpace().readStringWithWrapper('"')
            if tempKey == '}' or tempKey == '':
                break
            tempKey = StringProcessor.cutHeadAndTail(tempKey)
            if processor.skipSpace().readChar() != ':':
                raise RuntimeError('illegal syntax')
            tempVal = processor.skipSpace().readStringWithWrapper('"')
            if tempVal == '':
                raise RuntimeError('illegal syntax')
            tempVal = StringProcessor.cutHeadAndTail(tempVal) + '(event)'
            resultDict[tempKey] = tempVal
        return resultDict
    @staticmethod
    def stylesFactoryParser(stylesString):
        '''
        parse styles factory string to dictionary
        input: '{this.borderStyle = "none";}'
        output: {"borderStyle":"none"}
        '''
        stylesDict = {}
        processor = StringProcessor(stylesString)
        if processor.skipSpace().readChar() != '{':
            raise RuntimeError('illegal syntax')
        while True:
            tempWord = processor.skipSpace().skipString(';').skipSpace().readWord()
            if tempWord == '}':
                break
            if tempWord == 'this':
                if processor.skipSpace().readChar() != '.':
                    raise RuntimeError('illegal syntax')
                tempWord = processor.skipSpace().readWord()
            tempKey = tempWord
            tempChar = processor.skipSpace().readChar()
            if  tempChar != '=':
                raise RuntimeError('illegal syntax')
            tempChar = processor.skipSpace().readChar()
            if tempChar == '':
                raise RuntimeError('illegal syntax')
            processor.unRead(1)
            if tempChar == '"':
                tempVal = StringProcessor.cutHeadAndTail(processor.readStringWithWrapper('"'))
            else:
                tempVal = processor.readWord()
            stylesDict[tempKey] = tempVal
        return stylesDict
    @staticmethod
    def propertiesFactoryParser(propFactoryString):
        '''
        parse properties factory string to dictionry
        input: '{return ({"width":100, "height":100, "childDescriptors":[....]})}'
        output: ({"width":"100", "height":"100"}, [child1, child2])
        '''
        attributeDict = {}
        childrenList = []
        preProcessor = StringProcessor(propFactoryString)
        if preProcessor.skipSpace().readChar() != '{':
            raise RuntimeError('illegal syntax')
        if preProcessor.skipSpace().readWord() != 'return':
            raise RuntimeError('illegal syntax')
        if preProcessor.skipSpace().readChar() != '(':
            raise RuntimeError('illegal syntax')
        if preProcessor.skipSpace().readChar() != '{':
            raise RuntimeError('illegal syntax')
        preProcessor.unRead(1)
        processor = StringProcessor(preProcessor.readStringWithSameLayerBracket('{'))
        if processor.skipSpace().readChar() != '{':
            raise RuntimeError('illegal syntax')
        while True:
            tempWord = processor.skipSpace().skipString(',').skipSpace().readStringWithWrapper('"')
            if tempWord == '':
                tempWord = processor.skipSpace().readChar()
                if  tempWord == '}':
                    break
                else:
                    raise RuntimeError('illegal syntax')
            tempKey = StringProcessor.cutHeadAndTail(tempWord)
            if processor.skipSpace().readChar() != ':':
                raise RuntimeError('illegal syntax')
            if tempKey == 'childDescriptors':
                childrenList = UIComponentDescriptor.childrenListParser(\
                    processor.skipSpace().readStringWithSameLayerBracket('['))
            else:
                tempChar = processor.skipSpace().readChar()
                processor.unRead(1)
                if tempChar == '"':
                    tempWord = StringProcessor.cutHeadAndTail(processor.readStringWithWrapper('"'))
                elif tempChar == '[':
                    tempWord = processor.skipSpace().readStringWithSameLayerBracket('[')
                    tempWord = StringProcessor.cutHeadAndTail(tempWord)
                    tempList = tempWord.split(',')
                    for tempWord in tempList:
                        tempWord = tempWord.replace(' ', '')
                        tempWord = tempWord.replace('\n', '')
                        tempWord = tempWord.replace('\r', '')
                        tempWord = tempWord.replace('\t', '')
                        childrenList.append(UIComponentDescriptor(True).setType(tempWord))
                    continue
                else:
                    tempWord = processor.readWord()
                tempVal = tempWord
                attributeDict[tempKey] = tempVal
        return (attributeDict, childrenList)
    @staticmethod
    def childrenListParser(childDescriptorString):
        '''
        input: '[.....]'
        add children to childrenList of propertiesFactoryParser function
        '''
        resultList = []
        processor = StringProcessor(childDescriptorString)
        if processor.skipSpace().readChar() != '[':
            raise RuntimeError('illegal syntax')
        while True:
            tempWord = processor.skipSpace().skipString(',').skipSpace().readWord() 
            if tempWord == ']':
                break
            if tempWord != 'new':
                raise RuntimeError('illegal syntax')
            if processor.skipSpace().readWord() != 'UIComponentDescriptor':
                raise RuntimeError('illegal syntax')
            if processor.skipSpace().readChar() != '(':
                raise RuntimeError('illegal syntax')
            if processor.skipSpace().readChar() != '{':
                raise RuntimeError('illegal syntax')
            processor.unRead(2)
            resultList.append(UIComponentDescriptor.parserDescriptorFromString(\
                'new UIComponentDescriptor ' + processor.readStringWithSameLayerBracket('(')))
        return resultList
class StringProcessor:
    '''
    add convenience to analyse string
    '''
    def __init__(self, s):
        self.__strBuffer = s
        self.__pointer = 0
    def skipSpace(self):
        '''
        ignore spaces
        '''
        strLen = len(self.__strBuffer)
        while self.__pointer < strLen and self.__strBuffer[self.__pointer].isspace():
            self.__pointer += 1
        return self
    def readChar(self):
        '''
        return current char and move pointer
        return empty string if there is no char in buffer
        '''
        if self.__pointer == len(self.__strBuffer):
            return ''
        self.__pointer += 1
        return self.__strBuffer[self.__pointer - 1]
    def readWord(self):
        '''
        return current word and move pointer
        a word is alphanumeric, or a float number
        return current symbol if current pointer points to a unalphanumeric symbol
        return empty string if there is no char in buffer
        '''
        strLen = len(self.__strBuffer)
        if self.__pointer >= strLen:
            return ''
        tempPointer = self.__pointer
        if self.__strBuffer[self.__pointer] == '0':
            self.__pointer += 1
            if self.__pointer <= strLen:
                if self.__strBuffer[self.__pointer] == 'x' or self.__strBuffer[self.__pointer] == 'X':
                    while self.__pointer < strLen and (self.__strBuffer[self.__pointer].isalnum()):
                        self.__pointer += 1
            else:
                pass
        elif self.__strBuffer[self.__pointer] == '.' or self.__strBuffer[self.__pointer].isnumeric():
            tempString = self.__strBuffer[self.__pointer]
            self.__pointer += 1
            while self.__pointer < strLen:
                tempString += self.__strBuffer[self.__pointer]
                if not StringProcessor.isFloat(tempString):
                    break
                self.__pointer += 1
        elif not (self.__strBuffer[self.__pointer].isalnum() or self.__strBuffer[self.__pointer] == '_'):
            self.__pointer += 1
        else:
            while self.__pointer < strLen and (self.__strBuffer[self.__pointer].isalnum() or self.__strBuffer[self.__pointer] == '_'):
                self.__pointer += 1
        return self.__strBuffer[tempPointer:self.__pointer]
    def readStringWithWrapper(self, wrapperString):
        '''
        return sub string and move pointer
        the string is begin with the wrapper string,
        and end with it, if not, return empty string
        also return empty string when there is no char in buffer
        '''
        wrapperLen = len(wrapperString)
        subStr = wrapperString
        headStr = self.readString(wrapperLen)
        if headStr != wrapperString:
            self.unRead(len(subStr))
            return ''
        while True:
            tempChar = self.readChar()
            if tempChar == '':
                self.unRead(len(subStr))
                return ''
            if tempChar == wrapperString[0]:
                self.unRead(1)
                tempStr = self.readString(wrapperLen)
                if tempStr == wrapperString:
                    subStr += tempStr
                    return subStr
                self.unRead(len(tempStr) - 1)
            subStr += tempChar
    def readString(self, charNum):
        '''
        return sub string from string buffer,
        if char num is equal or less than 0,
        it will return empty string
        if there is no enough chars in buffer,
        it will return all chars left in buffer
        '''
        if charNum <= 0:
            return ''
        strLen = len(self.__strBuffer)
        if self.__pointer >= strLen:
            return ''
        tempPointer = self.__pointer
        self.__pointer += charNum
        if self.__pointer >= strLen:
            self.__pointer = strLen
        return self.__strBuffer[tempPointer:self.__pointer]
    def unRead(self, charNum):
        '''
        move pointer back charNum chars
        '''
        if charNum <= 0:
            return self
        self.__pointer -= charNum
        if self.__pointer < 0:
            self.__pointer = 0
        return self
    def readStringWithSameLayerBracket(self, headBracket):
        '''
        get a sub string that is wrapped by headBracket and tailBracket
        it will ensure that the two brackets are in the same layer
        '''
        if headBracket == '{':
            tailBracket = '}'
        elif headBracket == '[':
            tailBracket = ']'
        elif headBracket == '(':
            tailBracket = ')'
        elif headBracket == '<':
            tailBracket = '>'
        else:
            tailBracket = ''
        if tailBracket == '':
            raise  RuntimeError('illegal bracket : ' + headBracket)
        currentLayer = 0
        headPointer = self.__pointer
        tempChar = self.readChar()
        if tempChar == '':
            return ''
        if tempChar != headBracket:
            self.unRead(1)
            return ''
        while True:
            tempChar = self.readChar()
            if tempChar == '"' or tempChar == "'":
                self.unRead(1)
                if self.readStringWithWrapper(tempChar) == '':
                    raise RuntimeError('illegal syntax')
            elif tempChar == headBracket:
                currentLayer += 1
            elif tempChar == tailBracket:
                if currentLayer > 0:
                    currentLayer -= 1
                else:
                    return self.__strBuffer[headPointer:self.__pointer]
            elif tempChar == '':
                raise RuntimeError('illegal syntax')
            else:
                pass
    def skipString(self, s):
        '''
        jump string and return self
        '''
        strLen = len(s)
        if self.readString(strLen) != s:
            self.unRead(strLen)
        return self
    def getStringInBuffer(self):
        '''
        return string left in buffer
        '''
        if self.__pointer >= len(self.__strBuffer):
            return ''
        else:
            return self.__strBuffer[self.__pointer:len(self.__strBuffer) - 1]
    @staticmethod
    def isWrappedBy(originalString, wrapperString, ignoreSideSpaces = True):
        '''
        determine if originalString is wrapped by wrapperString
        ignoreSideSpaces is used to setting whether it should ignore the front and end spaces
        '''
        if ignoreSideSpaces:
            currentString = StringProcessor.removeFrontEndSpaces(originalString)
        else:
            currentString = originalString
        wrapperLen = len(wrapperString)
        headStr = currentString[0:wrapperLen]
        if headStr != wrapperString:
            return False
        currentLen = len(currentString)
        tailStr = currentString[currentLen - wrapperLen:currentLen]
        if tailStr != wrapperString:
            return False
        return True
    @staticmethod
    def getNoneSpaceSite(originalString):
        '''
        get front and end site that is not spaces
        output: (headSite, tailSite)
        if no non-space char in string, headSite will larger than tailSite
        '''
        headSite = 0
        tailSite = len(originalString) - 1
        while headSite <= tailSite and originalString[headSite].isspace():
            headSite += 1
        if headSite <= tailSite:
            while originalString[tailSite].isspace():
                tailSite -= 1
        return (headSite, tailSite)
    @staticmethod
    def removeFrontEndSpaces(originalString):
        '''
        remove the spaces of originalString and return
        '''
        (head, tail) = StringProcessor.getNoneSpaceSite(originalString)
        if head > tail:
            return ''
        else:
            return originalString[head:tail + 1]
    @staticmethod
    def cutHeadAndTail(s):
        '''
        delete first char and the last char
        '''
        return s[1:len(s) - 1]
    @staticmethod
    def isFloat(s):
        '''
        return if the input string is a number, include '.'
        '''
        if s.isnumeric():
            return True
        partition = s.partition('.')
        if (partition[0].isdigit() and partition[1]=='.' and partition[2].isdigit()) or \
            (partition[0]=='' and partition[1]=='.' and partition[2].isdigit()) or \
            (partition[0].isdigit() and partition[1]=='.' and partition[2]==''):
            return True
        return False

def uiComponentDescripter2XML(uiComponentDescripter, typePrefixDict, defaultPrefix):
    '''
    convert UIComponentDescriptor to XML
    '''
    def addPrefix(s):
        if s in typePrefixDict:
            return typePrefixDict[s] + str(s)
        else:
            return defaultPrefix + str(s)
    def createXMLNode(doc, descriptor):
        if descriptor.isSimple():
            node = doc.createElement(descriptor.getType())
        else:
            node = doc.createElement(addPrefix(descriptor.getType()))
        if descriptor.getID() != '':
            node.setAttribute('id', descriptor.getID())
        for (k, v) in descriptor.getEventIter():
            node.setAttribute(k, v)
        for (k, v) in descriptor.getAttributeIter():
            node.setAttribute(k, v)
        for child in descriptor.getChildrenIter():
            node.appendChild(createXMLNode(doc, child))
        return node
    document = Document()
    document.appendChild(createXMLNode(document, uiComponentDescripter))
    return document

def fromFileToFile(readPath, typePrefixDict = {}, defaultPrefix = '', writePath = ''):
    '''
    read file descriptor from readPath, and write XML to writePath
    '''
    if writePath == '':
        writePath = readPath + '.xml'
    readFile = file = open(readPath, 'rb')
    len = readFile.seek(0, 2)
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