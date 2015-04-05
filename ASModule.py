from StringProcessor import StringProcessor
import FileProcessor
class ASFunction:
    def __init__(self, name=''):
        self.__name = name
        self.__body = ''
        self.__returnType = 'void'
        self.__argumentDict = {}
    def getName(self):
        return self.__name
    def setName(self, name):
        self.__name = name
        return self
    def getReturnType(self):
        return self.__returnType
    def setReturnType(self, type):
        self.__returnType = type
        return self
    def getBody(self):
        return self.__body
    def setBody(self, body):
        self.__body = body
        return self
    def hasArgument(self, argumentName):
        return argumentName in self.__argumentDict
    def setArgument(self, argument):
        self.__argumentDict[argument.getName()] = argument
        return self
    def removeArgument(self, argument):
        if argument.getName() in self.__argumentDict:
            del self.__argumentDict[argument.getName()]
        return self
    def getArgumentsIter(self):
        return self.__argumentDict.items()

class ASVariable:
    def __init__(self, name=''):
        self.__name = name
        self.__value = ''
        self.__type = ''
    def getName(self):
        return self.__name
    def setName(self, name):
        self.__name = name
        return self
    def getType(self):
        return self.__type
    def setType(self, type):
        self.__type = type
        return self
    def getValue(self):
        return self.__value
    def setValue(self, value):
        self.__value = value
        return self

class ASClass:
    def __init__(self):
        self.__name = ''
        self.__funcDict = {}
        self.__varDict = {}
    def getName(self):
        return self.__name
    def setName(self, name):
        self.__name = name
        return self
    def setFunction(self, function):
        self.__funcDict[function.getName()] = function
    def removeFunction(self, function):
        if function.getName() in self.__funcDict:
            del self.__funcDict[function.getName()]
        return self
    def hasFunction(self, functionName):
        return functionName in self.__funcDict
    def getFunctionsIter(self):
        return self.__funcDict.items()
    def setVariable(self, variable):
        self.__varDict[variable.getName()] = variable
    def removeVariable(self, variable):
        if variable.getName() in self.__varDict:
            del self.__varDict[variable.getName()]
        return self
    def hasVariable(self, variableName):
        return variableName in self.__varDict
    def getVariablesIter(self):
        return self.__varDict.items()

def isLegalName(s):
    tempStr = s.strip()
    if tempStr == '':
        return False
    if tempStr[0].isnumeric():
        return False
    for pointer in range(0, len(tempStr)):
        if not (tempStr[pointer].isalnum() or tempStr[pointer] == '_'):
            return False
    return True

def isLegalNumber(s):
    tempStr = s.strip()
    if tempStr == '':
        return False
    if not tempStr.startswith('0'):
        try:
            float(tempStr)
        except:
            return False
    if tempStr.startswith('0x'):
        try:
            int(tempStr, 16)
        except:
            return False
    elif tempStr.startswith('0'):
        try:
            int(tempStr, 8)
        except:
            return False
    return True

def isLegalValue(s):
    if isLegalNumber(s) or isLegalName(s):
        return True
    if StringProcessor.isWrappedBy(s.strip(), '"') or StringProcessor.isWrappedBy(s.strip(), "'"):
        return True
    return False

def removeComments(s):
    resultStr = ''
    strlen = len(s)
    pointer = 0
    while True:
        if pointer >= strlen:
            return resultStr
        tempChar = s[pointer]
        if tempChar == '"' or tempChar == "'":
            resultStr += tempChar
            pointer += 1
            while True:
                if pointer >= strlen:
                    raise RuntimeError('end of file encountered when finding ' + quote)
                if s[pointer] == '\\':
                    resultStr += '\\'
                    pointer += 1
                    if pointer >= strlen:
                        raise RuntimeError('read to the end of file after \\ when finding ' + quote)
                    resultStr += s[pointer]
                elif s[pointer] == tempChar:
                    resultStr += tempChar 
                    pointer += 1
                    break
                else:
                    resultStr += s[pointer]
                pointer += 1
        elif tempChar == '/':
            pointer += 1
            tempChar = s[pointer]
            if tempChar == '/':
                pointer += 1
                while pointer < strlen:
                    pointer += 1
                    if s[pointer - 1] == '\n':
                        if s[pointer - 2] == '\r':
                            resultStr += '\r\n'
                        resultStr += '\n'
                        break
            elif tempChar == '*':
                pointer += 1
                while True:
                    while True:
                        if pointer >= strlen:
                            raise RuntimeError('illegal syntax, hanging /*')
                        if s[pointer] == '\\':
                            pointer += 1
                            if pointer >= strlen:
                                raise RuntimeError('illegal syntax, hanging /*')
                            pointer += 1
                        elif s[pointer] == '*':
                            pointer += 1
                            break
                        else:
                            pointer += 1
                    tempChar = s[pointer]
                    if tempChar == '/':
                        pointer += 1
                        break
                    else:
                        pointer += 1
            else:
                raise RuntimeError('illegal syntax, hanging /')
        else:
            resultStr += s[pointer]
            pointer += 1

if __name__ == '__main__':
    s = FileProcessor.readAllFromFile('D:\\testin.txt')
    s = removeComments(s)
    FileProcessor.writeAllToFile(s, 'D:\\testout.txt')