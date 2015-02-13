#!/usr/bin/env python

from __future__ import with_statement
import re


def descriptions(fd):
    START = re.compile('^9.1.1\s+ON[TU]-G$')
    STOP = re.compile('^10\s+')
    IGNORE = (
            'ITU-T Rec. G.984.4 (06/2004)',
            'Rec. ITU-T G.984.4 (02/2008)',
            'Rec. ITU-T G.988 (10/2012)',
            '-----------------------'
            )

    fd.readline()
    for line in fd:
        line = line.rstrip()

        # skip some shit
        skip = False

        for ignore in IGNORE:
            if ignore in line:
                skip = True
                break

        if skip: continue

        if START:
            if not START.match(line): continue
            START = None


        if STOP.match(line):
            break

        yield line

def identifiers(fd):

    START = re.compile('\s+Table.*Managed entity identifiers')
    STOP = re.compile('.*65535\s+Reserved')

    IGNORE = (
            'ITU-T Rec. G.984.4 (06/2004)',
            'Rec. ITU-T G.988 (10/2012)',
            '-----------------------',
            'B-PON'
            )

    fd.readline()
    for line in fd:
        line = line.rstrip()

        # skip some shit
        skip = False

        for ignore in IGNORE:
            if ignore in line:
                skip = True
                break

        if skip: continue

        if START:
            if not START.match(line): continue
            START = None


        if STOP.search(line):
            break

        try:
            number, name = line.split(None, 1)
            if name == '(Reserved)': continue
            if name == '(Intentionally left blank)': continue
            if 'deprecated' in name: continue
            if 'obsolete' in name: continue
            if number in ('1', '258', '259'): continue
            if '(' in name:
                name, _ = name.split(None, 1)
            yield (int(number), name)
        except:
            pass

if __name__ == '__main__':

    def usage():
        print sys.argv[0], '<-i|-d> <filename>'
        sys.exit(1)

    import sys
    from getopt import getopt, GetoptError

    try:
        opts, args = getopt(sys.argv[1:], 'id')
    except GetoptError as err:
        print str(err)
        usage()

    if len(args) != 1: usage()

    filename = args[0]

    actions = []
    for o, a in opts:
        if o == '-i':
            actions.append(identifiers)
        elif o == '-d':
            actions.append(descriptions)
        else:
            usage()

    if not actions: usage()

    for action in actions:
        with open(filename) as fd:
            for result in action(fd):
                print result

