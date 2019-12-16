#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

class TestCaseUtils(object):

    def __init__(self):
        self.__testcase_list = []

    def __traversal_dir(self,path):
        for rt, dirs, files in os.walk(path):
            files.sort()
            for f in files:
                file_path = os.path.join(rt, f)
                if os.path.isfile(file_path):
                    self.__testcase_list.append(file_path)

    def testcase_path(self,dirname,paths):
        if not paths:
            raise Exception('test case is empty.')
        for path in paths:
            file_path = os.path.join(dirname,path)
            if os.path.isfile(file_path):
                self.__testcase_list.append(file_path)
            else:
               self.__traversal_dir(os.path.join(dirname, path))
        if not self.__testcase_list:
            raise Exception('test case is empty.')
        return self.__testcase_list