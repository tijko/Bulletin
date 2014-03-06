#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import simplejson

from twisted.python import filepath
from twisted.internet import inotify
from twisted.internet import reactor

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class Notifier(object):

    def __init__(self, recipent, path):
        self.recipent = recipent
        self.path = path
        self.set_watch

    @property
    def set_watch(self):
        self.notifier = inotify.INotify() 
        self.notifier.startReading()
        try:
            self.notifier.watch(filepath.FilePath(self.path), 
                                mask=inotify.IN_WATCH_MASK | inotify.IN_ACCESS, 
                                callbacks=[self.inotify_twisted])
        except inotify.INotifyError, e:
            error_message = simplejson.dumps(str(e))
            self.recipent.sendLine(error_message)

    def signal_event(self, event_dict):
        event = simplejson.dumps(event_dict)
        self.recipent.sendLine(event)

    def inotify_twisted(self, ignored, path, mask):
        alpha_event = inotify.humanReadableMask(mask)
        event = {time.time(): {'mask':mask, 'event':alpha_event[0], 'path':self.path}}
        self.signal_event(event)


class ClientHandle(LineReceiver):
    
    def __init__(self, clients, logger):
        self.clients = clients
        self.logger = logger

    def connectionMade(self):
        self.clients[self] = len(self.clients)
        self.logger.info('Client <%s> joined', self)

    def connectionLost(self, reason):
        del self.clients[self]
        self.logger.info('Client <%s> left', self)

    def lineReceived(self, path):
        self.notify = Notifier(self, path.strip('\r\n'))


class NotifyFactory(Factory):
    
    def __init__(self):
        basedir = os.environ['HOME'] + '/Bulletin'
        self._format = '%(asctime)s - %(levelname)s - %(message)s'
        self.logger = logging.getLogger('board')
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(os.path.join(basedir, '.board.log'), 'w')
        self.formatter = logging.Formatter(self._format)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.info('twisted board')
        self.limit = 1000
        self.clients = dict()
    
    def buildProtocol(self, addr):
        if len(self.clients) > self.limit:
            return 
        return ClientHandle(self.clients, self.logger)


if __name__ == '__main__':
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(0)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(1)
    reactor.listenUNIX('/tmp/twisted', NotifyFactory())
    reactor.run()

