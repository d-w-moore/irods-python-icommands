from irods.session import iRODSSession

import atexit
import re
import json
import io
import os
import ssl

_env_init_keys_regex = re.compile('irods_(host|port|(zone|user)_name)$')

try:
    _env_file = os.environ['IRODS_ENVIRONMENT_FILE']
except KeyError:
    _env_file = os.path.expanduser('~/.irods/irods_environment.json')

def get_irods_client_env(default_value=None):
    try:
        return json.load(open(_env_file,"r"))
    except:
        return default_value

def _partition_json_keys(dct):
    remove = lambda s,sub,sfx=False: ( s[len(sub):] if s.startswith(sub) else s) if not sfx \
                                else ( s[:-len(sub)] if s.endswith(sub) else s)
    argkeys = set(k for k in dct if _env_init_keys_regex.match(k))
    remkeys = set(dct.keys()) - argkeys
    return { remove(remove(k,"irods_"),"_name",sfx=1):v for k,v in dct.items() if k in argkeys }, \
           { k:v for k,v in dct.items() if k not in argkeys }

def _make_session(*x,**kw):
    ssl_context = ssl.create_default_context( purpose=ssl.Purpose.SERVER_AUTH,
                                              cafile=None, capath=None, cadata=None)
    kw.update({'ssl_context':ssl_context})
    session = iRODSSession(*x, **kw)
    if not hasattr(iRODSSession, '__del__'):
        atexit.register(lambda : session.cleanup() if session else None)
    return session

def irods_session_from_args(*x,**kw):
    borrow_from_env = kw.pop('borrow_from_env',False)
    file_config = get_irods_client_env( default_value={} ) if borrow_from_env else {} 
    init, non_init = _partition_json_keys(file_config)
    kw.update(init)
    ses = _make_session(*x,**kw)
    # TODO - process any non-init keys?
    return ses

def irods_session_from_env_file(*x,**kw):
    kw.update(irods_env_file=_env_file)
    return _make_session(*x,**kw)

