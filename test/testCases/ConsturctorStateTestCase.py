import unittest
import FileProcessor
import ConstructorState
import os.path as path

class ConsturctorStateTestCase(unittest.TestCase):
    pass

class ConstructorStateFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        p = path.abspath('test/testFiles/constructor_state.txt')
        self.testStr = FileProcessor.readAllFromFile(p)
    def tearDown(self):
        return super().tearDown() 
    def testSplitStatements(self):
        statementsList = ConstructorState.splitStatements(self.testStr)
        assert statementsList[0].getHead() == 'this.abc=1+2'
        assert statementsList[1].getHead() == 'abcde()'
        assert statementsList[2].getHead() == 'this.def'
        assert statementsList[3].getHead() == ''
        assert statementsList[4].getHead() == ''
        assert statementsList[5].getHead() == 'if(a>b){'
        assert statementsList[5].getChildStatementCount() == 2
        assert statementsList[5].getChildStatementAt(0).getHead() == 'this.def="abc"'
        assert statementsList[5].getChildStatementAt(1).getHead() == 'this.abc=1+2'
        assert statementsList[0].getTail() == ';'
        assert statementsList[1].getTail() == ';'
        assert statementsList[2].getTail() == ';'
        assert statementsList[3].getTail() == ';'
        assert statementsList[4].getTail() == ';'
        assert statementsList[5].getTail() == '}'
        assert statementsList[5].getChildStatementAt(0).getTail() == ';'
        assert statementsList[5].getChildStatementAt(1).getTail() == ';'

if __name__ == '__main__':
    unittest.main()
