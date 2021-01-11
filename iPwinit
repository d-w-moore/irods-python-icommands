#!/usr/bin/env python
from os.path import expanduser
from os import chmod
from getpass import getpass
from irods.password_obfuscation import encode as pw_encode
auth_file = expanduser('~/.irods/.irodsA')
open(auth_file,'w').write(pw_encode(getpass('irods password ->')))
chmod (auth_file,0o600)
