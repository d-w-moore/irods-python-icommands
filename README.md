# irods-python-icommands

A basic set of pure-Python [iRODS](http://github.com/irods/irods) clients.  

This is a work in progress at the moment, so these commands
don't follow quite the same standards as the officially supported
[icommands](http://github.com/irods/irods_client_icommands).

But they do at least supply a ready substitute for iinit !

## Prerequisites:
   * `git` (with which to clone this repository)
   * [PRC](http://github.com/irods/python-irodsclient) installed
      - can install with `pip install python-irodsclient`
   * a running irods server as the target host/port/user/zone to be accessed.
     (Or ... use the first part of the demo below to download and run your own local one in docker.)
     
## Demo:

   * for access to a running iRODS instance:
     ```
     $ docker pull dwmoore/irods_pkg_postgres:latest
     $ docker run -it --name irods_test --hostname "$(hostname)" \
       -p 1247:1247 -p 20000-20199:20000-20199 \
       dwmoore/irods_pkg_postgres:latest
     $ docker exec irods_test /start_postgresql_and_irods.sh
     ```
   * now download these commands, set your PATH, and you're off!
     ```
     $ git clone https://github.com/d-w-moore/irods-python-icommands
     $ cd irods-python-icommands ; PATH="$(pwd):$PATH"
     $ ./iHostinit -h "$(hostname)" -z tempZone -u rods -p 1247 
     $ ./iPwinit 
     irods password -> #### (silent entry)
     $ ./iLs
     C /tempZone/home/rods
     $ ./iMkdir /tempZone/home/rods/subcoll
     $ ./iLs -r /tempZone/home/rods
     C /tempZone/home/rods
     C /tempZone/home/rods/subcoll
     $ echo "Hello" > World
     $ ./iPut World /tempZone/home/rods/World.dat
     $ ./iGet World.dat
     $ diff World.dat World
     ```
