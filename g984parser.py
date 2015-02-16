#!/usr/bin/env python

from pprint import pprint

import ply.yacc as yacc

from g984lexer import tokens

def p_entities(p):
    '''entities : entity
                | entities entity
    '''
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 3:
        p[0] = p[1] + (p[2],)
    pprint(p[0])

def p_entity(p):
    '''entity : header relationships attributes actions notifications'''
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
    '''attribute : MEID attrdesc
                 | ANAME attrdesc
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
    #p[0] = p[1][1] + (
    if len(p) == 2:
        p[0] = ('flags', (p[1],))
    else:
        p[0] = ('flags', p[1][1] + (p[2],))

def p_flag(p):
    'flag : LPAREN text RPAREN'
    p[0] = ('flag', p[2])

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

def p_error(p):
    print "Syntax error in input!", p

parser = yacc.yacc()

if __name__ == '__main__':
    import sys
    from g984lexer import lexer
    #parser.parse( sys.argv[1], debug=1, lexer=lexer)
    parser.parse( sys.argv[1], lexer=lexer)
