topdownparser
=============

A recursive descent decent parser written for a graduate compiler course. For
academic integrity reasons, the rest of the compiler is not publicily available.

Note on Quality
----------------
The code in the parser is not very pythonic and represents some very early work
while I was learning python. I made several updates to the code to make it more
readable (mainly comments) but in general, the code is
probably very poor. A large number of the lines are greater than 80 characters
which is not PEP8 compliant, for example.

**Its still a hand written parser though, which I think is pretty cool. =)**

Grammar
-------
The parser is designed to recognize the grammar in grammar.txt. I already
removed left recursion when creating this grammar (this is why you see production
rules such as if, ifPrime, and ifPrime2).

Usage
-----
To see a list of tokens:

> python scanner.py simple\_expr.ice9
> ('ID', 'x')
> ('OP', '+')
> ('INT', '2')
> ('OP', '/')
> ('INT', '3')
> ('SYM', ';')
> ('NL', 'NL')
> ('EOF', 'EOF')

To see the full parse tree:

> python ice9.py < simple\_expr.ice9
> (#PGRM#)
>  (#Stms#)
>   (#Stm#)
>    (#Expr#)
>    (#Low#)
>     (#Med#)
>      (#High#)
>       (#End#)
>        (x)
>     (+)
>      (#Med#)
>       (#High#)
>        (#End#)
>         (2)
>       (/)
>        (#High#)
>         (#End#)
>          (3)

Changelog
---------
10/09/12 - After several years of sitting on github unedited, made several style
          changes to fit with pep8, etc.
03/01/09 - Added code to create parse tree from parser
02/01/09 - Developed initial version of parser.

