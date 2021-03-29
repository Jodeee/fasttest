#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import unittest
import collections
from fasttest.common import *

class TestInfo(object):
    """
    This class keeps useful information about the execution of a
    test method.
    """

    # Possible test outcomes
    (SUCCESS, FAILURE, ERROR, SKIP) = range(4)

    def __init__(self, test_method, status=SUCCESS, err=None):
        self.status = status
        self.elapsed_time = 0
        self.start_time = 0
        self.stop_time = 0
        self.err = err

        self.report = None
        self.case_path = test_method.test_case_path
        self.data_id = test_method.test_case_path.split('/')[-1].split(os.sep)[-1].split(".")[0]
        self.case_name = test_method.test_case_path.split('/')[-1].split(os.sep)[-1].split(".")[0]
        self.snapshot_dir = test_method.snapshot_dir
        self.module_name = test_method.module
        self.description = test_method.description
        self.test_case_steps = {}

class TestResult(unittest.TextTestResult):

    def __init__(self,stream, descriptions, verbosity):
        super(TestResult,self).__init__(stream,descriptions,verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.descriptions = descriptions
        self.result = collections.OrderedDict()
        self.successes = []
        self.testinfo = None

    def _save_output_data(self):
        '''
        :return:
        '''
        try:
            self._stdout_data = Var.case_message
            Var.case_message = ""
            Var.case_step_index = 0
            Var.case_snapshot_index = 0
        except AttributeError as e:
            pass

    def startTest(self, test):
        '''
        :param test:
        :return:
        '''
        super(TestResult,self).startTest(test)
        self.start_time = time.time()
        Var.test_case_steps = {}
        Var.is_debug = False

    def stopTest(self, test):
        '''
        :param test:
        :return:
        '''
        self._save_output_data()
        unittest.TextTestResult.stopTest(self,test)
        self.stop_time = time.time()
        self.report = test.report
        self.testinfo.start_time = self.start_time
        self.testinfo.stop_time = self.stop_time
        self.testinfo.report = self.report
        self.testinfo.test_case_steps = Var.test_case_steps
        if test.module not in self.result.keys():
            self.result[test.module] = []
        self.result[test.module].append(self.testinfo)
        self.testinfo = None
        Var.test_case_steps = {}
        Var.is_debug = False

    def addSuccess(self, test):
        '''
        :param test:
        :return:
        '''
        super(TestResult,self).addSuccess(test)
        self._save_output_data()
        self.testinfo = TestInfo(test, TestInfo.SUCCESS)
        self.successes.append(test)

    def addError(self, test, err):
        '''
        :param test:
        :return:
        '''
        super(TestResult,self).addError(test,err)
        self._save_output_data()
        _exc_str = self._exc_info_to_string(err, test)
        self.testinfo = TestInfo(test, TestInfo.ERROR, _exc_str)
        log_error(' case: {}'.format(self.testinfo.case_path), False)
        log_error(_exc_str, False)

    def addFailure(self, test, err):
        '''
        :param test:
        :return:
        '''
        super(TestResult,self).addFailure(test,err)
        self._save_output_data()
        _exc_str = self._exc_info_to_string(err, test)
        self.testinfo = TestInfo(test, TestInfo.FAILURE, _exc_str)
        log_error(' case: {}'.format(self.testinfo.case_path), False)
        log_error(_exc_str, False)

    def addSkip(self, test, reason):
        '''
        :param test:
        :return:
        '''
        super(TestResult,self).addSkip(test,reason)
        self._save_output_data()
        self.testinfo = TestInfo(test, TestInfo.SKIP)

    def addExpectedFailure(self, test, err):
        '''
        :param test:
        :param err:
        :return:
        '''
        super(TestResult, self).addFailure(test, err)
        self._save_output_data()
        _exc_str = self._exc_info_to_string(err, test)
        self.testinfo = TestInfo(test, TestInfo.FAILURE, _exc_str)
        log_error(' case: {}'.format(self.testinfo.case_path), False)
        log_error(_exc_str, False)

