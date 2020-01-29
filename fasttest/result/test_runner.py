#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import unittest
from fasttest.common import Var
from fasttest.result.test_result import TestResult
from fasttest.result.html_result import HTMLTestRunner


class TestRunner(unittest.TextTestRunner):

    def __init__(self,stream=sys.stderr,
                 descriptions=True, verbosity=1,
                 failfast=False, buffer=False,resultclass=None):
        unittest.TextTestRunner.__init__(self, stream, descriptions, verbosity,
                                failfast=failfast, buffer=buffer)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        if resultclass is None:
            self.resultclass = TestResult
        else:
            self.resultclass = resultclass

    def _makeResult(self):
            return  self.resultclass(self.stream,self.descriptions,self.verbosity)

    def run(self, test):
        '''
        :param test:
        :return:
        '''
        result = self._makeResult()
        result.failfast = self.failfast
        result.buffer = self.buffer
        starTime = time.time()
        test(result)
        stopTime = time.time()
        html_file = os.path.join(Var.report,'report.html')
        fp = open(html_file,'wb')
        html_runner = HTMLTestRunner(stream=fp,
                                     title='Test Results',
                                     description='Test')
        html_runner.generateReport(result,starTime,stopTime)
        fp.close()

        return result




