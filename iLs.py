#!/usr/bin/env python

from __future__ import print_function

from pycommands.common import irods_session_from_env_file
from irods.exception import CollectionDoesNotExist

from os.path import expanduser
import sys

from getopt import getopt
opt,arg=getopt(sys.argv[1:],'rS')
optD = dict(opt)

def annotation(typecode):
    return '' if '-S' in optD else (typecode + '\t')

def print_item(typecode, path):
    print(annotation(typecode) + path)

with irods_session_from_env_file() as s:

    if not arg:
        arg=['/{0.zone}/home/{0.username}'.format(s)]

    tc = 'C'
    try:
        obj = s.collections.get(arg[0])
    except CollectionDoesNotExist:
        obj = s.data_objects.get(arg[0])
        tc = 'D'

    if tc == 'D':
        print_item(tc,obj.path)
    else:
        if '-r' in optD:
            # -- walk the subtree
            for this,subcols,dataobjs in obj.walk():
                print_item('C',this.path)
                for d in dataobjs:
                    print_item('D',d.path)
        else:
            # -- display only one object, and immediate children
                print_item('C',obj.path)
                for d in obj.data_objects:
                    print_item('D',d.path)
                for c in obj.subcollections:
                    print_item('C',c.path)