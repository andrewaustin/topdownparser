#!/usr/bin/python
from scanner import ice9Scanner
from tree import Node
import sys

DEBUG = 0

class SyntaxError(Exception):
    def __init__(self, line, token):
        self.line = line
        self.token = token
    def __str__(self):
        if self.token == ('EOF', 'EOF'):
            return "line " + str(self.line) + ": syntax error near end of file"
        return  "line "+ str(self.line) + ": syntax error near " + self.token[1]

class ice9Parser:
    def __init__(self):
        self.token = ""
        self.tokens = []
        self.currentLine = 1
        self.current = None

    def makenode(rule):
        def modify(self):
            self.current = self.current.addChild(Node('#' + rule.func_name + '#', self.currentLine))
            val = rule(self)
            if val:
                if len(self.current.children) == 0:
                    node = self.current.remove()
                    self.current = node.parent
                else:
                    self.current = self.current.parent
            else:
                node = self.current.remove()
                self.current = node.parent
            return val
        return modify
     
    def getCurrentLine(self):
        return self.currentLine

    def getNextToken(self):
        token = self.tokens.pop(0)
        while token == ('NL', 'NL'):
            token = self.tokens.pop(0)
            self.currentLine += 1
        return token

    def parse(self, tokens):
        # make sure each parse tree is fresh
        self.__init__()
        self.tokens = tokens
        try:
            self.Goal()
            if DEBUG:
                print self.current
        except SyntaxError, e:
            print e
            sys.exit(1)
        return self.current
 
    def Goal(self):
        self.token = self.getNextToken()
        # Goal -> Program
        if self.Program() and self.token[0] == 'EOF':
            return True
        else:
            #error
            return False
      
    def Program(self):
        self.current = Node('#PGRM#')
        while self.var() or self.type() or self.forward() or self.proc():
            pass
        else:
            # Program -> Stms
            if not self.Stms():
                raise SyntaxError(self.getCurrentLine(), self.token) 
        return True

    @makenode    
    def var(self):
        if self.token == ('KEY', 'var'):
            self.token = self.getNextToken()
            return self.varlist()
        return False
    
    @makenode
    def varlist(self):
        if self.idlist():
            if self.token == ('SYM', ':'):
                self.token = self.getNextToken()
                if self.typeid():
                    while self.token == ('SYM', '['):
                        self.current = self.current.addChild(Node('[]', self.currentLine))
                        self.token = self.getNextToken()
                        if self.token[0] == 'INT':
                            self.current.addChild(Node(self.token[1], self.currentLine))
                            self.token = self.getNextToken()
                            if self.token == ('SYM', ']'):
                                self.current = self.current.parent
                                self.token = self.getNextToken()
                                continue                               
                        raise SyntaxError(self.getCurrentLine(), self.token)
                    else:
                        while self.token == ('SYM', ','):
                            self.token = self.getNextToken()
                            if self.varlist():
                                continue
                            else:
                                raise SyntaxError(self.getCurrentLine(), self.token)
                    return True
        raise SyntaxError(self.getCurrentLine(), self.token)
    
    @makenode
    def idlist(self):
        if self.token[0] == 'ID':
            self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            while self.token == ('SYM', ','):
                self.token = self.getNextToken()
                if self.token[0] == 'ID':
                    self.current.addChild(Node(self.token[1], self.currentLine))
                    self.token = self.getNextToken()
                    continue
                raise SyntaxError(self.getCurrentLine(), self.token)
            return True
        return False

    @makenode
    def type(self):
        if self.token == ('KEY', 'type'):
            self.token = self.getNextToken()
            if self.token[0] == 'ID':
                self.current.addChild(Node(self.token[1], self.currentLine))
                self.token = self.getNextToken()
                if self.token == ('OP', '='):
                    self.token = self.getNextToken()
                    if self.typeid():
                        while self.token == ('SYM', '['):
                            self.current = self.current.addChild(Node('[]', self.currentLine))
                            self.token = self.getNextToken()
                            if self.token[0] == 'INT':
                                self.current.addChild(Node(self.token[1], self.currentLine))
                                self.token = self.getNextToken()
                                if self.token == ('SYM', ']'):
                                    self.current = self.current.parent
                                    self.token = self.getNextToken()
                                    continue
                            raise SyntaxError(self.getCurrentLine(), self.token)
                        return True
            raise SyntaxError(self.getCurrentLine(), self.token)                
        return False

    @makenode
    def forward(self):
        if self.token == ('KEY', 'forward'):
            self.token = self.getNextToken()
            if self.token[0] == 'ID':
                self.token = self.getNextToken()
                if self.token == ('SYM', '('):
                    self.token = self.getNextToken()
                    if self.declist():
                        if self.token == ('SYM', ')'):
                            self.token = self.getNextToken()
                            if self.token == ('SYM', ':'):
                                self.token = self.getNextToken()
                                if self.typeid():
                                    return True
                                else:
                                    raise SyntaxError(self.getCurrentLine(), self.token)
                            return True        
            raise SyntaxError(self.getCurrentLine(), self.token)
        return False

    @makenode
    def proc(self):
        if self.token == ('KEY', 'proc'):
            self.token = self.getNextToken()
            if self.token[0] == 'ID':
                self.current = self.current.addChild(Node(self.token[1], self.currentLine))
                self.token = self.getNextToken()
                if self.token == ('SYM', '('):
                    #self.current = self.current.addChild(Node('()', self.currentLine))
                    self.token = self.getNextToken()
                    if self.declist():
                        self.current = self.current.parent
                        if self.token == ('SYM', ')'):
                            self.token = self.getNextToken()
                            res =  self.procPrime()
                            #self.current = self.current.parent
                            return res
            raise SyntaxError(self.getCurrentLine(), self.token)
        return False

    def procPrime(self):
        if self.token == ('SYM', ':'):
            #self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            if self.typeid():
                return self.procEnd()
            raise SyntaxError(self.getCurrentLine(), self.token)
        return self.procEnd()

    def procEnd(self):
        while self.type() or self.var():
            continue
        while self.Stm():
            continue
        if self.token == ('KEY', 'end'):
            #self.current.addChild(Node('#ProcEnd#', self.currentLine))
            self.token = self.getNextToken()
            return True
        raise SyntaxError(self.getCurrentLine(), self.token)
        return False

    def declist(self):
        if self.idlist():
            if self.token == ('SYM', ':'):
                self.token = self.getNextToken()
                if self.typeid():
                    while self.token == ('SYM', ','):
                        self.token = self.getNextToken()
                        if not self.declist():
                            raise SyntaxError(self.getCurrentLine(), self.token)
                    else:
                        return True
            
            raise SyntaxError(self.getCurrentLine(), self.token)
        return True
    
    @makenode
    def Stms(self):
        #Stms -> Stm { Stm }
        if self.Stm():
            while self.token != ('EOF', 'EOF') and self.Stm():
                pass
            return True
        raise SyntaxError(self.getCurrentLine(), self.token)

    @makenode
    def Stm(self):
        # Stm -> if
        if self.ifStm():
            return True
        # Stm -> do
        elif self.doStm():
            return True
        # Stm -> fa
        elif self.faStm():
            return True
        # Stm -> return | exit | break
        elif self.token[0] == 'KEY' and (self.token[1] == 'return' or self.token[1] == 'exit' or self.token[1] == 'break'):
            self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            if self.token == ('SYM', ';'):
                self.token = self.getNextToken()
                return True
            else:
                #syntax error
                return False
        # Stm -> writes | write
        elif self.token[0] == 'KEY' and (self.token[1] == 'writes' or self.token[1] == 'write'):
            self.current = self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            if self.Expr():
                self.current = self.current.parent
                if self.token == ('SYM', ';'):
                    self.token = self.getNextToken()
                    return True
            raise SyntaxError(self.getCurrentLine(), self.token)
        # Stm -> Expr
        elif self.Expr():
            if self.token == ('SYM', ';'):
                self.token = self.getNextToken()
                return True
            raise SyntaxError(self.getCurrentLine(), self.token)
        # Stm -> ;        
        elif self.token == ('SYM', ';'):
            # Don't add ; to the tree
            self.token = self.getNextToken()
            return True
        else:
            return False
    
    @makenode
    def ifStm(self):
        if self.token[0] == "KEY" and self.token[1] == "if":
            self.current = self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            if self.Expr():
                if self.token[0] == 'SYM' and self.token[1] == '->':
                    self.token = self.getNextToken()
                    if self.Stms():
                        res = self.ifPrime()
                        self.current.addChild(Node('#EndIf#', self.currentLine))
                        self.current = self.current.parent
                        return res
                raise SyntaxError(self.getCurrentLine(), self.token)
        return False

    @makenode
    def ifPrime(self):
        if self.token[0] == 'SYM' and self.token[1] == '[]':
            #self.current = self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            return self.ifDoublePrime()
        elif self.token[0] == 'KEY' and self.token[1] == 'fi':
            self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            return True
        return False    

    @makenode
    def ifDoublePrime(self):
        if self.token[0] == 'KEY' and self.token[1] == 'else':
            self.current = self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            if self.token[0] == 'SYM' and self.token[1] == '->':
                self.token = self.getNextToken()
                if self.Stms():
                    if self.token[0] == 'KEY' and self.token[1] == 'fi':
                        self.current = self.current.parent
                        self.token = self.getNextToken()
                        return True
            raise SyntaxError(self.getCurrentLine(), self.token)
        elif self.Expr():
            if self.token[0] == 'SYM' and self.token[1] == '->':
                self.token = self.getNextToken()
                if self.Stms():
                    return self.ifPrime()
            raise SyntaxError(self.getCurrentLine(), self.token)
        return False
    
    @makenode
    def doStm(self):
        if self.token[0] == 'KEY' and self.token[1] == 'do':
            self.current = self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            if self.Expr():
                if self.token[0] == 'SYM' and self.token[1] == '->':
                    
                    self.token = self.getNextToken()
                    if self.Stms():
                        if self.token[0] == 'KEY' and self.token[1] == 'od':
                            self.current.addChild(Node('#doEnd#', self.currentLine))
                            self.current = self.current.parent
                            self.token = self.getNextToken()
                            return True
            raise SyntaxError(self.getCurrentLine(), self.token)
        return False

    @makenode
    def faStm(self):
        if self.token[0] == 'KEY' and self.token[1] == 'fa':
            self.current = self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            if self.token[0] == "ID":
                self.current.addChild(Node(self.token[1], self.currentLine))
                self.token = self.getNextToken()
                if self.token[0] == 'SYM' and self.token[1] == ':=':
                    self.current.addChild(Node(self.token[1], self.currentLine))
                    self.token = self.getNextToken()
                    if self.Expr():
                        if self.token[0] == 'KEY' and self.token[1] == 'to':
                            self.current.addChild(Node(self.token[1], self.currentLine))
                            self.token = self.getNextToken()
                            if self.Expr():
                                if self.token[0] == 'SYM' and self.token[1] == '->':
                                    self.token = self.getNextToken()
                                    if self.Stms():
                                        if self.token[0] == 'KEY' and self.token[1] == 'af':
                                            self.current.addChild(Node('#EndFa#', self.currentLine))
                                            self.current = self.current.parent
                                            self.token = self.getNextToken()
                                            return True
            raise SyntaxError(self.getCurrentLine(), self.token)
        return False

    @makenode
    def typeid(self):
        if self.token[0] == 'ID':
            self.current.addChild(Node(self.token[1], self.currentLine))
            self.token = self.getNextToken()
            return True
        return False

    @makenode
    def Expr(self):
        # Expr -> Low ExprPrime
        if self.Low():
            return self.ExprPrime()
        else:
            return False
   
    def ExprPrime(self):
        if self.token == ('OP', '=') or self.token == ('OP', '!=') or \
            self.token == ('OP', '>') or self.token == ('OP', '<') or \
            self.token == ('OP', '>=') or self.token == ('OP', '<='): 
                self.current = self.current.addChild(Node(self.token[1], self.currentLine, self.token[0]))
                self.token = self.getNextToken()
                if not self.Low():
                    raise SyntaxError(self.getCurrentLine(), self.token)
                self.current = self.current.parent
        # empty string
        return True       

    @makenode
    def Low(self):
        if self.Med():
            return self.LowPrime()
        else:
            return False
    
    def LowPrime(self):
        if self.token == ('OP', '+') or self.token == ('OP', '-'):
            self.current = self.current.addChild(Node(self.token[1], self.currentLine, self.token[0]))
            self.token = self.getNextToken()
            if self.Med():
                ret =  self.LowPrime()
                self.current = self.current.parent
                return ret
            raise SyntaxError(self.getCurrentLine(), self.token)
        # empty string
        return True

    @makenode
    def Med(self):
       if self.High():
           return self.MedPrime()
       else:
           return False
    
    def MedPrime(self):
        if self.token == ('OP', '*') or self.token == ('OP', '/') or self.token == ('OP', '%'):
                self.current = self.current.addChild(Node(self.token[1], self.currentLine, self.token[0]))
                self.token = self.getNextToken()
                if self.High():
                    res = self.MedPrime()
                    self.current = self.current.parent
                    return res
                raise SyntaxError(self.getCurrentLine(), self.token)
        # empty string
        return True

    @makenode
    def High(self):
        if self.End():
            # rewind tree
            return True
        elif self.token == ("OP", '-') or self.token == ('OP', '?'):
                if self.token == ("OP", '-'):
                    self.current = self.current.addChild(Node('neg', self.currentLine, self.token[0]))
                else:
                    self.current = self.current.addChild(Node('?', self.currentLine, self.token[0]))
                self.token = self.getNextToken()
                if not self.High():
                    raise SyntaxError(self.getCurrentLine(), self.token)
                self.current = self.current.parent
                return True
        # empty string
        return False        

    @makenode
    def End(self):
        if self.token[1] == '(':
            self.current = self.current.addChild(Node('()', self.currentLine))
            self.token = self.getNextToken()
            if self.Expr():
                if self.token[1] == ')':
                    self.current = self.current.parent
                    self.token = self.getNextToken()
                    return True
            raise SyntaxError(self.getCurrentLine(), self.token)
        elif self.token[0] == 'INT' or self.token[0] == "STR":
            self.current.addChild(Node(self.token[1], self.currentLine, self.token[0]))
            self.token = self.getNextToken()
            return True
        elif self.token[0] == 'KEY':
            if self.token[1] == 'true' or self.token[1] == 'false' or self.token[1] == 'read':
                if self.token[1] == 'true' or self.token[1] == 'false':
                    self.current.addChild(Node(self.token[1], self.currentLine, 'bool'))
                else:
                    self.current.addChild(Node(self.token[1], self.currentLine, self.token[0]))
                self.token = self.getNextToken()
                return True
            return False
        elif self.token[0] == "ID":
            self.current = self.current.addChild(Node(self.token[1], self.currentLine, self.token[0]))
            self.token = self.getNextToken()
            if self.token[0] == 'SYM' and self.token[1] == '(':
                self.token = self.getNextToken()
                res = self.ProcCall()
                if res:
                    self.current.type = 'procCall'
                    #self.current.data = self.current.data + '()'
                self.current = self.current.parent
                return res
            elif self.LValuePrime():
                self.current = self.current.parent
                res = self.Assn()
                return res
        return False

    def LValuePrime(self):
        if self.token[0] == 'SYM' and self.token[1] == '[':
            self.current = self.current.addChild(Node('[]', self.currentLine))
            self.token = self.getNextToken()
            if self.Expr():
                if self.token[0] == 'SYM' and self.token[1] == ']':
                    self.current = self.current.parent
                    self.token = self.getNextToken()
                    return self.LValuePrime()
            
            raise SyntaxError(self.getCurrentLine(), self.token)
        return True

    def Assn(self):
        if self.token[0] == 'SYM' and self.token[1] == ':=':
            self.current = self.current.addChild(Node(self.token[1], self.currentLine, 'OP'))
            self.token = self.getNextToken()
            if not self.Expr():
                raise SyntaxError(self.getCurrentLine(), self.token)
            self.current = self.current.parent
        return True
    
    @makenode
    def ProcCall(self):
        if self.token[0] == 'SYM' and self.token[1] == ')':
            self.token = self.getNextToken()
            return True
        else:
            while self.Expr():
                if self.token[0] == 'SYM' and self.token[1] == ",":
                    self.token = self.getNextToken()
                elif self.token[0] == 'SYM' and self.token[1] == ')':
                    self.token = self.getNextToken()
                    return True
            return False

if __name__ == "__main__":
    DEBUG = 1
    p = ice9Parser()
    s = ice9Scanner()
    #f = open(sys.argv[1])
    #p.parse(s.scan(f.read()))
    #p.parse(s.scan(';'))
    #p.parse(s.scan(';;;;;;;;'))
    #p.parse(s.scan('42;'))
    #p.parse(s.scan('\'mystring\';'))
    #p.parse(s.scan('(42);'))
    #p.parse(s.scan('5+2;'))
    #p.parse(s.scan('-2;'))
    #p.parse(s.scan('----2;'))
    #p.parse(s.scan('x+2;'))
    #p.parse(s.scan('x+---2;'))
    #p.parse(s.scan('x;'))
    #p.parse(s.scan('x+2/3;'))
    #p.parse(s.scan('3/2+1;'))
    #p.parse(s.scan('3/2 + 1/2;'))
    #p.parse(s.scan('3/-2+1;'))
    #p.parse(s.scan('3/-2 + -3/-3 + x - 3 + y/2;'))
    #p.parse(s.scan('x<=2;'))
    #p.parse(s.scan('x();'))
    #p.parse(s.scan('x(2);'))
    #p.parse(s.scan('x(2,2,2);'))
    #p.parse(s.scan('z(2,x,y);'))
    #p.parse(s.scan('x[2];'))
    #p.parse(s.scan('x:=2;'))
    #p.parse(s.scan('x(x:=2);'))
    #p.parse(s.scan('x(x:=2*y);'))
    #p.parse(s.scan('write x+2;'))
    #p.parse(s.scan('writes 3%2;'))
    #p.parse(s.scan('break;'))
    #p.parse(s.scan('exit;'))
    #p.parse(s.scan('return;'))
    #p.parse(s.scan('if (n < 1) + (n > 100) -> write "wrong"; exit; fi'))
    #p.parse(s.scan('fa i := 0 to n -> a[i] := read; af'))
    p.parse(s.scan('var k:int do k < 4 -> k := k + 1; od'))
    #p.parse(s.scan('var n, t: int ;'))
    #p.parse(s.scan('var a: int[100] ;'))
    #p.parse(s.scan('N := check();'))
    #p.parse(s.scan('proc error() write "x"; exit; end ;'))
    #p.parse(s.scan('if (n <= 1) -> xyz := a; [] else -> write x % 3 + 4 * (4 * 4); fi'))
    #p.parse(s.scan('var Seed : int ;'))
    #p.parse(s.scan('type foo = int ;'))
    #p.parse(s.scan('var Seed, CUTOFF : int ;'))
    #p.parse(s.scan('\n\n4\n\t+2\n\n;\n\n'))
    #p.parse(s.scan('\t\n\t\n\t\n42;\t\t\t;'))

    #print "FAILURES SHOULD OCCUR AFTER THIS LINE:"
    #p.parse(s.scan('+2;'))
    #p.parse(s.scan('x[2,2];'))
    #p.parse(s.scan('x+---+2;'))
    #p.parse(s.scan('writeX x + 2;'))
    #p.parse(s.scan('writes x + ;'))
    #p.parse(s.scan('\n\n+\n2\n\n;\n\n'))
    #p.parse(s.scan('\t\t\n\n\t\t\t\t\t\n\n\n\n\t+;\n\t'))
    #p.parse(s.scan('type foo = int[3]'))
