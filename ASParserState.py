import ASModule
from StringProcessor import StringProcessor
import FileProcessor

class ASPaserState:
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
        s = currentReadString.strip()
        if s == 'package':
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
            return ClassDec1
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
        return ErrorState

class ClassDec1(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'class':
            return ClassDec2
        return ErrorState

class ClassDec2(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
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
            return ClassExtends2
        return ErrorState

class ClassExtends2(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '.':
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
            return ClassImplements2
        return ErrorState

class ClassImplements2(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '.':
            return ClassImplements1
        if currentReadString == '{':
            return InClass

class InClass(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            return InClass
        if currentReadString == '}':
            return EndClass
        if currentReadString == 'public' or currentReadString == 'private' or currentReadString == 'protected':
            return MemberDec
        if currentReadString == 'static':
            return StaticMemDec
        if currentReadString == 'final':
            return FinalFuncDec
        if currentReadString == 'var':
            return VarDec
        if currentReadString == 'const':
            return ConstDec
        if currentReadString == 'function':
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
            return StaticMemDec
        if currentReadString == 'final':
            return FinalFuncDec
        if currentReadString == 'var':
            return VarDec
        if currentReadString == 'const':
            return ConstDec
        if currentReadString == 'function':
            return FuncDec
        return ErrorState

class StaticMemDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == 'final':
            return FinalFuncDec
        if currentReadString == 'var':
            return VarDec
        if currentReadString == 'const':
            return ConstDec
        if currentReadString == 'function':
            return FuncDec
        return ErrorState

class EndClass(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            return EndClass
        if currentReadString == '}':
            return EndPkg
        return ErrorState

class ConstDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            return VarName
        return ErrorState

class VarDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
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
            return VarTypeName
        return ErrorState

class VarTypeName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            return InClass 
        if currentReadString == '.':
            return VarTypeNamePoint
        if currentReadString == '=':
            return VarValue
        return ErrorState

class VarTypeNamePoint(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            return VarTypeName

class VarValue(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ';':
            return InClass
        return VarValue

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
            return GetFuncDec
        if currentReadString == 'set':
            return SetFuncDec
        if ASModule.isLegalName(currentReadString):
            return FuncName
        return ErrorState

class GetFuncDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            return GetFuncName
        return ErrorState

class SetFuncDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
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
            return FuncArgName
        return ErrorState

class FuncArgName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ',':
            return FuncArgDec
        if currentReadString == ':':
            return FuncArgTypeDec
        if currentReadString == ')':
            return EndFuncArgDec
        return ErrorState

class FuncArgTypeDec(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            return FuncArgTypeName
        return ErrorState

class FuncArgTypeName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == ',':
            return FuncArgDec
        if currentReadString == ')':
            return EndFuncArgDec
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
            return FuncTypeName
        return ErrorState

class FuncTypeName(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if currentReadString == '.':
            return FuncTypeNamePoint
        if currentReadString == '{':
            return InFunc
        return ErrorState

class FuncTypeNamePoint(ASPaserState):
    @staticmethod
    def nextPaser(currentReadString):
        if ASModule.isLegalName(currentReadString):
            return FuncTypeName
        return ErrorState

class InFunc(ASPaserState):
    __layer = 0
    @staticmethod
    def nextPaser(currentReadString):
        print('InFunc.__layer is ' + str(InFunc.__layer))
        if currentReadString == '}':
            if InFunc.__layer <= 0:
                return InClass
            else:
                InFunc.__layer -= 1
        if currentReadString == '{':
            InFunc.__layer += 1
        return InFunc

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

def parseASString(s):
    processor = StringProcessor(s)
    state = StartState
    while not state.isEnd():
        print(state)
        tempWord = processor.skipSpace().readWord()
        print(tempWord)
        state = state.nextPaser(tempWord)
    print(state)

if __name__ == '__main__':
    s = FileProcessor.readAllFromFile('D:\\teststate.as')
    s = ASModule.removeComments(s)
    parseASString(s)