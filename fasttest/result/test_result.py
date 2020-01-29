#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import unittest
from fasttest.common import *


def testcase_name(test_method):
    testcase = type(test_method)

    # Ignore module name if it is '__main__'
    module = testcase.__module__ + '.'
    if module == '__main__.':
        module = ''
    result = module + testcase.__name__
    return result

class TestInfo(object):
    """
    This class keeps useful information about the execution of a
    test method.
    """

    # Possible test outcomes
    (SUCCESS, FAILURE, ERROR, SKIP) = range(4)

    def __init__(self, test_result, test_method, outcome=SUCCESS, err=None, subTest=None):
        self.test_result = test_result
        self.outcome = outcome
        self.elapsed_time = 0
        self.start_time = 0
        self.stop_time = 0
        self.err = err
        self.stdout = test_result._stdout_data

        self.test_description = self.test_result.getDescription(test_method)
        self.test_exception_info = (
            '' if outcome in (self.SUCCESS, self.SKIP)
            else self.test_result._exc_info_to_string(
                    self.err, test_method)
        )
        self.dataId = test_method.testcase_path.split('/')[-1].split(os.sep)[-1].split(".")[0]
        self.casename = test_method.testcase_path.split('/')[-1].split(os.sep)[-1].split(".")[0]
        self.snapshot_dir = test_method.snapshot_dir
        self.module_name = test_method.module
        self.description = test_method.description

class TestResult(unittest.TextTestResult):

    def __init__(self,stream, descriptions, verbosity,infoclass = None):
        super(TestResult,self).__init__(stream,descriptions,verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.descriptions = descriptions
        self.result = []
        self.successes = []
        self.infoclass = TestInfo if infoclass is None else infoclass

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

    def stopTest(self, test):
        '''
        :param test:
        :return:
        '''
        self._save_output_data()
        unittest.TextTestResult.stopTest(self,test)
        self.stop_time = time.time()
        self.result[-1][1].start_time = self.start_time
        self.result[-1][1].stop_time = self.stop_time
        self.report = Var.report

    def addSuccess(self, test):
        '''
        :param test:
        :return:
        '''
        super(TestResult,self).addSuccess(test)
        self._save_output_data()
        testinfo = self.infoclass(self,test,self.infoclass.SUCCESS)
        self.result.append((self.infoclass.SUCCESS,testinfo,''))
        self.successes.append(testinfo)

    def addError(self, test, err):
        '''
        :param test:
        :return:
        '''
        super(TestResult,self).addError(test,err)
        self._save_output_data()
        testinfo = self.infoclass(self,test,self.infoclass.ERROR,err)
        _exc_str = self._exc_info_to_string(err,test)
        log_error(_exc_str,False)
        self.result.append((self.infoclass.ERROR,testinfo,_exc_str))

    def addFailure(self, test, err):
        '''
        :param test:
        :return:
        '''
        super(TestResult,self).addFailure(test,err)
        self._save_output_data()
        testinfo = self.infoclass(self,test,self.infoclass.FAILURE,err)
        _exc_str = self._exc_info_to_string(err,test)
        log_error(_exc_str, False)
        self.result.append((self.infoclass.FAILURE,testinfo,_exc_str))

    def addSkip(self, test, reason):
        '''
        :param test:
        :return:
        '''
        super(TestResult,self).addSkip(test,reason)
        self._save_output_data()
        testinfo = self.infoclass(self,test,self.infoclass.SKIP,reason)
        self.result.append((self.infoclass.SKIP,testinfo,reason))

    def addExpectedFailure(self, test, err):
        '''
        :param test:
        :param err:
        :return:
        '''
        super(TestResult, self).addFailure(test, err)
        self._save_output_data()
        testinfo = self.infoclass(self, test, self.infoclass.FAILURE, err)
        _exc_str = self._exc_info_to_string(err, test)
        log_error(_exc_str, False)
        self.result.append((self.infoclass.FAILURE, testinfo, _exc_str))

