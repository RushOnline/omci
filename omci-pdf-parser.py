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
        'HEADER',
        'TEXT'
        )

def t_HEADER(t):
    r'^9\.\d+\.\d+\s+.*$'
    try:
        t.value = t.value.split(None, 1)
        return t
    except ValueError:
        t_error(t)

@TOKEN(section_re)
def t_SECTION(t):
    t.type = t.value.upper()
    return t

def t_error(t):
    t.lexer.skip(len(t.value))
    t.lexer.text.append(t.value)
    t.type = 'TEXT'
    return t

lexer = lex.lex()

class Metadata:
    pass

if __name__ == '__main__':

    import tripper
    import sys

    with open(sys.argv[1]) as fd:
        for line in tripper.descriptions(fd):
            lexer.state = 'initial'
            lexer.text = []
            lexer.metadata = Metadata()
            lexer.input(line)
            while True:
                tok = lexer.token()
                if not tok: break
                print repr(tok.type), repr(tok.value)
