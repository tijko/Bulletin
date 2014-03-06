Bulletin
========


Bulletin is a python module that monitors filesystem events.  There are two 
parts to Bulletin, one is the server and the other, client threads. The twisted
framework will need to be install before using [first](https://twistedmatrix.com/trac/)

##Usage

The server `board.py` uses twisted and sets up the actually event watches and 
signals the client threads over unix sockets.  

Run the `board.py` file to start the server.  The server runs as a daemon which
can be set-up to be called at startup.  There is a log file for client connects
and disconnects that is kept in bulletins home directory under `.board.log`.


The client `bulletin.py` module has one main class `Thumbtac`:

    >>> from bulletin import Thumbtac

This class is called with the path of the file/directory that is going to be 
monitored.

    >>> tac = Thumbtac('/tmp/local')

This instance connects to the server and creates a watch for the file 
`/tmp/local`.  Call the `start` method to begin the watch thread:

    >>> tac.start()

Now whenever any events occur with the `/tmp/local` file, they will be sent to
`.notices`

    # after an event to /tmp/local
    >>> 
    >>> tac.notices
    {1394144903.489334: {'path': '/tmp/local', 'mask': 4, 'event': 'attrib'}, 
     1394144900.673219: {'path': '/tmp/local', 'mask': 1, 'event': 'access'}, 
     1394144903.404146: {'path': '/tmp/local', 'mask': 2048, 'event': 'move_self'}}

Which is a `dict` of `dict`s of:

* Current time in seconds since the epoch of the event as the keys
  * 'path' as a key in the sub-dict for the path of the watch
  * 'mask' as a key in the sub-dict for the event-mask number
  * 'event' as the actually event name


