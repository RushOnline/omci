#!/usr/bin/env python

from __future__ import with_statement

from ply import lex
from ply.lex import TOKEN

sections = (
        'Relationships',
        'Attributes',
        'Actions',
        'Notifications'
        )

section_re = r'^(' + '|'.join(sections) + ')$'

tokens = tuple([ section.upper() for section in sections ]) + (
        'PARA',
        'WS',
        'ENTITYNAME',
        'WORD',
        'LPAREN',
        'RPAREN',
        'COLON',
        )

t_WS = r'\s+'
t_PARA = r'9\.\d+\.\d+'

def t_WORD(t):
    r'\S+'
    lexer.text.append(t.value)

@TOKEN(section_re)
def t_SECTION(t):
    t.type = t.value.upper()
    return t

def t_error(t):
    t.lexer.skip(1)
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex()

if __name__ == '__main__':

    import tripper
    import sys

    with open(sys.argv[1]) as fd:
        for line in tripper.descriptions(fd):
            lexer.state = 'initial'
            lexer.text = []
            lexer.input(line)
            while True:
                tok = lexer.token()
                if not tok: break
                print repr(tok.type), repr(tok.value)
