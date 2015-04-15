#coding=utf-8
from xml.dom.minidom import Document
from StringProcessor import StringProcessor
import codecs
class UIComponentDescriptor(object):
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
        for (k, v) in self.getAttributesIter():
            resultString += ('attribute : ' + k + ' --- ' + v + '\n')
        for (k, v) in self.getEventsIter():
            resultString += ('event : ' + k + ' --- ' + v + '\n')
        for child in self.getChildrenIter():
            resultString += ('\n' + str(child) + '\n')
        if self.__isSimple:
            resultString += 'is simple descriptor'
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
    def setAttribute(self, attrKey, attrVal):
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
    def getAttributesIter(self):
        '''
        get the attribute iterator of self
        '''
        return self.__attributes.items()
    def setEvent(self, eventKey, eventVal):
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
    def getEventsIter(self):
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
                tempType = ''
                while True:
                    tempType += inputObjectProcessor.skipSpace().readWord()
                    if tempType == '':
                        raise RuntimeError('illegal syntax')
                    charAfterType = inputObjectProcessor.readChar()
                    if charAfterType == '':
                        raise RuntimeError('illegal syntax')
                    if charAfterType == '.':
                        tempType += charAfterType
                    else:
                        inputObjectProcessor.unRead(1)
                        break
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
                    resultDescriptor.setEvent(k, v)
                continue
            elif tempKey == 'stylesFactory':
                UIComponentDescriptor.__skipFunctionDeclaration(inputObjectProcessor, 'void')
                if inputObjectProcessor.skipSpace().readChar() != '{':
                    raise RuntimeError('illegal syntax')
                stylesDict = UIComponentDescriptor.stylesFactoryParser(\
                    inputObjectProcessor.unRead(1).readStringWithSameLayerBracket('{'))
                for (k, v) in stylesDict.items():
                    resultDescriptor.setAttribute(k, v)
                continue
            elif tempKey == 'propertiesFactory':
                UIComponentDescriptor.__skipFunctionDeclaration(inputObjectProcessor, 'Object')
                if inputObjectProcessor.skipSpace().readChar() != '{':
                    raise RuntimeError('illegal syntax')
                (attrsDict, childrenList) = UIComponentDescriptor.propertiesFactoryParser(\
                    inputObjectProcessor.unRead(1).readStringWithSameLayerBracket('{'))
                for (k, v) in attrsDict.items():
                    resultDescriptor.setAttribute(k, v)
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
                    if tempWord == 'new':
                        tempConstructor = processor.skipSpace().readWord()
                        if tempConstructor == 1 and (not tempConstructor.isalpha()):
                            raise RuntimeError('illegal syntax')
                        tempWord = ''.join([tempWord, ' ', tempConstructor])
                    tempChar = processor.skipSpace().readChar()
                    processor.unRead(1)
                    if tempChar == '(':
                        tempBracket = processor.readStringWithSameLayerBracket('(')
                        if tempBracket == '':
                            raise RuntimeError('illegal syntax')
                        tempWord = tempWord + tempBracket
                        uicd = UIComponentDescriptor().setType(tempKey)
                        uicd.addChild(UIComponentDescriptor(True).setType(tempWord))
                        childrenList.append(uicd)
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
        for (k, v) in descriptor.getEventsIter():
            node.setAttribute(k, v)
        for (k, v) in descriptor.getAttributesIter():
            node.setAttribute(k, v)
        for child in descriptor.getChildrenIter():
            node.appendChild(createXMLNode(doc, child))
        return node
    document = Document()
    document.appendChild(createXMLNode(document, uiComponentDescripter))
    return document