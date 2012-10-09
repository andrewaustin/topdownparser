#!/usr/bin/python
from scanner import ice9Scanner
from parser import ice9Parser
import sys

p = ice9Parser()
s = ice9Scanner()
tree = p.parse(s.scan(sys.stdin.read()))
print tree
