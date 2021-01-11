# irods-python-icommands

1. install [PRC](http://github.com/irods/python-irodsclient)
1. ```
   $ ./iHostinit 
   irods server host -> inspiron
   irods server port -> 1247
   irods user -> rods
   irods zone -> tempZone
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
