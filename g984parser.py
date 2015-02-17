#!/usr/bin/env python

import re
from pprint import pprint
from copy import deepcopy

import ply.yacc as yacc

from g984lexer import tokens

def p_entities(p):
    '''entities : entities entity
                | entity
    '''
    if len(p) == 2:
        p[0] = ( p[1], )
    elif len(p) == 3:
        p[0] = p[1] + ( p[2], )

def p_entity(p):
    '''entity : header relationships attributes actions notifications
              | header relationships attributes actions
              | header
    '''
    p[0] = tuple(p[1:])

def p_header(p):
    '''header : HEADER text'''
    p[0] = ('header', p[1], p[2][1])

def p_relationships(p):
    '''relationships : RELATIONSHIPS text'''
    p[0] = ('relationships', p[2][1])

def p_attributes(p):
    '''attributes : ATTRIBUTES attribs'''
    p[0] = p[2]

def p_attribs(p):
    '''attribs : attribute
               | attribs attribute
    '''
    if len(p) == 2:
        p[0] = ('attributes', (p[1],))
    elif len(p) == 3:
        p[0] = ('attributes', p[1][1] + (p[2],))

def p_attribute(p):
    '''attribute : ANAME attrdesc
    '''
    p[0] = (p[1], p[2])

def p_attrdesc(p):
    '''attrdesc : attrdesc text
                | attrdesc flags
                | empty
    '''
    if len(p) == 2:
        p[0] = ('attr-desc', tuple(), '')
    elif len(p) == 3:
        if p[2][0] == 'flags':
            p[0] = ('attr-desc', p[1][1] + (p[2],), p[1][2])
        elif p[2][0] == 'text':
            p[0] = ('attr-desc', p[1][1], p[1][2] + p[2][1])

def p_flags(p):
    '''flags : flags flag
             | flag
    '''
    if len(p) == 2:
        p[0] = ('flags', (p[1],))
    else:
        p[0] = ('flags', p[1][1] + (p[2][1],))

def p_flag(p):
    'flag : LPAREN text RPAREN'
    flag = p[2][1]

    if flag == 'mandatory':
        p[0] = ('flag', 'mandatory')
    elif flag == 'optional':
        p[0] = ('flag', 'optional')
    else:
        flags = tuple()
        for xflag in re.split('\W+', flag):
            if xflag in ['R','W','Set-by-create']:
                flags = flags + (xflag,)
        if flags:
            p[0] = ('flag', flags)
        else:
            try:
                p[0] = ('size', int(re.match('(\d+).*byte', flag).groups()[0]))
            except:
                pass
    if not p[0]:
        p[0] = ('flag-ext', '(%s)' % flag)

def p_actions(p):
    '''actions : ACTIONS text'''
    p[0] = ('actions', p[2])

def p_notifications(p):
    '''notifications : NOTIFICATIONS text'''
    p[0] = ('notifications', p[2])

def p_empty(p):
    'empty :'
    pass

def p_text(p):
    '''
    text : text TEXT
         | empty
    '''
    if len(p) == 3:
        p[0] = ('text', p[1][1] + p[2])
    else:
        p[0] = ('text', '')

def p_error(t):
    if t.type in ( 'RPAREN', 'LPAREN' ):
        parser.errok()
        return
    raise SyntaxError('%s : line %d' % (t, t.lineno))

parser = yacc.yacc()

if __name__ == '__main__':
    import sys
    from g984lexer import lexer
    #ast = parser.parse( sys.argv[1], debug=1, lexer=lexer)
    ast = parser.parse( sys.argv[1], lexer=lexer)
    pprint(ast)
    #print len(ast)
