#!/usr/bin/env python

import ply.yacc as yacc

from g984lexer import tokens

def p_entities(p):
    '''entities : entity
                | entities entity
    '''
    return p

def p_entity(p):
    '''entity : header relationships attributes actions notifications'''
    return p

def p_header(p):
    '''header : HEADER text'''
    return p

def p_relationships(p):
    '''relationships : RELATIONSHIPS text'''
    return p

def p_attributes(p):
    '''attributes : ATTRIBUTES attribs'''
    return p

def p_attribs(p):
    '''attribs : attribute
               | attribs attribute
    '''
    return p

def p_attribute(p):
    '''attribute : MEID attrdesc
                 | ANAME attrdesc
    '''
    return p

def p_attrdesc(p):
    '''attrdesc : attrdesc text
                | attrdesc flags
                | empty
    '''
    return p

def p_flags(p):
    '''flags : flag
             | flags flag
    '''
    return p

def p_flag(p):
    'flag : LPAREN text RPAREN'
    return p

def p_actions(p):
    '''actions : ACTIONS text'''
    return p

def p_notifications(p):
    '''notifications : NOTIFICATIONS text'''
    return p

def p_empty(p):
    'empty :'
    pass

def p_text(p):
    '''
    text : text TEXT
         | empty
    '''
    return p

def p_error(p):
    print "Syntax error in input!", p

parser = yacc.yacc()

if __name__ == '__main__':
    import sys
    from g984lexer import lexer
    #parser.parse( sys.argv[1], debug=1, lexer=lexer)
    parser.parse( sys.argv[1], lexer=lexer)
