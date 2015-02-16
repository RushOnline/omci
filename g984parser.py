#!/usr/bin/env python

import ply.yacc as yacc

from g984lexer import tokens

def p_entities(p):
    '''entities : entity
                | entities entity
    '''
    pass

def p_entity(p):
    '''entity : header relationships attributes actions notifications'''
    pass

def p_header(p):
    '''header : HEADER text'''
    pass

def p_relationships(p):
    '''relationships : RELATIONSHIPS text'''
    pass

def p_attributes(p):
    '''attributes : ATTRIBUTES attribs'''
    pass

def p_attribs(p):
    '''attribs : attribute
               | attribs attribute
    '''
    pass

def p_attribute(p):
    '''attribute : MEID attrdesc
                 | ANAME attrdesc
    '''
    pass

def p_attrdesc(p):
    '''attrdesc : attrdesc text
                | attrdesc flags
                | empty
    '''
    pass

def p_flags(p):
    '''flags : flags flag
             | flag
    '''
    pass

def p_flag(p):
    'flag : LPAREN text RPAREN'
    pass

def p_actions(p):
    '''actions : ACTIONS text'''
    pass

def p_notifications(p):
    '''notifications : NOTIFICATIONS text'''
    p[0] = p[2]

def p_empty(p):
    'empty :'
    pass

def p_text(p):
    '''
    text : text TEXT
         | empty
    '''
    if len(p) == 3:
        p[0] = (p[1] or '') + p[2]
    else:
        p[0] = ''

def p_error(p):
    print "Syntax error in input!", p

parser = yacc.yacc()

if __name__ == '__main__':
    import sys
    from g984lexer import lexer
    #parser.parse( sys.argv[1], debug=1, lexer=lexer)
    parser.parse( sys.argv[1], lexer=lexer)
