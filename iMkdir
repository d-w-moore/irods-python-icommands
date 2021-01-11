#!/usr/bin/env python
from __future__ import print_function

from irods.session import iRODSSession

from os.path import expanduser
from getopt import getopt

import sys
opt,arg = getopt(sys.argv[1:],'')

with iRODSSession(
     irods_env_file=expanduser('~/.irods/irods_environment.json')) as s:

  s.collections.create(*arg[:1])
