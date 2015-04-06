from StringProcessor import StringProcessor
import FileProcessor
class ASMember:
    def __init__(self, name=''):
        self._name = name
        self._body = ''
        self._type = ''
        self._access = ''
        self._isStatic = False
    def getName(self):
        return self._name
    def setName(self, name):
        self._name = name
        return self
    def getType(self):
        return self._type
    def setType(self, type):
        self._type = type
        return self
    def getAccessPermission(self):
        return self._access
    def setAccessPermission(self, access):
        self._access = access
        return self
    def isStatic(self):
        return self._isStatic
    def setStatic(self, boolean):
        if boolean:
            self._isStatic = True
        else:
            self._isStatic = False
        return self

class ASFunction(ASMember):
    _USAGE_NORMAL = 0
    _USAGE_GETTER = 1
    _USAGE_SETTER = 2
    def __init__(self, name=''):
        super(ASFunction, self).__init__(name)
        self._body = ''
        self._argumentDict = {}
        self._isFinal = False
        self._usage = ASFunction._USAGE_NORMAL
    def getBody(self):
        return self._body
    def setBody(self, body):
        self._body = body
        return self
    def hasArgument(self, argumentName):
        return argumentName in self._argumentDict
    def setArgument(self, argument):
        self._argumentDict[argument.getName()] = argument
        return self
    def removeArgument(self, argument):
        if argument.getName() in self._argumentDict:
            del self._argumentDict[argument.getName()]
        return self
    def getArgumentsIter(self):
        return self._argumentDict.items()
    def isFinal(self):
        return self._isFinal
    def setFinal(self, boolean):
        if boolean:
            self._isFinal = True
        else:
            self._isFinal = False
        return self
    def isGetter(self):
        return self._usage == ASFunction._USAGE_GETTER
    def isSetter(self):
        return self._usage == ASFunction._USAGE_SETTER
    def isNormal(self):
        return self._usage == ASFunction._USAGE_NORMAL
    def setGetter(self):
        self._usage = ASFunction._USAGE_GETTER
        return self
    def setSetter(self):
        self._usage = ASFunction._USAGE_SETTER
        return self
    def setNormal(self):
        self._usage = ASFunction._USAGE_NORMAL
        return self

class ASVariable(ASMember):
    def __init__(self, name=''):
        super(ASVariable, self).__init__(name)
        self._value = ''
        self._isConst = False
    def getValue(self):
        return self._value
    def setValue(self, value):
        self._value = value
    def isConst(self):
        return self._isConst
    def setConst(self, boolean):
        if boolean:
            self._isConst = True
        else:
            self._isConst = False
        return self

class ASClass:
    def __init__(self):
        self._name = ''
        self._access = ''
        self._implementsSet = set([])
        self._extend = ''
        self._importsSet = set([])
        self._funcsDict = {}
        self._gettersDict = {}
        self._settersDict = {}
        self._varsDict = {}
    def getName(self):
        return self._name
    def setName(self, name):
        self._name = name
        return self
    def setFunction(self, function):
        self._funcsDict[function.getName()] = function
    def removeFunction(self, function):
        if function.getName() in self._funcsDict:
            del self._funcsDict[function.getName()]
        return self
    def hasFunction(self, functionName):
        return functionName in self._funcsDict
    def getFunctionsIter(self):
        return self._funcsDict.items()

    def setGetter(self, getter):
        self._gettersDict[getter.getName()] = getter
    def removeGetter(self, getter):
        if getter.getName() in self._gettersDict:
            del self._gettersDict[getter.getName()]
        return self
    def hasGetter(self, getterName):
        return getterName in self._gettersDict
    def getGettersIter(self):
        return self._gettersDict.items()

    def setSetter(self, setter):
        self._settersDict[setter.getName()] = setter
    def removeSetter(self, setter):
        if setter.getName() in self._settersDict:
            del self._settersDict[setter.getName()]
        return self
    def hasSetter(self, setterName):
        return setterName in self._settersDict
    def getSettersIter(self):
        return self._settersDict.items()

    def setVariable(self, variable):
        self._varsDict[variable.getName()] = variable
    def removeVariable(self, variable):
        if variable.getName() in self._varsDict:
            del self._varsDict[variable.getName()]
        return self
    def hasVariable(self, variableName):
        return variableName in self._varsDict
    def getVariablesIter(self):
        return self._varsDict.items()
    def hasImplement(self, implement):
        return implement in self._implementsSet
    def addImplement(self, implement):
        self._implementsSet.add(implement)
        return self
    def getImplementsIter(self):
        return iter(self._implementsSet)
    def getAccessPermission(self):
        return self._access
    def setAccessPermission(self, accessPermission):
        self._access = accessPermission
        return self
    def getExtend(self):
        return self._extend 
    def setExtend(self, extend):
        self._extend = extend
        return self
    def hasImport(self, imp):
        return imp in self._importsSet
    def addImport(self, imp):
        self._importsSet.add(imp)
        return self
    def getImportsIter(self):
        return iter(self._importsSet)

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
    pass