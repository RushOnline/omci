#!/usr/bin/env python

from ply import lex
from ply.lex import TOKEN
import re

sections = (
        'Relationships',
        'Attributes',
        'Actions',
        'Notifications'
        )

section_re = r'^(' + '|'.join(sections) + ')$'

tokens = tuple([ section.upper() for section in sections ]) + (
        'HEADER',
        'TEXT',
        'ANAME',
        'MEID',
        'LPAREN',
        'RPAREN'
        )

states = tuple([(state.lower(), 'exclusive') for state in (sections + ('acontent', 'fcontent'))])

def t_attributes_MEID(t):
    r'^\s+.*:'
    t.lexer.indent = len(t.value) - len(t.value.lstrip())
    t.value = t.value.strip(' \t:\r\n')
    t.lexer.begin('acontent')
    return t

def t_acontent_LPAREN(t):
    r'\('
    return t

def t_acontent_RPAREN(t):
    r'\)'
    return t

def t_acontent_error(t):
    paren = re.search(r'\(|\)', t.value)
    if paren:
        #print '%s "%s"' % (paren.end(), t.value)
        t.value = t.value[:paren.end()-1]

    t.lexer.skip(len(t.value))
    t.type = 'TEXT'
    return t

def t_acontent_ANAME(t):
    r'^\s+.*:'
    indent = len(t.value) - len(t.value.lstrip())
    if abs(indent - t.lexer.indent) < 3:
        t.value = t.value.strip(' \t:\r\n')
        return t

def t_ANY_HEADER(t):
    r'^9\.\d+\.\d+\s+.*$'
    try:
        t.value = t.value.split(None, 1)
        return t
    except ValueError:
        t_error(t)

@TOKEN(section_re)
def t_ANY_SECTION(t):
    t.type = t.value.upper()
    t.lexer.begin(t.value.lower())
    return t

def t_ANY_error(t):
    skip = re.match(r'\s+|\S+', t.value)
    t.lexer.skip(skip.end())
    t.type = 'TEXT'
    t.value = t.value[:skip.end()]
    return t

lexer = lex.lex()

if __name__ == '__main__':

    import tripper
    import sys

    with open(sys.argv[1]) as fd:
        lexer.indent = 0
        lexer.text = ''
        for line in tripper.descriptions(fd):
            lexer.input(line)
            while True:
                tok = lexer.token()
                if not tok: break
                if tok.type == 'TEXT':
                    lexer.text += tok.value
                elif lexer.text:
                    lexer.text = ''
                print repr(tok.type), repr(tok.value)
            if lexer.text:
                lexer.text += '\n'
