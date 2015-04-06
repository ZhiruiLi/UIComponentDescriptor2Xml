#coding=utf-8
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
        if self.__strBuffer[self.__pointer] == '0' and self.__pointer < strLen and self.__strBuffer[self.__pointer + 1].lower() == 'x':
            self.__pointer += 1
            if self.__strBuffer[self.__pointer] == 'x' or self.__strBuffer[self.__pointer] == 'X':
                while self.__pointer < strLen and (self.__strBuffer[self.__pointer].isalnum()):
                    self.__pointer += 1
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
    def unRead(self, charNum = 1):
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
    def readTo(self, token):
        '''
        read to a token and return string has read
        '''
        readString = ''
        while True:
            tempChar = self.readChar()
            if tempChar == '':
                self.unRead(len(readString))
                return ''
            if tempChar == token[0]:
                tempToken = self.unRead().readString(len(token))
                if tempToken == token:
                    readString += token
                    return readString
                self.unRead(len(tempToken) - 1)
            readString += tempChar

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

if __name__ == '__main__':
    processor = StringProcessor('aaa/ */abc123/f')
    print(processor.readTo('/*'))
    print(processor.readWord())