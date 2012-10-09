#!/usr/bin/python

#Handle deprecation of sre module for version of python prior to 2.5
try:
    from re import Scanner
except ImportError:
    from sre import Scanner

import sys


class ice9Scanner:
    """Class that creates an ice9 lexical scanner."""

    def __init__(self):
        """Constructor. Simply initializes the current line to 1."""
        self.line = 1

    # Token definitions
    def ignore(self, scanner, token):
        """For tokens that should be ignored."""
        pass

    def key(self, scanner, token):
        """For tokens that are keywords."""
        return "KEY", token

    def identifier(self, scanner, token):
        """For tokens that are identifiers."""
        return "ID", token

    def operator(self, scanner, token):
        """For tokens that are operators."""
        return "OP", token

    def symbol(self, scanner, token):
        """For tokens that are symbols."""
        return "SYM", token

    def integer(self, scanner, token):
        """For tokens that are integers."""
        return "INT", token

    def newline(self, scanner, token):
        """For tokens that are newlines. Increase line count."""
        self.line += 1
        return "NL", "NL"

    def string(self, scanner, token):
        """For tokens that are strings."""
        return "STR", token

    def scan(self, input):
        """Preforms the scan of the input and outputs any errors including
           line on which the lexical error occured."""
        scanner = Scanner([
            (r"[\n]", self.newline),
            (r"\"[^\"\n]*\"", self.string),
            (r"\'[^\'\n]*\'", self.string),
            (r"\b(if|fi|else|do|od|fa|af|to|proc)\b", self.key),
            (r"\b(end|return|forward|var|type|break)\b", self.key),
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
            print "line %s: illegal character (%s)" % (
                    self.line, remainder[:1])
            sys.exit(1)
        else:
            return tokens

if __name__ == "__main__":
    s = ice9Scanner()
    f = open(sys.argv[1])
    tokens = s.scan(f.read())
    for token in tokens:
        print token
