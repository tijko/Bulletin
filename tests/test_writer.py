#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def write_test():
    current_dir = os.getcwd()
    test_file = os.path.join(current_dir, 'test_file.txt')
    file_handle = open(test_file, 'w')
    file_handle.write("Write test event.")
    file_handle.close()


if __name__ == '__main__':
    write_test()
