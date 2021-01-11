#!/usr/bin/env python
import json
import os
import sys
from os.path import expanduser,exists
from getopt import getopt

opt,arg = getopt(sys.argv[1:],'h:p:u:z:')
optD = dict(opt)

home_env_path = expanduser('~/.irods')

if not exists(home_env_path):
    os.makedirs(home_env_path)

try: raw_input
except NameError: raw_input = input

host = optD.get('-h') or raw_input('irods server host -> ')
port = optD.get('-p') or raw_input('irods server port -> ')
user = optD.get('-u') or raw_input('irods user -> ')
zone = optD.get('-z') or raw_input('irods zone -> ')

json.dump( {
             "irods_host": host,
             "irods_port": int(port),
             "irods_user_name": user,
             "irods_zone_name": zone
           },
           open(expanduser('~/.irods/irods_environment.json'),'w'),
           indent=4
)
