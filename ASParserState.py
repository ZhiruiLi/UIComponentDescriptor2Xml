import ASModule
from StringProcessor import StringProcessor

class ASPaserState:
    _currentClass = None
    _currentFunc = None
    _currentVar = None
    _currentArgument = None
    _currentImplement = ''
    @staticmethod
    def nextPaser(currentReadString):
        raise RuntimeError('unknown state')
    @staticmethod
    def isStart():
        return False
    @staticmethod
    def isEnd():
        return False
    @staticmethod
    def isError():
        return False

class StartState(ASPaserState):
    @staticmethod
    def isStart():
        return True
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'package':
            ASPaserState._currentClass = ASModule.ASClass()
            return PkgDec1
        else:
            return ErrorState

class ErrorState(ASPaserState):
    @staticmethod
    def isEnd():
        return True
    @staticmethod
    def isError():
        return True
    @staticmethod
    def nextPaser(currentReadString):
        return self

class EndPkg(ASPaserState):
    @staticmethod
    def isEnd():
        return True
    @staticmethod
    def nextPaser(currentReadString):
        return EndPkg
    
class PkgDec1(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            return PkgDec2
        if currentReadString == '{':
            return InPkg
        return ErrorState

class PkgDec2(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '.':
            return PkgDec1
        if currentReadString == '{':
            return InPkg
        return ErrorState

class InPkg(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            return InPkg
        if currentReadString == '}':
            return EndPkg
        if currentReadString == 'import':
            return ImportPkg1
        if currentReadString == 'public':
            return ClassAccessPermission
        if currentReadString == 'use':
            return NameSpaceDec1
        return ErrorState

class ImportPkg1(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '*':
            return ImportPkgAll
        if ASModule.isLegalName(currentReadString):
            return ImportPkg2
        return ErrorState

class ImportPkg2(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '.':
            return ImportPkg1
        if currentReadString == ';':
            return InPkg
        return ErrorState

class ImportPkgAll(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            return InPkg
        return ErrorState

class NameSpaceDec1(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'namespace':
            return NameSpaceDec2
        return ErrorState

class NameSpaceDec2(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            return NameSpaceName
        return ErrorState

class NameSpaceName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            return InPkg
        return NameSpaceName

class ClassAccessPermission(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'class':
            return ClassDec
        return ErrorState

class ClassDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            ASPaserState._currentClass.setName(currentReadString)
            return ClassName
        return ErrorState

class ClassName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'extends':
            return ClassExtends1
        if currentReadString == 'implements':
            return ClassImplements1
        if currentReadString == '{':
            return InClass
        return ErrorState

class ClassExtends1(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            tempClass = ASPaserState._currentClass
            tempClass.setExtend(tempClass.getExtend() + currentReadString)
            return ClassExtends2
        return ErrorState

class ClassExtends2(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '.':
            tempClass = ASPaserState._currentClass
            tempClass.setExtend(tempClass.getExtend() + currentReadString)
            return ClassExtends1
        if currentReadString == '{':
            return InClass
        if currentReadString == 'implements':
            return ClassImplements1
        return ErrorState

class ClassImplements1(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            ASPaserState._currentImplement += currentReadString
            return ClassImplements2
        return ErrorState

class ClassImplements2(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '.':
            ASPaserState._currentImplement += currentReadString
            return ClassImplements1
        if currentReadString == '{':
            ASPaserState._currentClass.addImplement(ASPaserState._currentImplement)
            ASPaserState._currentImplement = ''
            return InClass
        if currentReadString == ',':
            ASPaserState._currentClass.addImplement(ASPaserState._currentImplement)
            ASPaserState._currentImplement = ''
            return ClassImplements1
        return ErrorState

class InClass(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            return InClass
        if currentReadString == '}':
            tempClass = ASPaserState._currentClass 
            if tempClass != None:
                '''
                print('class name : ' + tempClass.getName())
                print('class extend : ' + tempClass.getExtend())
                print('class implement : ')
                for imp in tempClass.getImplementsIter():
                    print('--' + imp)
                print('class vars : ')
                for (varName, var) in tempClass.getVariablesIter():
                    print('--' + varName)
                print('class funcs : ')
                for (funcName, func) in tempClass.getFunctionsIter():
                    print('--' + funcName)
                print('class getters : ')
                for (funcName, func) in tempClass.getGettersIter():
                    print('--' + funcName)
                print('class setters : ')
                for (funcName, func) in tempClass.getSettersIter():
                    print('--' + funcName)
                '''
            return InPkg
        if currentReadString == 'public' or currentReadString == 'private' or currentReadString == 'protected':
            ASPaserState._currentFunc = ASModule.ASFunction()
            ASPaserState._currentFunc.setAccessPermission(currentReadString)
            ASPaserState._currentVar = ASModule.ASVariable()
            ASPaserState._currentVar.setAccessPermission(currentReadString)
            return MemberDec
        if currentReadString == 'static':
            ASPaserState._currentFunc = ASModule.ASFunction()
            ASPaserState._currentFunc.setStatic(True)
            ASPaserState._currentVar = ASModule.ASVariable()
            ASPaserState._currentVar.setStatic(True)
            return StaticMemDec
        if currentReadString == 'final':
            ASPaserState._currentFunc = ASModule.ASFunction()
            ASPaserState._currentFunc.setFinal(True)
            return FinalFuncDec
        if currentReadString == 'var':
            ASPaserState._currentVar = ASModule.ASVariable()
            return VarDec
        if currentReadString == 'const':
            ASPaserState._currentVar = ASModule.ASVariable()
            ASPaserState._currentVar.setConst(True)
            return ConstDec
        if currentReadString == 'function':
            ASPaserState._currentFunc = ASModule.ASFunction()
            return FuncDec
        if currentReadString == '[':
            return MetaDataTag
        return ErrorState

class MetaDataTag(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ']':
            return InClass
        return MetaDataTag

class MemberDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'static':
            if ASPaserState._currentFunc == None:
                ASPaserState._currentFunc = ASModule.ASFunction()
            ASPaserState._currentFunc.setStatic(True)
            if ASPaserState._currentVar == None:
                ASPaserState._currentVar = ASModule.ASVariable()
            ASPaserState._currentVar.setStatic(True)
            return StaticMemDec
        if currentReadString == 'final':
            if ASPaserState._currentFunc == None:
                ASPaserState._currentFunc = ASModule.ASFunction()
            ASPaserState._currentFunc.setFinal(True)
            return FinalFuncDec
        if currentReadString == 'var':
            if ASPaserState._currentVar == None:
                ASPaserState._currentVar = ASModule.ASVariable()
            return VarDec
        if currentReadString == 'const':
            if ASPaserState._currentVar == None:
                ASPaserState._currentVar = ASModule.ASVariable()
            ASPaserState._currentVar.setConst(True)
            return ConstDec
        if currentReadString == 'function':
            if ASPaserState._currentFunc == None:
                ASPaserState._currentFunc = ASModule.ASFunction()
            return FuncDec
        return ErrorState

class StaticMemDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'final':
            ASPaserState._currentFunc.setFinal(True)
            return FinalFuncDec
        if currentReadString == 'var':
            return VarDec
        if currentReadString == 'const':
            ASPaserState._currentVar.setConst(True)
            return ConstDec
        if currentReadString == 'function':
            return FuncDec
        return ErrorState

class ConstDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            ASPaserState._currentVar.setName(currentReadString)
            return VarName
        return ErrorState

class VarDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            ASPaserState._currentVar.setName(currentReadString)
            return VarName
        return ErrorState

class VarName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            return InClass
        if currentReadString == '=':
            return VarValue
        if currentReadString == ':':
            return VarTypeDec
        return ErrorState

class VarTypeDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            tempVar = ASPaserState._currentVar
            tempVar.setType(tempVar.getType() + currentReadString)
            return VarTypeName
        return ErrorState

class VarTypeName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            '''
            print('new var : ')
            print('var name is : ' + ASPaserState._currentVar.getName())
            print('var type is : ' + ASPaserState._currentVar.getType())
            print('var val is : ' + ASPaserState._currentVar.getValue())
            print('isStatic? : ' + str(ASPaserState._currentVar.isStatic()))
            print('isConst? : ' + str(ASPaserState._currentVar.isConst()))
            '''
            ASPaserState._currentClass.setVariable(ASPaserState._currentVar)
            ASPaserState._currentVar = None
            ASPaserState._currentFunc = None
            return InClass 
        if currentReadString == '.':
            tempVar = ASPaserState._currentVar
            tempVar.setType(tempVar.getType() + currentReadString)
            return VarTypeDec
        if currentReadString == '=':
            return VarValue
        return ErrorState

class VarValue(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        appendVal = lambda:ASPaserState._currentVar.setValue(\
            ASPaserState._currentVar.getValue() +\
            currentReadString)
        if currentReadString == ';':
            '''
            print('new var : ')
            print('var name is : ' + ASPaserState._currentVar.getName())
            print('var type is : ' + ASPaserState._currentVar.getType())
            print('var val is : ' + ASPaserState._currentVar.getValue())
            print('isStatic? : ' + str(ASPaserState._currentVar.isStatic()))
            print('isConst? : ' + str(ASPaserState._currentVar.isConst()))
            '''
            ASPaserState._currentClass.setVariable(ASPaserState._currentVar)
            ASPaserState._currentVar = None
            ASPaserState._currentFunc = None
            return InClass
        if currentReadString == '"':
            appendVal()
            return InVarValueQuote
        appendVal()
        return VarValue

class InVarValueQuote(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        appendVal = lambda:ASPaserState._currentVar.setValue(ASPaserState._currentVar.getValue() + currentReadString)
        if currentReadString == '\\':
            appendVal()
            return AfterVarValueQuoteBackSlash
        if currentReadString == '"':
            appendVal()
            return VarValue
        appendVal()
        return InVarValueQuote
    
class AfterVarValueQuoteBackSlash(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        ASPaserState._currentVar.setValue(ASPaserState._currentVar.getValue() + currentReadString)
        return InVarValueQuote

class FinalFuncDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'function':
            return FuncDec
        return ErrorState

class FuncDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'get':
            ASPaserState._currentFunc.setGetter()
            return GetFuncDec
        if currentReadString == 'set':
            ASPaserState._currentFunc.setSetter()
            return SetFuncDec
        if ASModule.isLegalName(currentReadString):
            ASPaserState._currentFunc.setName(currentReadString)
            return FuncName
        return ErrorState

class GetFuncDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            ASPaserState._currentFunc.setName(currentReadString)
            return GetFuncName
        return ErrorState

class SetFuncDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            ASPaserState._currentFunc.setName(currentReadString)
            return SetFuncName
        return ErrorState

class FuncName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '(':
            return FuncArgDec
        return ErrorState

class FuncArgDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ')':
            return EndFuncArgDec
        if ASModule.isLegalName(currentReadString):
            ASPaserState._currentArgument = ASModule.ASVariable()
            ASPaserState._currentArgument.setName(currentReadString)
            return FuncArgName
        return ErrorState

class FuncArgName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ',':
            ASPaserState._currentFunc.setArgument(ASPaserState._currentArgument)
            ASPaserState._currentArgument = None
            return FuncArgDec
        if currentReadString == ':':
            return FuncArgTypeDec
        if currentReadString == ')':
            ASPaserState._currentFunc.setArgument(ASPaserState._currentArgument)
            ASPaserState._currentArgument = None
            return EndFuncArgDec
        return ErrorState

class FuncArgTypeDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            tempArg = ASPaserState._currentArgument
            tempArg.setName(tempArg.getName() + currentReadString)
            return FuncArgTypeName
        return ErrorState

class FuncArgTypeName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ',':
            ASPaserState._currentFunc.setArgument(ASPaserState._currentArgument)
            ASPaserState._currentArgument = None
            return FuncArgDec
        if currentReadString == ')':
            ASPaserState._currentFunc.setArgument(ASPaserState._currentArgument)
            ASPaserState._currentArgument = None
            return EndFuncArgDec
        if currentReadString == '.':
            tempArg = ASPaserState._currentArgument
            tempArg.setName(tempArg.getName() + currentReadString)
            return FuncArgTypeDec
        return ErrorState

class EndFuncArgDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '{':
            return InFunc
        if currentReadString == ':':
            return FuncTypeDec
        return ErrorState

class FuncTypeDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            tempFunc = ASPaserState._currentFunc
            tempFunc.setType(tempFunc.getType() + currentReadString)
            return FuncTypeName
        return ErrorState

class FuncTypeName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '.':
            tempFunc = ASPaserState._currentFunc
            tempFunc.setType(tempFunc.getType() + currentReadString)
            return FuncTypeDec
        if currentReadString == '{':
            return InFunc
        return ErrorState

class InFunc(ASPaserState):
    __layer = 0
    @staticmethod
    def nextPaser(currentReadString):
        appendBody = lambda s:ASPaserState._currentFunc.setBody(ASPaserState._currentFunc.getBody() + s)
        appendWithNewLine = lambda:appendBody(currentReadString + '\r\n')
        appendCurrent = lambda:appendBody(currentReadString)
        indentUnit = '    '
        if currentReadString == '}':
            if InFunc.__layer <= 0:
                '''
                print('read func')
                print('func name : ' + ASPaserState._currentFunc.getName())
                print('func access : ' + ASPaserState._currentFunc.getAccessPermission())
                print('func type : ' + ASPaserState._currentFunc.getType())
                print('is Final : ' + str(ASPaserState._currentFunc.isFinal()))
                print('is Static : ' + str(ASPaserState._currentFunc.isStatic()))
                print('is Normal : ' + str(ASPaserState._currentFunc.isNormal()))
                print('body : ')
                print(ASPaserState._currentFunc.getBody())
                '''
                tempFunc = ASPaserState._currentFunc
                if tempFunc.isGetter():
                    ASPaserState._currentClass.setGetter(tempFunc)
                elif tempFunc.isSetter():
                    ASPaserState._currentClass.setSetter(tempFunc)
                else:
                    ASPaserState._currentClass.setFunction(tempFunc)
                ASPaserState._currentVar = None
                ASPaserState._currentFunc = None
                return InClass
            else:
                InFunc.__layer -= 1
                appendWithNewLine()
                return InFunc
        if currentReadString == '{':
            InFunc.__layer += 1
            appendWithNewLine()
            return InFunc
        if currentReadString == '"':
            appendCurrent()
            return InFuncQuote
        if currentReadString == ';':
            appendWithNewLine()
            return InFunc
        appendCurrent()
        return InFunc

class InFuncQuote(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        appendBody = lambda:ASPaserState._currentFunc.setBody(ASPaserState._currentFunc.getBody() + currentReadString)
        if currentReadString == '\\':
            appendBody()
            return AfterInFuncQuoteBackSlash
        if currentReadString == '"':
            appendBody()
            return InFunc
        appendBody()
        return InFuncQuote
    
class AfterInFuncQuoteBackSlash(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        ASPaserState._currentFunc.setBody(ASPaserState._currentFunc.getBody() + currentReadString)
        return InFuncQuote


class GetFuncName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '(':
            return GetFuncArgDec
        return ErrorState

class GetFuncArgDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ')':
            return EndGetFuncArgDec
        return ErrorState

class EndGetFuncArgDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '{':
            return InFunc
        if currentReadString == ':':
            return FuncTypeDec
        return ErrorState

class SetFuncName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '(':
            return SetFuncArgDec
        return ErrorState

class SetFuncArgDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            return SetFuncArgName
        return ErrorState

class SetFuncArgName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ':':
            return SetFuncArgTypeDec
        if currentReadString == ')':
            return EndSetFuncArgDec
        return ErrorState

class SetFuncArgTypeDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            return SetFuncArgTypeName
        return ErrorState

class SetFuncArgTypeName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ')':
            return EndSetFuncArgDec
        return ErrorState

class EndSetFuncArgDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '{':
            return InFunc
        if currentReadString == ':':
            return FuncTypeDec
        return ErrorState

if __name__ == '__main__':
    pass