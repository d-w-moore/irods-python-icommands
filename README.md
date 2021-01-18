# irods-python-icommands

This is a basic set of pure-Python [iRODS](http://github.com/irods/irods) clients.  

It is a work in progress at the moment and  the ".py" commands
don't follow quite the same standards as the officially supported
[icommands](http://github.com/irods/irods_client_icommands).

In fact, it is possible this might move toward an [irods CLI](https://github.com/irods/irods_client_cli)
type of interface.

## Motivation:

The aim is eventually that these commands could be an decent surrogate for the icommands on platforms
where their installation is undesirable (such as under HPC requirements) or impossible (eg., on Windows).

## Initializing the client environment:

Currently, as a stand-in for **iinit** , the following two commands can be used  together to achieve 
the creation of the environment file and native authentication file in ~/.irodsA :

   * `iHostinit.py`
   * `iPwinit.py`

The i\*.py commands have been tested manually on native (non-WSL) Windows 10 with the following 
python-irodsclient [development branch](https://github.com/d-w-moore/python-irodsclient/commits/windows_uid)
and appear to work fine.

## Prerequisites:

   * `git` (with which to clone this repository)
   * [PRC](http://github.com/irods/python-irodsclient) installed
      - can install with `pip install python-irodsclient`
   * a running irods server as the target host/port/user/zone to be accessed.
     (Or ... use the first part of the demo below to download and run your own local one in docker.)
     
## Demo (Linux):

   * If access to a running iRODS instance is unavailable, run one via docker:
     ```
     $ docker pull dwmoore/irods_pkg_postgres:latest
     $ docker run -it --name irods_test --hostname "$(hostname)" \
       -p 1247:1247 -p 20000-20199:20000-20199 \
       dwmoore/irods_pkg_postgres:latest
     $ docker exec irods_test /start_postgresql_and_irods.sh
     ```
   * Then download these commands to the host, and access iRODS via the Python client commands.
     ```
     $ git clone https://github.com/d-w-moore/irods-python-icommands
     $ cd irods-python-icommands ; PATH="$(pwd):$PATH"
     $ ./iHostinit -h "$(hostname)" -z tempZone -u rods -p 1247 
     $ ./iPwinit.py
     irods password -> #### (silent entry)
     $ ./iLs.py
     C /tempZone/home/rods
     $ ./iMkdir.py /tempZone/home/rods/subcoll
     $ ./iLs.py -r /tempZone/home/rods
     C /tempZone/home/rods
     C /tempZone/home/rods/subcoll
     $ echo "Hello" > World
     $ ./iPut.py World /tempZone/home/rods/World.dat
     $ ./iGet.py World.dat
     $ diff World.dat World
     ```
