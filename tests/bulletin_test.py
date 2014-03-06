#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import unittest
import subprocess

sys.path.insert(0, os.getcwd().rstrip("tests"))

from bulletin.bulletin import Thumbtac


#XXX Have board.py(server) running before attempting to run

class ThumbtacTestCase(unittest.TestCase):

    def setUp(self):
        current_dir = os.getcwd()
        self.test_file = os.path.join(current_dir, 'test_file.txt')
        test_handle = open(self.test_file, 'w')
        test_handle.close()
        stats = os.stat(self.test_file)
        self.start_size = stats.st_size
        self.client = Thumbtac(self.test_file)
        self.client.start()
        wrt = subprocess.Popen(["python2", "test_writer.py"], 
                                stdout=subprocess.PIPE)
        wrt.communicate()

    def tearDown(self):
        self.client.end()
        os.unlink(self.test_file)


class ConnTestCase(ThumbtacTestCase):

    def test_server(self):
        assert(os.path.exists('/tmp/twisted'))

    def test_connection(self):
        assert(self.client.is_alive())


class EventsTestCase(ThumbtacTestCase):

    def test_event_modify(self):
        events = self.client.notices.values()
        event_types = [i['event'] for i in events]
        assert(any(e == 'modify' for e in event_types))


class TimeTestCase(ThumbtacTestCase):

    def test_time_accessed(self):
        stat = os.stat(self.test_file)
        st_last_accessed = time.ctime(stat.st_atime)
        tac_accessed = self.client.last_notice
        assert(st_last_accessed == tac_accessed)


class SizeTestCase(ThumbtacTestCase):

    def test_size_change(self):
        wrt_bytes = 17
        assert(self.client.size_diff == wrt_bytes)


if __name__ == '__main__':
    unittest.main()
