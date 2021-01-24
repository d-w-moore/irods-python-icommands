#!/usr/bin/env python

from __future__ import print_function

from pycommands.common import irods_session_from_env_file

from irods.exception import CollectionDoesNotExist
from irods.models import DataObject,Collection

from os.path import expanduser
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("object", nargs='?', type=str, help="list object and sub objects.")
parser.add_argument("-r", "--recursive", action = 'store_true')
parser.add_argument("-a", "--annotation", type=str, choices=['none','default','checksum'], default = 'default',
                    help="annotation for each object listed")
args = parser.parse_args()

def coll_id_from_name( name, session, memo={} ):
    myid = memo.get(name)
    if myid is None:
        myid = session.query(Collection.id).filter(Collection.name == name).one()[Collection.id]
        memo[name] = myid
    return myid

if args.annotation == 'checksum':
    def cksumF(path,session):
        path_elements = path.split('/')
        collection = '/'.join(path_elements[:-1])
        c_id = coll_id_from_name (collection,session)
        cksum = session.query(DataObject).filter(
                  DataObject.collection_id == c_id,
                  DataObject.name == path_elements[-1]
        ).one()[DataObject.checksum]
        return cksum if cksum else ''
else:
    cksumF = None

def annotate(typecode,sess,path=None):
    return '' if (args.annotation == 'none') else (typecode +
        ( ' '+cksumF(path,sess) if typecode == 'D' and path and cksumF else '' )
        + '\t')

def print_item(typecode, sess, path):
    print(annotate(typecode,sess,path) + path)

#--------------------------------------#--------------------------------------

with irods_session_from_env_file() as s:
    if args.object is None:
        args.object='/{0.zone}/home/{0.username}'.format(s)
    tc = 'C'
    try:
        obj = s.collections.get(args.object)
    except CollectionDoesNotExist:
        obj = s.data_objects.get(args.object)
        tc = 'D'
    if tc == 'D':
        print_item(tc,s,obj.path)
    else:
        if args.recursive:
            # -- walk the subtree
            for this,subcols,dataobjs in obj.walk():
                print_item('C',s,this.path)
                for d in dataobjs:
                    print_item('D',s,d.path)
        else:
            # -- display only one object, and immediate children
                print_item('C',s,obj.path)
                for d in obj.data_objects:
                    print_item('D',s,d.path)
                for c in obj.subcollections:
                    print_item('C',s,c.path)
