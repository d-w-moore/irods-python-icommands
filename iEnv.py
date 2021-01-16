#!/usr/bin/env python

from __future__ import print_function

from pycommands.common import ( irods_session_from_env_file,
                                irods_session_from_args,
                                get_irods_client_env )
import getopt,getpass,sys,json

opt,arg = getopt.getopt(sys.argv[1:],'p')
optD = dict(opt)

try:
    if '-p' in optD:
        pw=getpass.getpass('irods password -> ')
        session = irods_session_from_args(borrow_from_env=True,password=pw)
    else:
        session = irods_session_from_env_file()
except:
    session = None

if session:
    home = session.collections.get('/{0.zone}/home/{0.username}'.format(session))
    print ('home iRods collection = %s\n' % home.path)

print ('client configuration =\n%s\n' % json.dumps(get_irods_client_env(),indent=4))
