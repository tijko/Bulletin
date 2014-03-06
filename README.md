Bulletin
========


Bulletin is a python module that monitors filesystem events.  There are two parts to Bulletin, one is the server and the other the client threads.  The server `board.py` uses twisted and sets up the actually event watches and signals the client threads over unix sockets.
