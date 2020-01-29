#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest
import traceback
from fasttest.common import *


class TestCase(unittest.TestCase):
    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            attrvalue = None
            self.__setattr__(item, attrvalue)
            return attrvalue

    def __init__(self, methodName="runTest"):
        super(TestCase, self).__init__(methodName)
        if not Var.testcase:
            raise NameError("name 'testcase' is not defined")
        for key, value in Var.testcase.items():
            setattr(self, key, value)
        self.snapshot_dir = os.path.join(Var.report, self.module, self.testcase_path.split(os.sep)[-1].split(".")[0])

    def run(self, result=None):

        try:
            Var.case_step_index = 0
            Var.case_snapshot_index = 0
            Var.snapshot_dir = self.snapshot_dir
            if not os.path.exists(Var.snapshot_dir):
                os.makedirs(Var.snapshot_dir)
            log_info("******************* TestCase {} Start *******************".format(self.description))
            unittest.TestCase.run(self, result)
            log_info("******************* Total: {}, Pass: {}, Failed: {}, Error: {}, Skipped: {} ********************\n"
                    .format(result.testsRun, len(result.successes), len(result.failures), len(result.errors), len(result.skipped)))
        except:
            traceback.print_exc()