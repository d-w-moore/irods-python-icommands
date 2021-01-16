#!/usr/bin/env python

from __future__ import print_function

from pycommands.common import (die, irods_session_from_env_file)
from irods.exception import CollectionDoesNotExist
from irods.manager.data_object_manager import DataObjectManager
from irods.data_object import iRODSDataObject

import sys

from getopt import getopt
opts,args = getopt(sys.argv[1:],'rC:')
optD = dict(opts)

ses = irods_session_from_env_file()

get_chksum = getattr(ses.data_objects, 'chksum', None)
if not get_chksum:
    die('Need a more recent release of python-irodsclient',1)

def print_checksum(obj,**options):
    if isinstance(obj,iRODSDataObject):
        outp = get_chksum(obj.path,**options)
    else:
        outp = optD.get('-C','C')
    print(outp + "\t" + obj.path)

def walk_collection_for_checksums(coll_obj,**options):
    for this,subcols,dataobjs in coll_obj.walk():
        for d in dataobjs:
            print_checksum(d)

# -- main --

for arg in args:
    try:
        obj = ses.collections.get(arg)
        if '-r' in optD:
            walk_collection_for_checksums(obj)
            continue
    except CollectionDoesNotExist:
        obj = ses.data_objects.get(arg)
    print_checksum(obj)
