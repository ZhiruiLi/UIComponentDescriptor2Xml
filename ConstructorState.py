from StringProcessor import StringProcessor
class ConstructorState(object):
    _currentString = ''
    @staticmethod
    def nextState(s):
        return ConstructorState
    @staticmethod
    def isStart():
        return False
    @staticmethod
    def isEnd():
        return False
    @staticmethod
    def isError():
        return False

class StartState(ConstructorState):
    @staticmethod
    def isStart():
        return True
    @staticmethod
    def nextState(s):
        return super().nextState()



'''
class Statement:
    def __init__(self):
        self._childStatements = []
        self._head = ''
        self._tail = ''
    def getHead(self):
        return self._head
    def setHead(self, head):
        self._head = head
        return self
    def appendHead(self, append):
        self._head += append
        return self
    def getTail(self):
        return self._tail
    def setTail(self, tail):
        self._tail = tail
        return self
    def appendTail(self, append):
        self._tail += append
        return self
    def addChildStatement(self, statement):
        self._childStatements.append(statement)
        return self
    def getChildStatementsIter(self):
        return iter(self._childStatements)
    def getChildStatementAt(self, site):
        return self._childStatements[site]
    def getChildStatementCount(self):
        return len(self._childStatements)
    def removeChildStatement(self, statement):
        if statement in self._childStatements:
            self._childStatements.remove(statement)
        return self

def splitStatements(s):
    processor = StringProcessor(s)
    resultList = []
    tempStatement = Statement() 
    while True:
        tempWord = processor.skipSpace().readWord()
        if tempWord == '':
            if not tempStatement == None:
                raise RuntimeError('string ends incorrectly')
            return resultList
        if tempStatement == None:
            tempStatement = Statement() 
        if tempWord == '"':
            processor.unRead(1)
            tempWord = processor.readStringWithWrapper('"')
            if tempWord == '':
                raise RuntimeError('can not find tail quote')
            tempStatement.appendHead(tempWord)
        elif tempWord == '{':
            tempStatement.appendHead(tempWord)
            processor.unRead(1)
            tempWord = processor.readStringWithSameLayerBracket('{')
            if tempWord == '':
                raise RuntimeError('can not find tail brace')
            tempWord = StringProcessor.cutHeadAndTail(tempWord)
            for child in splitStatements(tempWord):
                tempStatement.addChildStatement(child)
            tempStatement.appendTail('}')
            resultList.append(tempStatement)
            tempStatement = None
        elif tempWord == ';':
            tempStatement.appendTail(tempWord)
            resultList.append(tempStatement)
            tempStatement = None
        else:
            tempStatement.appendHead(tempWord)
'''