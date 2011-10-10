#!/usr/bin/python
try:
    from re import Scanner
except ImportError:
    from sre import Scanner

import sys

# very poor ice9Scanner
class ice9Scanner:
    def __init__(self):
        self.line = 1

    def ignore(self, scanner, token):
        pass
    def key(self, scanner, token):
        return "KEY", token
    def identifier(self, scanner, token): 
        return "ID", token
    def operator(self, scanner, token):   
        return "OP", token
    def symbol(self, scanner, token):
        return "SYM", token
    def integer(self, scanner, token):    
        return "INT", token
    def newline(self, scanner, token):
        self.line += 1
        return "NL", "NL"
    def string(self, scanner, token):
        return "STR", token

    def scan(self, input):
        scanner = Scanner([
            (r"[\n]", self.newline),
            (r"\"[^\"\n]*\"", self.string),
            (r"\'[^\'\n]*\'", self.string),
            (r"\b(if|fi|else|do|od|fa|af|to|proc|end|return|forward|var|type|break)\b", self.key),
            (r"\b(exit|true|false|writes|write|read)\b", self.key),
            (r"[A-Za-z][A-Za-z0-9_]*", self.identifier),
            (r"\-\>|\(|\)|\[\]|\[|\]|;|:\=|:|\,", self.symbol),
            (r"\+|\-|\/|\*|\=|\%|!\=|\>=|\<=|\>|\<|\?", self.operator),
            (r"[0-9]+", self.integer),
            (r"#.*(?=\n?)", self.ignore),
            (r"[\t ]+", self.ignore),
            ])
        tokens, remainder = scanner.scan(input)
        tokens.append(('EOF', 'EOF'))

        if remainder:
            print "line " + str(self.line) + ": illegal character (" + remainder[:1] + ")"
            sys.exit(1)
        else:
            return tokens

if __name__ == "__main__":
    s = ice9Scanner()
    f = open(sys.argv[1])
    tokens = s.scan(f.read())
    for token in tokens:
        print token
