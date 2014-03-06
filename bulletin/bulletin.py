#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import select
import simplejson

from threading import Thread


class Thumbtac(Thread):

    def __init__(self, path, saddr='/tmp/twisted'):
        super(Thumbtac, self).__init__()
        self._alive = False
        self.notices = dict()
        self._path = path
        self._saddr = saddr
        stats = os.stat(path)
        self._st_size = stats.st_size
        self._events = select.poll()
        self._set_watch 

    @property
    def modified(self):
        events = self.notices.values()
        if any(event['event'] == 'modify' for event in events):
            return True
        return False

    @property
    def accessed(self):
        events = self.notices.values()
        if any(event['event'] == 'access' for event in events):
            return True
        return False

    @property
    def last_notice(self):
        try:
            return time.ctime(max(self.notices))
        except ValueError:
            return None

    @property
    def first_notice(self):
        try:
            return time.ctime(min(self.notices))
        except ValueError:
            return None

    @property
    def size_diff(self):
        stats = os.stat(self._path)
        cur_size = int(stats.st_size)
        return cur_size - int(self._st_size)

    @property
    def _set_watch(self):
        self._client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._client.connect((self._saddr))
        self._client.sendall(self._path + '\r\n')
        self._events.register(self._client, select.POLLIN)

    def _event_handle(self, fd, event):
        if fd == self._client.fileno():
            evts = self._client.recv(8092)
            if not evts:
                self._client.close()
                sys.exit()
            for evt in [e for e in evts.split("\r\n") if e]:
                event = simplejson.loads(evt)
                self.notices.update({float(k):v for k,v in event.items()})
            self._events.unregister(self._client)
            self._set_watch

    def end(self):
        self._alive = False

    def run(self):
        self._alive = True
        while self._alive:
            for (fd, ev) in self._events.poll(1):
                self._event_handle(fd, ev)
        self._client.close()
        return
