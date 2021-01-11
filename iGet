#!/usr/bin/env python
from __future__ import print_function

from irods.session import iRODSSession

from os.path import expanduser,basename
from getopt import getopt

import sys
opt,arg = getopt(sys.argv[1:],'')

with iRODSSession(
     irods_env_file=expanduser('~/.irods/irods_environment.json')) as s:
  
  if '/' not in arg[0]:
    arg[0] = '/{0.zone}/home/{0.username}/{1}'.format(s,arg[0])
  if not arg[1:]:
    arg.append(basename(arg[0]))

  s.data_objects.get( *arg[:2] )
